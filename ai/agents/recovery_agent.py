from utils.gemini_client import ask_gemini
import json

def generate_recovery(failed_step):
    prompt = f"""
You are a CLI recovery engine.

A command failed. Suggest recovery steps.

Return STRICT JSON:

{{
  "action": string,
  "fixes": [string],
  "explanation": string
}}

Failed Step:
{json.dumps(failed_step, indent=2)}
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "action": "manual_intervention",
            "fixes": [],
            "explanation": "AI response invalid"
        }