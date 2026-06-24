import json

from utils.gemini_client import ask_gemini


def planner_node(state):

    prompt = f"""
Convert the user request into CLI workflow.

Return JSON only.

Example:

{{
  "steps":[
    {{
      "id":1,
      "command":"mkdir demo"
    }}
  ]
}}

User Request:
{state["user_prompt"]}
"""

    result = ask_gemini(prompt)

    workflow = json.loads(
        result.replace("```json", "")
              .replace("```", "")
    )

    state["workflow"] = workflow

    return state