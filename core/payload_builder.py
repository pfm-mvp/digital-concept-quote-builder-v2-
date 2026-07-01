"""Build sanitized mock Odoo/n8n payloads."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any, List

from config.mock_odoo_config import OPERATING_UNITS, QUOTE_TEMPLATES, OPPORTUNITY_TYPES


def build_payload(
    intake: Dict[str, Any],
    selected_needs: List[str],
    component_result: Dict[str, Any],
    route_result: Dict[str, Any],
    roi_result: Dict[str, Any],
    review_checks: Dict[str, bool] | None = None,
) -> Dict[str, Any]:
    route_key = route_result["route_key"]
    now = datetime.now(timezone.utc).isoformat()
    review_checks = review_checks or {}

    concept_quote = {
        "company_name": intake.get("company_name"),
        "contact_name": intake.get("contact_name"),
        "contact_email": intake.get("contact_email"),
        "country": intake.get("country"),
        "customer_type": "Retail Chain",
        "stores": intake.get("stores"),
        "recommended_route": route_result["route"]["name"],
        "capex_total": roi_result["capex_total"],
        "monthly_service_total": roi_result["monthly_service_total"],
        "tco_total": roi_result["tco_total"],
        "realistic_extra_profit_year_total": roi_result["realistic_extra_profit_year_total"],
        "payback_months": roi_result["payback_months"],
        "roi_pct_over_horizon": roi_result["roi_pct_over_horizon"],
    }

    mock_odoo_payload = {
        "environment": "mock_only",
        "action": "preview_concept_quote_payload",
        "do_not_write_to_production_odoo": True,
        "operating_unit": OPERATING_UNITS["Retail Chain"],
        "opportunity_type": OPPORTUNITY_TYPES["Concept quote"],
        "quote_template_key": QUOTE_TEMPLATES["Retail Chain"][route_key],
        "salesperson_name": intake.get("salesperson"),
        "customer": {
            "company_name": intake.get("company_name"),
            "contact_name": intake.get("contact_name"),
            "contact_email": intake.get("contact_email"),
            "country": intake.get("country"),
        },
        "quote_lines_preview": component_result["components"],
        "commercial_totals": component_result["totals"],
        "human_review_required": True,
    }

    mock_n8n_payload = {
        "environment": "mock_only",
        "workflow_intent": "concept_quote_review",
        "do_not_trigger_live_workflow": True,
        "source": "pfm_digital_concept_quote_builder_v2",
        "created_at": now,
        "selected_needs": selected_needs,
        "route": route_result,
        "concept_quote": concept_quote,
        "mock_odoo_payload": mock_odoo_payload,
        "review": {
            "human_review_required": True,
            "checks": review_checks,
            "ready_for_internal_review": all(review_checks.values()) if review_checks else False,
        },
    }

    return {
        "source": "pfm_digital_concept_quote_builder_v2",
        "version": "2.0.0-mvp",
        "created_at": now,
        "environment": "mock_only",
        "not_sent_to_customer": True,
        "not_written_to_odoo": True,
        "human_review_required": True,
        "intake": intake,
        "selected_needs": selected_needs,
        "components": component_result,
        "route": route_result,
        "roi": roi_result,
        "concept_quote_preview": concept_quote,
        "mock_odoo_payload": mock_odoo_payload,
        "mock_n8n_payload": mock_n8n_payload,
    }
