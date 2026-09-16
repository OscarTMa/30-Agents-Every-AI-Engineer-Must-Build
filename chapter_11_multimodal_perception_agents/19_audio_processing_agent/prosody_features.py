from dataclasses import dataclass
import numpy as np

@dataclass
class ProsodicFeatures:
    pitch_mean_hz: float
    pitch_variability: float
    intensity_mean_db: float
    speaking_rate_wps: float

def extract_simulated_prosody(audio_waveform: np.ndarray, scenario: str = "frustrated") -> ProsodicFeatures:
    """
    Extracts acoustic prosodic features from audio waveform.
    Simulated parametric acoustic extractor.
    """
    rms = float(np.sqrt(np.mean(audio_waveform**2)))
    if scenario == "frustrated":
        return ProsodicFeatures(
            pitch_mean_hz=235.0,
            pitch_variability=45.0,
            intensity_mean_db=-12.5 + rms,
            speaking_rate_wps=5.8
        )
    elif scenario == "calm":
        return ProsodicFeatures(
            pitch_mean_hz=140.0,
            pitch_variability=15.0,
            intensity_mean_db=-24.0 + rms,
            speaking_rate_wps=3.2
        )
    else:
        return ProsodicFeatures(
            pitch_mean_hz=175.0,
            pitch_variability=25.0,
            intensity_mean_db=-18.0 + rms,
            speaking_rate_wps=4.0
        )