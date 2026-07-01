"""Formatting helpers for UI and payload readability."""
from __future__ import annotations


def money(value: float | int | None, compact: bool = False) -> str:
    if value is None:
        return "n/a"
    value = float(value)
    if compact:
        abs_v = abs(value)
        if abs_v >= 1_000_000:
            return f"€{value / 1_000_000:.1f}M".replace(".0M", "M")
        if abs_v >= 100_000:
            return f"€{value / 1_000:.0f}K"
    return "€{:,.0f}".format(value).replace(",", ".")


def pct(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.1f}%"


def months(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.1f} mo."
