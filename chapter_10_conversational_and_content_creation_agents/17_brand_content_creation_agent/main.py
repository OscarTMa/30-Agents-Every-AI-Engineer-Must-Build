import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from constraints import BrandGuidelines
from models import CampaignBrief
from pipeline import BrandContentCreationPipeline

load_dotenv(find_dotenv())

if __name__ == "__main__":
    guidelines = BrandGuidelines()
    brief = CampaignBrief(
        product="DataVault Pro",
        target_audience="CTOs and Data Engineering Leads",
        core_value_prop="Unified automated enterprise data governance and zero-trust lineage validation",
        guidelines=guidelines
    )

    pipeline = BrandContentCreationPipeline()
    print("=== Launching Autonomous Brand Content Creation Pipeline ===")
    campaign = pipeline.execute_campaign(brief)

    print("\n" + "="*80)
    print("CAMPAIGN DELIVERABLES SUMMARY")
    print("="*80)
    print(f"\n1. EMAIL NEWSLETTER (Preview):\n{campaign.email_newsletter[:250]}...\n")
    print(f"2. SEO BLOG ARTICLE (Preview):\n{campaign.seo_article[:250]}...\n")
    print(f"3. AD COPY (Preview):\n{campaign.ad_copy[:250]}...\n")

    print("4. MULTIMODAL ASSET REQUESTS:")
    for asset in campaign.asset_requests:
        print(f"   - [{asset.asset_type.upper()}] ID: {asset.asset_id} | Ratio: {asset.aspect_ratio}")
        print(f"     Prompt: {asset.prompt}")

    print("\n5. CLOSED-LOOP ANALYTICS & ADAPTATION:")
    for metric, val in campaign.analytics_feedback.items():
        print(f"   - {metric}: {val}")