from typing import TypedDict, Dict, List


class AgentState(TypedDict):
    user_prompt: str

    workflow: Dict

    safety_result: Dict

    simulation_result: Dict

    execution_log: List

    recovery_plan: Dict

    final_report: str

    approved: bool