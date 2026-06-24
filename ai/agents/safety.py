from utils.gemini_client import ask_gemini

def analyze_risk(workflow):
    """
    workflow = {
        "goal": "...",
        "steps": [
            {"action": "...", "reason": "..."}
        ]
    }
    """

    prompt = f"""
You are a terminal safety system for an AI agent.

Your job is to evaluate whether a CLI workflow is safe to execute.

RULES:
- Block dangerous system actions
- Block destructive file operations
- Block network/system shutdown commands
- Allow normal dev operations (install, run, build, test)

DANGEROUS PATTERNS:
- rm -rf
- delete all files
- format disk
- shutdown system
- overwrite system files
- credential exposure

Return ONLY valid JSON:

{{
  "risk": "LOW | MEDIUM | HIGH",
  "blocked": true | false,
  "reason": "short explanation"
}}

Workflow:
{workflow}
"""

    return ask_gemini(prompt)