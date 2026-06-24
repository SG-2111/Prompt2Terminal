from utils.gemini_client import ask_gemini

def generate_report(execution_log):
    prompt = f"""
You are an execution analyzer.

Summarize this CLI run in a clean report.

Include:
- summary
- success/failure insights
- improvement suggestions

Execution log:
{execution_log}
"""

    return ask_gemini(prompt)