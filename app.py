from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from config.mock_odoo_config import COUNTRIES, SALESPEOPLE
from config.pricing_config import DEFAULT_RETAIL_ASSUMPTIONS, REALISATION_SCENARIOS, PRICING_METADATA
from config.product_config import PERFORMANCE_NEEDS
from core.component_builder import build_retail_components
from core.formatting import money, months, pct
from core.payload_builder import build_payload
from core.roi_calculator import RetailAssumptions, calculate_retail_roi
from core.route_selector import select_route
from core.validation import validate_intake, review_checklist_complete

st.set_page_config(
    page_title="PFM Digital Concept Quote Builder v2",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
      --pfm-navy: #0C111D;
      --pfm-purple: #8B5CF6;
      --pfm-purple-dark: #762181;
      --pfm-red: #F04438;
      --pfm-surface: #F8FAFC;
      --pfm-border: #E4E7EC;
      --pfm-muted: #667085;
    }
    .block-container { padding-top: 1.2rem; padding-bottom: 3rem; }
    .pfm-hero {
      border: 1px solid var(--pfm-border);
      border-radius: 24px;
      padding: 28px 30px;
      background: linear-gradient(135deg, #0C111D 0%, #151B2B 65%, #271827 100%);
      color: white;
      box-shadow: 0 16px 40px rgba(16,24,40,.12);
      margin-bottom: 20px;
    }
    .pfm-hero h1 { margin: 0; font-size: 2.4rem; letter-spacing: -.04em; }
    .pfm-hero p { color: #D0D5DD; font-size: 1.05rem; margin-top: 10px; max-width: 980px; }
    .pfm-badge {
      display: inline-block; padding: 6px 10px; border-radius: 999px;
      background: rgba(139,92,246,.18); color: #C4B5FD; font-weight: 800;
      font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 12px;
    }
    .guardrail {
      border: 1px solid #FECACA; background: #FFF1F1; color: #7F1D1D;
      padding: 14px 16px; border-radius: 16px; margin: 12px 0 20px;
      font-weight: 700;
    }
    .metric-card {
      border: 1px solid var(--pfm-border); border-radius: 18px; padding: 18px;
      background: white; box-shadow: 0 6px 18px rgba(16,24,40,.06); min-height: 132px;
    }
    .metric-label { color: var(--pfm-muted); font-weight: 800; text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; }
    .metric-value { color: var(--pfm-navy); font-weight: 900; font-size: 1.8rem; margin-top: 10px; }
    .metric-card.dark { background: var(--pfm-navy); color: white; }
    .metric-card.dark .metric-value, .metric-card.dark .metric-label { color: white; }
    .metric-card.purple { background: linear-gradient(135deg, #A855F7, #762181); color: white; }
    .metric-card.purple .metric-value, .metric-card.purple .metric-label { color: white; }
    .small-muted { color: var(--pfm-muted); font-size: .92rem; }
    .component-row {
      border: 1px solid var(--pfm-border); border-radius: 16px; padding: 14px 16px;
      margin-bottom: 10px; background: white;
    }
    .component-row strong { color: var(--pfm-navy); }
    .chip { display:inline-block; padding: 4px 9px; border: 1px solid #D6BBFB; background:#F4EBFF; color:#762181; border-radius:999px; font-size:.8rem; font-weight:800; margin: 3px 4px 3px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pfm-hero">
      <div class="pfm-badge">Internal MVP · Retail v1 · Mock only</div>
      <h1>PFM Digital Concept Quote Builder v2</h1>
      <p>Internal sales workflow from customer need to concept quote preview, ROI/TCO context and sanitized mock payloads for Odoo/n8n review.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="guardrail">Guardrails: this app does not send customer emails, does not write to Odoo, does not trigger n8n, and does not create a final quotation. Human review is mandatory.</div>
    """,
    unsafe_allow_html=True,
)

# Session defaults
if "selected_needs" not in st.session_state:
    st.session_state.selected_needs = ["baseline_missing", "visitors_not_buying"]

assumption_defaults = DEFAULT_RETAIL_ASSUMPTIONS.copy()

tab_intake, tab_needs, tab_model, tab_preview, tab_payload = st.tabs([
    "1 · Sales intake",
    "2 · Needs & PFM fit",
    "3 · ROI/TCO model",
    "4 · Concept quote preview",
    "5 · Payload & review",
])

with tab_intake:
    st.subheader("Sales intake")
    st.caption("Required fields for an internal concept quote preview. Retail Chain only in this MVP.")
    c1, c2 = st.columns(2)
    with c1:
        company_name = st.text_input("Company name", value="Nelson Schoenen")
        contact_name = st.text_input("Contact name", value="")
        contact_email = st.text_input("Contact email", value="")
        country = st.selectbox("Country / entity", COUNTRIES, index=0)
    with c2:
        salesperson = st.selectbox("Salesperson", SALESPEOPLE, index=1)
        segment = st.text_input("Segment", value="Footwear Retail")
        stores = st.number_input("Number of stores", min_value=1, value=int(assumption_defaults["stores"]), step=1)
        current_measurement = st.selectbox(
            "Current measurement",
            ["Unknown", "Manual estimate", "Basic traffic counter", "Traffic + POS data", "Existing PFM customer"],
            index=2,
        )
    intake = {
        "company_name": company_name,
        "contact_name": contact_name,
        "contact_email": contact_email,
        "country": country,
        "salesperson": salesperson,
        "segment": segment,
        "stores": int(stores),
        "current_measurement": current_measurement,
        "customer_type": "Retail Chain",
    }
    errors = validate_intake(intake)
    if errors:
        st.warning("Required field check: " + " | ".join(errors))
    else:
        st.success("Required field check passed for mock preview.")

with tab_needs:
    st.subheader("Needs & PFM fit")
    st.caption("Select the business situations that match the customer conversation. These drive components and route selection.")
    labels = {need_id: f"{cfg['short_label']} — {cfg['label']}" for need_id, cfg in PERFORMANCE_NEEDS.items()}
    selected = st.multiselect(
        "Selected needs / performance leaks",
        options=list(PERFORMANCE_NEEDS.keys()),
        default=st.session_state.selected_needs,
        format_func=lambda x: labels[x],
    )
    if not selected:
        st.info("At least one need should be selected. Entrance Performance will be used as baseline if no need is selected.")
    st.session_state.selected_needs = selected

    st.markdown("### Selected PFM fit")
    for need_id in selected:
        cfg = PERFORMANCE_NEEDS[need_id]
        st.markdown(
            f"""
            <div class="component-row">
              <strong>{cfg['label']}</strong><br>
              <span class="small-muted">{cfg['description']}</span><br>
              {''.join([f'<span class="chip">{kpi}</span>' for kpi in cfg['kpis']])}
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_model:
    st.subheader("ROI/TCO model")
    st.caption("Indicative internal calculation based on the existing ROI logic. It is decision support, not an approved quotation.")
    m1, m2, m3 = st.columns(3)
    with m1:
        weekly_footfall = st.number_input("Weekly footfall per store", min_value=0, value=int(assumption_defaults["weekly_footfall_per_store"]), step=100)
        conversion_rate = st.number_input("Current conversion rate (%)", min_value=0.0, max_value=100.0, value=float(assumption_defaults["conversion_rate_pct"]), step=0.5)
        atv = st.number_input("Average ticket value (€)", min_value=0.0, value=float(assumption_defaults["average_ticket_value"]), step=1.0)
    with m2:
        gross_margin = st.slider("Gross margin (%)", min_value=0, max_value=100, value=int(assumption_defaults["gross_margin_pct"]), step=1)
        footfall_uplift = st.slider("Footfall uplift (%)", min_value=0.0, max_value=10.0, value=float(assumption_defaults["footfall_uplift_pct"]), step=0.1)
        conversion_uplift = st.slider("Conversion uplift (percentage points)", min_value=0.0, max_value=10.0, value=float(assumption_defaults["conversion_uplift_pp"]), step=0.1)
    with m3:
        atv_uplift = st.slider("ATV uplift (%)", min_value=0.0, max_value=10.0, value=float(assumption_defaults["atv_uplift_pct"]), step=0.1)
        realisation_scenario = st.selectbox("Realisation scenario", list(REALISATION_SCENARIOS.keys()), index=2)
        contract_years = st.number_input("Contract term / years", min_value=1, max_value=7, value=int(assumption_defaults["contract_years"]), step=1)

    advanced = st.expander("Advanced scope assumptions", expanded=False)
    with advanced:
        c1, c2, c3 = st.columns(3)
        with c1:
            open_days = st.number_input("Open days per week", min_value=1, max_value=7, value=int(assumption_defaults["open_days_per_week"]))
            capture_stores = st.number_input("Capture stores in scope", min_value=0, max_value=int(stores), value=0, step=1)
        with c2:
            instore_pilot_stores = st.number_input("In-store pilot stores", min_value=0, max_value=int(stores), value=1, step=1)
            avg_store_sqm = st.number_input("Average store sqm", min_value=0, value=150, step=10)
        with c3:
            saturday_share = st.slider("Saturday share (%)", 0, 100, int(assumption_defaults["saturday_share_pct"]), 1)
            saturday_boost = st.slider("Saturday ATV boost (%)", 0, 50, int(assumption_defaults["saturday_boost_pct"]), 1)

    component_result = build_retail_components(
        selected_need_ids=st.session_state.selected_needs,
        stores=int(stores),
        contract_years=int(contract_years),
        capture_stores=int(capture_stores),
        instore_pilot_stores=int(instore_pilot_stores),
        average_store_sqm=float(avg_store_sqm),
    )
    assumptions = RetailAssumptions(
        stores=int(stores),
        weekly_footfall_per_store=float(weekly_footfall),
        conversion_rate_pct=float(conversion_rate),
        average_ticket_value=float(atv),
        gross_margin_pct=float(gross_margin),
        footfall_uplift_pct=float(footfall_uplift),
        conversion_uplift_pp=float(conversion_uplift),
        atv_uplift_pct=float(atv_uplift),
        open_days_per_week=int(open_days),
        contract_years=int(contract_years),
        realisation_scenario=realisation_scenario,
        saturday_share_pct=float(saturday_share),
        saturday_boost_pct=float(saturday_boost),
    )
    roi_result = calculate_retail_roi(assumptions, component_result["totals"])
    route_result = select_route(st.session_state.selected_needs)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='metric-card dark'><div class='metric-label'>Payback</div><div class='metric-value'>{months(roi_result['payback_months'])}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='metric-card'><div class='metric-label'>Monthly service</div><div class='metric-value'>{money(roi_result['monthly_service_total'])}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='metric-card'><div class='metric-label'>3-year TCO</div><div class='metric-value'>{money(roi_result['tco_total'], compact=True)}</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='metric-card purple'><div class='metric-label'>Realistic profit / year</div><div class='metric-value'>{money(roi_result['realistic_extra_profit_year_total'], compact=True)}</div></div>", unsafe_allow_html=True)

    st.markdown("### Active concept components")
    for row in component_result["components"]:
        st.markdown(
            f"""
            <div class="component-row">
              <strong>{row['label']}</strong><br>
              Units: {row['units']} · CAPEX: {money(row['capex_total'])} · Monthly: {money(row['monthly_total'])} · TCO: {money(row['tco_total'])}
              <br><span class="small-muted">Pricing status: {row['pricing_status']} · Privacy review: {'Yes' if row['privacy_review_required'] else 'No'}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_preview:
    st.subheader("Concept quote preview")
    st.caption("Internal preview only. This is the commercial conversation output, not a final Odoo quotation.")
    route_result = select_route(st.session_state.selected_needs)
    component_result = build_retail_components(st.session_state.selected_needs, int(stores), int(contract_years), int(capture_stores), int(instore_pilot_stores), float(avg_store_sqm))
    roi_result = calculate_retail_roi(assumptions, component_result["totals"])

    left, right = st.columns([1, 1])
    with left:
        st.markdown(f"### Suggested route: {route_result['route']['name']}")
        st.write(route_result["route"]["headline"])
        st.write(route_result["route"]["description"])
        st.markdown("**Included:**")
        for item in route_result["route"]["includes"]:
            st.markdown(f"- {item}")
    with right:
        st.markdown("### Commercial indication")
        st.metric("Initial investment", money(roi_result["capex_total"]))
        st.metric("Monthly service", money(roi_result["monthly_service_total"]))
        st.metric("Indicative TCO", money(roi_result["tco_total"]))
        st.metric("Realistic extra profit / year", money(roi_result["realistic_extra_profit_year_total"], compact=True))
    st.info("Pricing is marked as demo_assumption and requires product/finance/sales review before external use.")

with tab_payload:
    st.subheader("Payload & human review")
    st.caption("Preview mock Odoo/n8n payloads. No live integrations are called.")

    st.markdown("### Human review checklist")
    review_checks = {
        "customer_details_checked": st.checkbox("Customer details checked"),
        "scope_checked": st.checkbox("Scope checked"),
        "pricing_assumptions_checked": st.checkbox("Pricing assumptions checked"),
        "country_entity_checked": st.checkbox("Country/entity checked"),
        "route_reviewed": st.checkbox("Route reviewed"),
        "privacy_sensitive_modules_checked": st.checkbox("Privacy-sensitive modules checked"),
        "sales_owner_approved": st.checkbox("Sales owner approved"),
    }

    component_result = build_retail_components(st.session_state.selected_needs, int(stores), int(contract_years), int(capture_stores), int(instore_pilot_stores), float(avg_store_sqm))
    roi_result = calculate_retail_roi(assumptions, component_result["totals"])
    route_result = select_route(st.session_state.selected_needs)
    payload = build_payload(intake, st.session_state.selected_needs, component_result, route_result, roi_result, review_checks)

    if review_checklist_complete(review_checks):
        st.success("Review checklist complete. Payload may be downloaded for internal review.")
    else:
        st.warning("Human review is incomplete. Download remains available for testing, but this is not ready for external use.")

    p1, p2 = st.tabs(["Mock Odoo payload", "Mock n8n payload"])
    with p1:
        st.json(payload["mock_odoo_payload"])
    with p2:
        st.json(payload["mock_n8n_payload"])

    filename = f"concept_quote_payload_{company_name.lower().replace(' ', '_') or 'company'}.json"
    st.download_button(
        "Download full JSON payload",
        data=json.dumps(payload, indent=2),
        file_name=filename,
        mime="application/json",
    )

    with st.expander("Pricing metadata"):
        st.json(PRICING_METADATA)
