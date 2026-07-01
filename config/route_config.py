"""Commercial route definitions for Retail v1 concept quote preview."""

ROUTES = {
    "essential": {
        "name": "Essential",
        "headline": "Measure the basics reliably",
        "description": "For retailers that first need a trusted baseline for store traffic and conversion potential.",
        "includes": [
            "Advantage Portal",
            "Data management",
            "Footfall",
            "Portfolio-wide report",
            "Sensor management",
            "Remote support",
            "Conversion rate",
        ],
    },
    "professional": {
        "name": "Professional",
        "headline": "Understand who visits and what attracts them",
        "description": "For retailers that want visitor profile insights, capture-rate context and richer performance explanation.",
        "includes": [
            "Everything in Essential",
            "Age / gender / group options",
            "Adults / kids",
            "Occupancy",
            "Capture rate",
        ],
    },
    "enterprise": {
        "name": "Enterprise",
        "headline": "Analyse journeys, zones and in-store behaviour",
        "description": "For retailers that want in-store analytics, zoning, dwell, Re-ID feasibility or advanced reporting.",
        "includes": [
            "Everything in Professional",
            "Re-ID / dwell feasibility",
            "Heat mapping",
            "Sales-data conversion report",
            "In-store journey analytics",
        ],
    },
}
