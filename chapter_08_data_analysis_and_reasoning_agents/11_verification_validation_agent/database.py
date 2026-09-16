from typing import Dict, Any

# Fuente de verdad interna autoritativa (Ground Truth)
TRUSTED_DATABASE: Dict[str, Dict[str, Any]] = {
    "ottawa_unemployment_rate_change_2024": {
        "value": -0.048,  # -4.8%
        "source": "Statistics Canada, Labour Force Survey, Table 14-10-0287-01",
        "notes": "Annual change from 2023 to 2024 for Ottawa-Gatineau CMA."
    },
    "city_budget_surplus_2024": {
        "value": 15_200_000,  # $15.2M
        "source": "City of Ottawa Annual Financial Report 2024",
        "notes": "Reported surplus for the fiscal year ending 2024."
    }
}