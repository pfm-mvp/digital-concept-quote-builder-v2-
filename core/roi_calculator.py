"""Pure retail ROI and TCO calculation helpers."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any

from config.pricing_config import REALISATION_SCENARIOS


@dataclass
class RetailAssumptions:
    stores: int
    weekly_footfall_per_store: float
    conversion_rate_pct: float
    average_ticket_value: float
    gross_margin_pct: float
    footfall_uplift_pct: float
    conversion_uplift_pp: float
    atv_uplift_pct: float
    open_days_per_week: int
    contract_years: int
    realisation_scenario: str
    saturday_share_pct: float = 18.0
    saturday_boost_pct: float = 0.0


def calculate_retail_roi(assumptions: RetailAssumptions, commercial_totals: Dict[str, float]) -> Dict[str, Any]:
    """Calculate indicative ROI for Retail Chain concept quote scenarios.

    Conversion uplift is interpreted as percentage points, matching the original
    ROI calculator behaviour. For example: 1.0 means 18% -> 19%.
    """
    stores = max(0, int(assumptions.stores))
    weekly_footfall = max(0.0, float(assumptions.weekly_footfall_per_store))
    open_days = max(1, int(assumptions.open_days_per_week))
    contract_years = max(1, int(assumptions.contract_years))

    conv = max(0.0, min(1.0, assumptions.conversion_rate_pct / 100.0))
    atv = max(0.0, assumptions.average_ticket_value)
    gross_margin = max(0.0, min(1.0, assumptions.gross_margin_pct / 100.0))

    footfall_uplift = assumptions.footfall_uplift_pct / 100.0
    conversion_uplift = assumptions.conversion_uplift_pp / 100.0
    atv_uplift = assumptions.atv_uplift_pct / 100.0
    sat_share = max(0.0, min(1.0, assumptions.saturday_share_pct / 100.0))
    sat_boost = assumptions.saturday_boost_pct / 100.0
    realisation_factor = REALISATION_SCENARIOS.get(assumptions.realisation_scenario, 0.25)

    visitors_year_store = weekly_footfall * 52
    baseline_revenue_store = visitors_year_store * conv * atv
    baseline_revenue_total = baseline_revenue_store * stores

    visitors_year_store_new = visitors_year_store * (1 + footfall_uplift)
    conv_new = max(0.0, min(1.0, conv + conversion_uplift))
    atv_new = atv * (1 + atv_uplift)

    non_sat_visitors = visitors_year_store_new * (1 - sat_share)
    sat_visitors = visitors_year_store_new * sat_share
    new_revenue_store = (
        non_sat_visitors * conv_new * atv_new
        + sat_visitors * conv_new * (1 + sat_boost) * atv_new
    )
    new_revenue_total = new_revenue_store * stores

    theoretical_uplift_total = max(0.0, new_revenue_total - baseline_revenue_total)
    theoretical_extra_profit_total = theoretical_uplift_total * gross_margin
    realistic_extra_profit_year = theoretical_extra_profit_total * realisation_factor

    capex_total = float(commercial_totals.get("capex_total", 0.0))
    monthly_total = float(commercial_totals.get("monthly_total", 0.0))
    one_off_total = float(commercial_totals.get("one_off_total", 0.0))
    tco_total = capex_total + one_off_total + monthly_total * 12 * contract_years

    realistic_extra_profit_over_horizon = realistic_extra_profit_year * contract_years
    net_value = realistic_extra_profit_over_horizon - tco_total
    roi_pct = (net_value / tco_total * 100.0) if tco_total > 0 else None

    monthly_profit_after_service = realistic_extra_profit_year / 12.0 - monthly_total
    payback_months = (capex_total + one_off_total) / monthly_profit_after_service if monthly_profit_after_service > 0 else None

    return {
        "assumptions": asdict(assumptions),
        "baseline_revenue_year_total": round(baseline_revenue_total, 2),
        "scenario_revenue_year_total": round(new_revenue_total, 2),
        "theoretical_uplift_year_total": round(theoretical_uplift_total, 2),
        "theoretical_extra_profit_year_total": round(theoretical_extra_profit_total, 2),
        "realisation_factor": realisation_factor,
        "realistic_extra_profit_year_total": round(realistic_extra_profit_year, 2),
        "capex_total": round(capex_total, 2),
        "monthly_service_total": round(monthly_total, 2),
        "one_off_total": round(one_off_total, 2),
        "tco_total": round(tco_total, 2),
        "net_value_over_horizon": round(net_value, 2),
        "roi_pct_over_horizon": round(roi_pct, 1) if roi_pct is not None else None,
        "payback_months": round(payback_months, 1) if payback_months is not None else None,
        "notes": [
            "Indicative decision-support calculation only.",
            "Conversion uplift is modelled as percentage points.",
            "Human review required before external use.",
        ],
    }
