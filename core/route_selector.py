"""Select the suggested commercial route from selected needs."""
from __future__ import annotations

from typing import List, Dict, Any

from config.product_config import PERFORMANCE_NEEDS, ROUTE_RANK
from config.route_config import ROUTES


def select_route(selected_need_ids: List[str]) -> Dict[str, Any]:
    best_key = "essential"
    reasons = []
    for need_id in selected_need_ids:
        need = PERFORMANCE_NEEDS.get(need_id)
        if not need:
            continue
        weight = need.get("route_weight", "essential")
        reasons.append({"need_id": need_id, "need": need["label"], "route_weight": weight})
        if ROUTE_RANK[weight] > ROUTE_RANK[best_key]:
            best_key = weight
    route = ROUTES[best_key]
    return {"route_key": best_key, "route": route, "reasoning": reasons}
