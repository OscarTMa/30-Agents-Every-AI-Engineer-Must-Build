import sys
from pathlib import Path
import numpy as np

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from audio_agent import AudioProcessingAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = AudioProcessingAgent()

    # Synthetic waveform array
    synthetic_waveform = np.sin(np.linspace(0, 100, 16000))
    raw_audio_text = "Um, uh, I have called three times today already and my enterprise server is still completely down!"

    print("=== Audio Processing & Voice Sentiment Agent ===")
    print("Processing incoming customer support voice stream...\n")

    result = agent.process_voice_interaction(synthetic_waveform, raw_audio_text, scenario="frustrated")
    vad = result["vad_analysis"]
    synthesis = result["synthesis"]

    print("1. PROSODIC ACOUSTIC & VAD ANALYSIS:")
    print(f"   - Detected State: {vad['primary_state']}")
    print(f"   - VAD Coordinates: Valence={vad['vad_coordinates']['valence']}, Arousal={vad['vad_coordinates']['arousal']}, Dominance={vad['vad_coordinates']['dominance']}")
    print(f"   - Mean Pitch: {vad['acoustic_features'].pitch_mean_hz} Hz | Speaking Rate: {vad['acoustic_features'].speaking_rate_wps} wps\n")

    print("2. SYNTHESIZED ACTIONABLE RESOLUTION:")
    print(f"   - Cleaned Transcript: \"{synthesis.transcription_cleaned}\"")
    print(f"   - Urgency Score:      {synthesis.acoustic_urgency_score} / 1.0")
    print(f"   - Recommended Action: {synthesis.agent_action_recommendation}")