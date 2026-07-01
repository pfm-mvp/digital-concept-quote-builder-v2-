"""Sanitized mock Odoo/n8n configuration.

No production IDs are used in this file. Replace only after an approved test
integration contract has been agreed with the Odoo/n8n owners.
"""

COUNTRIES = ["Netherlands", "Germany", "United Kingdom", "France", "Belgium", "Other"]
OPERATING_UNITS = {
    "Retail Chain": {"mock_id": "OU_SHOPS_TEST", "label": "Shops"},
}
OPPORTUNITY_TYPES = {
    "Concept quote": {"mock_id": "OPP_CONCEPT_TEST"},
    "Budget indication": {"mock_id": "OPP_BUDGET_TEST"},
    "Premium indication": {"mock_id": "OPP_PREMIUM_TEST"},
}
QUOTE_TEMPLATES = {
    "Retail Chain": {
        "essential": "MOCK_TEMPLATE_RETAIL_ESSENTIAL",
        "professional": "MOCK_TEMPLATE_RETAIL_PROFESSIONAL",
        "enterprise": "MOCK_TEMPLATE_RETAIL_ENTERPRISE",
    }
}
SALESPEOPLE = [
    "Anna Reilander",
    "Christiaan van Rooijen",
    "Mark King",
    "Raymond Sestig",
    "Other / to assign",
]
