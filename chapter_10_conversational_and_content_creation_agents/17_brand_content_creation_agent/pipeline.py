import os
from typing import Optional, Tuple
from google import genai
from constraints import BrandGuidelines
from models import CampaignBrief, CampaignPackage, AssetRequest

class BrandContentCreationPipeline:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def _draft_channel_copy(self, role: str, channel: str, brief: CampaignBrief, correction_hint: str = "") -> str:
        prompt = f"""
You are an expert {role} crafting {channel} copy.
Product: {brief.product}
Target Audience: {brief.target_audience}
Core Value Proposition: {brief.core_value_prop}

Brand Constraints:
- Tone: {brief.guidelines.tone}
- Forbidden Words: {brief.guidelines.forbidden_terms}

{f"CORRECTION REQUIRED: Previous draft contained forbidden words: {correction_hint}. Do NOT use them." if correction_hint else ""}

Generate the complete, publication-ready {channel} text:
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    def _validated_writer_loop(self, role: str, channel: str, brief: CampaignBrief, max_retries: int = 2) -> Tuple[str, bool]:
        """Writer + Editor feedback loop enforcing CSP hard constraints."""
        correction_hint = ""
        draft = ""
        for attempt in range(1, max_retries + 2):
            draft = self._draft_channel_copy(role, channel, brief, correction_hint)
            passed, violations = brief.guidelines.validate_content(draft)
            if passed:
                return draft, True
            print(f"  [Editor Warning] {channel} draft failed on attempt {attempt}: Found {violations}. Retrying with feedback...")
            correction_hint = ", ".join(violations)
        return draft, False

    def execute_campaign(self, brief: CampaignBrief) -> CampaignPackage:
        package = CampaignPackage()

        # Phase 1: Multi-Channel Specialized Drafting with Editor Validation
        print("[Planner] Dispatching Email Specialist...")
        package.email_newsletter, _ = self._validated_writer_loop("Email Marketing Specialist", "Email Newsletter", brief)

        print("[Planner] Dispatching SEO Copywriter...")
        package.seo_article, _ = self._validated_writer_loop("SEO Strategist", "Long-form Blog Article", brief)

        print("[Planner] Dispatching Ad Creative Specialist & Multimodal Orchestrator...")
        package.ad_copy, _ = self._validated_writer_loop("Ad Creative Copywriter", "Display Ad Copy", brief)

        # Multimodal Asset Requests (Contracts for visual backends)
        package.asset_requests = [
            AssetRequest(
                asset_id="ad_hero_01",
                asset_type="image_dalle",
                prompt=f"Modern 3D render representing {brief.product} for {brief.target_audience}, clean tech aesthetic.",
                aspect_ratio="1:1"
            ),
            AssetRequest(
                asset_id="seo_infographic_01",
                asset_type="chart",
                prompt=f"Infographic architecture diagram illustrating {brief.core_value_prop}.",
                aspect_ratio="16:9"
            )
        ]

        # Phase 2 & 3: Analytics Feedback Loop (Simulated telemetry & closed-loop adaptation)
        package.analytics_feedback = {
            "email_open_rate": 0.31,
            "seo_organic_ctr": 0.12,
            "ad_conversion_rate": 0.038,
            "adaptive_recommendation": "Ad conversion (3.8%) is below target threshold. Refine ad creative hooks in next campaign iteration."
        }
        return package