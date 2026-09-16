from typing import Dict, Any

class SpacedRepetitionScheduler:
    """
    SM-2 (SuperMemo-2) algorithm for calculating optimal retention intervals.
    """
    def update_interval(self, reps: int, interval: int, ease: float, quality: int) -> Dict[str, Any]:
        """
        Quality: 0 (failure) to 5 (flawless recall).
        """
        if quality >= 3:
            if reps == 0:
                new_interval = 1
            elif reps == 1:
                new_interval = 6
            else:
                new_interval = int(interval * ease)
            new_reps = reps + 1
        else:
            new_reps = 0
            new_interval = 1

        new_ease = max(1.3, ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        return {
            "reps": new_reps,
            "interval_days": new_interval,
            "ease_factor": round(new_ease, 2)
        }