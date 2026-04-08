from typing import Optional


MOCK_ZILLOW_DB = {
    "10001": {
        "median_home_value_range": "500K_700K",
        "property_type_guess": "condo",
        "property_value_confidence": 0.70,
        "property_type_confidence": 0.58,
        "area_variance_score": 0.40,
        "income_hint": "100K_150K",
        "area_profile": "dense_urban",
    },
    "10011": {
        "median_home_value_range": "750K_1M",
        "property_type_guess": "condo",
        "property_value_confidence": 0.74,
        "property_type_confidence": 0.64,
        "area_variance_score": 0.36,
        "income_hint": "150K_250K",
        "area_profile": "urban_high_income",
    },
    "11215": {
        "median_home_value_range": "1M_plus",
        "property_type_guess": "townhouse",
        "property_value_confidence": 0.68,
        "property_type_confidence": 0.55,
        "area_variance_score": 0.52,
        "income_hint": "150K_250K",
        "area_profile": "mixed_brownstone_residential",
    },
    "20007": {
        "median_home_value_range": "1M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.80,
        "property_type_confidence": 0.78,
        "area_variance_score": 0.25,
        "income_hint": "250K_plus",
        "area_profile": "affluent_residential",
    },
    "30339": {
        "median_home_value_range": "650K_900K",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.76,
        "property_type_confidence": 0.72,
        "area_variance_score": 0.28,
        "income_hint": "100K_150K",
        "area_profile": "suburban_affluent",
    },
    "33139": {
        "median_home_value_range": "750K_1M",
        "property_type_guess": "condo",
        "property_value_confidence": 0.79,
        "property_type_confidence": 0.81,
        "area_variance_score": 0.31,
        "income_hint": "150K_250K",
        "area_profile": "coastal_condo_market",
    },
    "60614": {
        "median_home_value_range": "500K_750K",
        "property_type_guess": "mixed",
        "property_value_confidence": 0.44,
        "property_type_confidence": 0.35,
        "area_variance_score": 0.78,
        "income_hint": "100K_150K",
        "area_profile": "mixed_urban",
    },
    "60657": {
        "median_home_value_range": "500K_750K",
        "property_type_guess": "condo",
        "property_value_confidence": 0.62,
        "property_type_confidence": 0.57,
        "area_variance_score": 0.49,
        "income_hint": "100K_150K",
        "area_profile": "urban_mixed_condo",
    },
    "75205": {
        "median_home_value_range": "1M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.84,
        "property_type_confidence": 0.80,
        "area_variance_score": 0.22,
        "income_hint": "250K_plus",
        "area_profile": "luxury_single_family",
    },
    "77005": {
        "median_home_value_range": "750K_1M",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.77,
        "property_type_confidence": 0.74,
        "area_variance_score": 0.27,
        "income_hint": "150K_250K",
        "area_profile": "affluent_suburban",
    },
    "78704": {
        "median_home_value_range": "500K_750K",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.69,
        "property_type_confidence": 0.63,
        "area_variance_score": 0.43,
        "income_hint": "100K_150K",
        "area_profile": "gentrifying_mixed",
    },
    "85016": {
        "median_home_value_range": "500K_750K",
        "property_type_guess": "townhouse",
        "property_value_confidence": 0.55,
        "property_type_confidence": 0.48,
        "area_variance_score": 0.61,
        "income_hint": "100K_150K",
        "area_profile": "mixed_suburban",
    },
    "89109": {
        "median_home_value_range": "250K_500K",
        "property_type_guess": "condo",
        "property_value_confidence": 0.72,
        "property_type_confidence": 0.76,
        "area_variance_score": 0.34,
        "income_hint": "50K_100K",
        "area_profile": "highrise_condo",
    },
    "90049": {
        "median_home_value_range": "2M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.89,
        "property_type_confidence": 0.87,
        "area_variance_score": 0.18,
        "income_hint": "250K_plus",
        "area_profile": "ultra_luxury_residential",
    },
    "90210": {
        "median_home_value_range": "2M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.91,
        "property_type_confidence": 0.90,
        "area_variance_score": 0.16,
        "income_hint": "250K_plus",
        "area_profile": "ultra_luxury_single_family",
    },
    "91302": {
        "median_home_value_range": "1M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.86,
        "property_type_confidence": 0.84,
        "area_variance_score": 0.20,
        "income_hint": "250K_plus",
        "area_profile": "gated_residential_luxury",
    },
    "94109": {
        "median_home_value_range": "750K_1M",
        "property_type_guess": "condo",
        "property_value_confidence": 0.66,
        "property_type_confidence": 0.69,
        "area_variance_score": 0.42,
        "income_hint": "150K_250K",
        "area_profile": "urban_high_cost",
    },
    "94123": {
        "median_home_value_range": "1M_plus",
        "property_type_guess": "condo",
        "property_value_confidence": 0.73,
        "property_type_confidence": 0.71,
        "area_variance_score": 0.39,
        "income_hint": "150K_250K",
        "area_profile": "high_end_mixed_urban",
    },
    "95014": {
        "median_home_value_range": "2M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.88,
        "property_type_confidence": 0.85,
        "area_variance_score": 0.21,
        "income_hint": "250K_plus",
        "area_profile": "silicon_valley_affluent",
    },
    "98109": {
        "median_home_value_range": "750K_1M",
        "property_type_guess": "condo",
        "property_value_confidence": 0.71,
        "property_type_confidence": 0.73,
        "area_variance_score": 0.37,
        "income_hint": "150K_250K",
        "area_profile": "urban_tech_corridor",
    },
    "98199": {
        "median_home_value_range": "1M_plus",
        "property_type_guess": "single_family",
        "property_value_confidence": 0.78,
        "property_type_confidence": 0.76,
        "area_variance_score": 0.30,
        "income_hint": "150K_250K",
        "area_profile": "coastal_affluent_residential",
    },
}


def get_zillow_features_by_zipcode(zipcode: str) -> Optional[dict]:
    """
    Return mocked Zillow-style enrichment features for a given ZIP code.

    Returned fields may include:
    - median_home_value_range
    - property_type_guess
    - property_value_confidence
    - property_type_confidence
    - area_variance_score
    - income_hint
    - area_profile
    """
    return MOCK_ZILLOW_DB.get(zipcode)