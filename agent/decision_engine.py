from agent.models import UserState
from agent.models import Decision
from agent.field_registry import FIELD_REGISTRY

from agent.field_registry import *


def evaluate_field_action(
    field_def: FieldDefinition,
    user_state: UserState
) -> Literal["ask", "confirm", "accept", "postpone"]:
    field_name = field_def.name
    field_state = user_state.fields.get(field_name)

    if field_state and field_state.status in {"confirmed", "user_provided"}:
        return "accept"

    if field_state and field_state.status == "inferred":
        confidence = field_state.confidence

        if field_def.ask_strategy == "infer_fallback_ask":
            if confidence >= 0.85:
                return "accept"
            elif confidence >= 0.55:
                return "confirm"
            return "ask"

        if field_def.ask_strategy == "infer_and_confirm":
            if confidence >= 0.85: return "accept"
            elif confidence >= 0.50: return "confirm"
            return "ask"

    if field_def.ask_strategy == "ask_directly":
        if field_def.sensitivity == "high" and user_state.behavior.patience_level < 4:
            return "postpone"
        return "ask"

    return "ask"



def get_next_decision(user_state: UserState) -> Decision | None:
    candidate_decisions = []

    for field_name, field_def in FIELD_REGISTRY.items():
        action = evaluate_field_action(field_def, user_state)

        if action == "accept":
            continue

        priority = compute_field_priority(field_def, action)

        candidate_decisions.append(
            {
                "field_name": field_name,
                "action": action,
                "priority": priority,
                "field_def": field_def,
            }
        )

    if not candidate_decisions:
        return None

    candidate_decisions.sort(key=lambda x: x["priority"], reverse=True)
    best = candidate_decisions[0]

    return Decision(
        field_name=best["field_name"],
        action=best["action"],
        reason=f"Selected based on business impact, sensitivity, and strategy: {best['field_def'].ask_strategy}"
    )


def compute_field_priority(field_def: FieldDefinition, action: str) -> float:
    business_score = {"low": 1, "medium": 2, "high": 3}[field_def.business_impact]
    sensitivity_penalty = {"low": 0, "medium": 0.5, "high": 1}[field_def.sensitivity]

    action_bonus = {
        "confirm": 2.0,
        "ask": 1.0,
        "postpone": -2.0,
        "accept": -10.0,
    }[action]

    return business_score + action_bonus - sensitivity_penalty