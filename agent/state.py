from agent.models import FieldValue, UserState

def get_field_value(user_state: UserState, field_name: str) -> FieldValue | None:
    return user_state.fields.get(field_name)


def set_field_value(user_state: UserState, field_name: str, field_value: FieldValue) -> None:
    user_state.fields[field_name] = field_value


def mark_field_confirmed(user_state: UserState, field_name: str) -> None:
    field_value = user_state.fields.get(field_name)
    if field_value:
        field_value.status = "confirmed"


def add_question_to_history(user_state: UserState, field_name: str) -> None:
    user_state.question_history.append(field_name)


def get_missing_or_unconfirmed_fields(user_state: UserState, field_registry: dict) -> list[str]:
    result = []

    for field_name in field_registry.keys():
        field_value = user_state.fields.get(field_name)

        if field_value is None:
            result.append(field_name)
        elif field_value.status in {"missing", "inferred"}:
            result.append(field_name)

    return result