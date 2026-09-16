from dataclasses import dataclass
from typing import Dict
from prosody_features import ProsodicFeatures

@dataclass
class VADProfile:
    valence: float    # -1.0 (Negative) to +1.0 (Positive)
    arousal: float    # 0.0 (Calm) to 1.0 (Excited / High Energy)
    dominance: float  # 0.0 (Submissive) to 1.0 (Assertive / In Control)

class VoiceSentimentEngine:
    """
    Maps prosodic acoustic correlates to the continuous 3D VAD emotional space.
    """
    def map_to_vad(self, features: ProsodicFeatures) -> Dict[str, any]:
        # Normalization heuristics
        norm_pitch = (features.pitch_mean_hz - 100.0) / 200.0  # 0 to 1
        norm_rate = features.speaking_rate_wps / 8.0          # 0 to 1

        if norm_pitch > 0.6 and norm_rate > 0.6:
            vad = VADProfile(valence=-0.75, arousal=0.88, dominance=0.82)
            detected_state = "Frustrated / Agitated"
        elif norm_pitch < 0.35 and norm_rate < 0.45:
            vad = VADProfile(valence=0.40, arousal=0.25, dominance=0.40)
            detected_state = "Calm / Receptive"
        else:
            vad = VADProfile(valence=0.05, arousal=0.50, dominance=0.50)
            detected_state = "Neutral"

        return {
            "primary_state": detected_state,
            "vad_coordinates": {
                "valence": round(vad.valence, 2),
                "arousal": round(vad.arousal, 2),
                "dominance": round(vad.dominance, 2)
            },
            "acoustic_features": features
        }