"""Demo pricing assumptions for the PFM Digital Concept Quote Builder v2.

These values are deliberately marked as demo assumptions. They are useful for
internal testing and payload-shape validation, but they are not an approved
commercial price list.
"""

PRICING_METADATA = {
    "currency": "EUR",
    "pricing_status": "demo_assumption",
    "approved": False,
    "approved_by": None,
    "valid_from": None,
    "note": "Internal MVP fixture only. Finance/product approval required before customer use.",
}

RETAIL_PRICING = {
    "entrance_performance": {
        "label": "Entrance Performance Layer",
        "capex_per_store": 1500,
        "monthly_per_store": 21,
        "status": "demo_assumption",
        "approved": False,
        "description": "Indicative entrance sensor and performance baseline pricing.",
    },
    "capture_rate": {
        "label": "Street Potential / Capture Rate Layer",
        "capex_per_store": 500,
        "monthly_per_store": 10,
        "default_scope_stores": 10,
        "status": "demo_assumption",
        "approved": False,
        "description": "Indicative passer-by / street traffic context add-on.",
    },
    "instore_journey": {
        "label": "In-store Journey Layer",
        "capex_per_sqm": 35,
        "monthly_per_sensor": 125,
        "sqm_coverage_per_sensor": 75,
        "default_pilot_stores": 1,
        "default_store_sqm": 150,
        "status": "demo_assumption",
        "approved": False,
        "description": "Indicative in-store analytics pilot pricing.",
    },
    "visitor_profile": {
        "label": "Visitor Profile Dataset Add-ons",
        "gender_monthly_per_sensor": 5,
        "adult_child_monthly_per_sensor": 5,
        "age_monthly_per_sensor_future": 5,
        "group_monthly_per_sensor": 5,
        "default_activation_scope": "entrances",
        "status": "needs_privacy_and_pricing_review",
        "approved": False,
        "privacy_review_required": True,
        "description": "Dataset add-ons on activated 3D sensors: gender, adult/child, age/future, groups.",
    },
}

REALISATION_SCENARIOS = {
    "Conservative": 0.10,
    "Cautious base": 0.15,
    "Realistic base": 0.25,
    "Strong adoption": 0.35,
    "Best case": 0.50,
}

DEFAULT_RETAIL_ASSUMPTIONS = {
    "stores": 50,
    "weekly_footfall_per_store": 8400,
    "conversion_rate_pct": 18.0,
    "average_ticket_value": 32.0,
    "gross_margin_pct": 60.0,
    "footfall_uplift_pct": 0.0,
    "conversion_uplift_pp": 0.0,
    "atv_uplift_pct": 0.0,
    "open_days_per_week": 6,
    "contract_years": 3,
    "realisation_scenario": "Realistic base",
    "saturday_share_pct": 18.0,
    "saturday_boost_pct": 0.0,
}
