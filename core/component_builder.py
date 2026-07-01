"""Build active concept quote components from selected needs."""
from __future__ import annotations

import math
from typing import Dict, List, Any

from config.pricing_config import RETAIL_PRICING
from config.product_config import PERFORMANCE_NEEDS


def selected_component_keys(selected_need_ids: List[str]) -> List[str]:
    keys: List[str] = []
    for need_id in selected_need_ids:
        for component in PERFORMANCE_NEEDS.get(need_id, {}).get("components", []):
            if component not in keys:
                keys.append(component)
    if "entrance_performance" not in keys:
        keys.insert(0, "entrance_performance")
    return keys


def build_retail_components(
    selected_need_ids: List[str],
    stores: int,
    contract_years: int,
    capture_stores: int | None = None,
    instore_pilot_stores: int | None = None,
    average_store_sqm: float | None = None,
) -> Dict[str, Any]:
    """Return component rows and totals for concept quote preview."""
    stores = max(0, int(stores))
    contract_years = max(1, int(contract_years))
    keys = selected_component_keys(selected_need_ids)
    rows: List[Dict[str, Any]] = []

    for key in keys:
        pricing = RETAIL_PRICING[key]
        if key == "entrance_performance":
            units = stores
            capex = units * pricing["capex_per_store"]
            monthly = units * pricing["monthly_per_store"]
            rows.append({
                "component_key": key,
                "label": pricing["label"],
                "units": units,
                "scope": stores,
                "capex_total": capex,
                "monthly_total": monthly,
                "one_off_total": 0,
                "tco_total": capex + monthly * 12 * contract_years,
                "pricing_status": pricing["status"],
                "privacy_review_required": False,
            })
        elif key == "capture_rate":
            scope = pricing["default_scope_stores"] if capture_stores is None else max(0, int(capture_stores))
            scope = min(scope, stores)
            capex = scope * pricing["capex_per_store"]
            monthly = scope * pricing["monthly_per_store"]
            rows.append({
                "component_key": key,
                "label": pricing["label"],
                "units": scope,
                "scope": scope,
                "capex_total": capex,
                "monthly_total": monthly,
                "one_off_total": 0,
                "tco_total": capex + monthly * 12 * contract_years,
                "pricing_status": pricing["status"],
                "privacy_review_required": False,
            })
        elif key == "instore_journey":
            pilot_stores = pricing["default_pilot_stores"] if instore_pilot_stores is None else max(0, int(instore_pilot_stores))
            pilot_stores = min(pilot_stores, stores)
            sqm = pricing["default_store_sqm"] if average_store_sqm is None else max(0.0, float(average_store_sqm))
            sensors_per_store = math.ceil(sqm / pricing["sqm_coverage_per_sensor"]) if sqm > 0 else 0
            units = pilot_stores * sensors_per_store
            capex = pilot_stores * sqm * pricing["capex_per_sqm"]
            monthly = units * pricing["monthly_per_sensor"]
            rows.append({
                "component_key": key,
                "label": pricing["label"],
                "units": units,
                "scope": pilot_stores,
                "capex_total": capex,
                "monthly_total": monthly,
                "one_off_total": 0,
                "tco_total": capex + monthly * 12 * contract_years,
                "pricing_status": pricing["status"],
                "privacy_review_required": True,
            })
        elif key == "visitor_profile":
            # Default activation on entrance sensors. This is deliberately separate
            # from hardware CAPEX and requires privacy/commercial review.
            units = stores
            monthly_per_sensor = (
                pricing["gender_monthly_per_sensor"]
                + pricing["adult_child_monthly_per_sensor"]
                + pricing["group_monthly_per_sensor"]
            )
            monthly = units * monthly_per_sensor
            rows.append({
                "component_key": key,
                "label": pricing["label"],
                "units": units,
                "scope": stores,
                "capex_total": 0,
                "monthly_total": monthly,
                "one_off_total": 0,
                "tco_total": monthly * 12 * contract_years,
                "pricing_status": pricing["status"],
                "privacy_review_required": True,
            })

    totals = {
        "capex_total": sum(r["capex_total"] for r in rows),
        "monthly_total": sum(r["monthly_total"] for r in rows),
        "one_off_total": sum(r["one_off_total"] for r in rows),
        "tco_total": sum(r["tco_total"] for r in rows),
    }
    return {"components": rows, "totals": totals}
