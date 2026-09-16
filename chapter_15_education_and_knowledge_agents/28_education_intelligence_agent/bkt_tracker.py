class BKTTracker:
    """
    Bayesian Knowledge Tracing (BKT) belief updater for student mastery.
    Models latent mastery state P(L) under observation uncertainty.
    """
    def __init__(self, p_transit: float = 0.10, p_slip: float = 0.05, p_guess: float = 0.20):
        self.p_transit = p_transit
        self.p_slip = p_slip
        self.p_guess = p_guess

    def update(self, p_mastery: float, correct: bool) -> float:
        # Step 1: Posterior calculation given observation P(L_n | obs)
        if correct:
            p_obs_given_mastery = 1.0 - self.p_slip
            p_obs_given_no_mastery = self.p_guess
        else:
            p_obs_given_mastery = self.p_slip
            p_obs_given_no_mastery = 1.0 - self.p_guess

        p_obs = (p_obs_given_mastery * p_mastery) + (p_obs_given_no_mastery * (1.0 - p_mastery))
        p_posterior = (p_obs_given_mastery * p_mastery) / p_obs

        # Step 2: Learning transition update P(L_{n+1}) = P(L_n|obs) + (1 - P(L_n|obs)) * P(T)
        p_updated = p_posterior + (1.0 - p_posterior) * self.p_transit
        return round(p_updated, 4)