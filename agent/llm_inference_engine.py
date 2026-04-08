import os
import json
from openai import OpenAI

from agent.models import FieldValue, UserState

client = OpenAI(api_key="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")


INFERABLE_FIELDS = [
    "property_use",
    "property_value",
    "currently_have_mortgage",
    "credit_score_rate",
]


def serialize_user_state(user_state: UserState) -> dict:
    serialized = {}

    for field_name, field_value in user_state.fields.items():
        serialized[field_name] = {
            "value": field_value.value,
            "source": field_value.source,
            "confidence": field_value.confidence,
            "status": field_value.status,
        }

    return serialized


def run_llm_inference(user_state: UserState) -> dict[str, FieldValue]:
    state_payload = serialize_user_state(user_state)

    prompt = f"""
You are an internal inference engine for an adaptive financial questionnaire.

Your job:
- Infer likely values for missing or still-unconfirmed fields
- Use only the evidence available in the current state
- Do not override confirmed or user_provided fields
- Be conservative
- Return valid JSON only

Return this schema:
{{
  "inferred_fields": {{
    "<field_name>": {{
      "value": "...",
      "confidence": 0.0,
      "source": "llm_inference"
    }}
  }}
}}

Allowed inferable fields:
{json.dumps(INFERABLE_FIELDS)}

Current user state:
{json.dumps(state_payload, indent=2)}
"""

    response = client.responses.create(
        model="gpt-5.4",
        input=prompt,
    )

    raw = response.output_text.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    inferred_fields = parsed.get("inferred_fields", {})
    results = {}

    for field_name, payload in inferred_fields.items():
        value = payload.get("value")
        confidence = payload.get("confidence")

        if value is None or confidence is None:
            continue

        results[field_name] = FieldValue(
            value=value,
            source="llm_inference",
            confidence=max(0.0, min(1.0, float(confidence))),
            status="inferred",
        )

    return results