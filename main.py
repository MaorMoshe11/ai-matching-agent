from agent.questionnaire_engine import AdaptiveQuestionnaireEngine
from data.mock_data import MOCK_USERS


def get_user_input(options):
    if options:
        print("Please choose one of the following options:")
        for idx, opt in enumerate(options):
            print(f"{idx + 1}. {opt}")

        while True:
            user_input = input("Enter option number: ").strip()

            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(options):
                    return options[idx]

            print("Invalid input, try again.")
    else:
        return input("Your answer: ").strip()


def main():
    print("Choose scenario:")
    print("1. standard_user")
    print("2. investor")
    print("3. veteran_user")

    scenario_choice = input("Enter scenario number: ").strip()
    scenario_map = {
        "1": "standard_user",
        "2": "luxury_investor",
        "3": "veteran_user",
    }

    scenario_name = scenario_map.get(scenario_choice, "standard_user")
    scenario = MOCK_USERS[scenario_name]

    engine = AdaptiveQuestionnaireEngine()
    engine.ingest_campaign_info(scenario["campaign_data"])
    engine.ingest_user_context(scenario["user_context"])

    step_idx = 0

    while True:
        decision = engine.step()

        if decision is None:
            print("\nQuestionnaire complete.")
            break

        step_idx += 1
        print(f"\n--- Step {step_idx} ---")
        print(f"Field: {decision.field_name}")
        print(f"Action: {decision.action}")
        print(f"Reason: {decision.reason}")

        if decision.action == "confirm":
            current_value = engine.user_state.fields[decision.field_name].value

            if decision.field_name == "zipcode":
                print(f"\nWe believe the property ZIP code may be {current_value}.")
                answer = input(
                    "Press Enter to accept, or type the correct ZIP code: "
                ).strip()

                if answer == "":
                    engine.apply_user_answer(decision.field_name, current_value)
                else:
                    engine.apply_user_answer(decision.field_name, answer)

            elif decision.field_name == "property_type":
                print(
                    f"\nOur system estimates that properties in this area are often '{current_value}'."
                )
                answer = input(
                    "Press Enter if this matches your property, or type the correct property type: "
                ).strip()

                if answer == "":
                    engine.apply_user_answer(decision.field_name, current_value)
                else:
                    engine.apply_user_answer(decision.field_name, answer)

            else:
                print(f"\nWe inferred: {current_value}")
                answer = input("Press Enter to accept, or type the correct value: ").strip()

                if answer == "":
                    engine.apply_user_answer(decision.field_name, current_value)
                else:
                    engine.apply_user_answer(decision.field_name, answer)

        elif decision.action == "ask":
            print(f"\n{decision.question_text}")
            answer = get_user_input(decision.options)
            engine.apply_user_answer(decision.field_name, answer)

        elif decision.action == "postpone":
            print(f"\nPostponing {decision.field_name} for now.")
            continue

    print("\nFinal user state:")
    for field_name, field_value in engine.user_state.fields.items():
        print(
            f"{field_name}: value={field_value.value}, "
            f"source={field_value.source}, "
            f"confidence={field_value.confidence:.2f}, "
            f"status={field_value.status}"
        )


if __name__ == "__main__":
    main()