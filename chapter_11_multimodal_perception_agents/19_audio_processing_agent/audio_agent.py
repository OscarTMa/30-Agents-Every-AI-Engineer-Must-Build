import os
import numpy as np
from typing import Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from prosody_features import extract_simulated_prosody
from vad_sentiment import VoiceSentimentEngine

class AcousticIntentSynthesis(BaseModel):
    transcription_cleaned: str = Field(description="Normalized verbal transcript")
    acoustic_urgency_score: float = Field(ge=0.0, le=1.0, description="Caller urgency assessed from prosody")
    agent_action_recommendation: str = Field(description="Recommended workflow action")

class AudioProcessingAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.sentiment_engine = VoiceSentimentEngine()

    def process_voice_interaction(self, raw_audio_waveform: np.ndarray, raw_transcript: str, scenario: str = "frustrated") -> dict:
        # Step 1: Extract physical prosodic features
        features = extract_simulated_prosody(raw_audio_waveform, scenario=scenario)

        # Step 2: Map to continuous VAD emotional space
        vad_analysis = self.sentiment_engine.map_to_vad(features)

        # Step 3: LLM Intent & Action Synthesis
        prompt = f"""
You are an expert conversational audio processing agent.
Analyze the caller interaction by integrating both the verbal text and acoustic prosodic metrics.

Verbal Raw Text: "{raw_transcript}"
Acoustic State: {vad_analysis['primary_state']}
VAD Coordinates: {vad_analysis['vad_coordinates']}
Pitch Mean: {features.pitch_mean_hz} Hz | Speaking Rate: {features.speaking_rate_wps} words/sec

Synthesize the cleaned transcript, assign an acoustic urgency score (0.0 to 1.0), and specify the immediate escalation or routing action.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AcousticIntentSynthesis,
                temperature=0.0
            )
        )
        synthesis = AcousticIntentSynthesis.model_validate_json(response.text)

        return {
            "vad_analysis": vad_analysis,
            "synthesis": synthesis
        }