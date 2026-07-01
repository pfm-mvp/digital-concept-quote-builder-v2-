from core.component_builder import build_retail_components
from core.roi_calculator import RetailAssumptions, calculate_retail_roi
from core.route_selector import select_route


def test_professional_route_for_visitor_profile():
    result = select_route(["baseline_missing", "visitor_profile_unknown"])
    assert result["route_key"] == "professional"


def test_roi_smoke():
    components = build_retail_components(["baseline_missing"], stores=50, contract_years=3)
    assumptions = RetailAssumptions(50, 8400, 18, 32, 60, 0, 1, 0, 6, 3, "Realistic base")
    roi = calculate_retail_roi(assumptions, components["totals"])
    assert roi["baseline_revenue_year_total"] > 0
    assert roi["tco_total"] > 0
