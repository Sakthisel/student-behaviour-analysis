import os
import json
from dotenv import load_dotenv
from google import genai

from utils.llm_utils import prepare_student_summary

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_report(df):
    # =============================
    # STEP 1: AGGREGATE & SORT
    # =============================
    data_json = prepare_student_summary(df)

    # =============================
    # STEP 2: PROMPT
    # =============================
    prompt = f"""
    You are an expert classroom analytics AI.
    Analyze the following student performance data. 

    STRICT GUIDELINES:
    - RANKING: The student with the highest 'gd_score' is the Top Performer.
    - DATA INTEGRITY: Use exact IDs and scores from the JSON.
    - ML INSIGHT: Use 'ml_engagement' (LOW, MEDIUM, HIGH) to provide context on their predicted behavior.
    - SCORING: Higher scores in attention, engagement, and GD are better.

    DATA:
    {json.dumps(data_json, indent=2)}

    EXPECTED OUTPUT FORMAT:
    
    TOP PERFORMER:
    - Student ID: [ID]
    - Reason: [Brief explanation of why they are #1]

    RANKING:
    1. Student ID: [ID] - [Score Summary]
    2. Student ID: [ID] - [Score Summary]

    INDIVIDUAL REPORTS:
    Student ID: [ID]
    - Attention: [Score]
    - Engagement: [Score]
    - Performance (GD): [Score]
    - ML Insight: [Interpretation of ml_engagement]
    - Strength: [Based on highest sub-score]
    - Weakness: [Based on lowest sub-score]
    - Recommendation: [Actionable pedagogical advice]

    FINAL SUMMARY:
    [Overall classroom trend]
    """

    # =============================
    # STEP 3: GENERATION
    # =============================
    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error during generation: {str(e)}"
