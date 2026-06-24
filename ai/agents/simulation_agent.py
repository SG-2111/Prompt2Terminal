from utils.gemini_client import ask_gemini
import json

def simulate_workflow(workflow):
    prompt = f"""
You are a CLI safety simulation engine.

Analyze this workflow and predict execution safety.

Return STRICT JSON only:

{{
  "results": [
    {{
      "step_id": int,
      "status": "safe" | "risky" | "blocked",
      "reason": string
    }}
  ],
  "overall_status": "SAFE" | "NOT SAFE"
}}

Workflow:
{json.dumps(workflow, indent=2)}
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "error": "Gemini returned invalid JSON",
            "raw_output": response
        }