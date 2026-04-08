MOCK_USERS = {
    "standard_user": {
        "campaign_data": {
            "intent": "home_improvement",
            "veteran_campaign": False,
        },
        "user_context": {
            "zipcode": "10001",
        },
        "mock_answers": {
            "zipcode": "10001",
            "property_type": "condo",
            "property_use": "primary_residence",
            "currently_have_mortgage": "yes",
            "annual_income": "100K_150K",
            "credit_score_rate": "670-739",
            "credit_line": "10K_50K",
            "property_value": "500K_750K",
            "military_veteran": "no",
        },
    },
    "luxury_investor": {
        "campaign_data": {
            "intent": "cash_out",
            "veteran_campaign": False,
            "property_use_hint": "investment_property",
        },
        "user_context": {
            "zipcode": "90210",
        },
        "mock_answers": {
            "zipcode": "90210",
            "property_type": "single_family",
            "currently_have_mortgage": "yes",
            "annual_income": "250K_plus",
            "credit_score_rate": "740+",
            "credit_line": "100K_plus",
            "property_value": "2M_plus",
            "military_veteran": "no",
        },
    },
    "veteran_user": {
        "campaign_data": {
            "intent": "debt_consolidation",
            "veteran_campaign": True,
        },
        "user_context": {
            "zipcode": "30339",
        },
        "mock_answers": {
            "zipcode": "30339",
            "property_type": "single_family",
            "property_use": "primary_residence",
            "currently_have_mortgage": "yes",
            "annual_income": "100K_150K",
            "credit_score_rate": "580-669",
            "credit_line": "10K_50K",
            "property_value": "650K_900K",
        },
    },
}