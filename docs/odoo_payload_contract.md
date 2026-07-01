# Mock Odoo Payload Contract

## Purpose

The Odoo payload in this MVP is a sanitized preview. It is designed to help PFM discuss the future Odoo data contract without writing to production.

## Current payload boundary

```json
{
  "environment": "mock_only",
  "action": "preview_concept_quote_payload",
  "do_not_write_to_production_odoo": true,
  "operating_unit": {"mock_id": "OU_SHOPS_TEST", "label": "Shops"},
  "opportunity_type": {"mock_id": "OPP_CONCEPT_TEST"},
  "quote_template_key": "MOCK_TEMPLATE_RETAIL_ESSENTIAL",
  "salesperson_name": "Christiaan van Rooijen",
  "customer": {},
  "quote_lines_preview": [],
  "commercial_totals": {},
  "human_review_required": true
}
```

## Open Odoo decisions

- Which country/entity should Retail v1 use first?
- Which pricelist applies to concept quote previews?
- Which Odoo quotation templates should exist per route?
- How should salesperson mapping work without hard-coded personal IDs?
- Should discounts be modelled in the app or only in Odoo?
- Which fields are mandatory before creating a real draft quote?
- What is the approval gate before any production Odoo action is allowed?

## Integration guardrail

Before any live integration:

- use test Odoo only;
- use service credentials managed by IT;
- validate all required fields;
- log every payload;
- keep human review mandatory;
- define failure handling and rollback behaviour.
