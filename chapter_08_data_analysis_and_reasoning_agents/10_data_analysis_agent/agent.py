import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class VizRecommendation(BaseModel):
    intent_summary: str = Field(description="Summary of the user's analytical intent")
    chart_type: Literal["line", "bar", "scatter", "table"] = Field(description="Recommended visual representation")
    x_axis: str = Field(description="Primary dimension or independent variable")
    y_axis: str = Field(description="Metric or dependent variable to evaluate")

class DataAnalysisAgent:
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def recommend_visualization(self, df: pd.DataFrame, query: str) -> VizRecommendation:
        """Cognitive intent analysis & schema recognition."""
        schema_info = {col: str(dtype) for col, dtype in df.dtypes.items()}
        prompt = f"""
You are a Lead Data Analyst. Given a user query and dataset schema, recommend the optimal visual representation.

Rules:
- Temporal trends -> 'line'
- Group comparisons -> 'bar'
- Continuous correlations / regressions -> 'scatter'
- Multi-dimensional summary -> 'table'

Dataset Schema: {schema_info}
Sample Data (Top 2 rows):
{df.head(2).to_dict(orient='records')}

User Query: "{query}"
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VizRecommendation,
                temperature=0.0
            )
        )
        return VizRecommendation.model_validate_json(response.text)

    def compute_statistical_reasoning(self, df: pd.DataFrame, x_col: str, y_col: str) -> Dict[str, Any]:
        """Performs descriptive statistics, correlation and OLS regression."""
        stats = {
            "mean_y": float(df[y_col].mean()),
            "std_y": float(df[y_col].std()),
            "correlation": float(df[x_col].corr(df[y_col])) if np.issubdtype(df[x_col].dtype, np.number) else None
        }

        # OLS regression if both features are numeric
        if np.issubdtype(df[x_col].dtype, np.number) and np.issubdtype(df[y_col].dtype, np.number):
            X = sm.add_constant(df[x_col])
            model = sm.OLS(df[y_col], X).fit()
            stats["r_squared"] = float(model.rsquared)
            stats["p_value"] = float(model.pvalues.iloc[1])
            stats["coefficient"] = float(model.params.iloc[1])
        return stats

    def render_visualization(self, df: pd.DataFrame, recommendation: VizRecommendation, output_path: str):
        """Renders the recommended chart to a PNG file."""
        fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
        
        if recommendation.chart_type == "bar":
            agg = df.groupby(recommendation.x_axis)[recommendation.y_axis].sum().reset_index()
            ax.bar(agg[recommendation.x_axis].astype(str), agg[recommendation.y_axis], color="#1f77b4")
            ax.set_ylabel(recommendation.y_axis)
        elif recommendation.chart_type == "line":
            ax.plot(df[recommendation.x_axis].astype(str), df[recommendation.y_axis], marker="o", color="#2ca02c")
            ax.set_ylabel(recommendation.y_axis)
        elif recommendation.chart_type == "scatter":
            ax.scatter(df[recommendation.x_axis], df[recommendation.y_axis], color="#d62728", alpha=0.8)
            ax.set_xlabel(recommendation.x_axis)
            ax.set_ylabel(recommendation.y_axis)

        ax.set_title(recommendation.intent_summary, fontsize=11, fontweight="bold")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close(fig)

    def analyze_and_explain(self, df: pd.DataFrame, query: str, output_image: str = "analysis_chart.png") -> str:
        # 1. Recommend visualization
        rec = self.recommend_visualization(df, query)
        print(f"[DataAnalysisAgent] Intent: {rec.intent_summary} -> Recommending '{rec.chart_type}' chart.")

        # 2. Compute statistics
        stats = self.compute_statistical_reasoning(df, rec.x_axis, rec.y_axis)
        
        # 3. Render visualization
        self.render_visualization(df, rec, output_image)
        print(f"[DataAnalysisAgent] Rendered chart saved to '{output_image}'.")

        # 4. Generate final grounded insight narrative
        prompt = f"""
You are a senior data analyst. Synthesize the analytical findings into a concise, professional executive narrative.

User Query: {query}
Recommendation: {rec.model_dump()}
Statistical Evidence: {stats}

Deliver an actionable, plain-language summary explaining trends, statistical significance, and variance.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text