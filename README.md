# PFM Digital Concept Quote Builder v2

Internal Streamlit MVP for turning a Retail Chain sales intake into a concept quote preview, ROI/TCO context and sanitized mock payloads for Odoo/n8n review.

This repo is intentionally separate from the customer-facing **PFM Retail Performance Scan v40**. Version 2 is not a visual customer demo; it is an internal quote-prep workflow prototype.

## Status

- Version: `2.0.0-mvp`
- Scope: Retail Chain only
- Environment: mock only
- Odoo: no production write
- n8n: no live trigger
- Customer email: not supported
- Human review: mandatory

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repo structure

```text
app.py
requirements.txt
README.md
config/
  pricing_config.py
  product_config.py
  route_config.py
  mock_odoo_config.py
core/
  roi_calculator.py
  component_builder.py
  route_selector.py
  payload_builder.py
  validation.py
  formatting.py
data/
  example_payload.json
docs/
  mvp_scope.md
  odoo_payload_contract.md
  n8n_payload_contract.md
  open_questions.md
```

## Design principles

1. Retail v1 only.
2. Concept quote preview only.
3. All Odoo/n8n output is mock and sanitized.
4. Pricing assumptions are marked as demo assumptions.
5. Human review is visible and required.
6. No production credentials, hard-coded production IDs or API calls.
7. Calculations live in pure Python helpers, not in a browser mega-script.

## Important guardrails

This app does **not**:

- create an Odoo quote;
- write to production Odoo;
- call an n8n webhook;
- send customer emails;
- create a final PDF quotation;
- approve pricing;
- replace sales/product/finance review.

## Relationship to v40

v40 remains the customer-facing conversation demo. This v2 repo uses the same conceptual direction:

- customer pains / performance leaks;
- PFM fit;
- ROI/TCO context;
- Essential / Professional / Enterprise route logic;
- structured payload thinking.

But v2 is rebuilt as a cleaner Streamlit-native internal MVP with separated config and core logic.
