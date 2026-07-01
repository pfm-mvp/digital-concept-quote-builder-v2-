"""Validation helpers for the concept quote builder."""
from __future__ import annotations

from typing import Dict, List, Any


def validate_intake(intake: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ["company_name", "contact_name", "contact_email", "country", "salesperson"]
    for field in required:
        if not str(intake.get(field, "")).strip():
            errors.append(f"Missing required field: {field.replace('_', ' ')}")
    if intake.get("stores", 0) <= 0:
        errors.append("Number of stores must be greater than 0.")
    if "@" not in str(intake.get("contact_email", "")):
        errors.append("Contact email should contain an @ sign.")
    return errors


def review_checklist_complete(checks: Dict[str, bool]) -> bool:
    return bool(checks) and all(checks.values())
