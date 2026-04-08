from agent.models import UserState, FieldValue, Decision
from agent.state import set_field_value, add_question_to_history
from agent.decision_engine import get_next_decision
from agent.question_catalog import QUESTION_CATALOG
from agent.llm_inference_engine import run_llm_inference
from data.zillow_mock_api import get_zillow_features_by_zipcode


class AdaptiveQuestionnaireEngine:
    def __init__(self):
        self.user_state = UserState()

    def ingest_campaign_info(self, campaign_data: dict) -> None:
        intent = campaign_data.get("intent")
        veteran_campaign = campaign_data.get("veteran_campaign", False)
        property_use_hint = campaign_data.get("property_use_hint")

        if intent:
            set_field_value(
                self.user_state,
                "loan_primary_purpose",
                FieldValue(
                    value=intent,
                    source="campaign",
                    confidence=0.85,
                    status="inferred",
                ),
            )

        if veteran_campaign:
            set_field_value(
                self.user_state,
                "military_veteran",
                FieldValue(
                    value="yes",
                    source="campaign_veteran_targeting",
                    confidence=0.95,
                    status="confirmed",
                ),
            )

        if property_use_hint:
            set_field_value(
                self.user_state,
                "property_use",
                FieldValue(
                    value=property_use_hint,
                    source="campaign_audience",
                    confidence=0.90,
                    status="confirmed",
                ),
            )

    def ingest_user_context(self, user_context: dict) -> None:
        zipcode = user_context.get("zipcode")

        if zipcode:
            set_field_value(
                self.user_state,
                "zipcode",
                FieldValue(
                    value=zipcode,
                    source="ip_lookup",
                    confidence=0.60,
                    status="inferred",
                ),
            )

            zillow_features = get_zillow_features_by_zipcode(zipcode)
            if zillow_features:
                set_field_value(
                    self.user_state,
                    "property_value",
                    FieldValue(
                        value=zillow_features["median_home_value_range"],
                        source="zillow_mock_api",
                        confidence=zillow_features["property_value_confidence"],
                        status="inferred",
                    ),
                )

                set_field_value(
                    self.user_state,
                    "property_type",
                    FieldValue(
                        value=zillow_features["property_type_guess"],
                        source="zillow_mock_api",
                        confidence=zillow_features["property_type_confidence"],
                        status="inferred",
                    ),
                )

                income_hint = zillow_features.get("income_hint")
                if income_hint:
                    set_field_value(
                        self.user_state,
                        "annual_income",
                        FieldValue(
                            value=income_hint,
                            source="zipcode_affluence_prior",
                            confidence=0.45,
                            status="inferred",
                        ),
                    )

    def run_inference_pass(self) -> None:
        inferred = run_llm_inference(self.user_state)

        for field_name, field_value in inferred.items():
            existing = self.user_state.fields.get(field_name)

            if existing and existing.status in {"confirmed", "user_provided"}:
                continue

            if existing is None or field_value.confidence > existing.confidence:
                set_field_value(self.user_state, field_name, field_value)

    def get_next_question(self) -> Decision | None:
        decision = get_next_decision(self.user_state)

        if decision is None:
            return None

        question_meta = QUESTION_CATALOG.get(decision.field_name, {})
        decision.question_text = question_meta.get("question_text")
        decision.options = question_meta.get("options")

        return decision

    def apply_user_answer(self, field_name: str, value: str) -> None:
        set_field_value(
            self.user_state,
            field_name,
            FieldValue(
                value=value,
                source="user",
                confidence=1.0,
                status="user_provided",
            ),
        )
        add_question_to_history(self.user_state, field_name)

    def step(self) -> Decision | None:
        self.run_inference_pass()
        return self.get_next_question()