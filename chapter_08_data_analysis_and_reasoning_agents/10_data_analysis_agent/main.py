import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from agent import DataAnalysisAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    # 1. Crear dataset sintético de marketing y ventas
    csv_file = "marketing_campaign_data.csv"
    data = {
        "region": ["North", "South", "East", "West", "Central", "North", "South", "East", "West", "Central"],
        "marketing_spend": [12000, 8500, 15000, 22000, 9000, 13500, 9200, 16000, 24000, 9800],
        "revenue": [54000, 39000, 68000, 95000, 41000, 61000, 42000, 71000, 102000, 45000],
        "quarter": ["Q1", "Q1", "Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q2", "Q2"]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    agent = DataAnalysisAgent()
    query = "Evaluate the relationship and impact between marketing spend and generated revenue across regions."
    
    report = agent.analyze_and_explain(df, query, output_image="marketing_spend_vs_revenue.png")
    print("\n================ EXECUTIVE DATA INSIGHT REPORT ================")
    print(report)