import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from vqa_agent import VisionLanguageAgent

load_dotenv(find_dotenv())

def create_mock_workspace_image(output_path: str):
    """Generates a synthetic workspace visual scene for demonstration."""
    img = Image.new("RGB", (600, 400), color=(240, 243, 246))
    draw = ImageDraw.Draw(img)

    # Desk surface
    draw.rectangle([(50, 250), (550, 380)], fill=(139, 90, 43))

    # Laptop
    draw.rectangle([(150, 200), (300, 280)], fill=(70, 70, 70))
    draw.polygon([(150, 280), (300, 280), (320, 310), (130, 310)], fill=(160, 160, 160))

    # Coffee cup precariously balanced near edge
    draw.rectangle([(480, 230), (520, 280)], fill=(180, 50, 50))
    draw.ellipse([(475, 240), (485, 270)], outline=(180, 50, 50), width=3)

    # Document stack
    draw.rectangle([(450, 280), (540, 320)], fill=(255, 255, 255), outline=(100, 100, 100))

    img.save(output_path)

if __name__ == "__main__":
    image_path = os.path.join(CURRENT_DIR, "sample_workspace.png")
    create_mock_workspace_image(image_path)

    agent = VisionLanguageAgent()
    question = "Is there any object in an unstable or risky position on the desk? Describe the spatial relationship."
    
    print("=== Vision-Language Perception Agent ===")
    print(f"Analyzing: {image_path}")
    print(f"Question:  {question}\n" + "="*70)

    result = agent.answer_visual_query(image_path, question)
    print(f"Visual CoT Reasoning:\n{result.step_by_step_analysis}\n")
    print(f"Definitive Grounded Answer:\n{result.answer}")