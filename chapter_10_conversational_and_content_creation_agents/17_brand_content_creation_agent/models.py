from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class CampaignBrief:
    product: str
    target_audience: str
    core_value_prop: str
    guidelines: Any

@dataclass
class AssetRequest:
    """Structured contract for multimodal asset generation."""
    asset_id: str
    asset_type: str  # e.g., 'image_dalle', 'chart'
    prompt: str
    aspect_ratio: str = "16:9"

@dataclass
class CampaignPackage:
    email_newsletter: str = ""
    seo_article: str = ""
    ad_copy: str = ""
    asset_requests: List[AssetRequest] = field(default_factory=list)
    analytics_feedback: Dict[str, Any] = field(default_factory=dict)