# Mock n8n Payload Contract

## Purpose

The n8n payload is a mock workflow input that can be used to design future automation. It does not trigger a live workflow.

## Current payload intent

```json
{
  "environment": "mock_only",
  "workflow_intent": "concept_quote_review",
  "do_not_trigger_live_workflow": true,
  "source": "pfm_digital_concept_quote_builder_v2",
  "selected_needs": [],
  "route": {},
  "concept_quote": {},
  "mock_odoo_payload": {},
  "review": {
    "human_review_required": true,
    "ready_for_internal_review": false
  }
}
```

## Future workflow candidates

- Save payload to SharePoint/OneDrive for audit trail.
- Create internal review task.
- Create test Odoo draft quote after approval.
- Generate commercial one-pager after template approval.
- Notify salesperson when required fields are missing.

## Guardrails

- No live workflow in MVP.
- No customer email.
- No production Odoo write.
- No secrets in repo.
- Human review remains mandatory.
