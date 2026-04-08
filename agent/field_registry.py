from typing import List, Optional
"""
decision_engine.py

Responsibility:
Decide the next best action for each missing or unconfirmed field.

Inputs:
- user_state (dict containing gathered and inferred values)
- field registry metadata

Outputs:
- action recommendation: ask / confirm / accept / postpone

Does NOT:
- call external APIs
- render UI
- store persistent state
"""

from dataclasses import dataclass
from typing import Literal, Optional, Dict


@dataclass
class FieldDefinition:
    name: str
    inferability: Literal["high", "medium", "low", "none"]
    business_impact: Literal["high", "medium", "low"]
    sensitivity: Literal["high", "medium", "low"]
    ask_strategy: Literal["infer_fallback_ask", "infer_and_confirm", "ask_directly"]
    required_for_matching: bool = True
    imputation_source: Optional[str] = None
    description: str = ""
    allowed_values: Optional[List[str]] = None
    input_type: Literal["free_text", "categorical", "range"] = "free_text"

# The Field Registry acting as the single source of truth for the AI Agent
FIELD_REGISTRY: Dict[str, FieldDefinition] = {

    "loan_primary_purpose": FieldDefinition(
        name="loan_primary_purpose",
        inferability="high",
        business_impact="high",
        sensitivity="low",
        ask_strategy="infer_fallback_ask",
        imputation_source="campaign_intent",
        description="If inferred from campaign intent, accept it. Else, fallback to asking.",
        input_type = "free_text"
    ),

    "military_veteran": FieldDefinition(
        name="military_veteran",
        inferability="high",
        business_impact="medium",
        sensitivity="low",
        ask_strategy="infer_fallback_ask",
        input_type="categorical",
        allowed_values=["yes", "no"],
        imputation_source="campaign_targeting",
        description="If user came from a veterans campaign, accept. Otherwise ask directly."
    ),

    "zipcode": FieldDefinition(
        name="zipcode",
        inferability="high",
        business_impact="high",
        sensitivity="low",
        ask_strategy="infer_and_confirm",
        imputation_source="ip_address_or_campaign",
        description="Guess based on IP/Browser. Must confirm with user to ensure property location accuracy."
    ),

    "property_type": FieldDefinition(
        name="property_type",
        inferability="high",
        business_impact="high",
        sensitivity="low",
        ask_strategy="infer_and_confirm",
        imputation_source="zipcode_and_segment",
        description="Deduce from residential area, then present to the user for a quick confirmation.",
        input_type = "categorical",
        allowed_values = ['Single-family', "Apartments", "Villas", "Duplexes", "None of the above"]
    ),

    "property_use": FieldDefinition(
        name="property_use",
        inferability="medium",
        business_impact="high",
        sensitivity="medium",
        ask_strategy="infer_and_confirm",
        imputation_source="campaign_audience",
        description="Try to infer from investor audiences. High variance exists, so confirmation is required.",
        input_type="categorical",
        allowed_values= ["Primary Residence", "Second Home", "Investment"]
    ),

    "property_value": FieldDefinition(
        name="property_value",
        inferability="medium",
        business_impact="high",
        sensitivity="high",
        ask_strategy="infer_and_confirm",
        imputation_source="zipcode_and_real_estate_api",
        description="Estimate using APIs based on zipcode, then ask user to validate the range."
    ),

    "currently_have_mortgage": FieldDefinition(
        name="currently_have_mortgage",
        inferability="medium",
        business_impact="high",
        sensitivity="medium",
        ask_strategy="infer_and_confirm",
        imputation_source="demographics_and_interests",
        description="Guess based on age and campaign data. Ask user to validate.",
        input_type="categorical",
        allowed_values=["Yes","No"]
    ),

    "annual_income": FieldDefinition(
        name="annual_income",
        inferability="low",
        business_impact="high",
        sensitivity="high",
        ask_strategy="ask_directly",
        imputation_source=None,
        description="Weak inferability. Must ask the user directly."
    ),

    "credit_line": FieldDefinition(
        name="credit_line",
        inferability="none",
        business_impact="high",
        sensitivity="high",
        ask_strategy="ask_directly",
        imputation_source=None,
        description="Internal financial metric. Almost impossible to infer accurately. Must ask."
    ),

    "credit_score_rate": FieldDefinition(
        name="credit_score_rate",
        inferability="medium",
        business_impact="high",
        sensitivity="high",
        ask_strategy="infer_and_confirm",
        imputation_source="previous_answers",
        description="Estimate range based on mortgage size, salary, and geo. Ask user to confirm.",
        input_type="categorical",
        allowed_values=["380-579" , "580-669" , "670-739" , "740+"]
    )
}

