from dotenv import load_dotenv, find_dotenv
from verifier import VerificationValidationAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    article_text = """
    A new report on Ottawa's economy shows promising signs of recovery.
    According to official city documents, the city's unemployment rate fell by 5% last year,
    a significant improvement driven by the tech sector. Furthermore, the municipal
    government reported a budget surplus of $12 million for the 2024 fiscal year.
    """

    agent = VerificationValidationAgent()
    print("Starting Verification & Validation Agent Fact-Check...")
    claims = agent.extract_claims(article_text)
    print(f"Extracted {len(claims)} verifiable claims. Cross-referencing against internal ground truth...\n" + "="*80)

    for c in claims:
        result = agent.verify_claim(c)
        print(f"Claim:   \"{result['claim']}\"")
        print(f"Status:  [{result['status']}]")
        print(f"Details: {result['details']}")
        if "source" in result:
            print(f"Source:  {result['source']}")
        print("-" * 80)