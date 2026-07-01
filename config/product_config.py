"""Retail v1 performance needs and component mapping.

This is a clean, internal version based on the customer-facing v40 behaviour,
not a copy of the v40 mega-index implementation.
"""

PERFORMANCE_NEEDS = {
    "baseline_missing": {
        "label": "We do not have a trusted performance baseline",
        "short_label": "Trusted baseline",
        "description": "Sales or transactions are known, but visitor volumes are not trusted enough to judge store performance.",
        "kpis": ["footfall", "conversion_rate", "sales_per_visitor"],
        "components": ["entrance_performance"],
        "route_weight": "essential",
        "privacy_review_required": False,
    },
    "visitors_not_buying": {
        "label": "We have visitors, but not enough buyers",
        "short_label": "Conversion leak",
        "description": "Traffic is visible, but the moment, store or reason for conversion leakage is still unclear.",
        "kpis": ["conversion_rate", "sales_per_visitor", "store_hour_performance"],
        "components": ["entrance_performance"],
        "route_weight": "essential",
        "privacy_review_required": False,
    },
    "street_vs_store": {
        "label": "We do not know if the problem is the street or the store",
        "short_label": "Capture rate",
        "description": "The business needs to separate street potential from in-store performance.",
        "kpis": ["capture_rate", "passerby_traffic", "street_traffic"],
        "components": ["entrance_performance", "capture_rate"],
        "route_weight": "professional",
        "privacy_review_required": False,
    },
    "stores_unfairly_compared": {
        "label": "Stores are compared unfairly",
        "short_label": "Portfolio benchmark",
        "description": "Different formats, store sizes and locations are compared without enough context.",
        "kpis": ["portfolio_benchmark", "peer_group_index", "sales_per_visitor"],
        "components": ["entrance_performance"],
        "route_weight": "essential",
        "privacy_review_required": False,
    },
    "staffing_service_moments": {
        "label": "Staffing and service moments rely too much on feeling",
        "short_label": "Service moments",
        "description": "Teams need better visibility on peak moments, missed opportunities and store-hour pressure.",
        "kpis": ["hourly_traffic", "conversion_by_hour", "service_pressure"],
        "components": ["entrance_performance"],
        "route_weight": "essential",
        "privacy_review_required": False,
    },
    "visitor_profile_unknown": {
        "label": "We do not know who is entering our stores",
        "short_label": "Visitor profile",
        "description": "The retailer wants to understand gender, adults/kids, age/future and group context.",
        "kpis": ["gender", "adult_child", "age_future", "groups", "visitor_profile"],
        "components": ["entrance_performance", "visitor_profile"],
        "route_weight": "professional",
        "privacy_review_required": True,
    },
    "groups_distort_conversion": {
        "label": "Families and groups make conversion look worse than it is",
        "short_label": "Groups / buying units",
        "description": "Group counting and adult/child context are needed to explain conversion more fairly.",
        "kpis": ["groups", "adult_child", "buying_units", "family_share"],
        "components": ["entrance_performance", "visitor_profile"],
        "route_weight": "professional",
        "privacy_review_required": True,
    },
    "instore_unknown": {
        "label": "We do not know what happens after people enter",
        "short_label": "In-store journey",
        "description": "The retailer needs to understand journeys, zones, dwell and layout performance.",
        "kpis": ["zone_traffic", "dwell_time", "heatmap", "route_flow"],
        "components": ["entrance_performance", "instore_journey"],
        "route_weight": "enterprise",
        "privacy_review_required": True,
    },
    "entrance_bounce": {
        "label": "People step in, hesitate and leave again",
        "short_label": "Entrance bounce",
        "description": "The store may lose visitors immediately after entry due to layout, greeting or product visibility.",
        "kpis": ["entrance_bounce", "dwell_time", "route_flow"],
        "components": ["entrance_performance", "instore_journey"],
        "route_weight": "enterprise",
        "privacy_review_required": True,
    },
}

ROUTE_RANK = {"essential": 1, "professional": 2, "enterprise": 3}
