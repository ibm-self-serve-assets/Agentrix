from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import pulp

@tool
def generate_procurement_plan(is_optimized: bool = False) -> dict:
    """
    Generates and compares procurement plans with and without optimization,
    incorporating budget and supplier capacity constraints to potentially show savings.

    Returns:
    - Dictionary containing two lists: 'optimized_plan' and 'non_optimized_plan'.
    """
    try:
        # Hardcoded restock data
        restock_data = [
            {"sku": "SKU001", "current_stock": 5, "reorder_level": 100},  # Need 95 units
            {"sku": "SKU002", "current_stock": 20, "reorder_level": 100},  # Need 80 units
            {"sku": "SKU003", "current_stock": 2, "reorder_level": 50},   # Need 48 units
            {"sku": "SKU004", "current_stock": 10, "reorder_level": 200},  # Need 190 units
        ]

        # Modified supplier data with constraints designed to show optimization savings
        suppliers_data = [
            {"sku": "SKU001", "supplier": "Supplier A - Low Cost (Limited)", "lead_time_days": 3, "unit_cost": 2.5, "capacity": 50},
            {"sku": "SKU001", "supplier": "Supplier B - Med Cost (High Capacity)", "lead_time_days": 10, "unit_cost": 2.7, "capacity": 200},

            {"sku": "SKU002", "supplier": "Supplier C - Very Low Cost (Limited)", "lead_time_days": 5, "unit_cost": 1.5, "capacity": 60},
            {"sku": "SKU002", "supplier": "Supplier D - Low Cost (High Capacity)", "lead_time_days": 4, "unit_cost": 1.6, "capacity": 150},

            {"sku": "SKU003", "supplier": "Supplier E - Low Cost (Sufficient)", "lead_time_days": 8, "unit_cost": 3.0, "capacity": 100},
            {"sku": "SKU003", "supplier": "Supplier F - High Cost", "lead_time_days": 10, "unit_cost": 3.5, "capacity": 100},

            {"sku": "SKU004", "supplier": "Supplier G - Low Cost (Limited)", "lead_time_days": 7, "unit_cost": 1.1, "capacity": 100},
            {"sku": "SKU004", "supplier": "Supplier H - Med Cost (High Capacity)", "lead_time_days": 4, "unit_cost": 1.2, "capacity": 300},
        ]

        total_budget = 800  # Keep a reasonable budget

        # --- Generate Optimized Plan with Constraints ---
        optimized_plan = []
        non_optimized_plan = []

        prob = pulp.LpProblem("Constrained Procurement Optimization V2", pulp.LpMinimize)
        procurement_vars = {}

        # If is_optimized is True, apply optimization logic
        if is_optimized:
            for restock in restock_data:
                sku = restock["sku"]
                quantity_needed = restock["reorder_level"] - restock["current_stock"]
                if quantity_needed > 0:
                    options = [s for s in suppliers_data if s["sku"] == sku and s["capacity"] >= quantity_needed] # Consider capacity
                    for option in options:
                        var_name = f"{sku}_{option['supplier'].replace(' ', '_')}"
                        procurement_vars[var_name] = pulp.LpVariable(var_name, lowBound=0, cat='Continuous')

            prob += pulp.lpSum(procurement_vars[var] * [s["unit_cost"] for s in suppliers_data if f"{s['sku']}_{s['supplier'].replace(' ', '_')}" == var][0] for var in procurement_vars)

            for restock in restock_data:
                sku = restock["sku"]
                quantity_needed = restock["reorder_level"] - restock["current_stock"]
                if quantity_needed > 0:
                    available_options = [s for s in suppliers_data if s["sku"] == sku and s["capacity"] >= quantity_needed]
                    if available_options:
                        prob += pulp.lpSum(procurement_vars.get(f"{sku}_{option['supplier'].replace(' ', '_')}", 0) for option in available_options) == quantity_needed
                    else:
                        return {"error": f"Insufficient supplier capacity for SKU {sku}"}

            prob += pulp.lpSum(procurement_vars[var] * [s["unit_cost"] for s in suppliers_data if f"{s['sku']}_{s['supplier'].replace(' ', '_')}" == var][0] for var in procurement_vars) <= total_budget

            prob.solve()

            # Extract optimized procurement decisions
            for restock in restock_data:
                sku = restock["sku"]
                quantity_needed = restock["reorder_level"] - restock["current_stock"]
                if quantity_needed > 0:
                    options = [s for s in suppliers_data if s["sku"] == sku and s["capacity"] >= quantity_needed]
                    for option in options:
                        var_name = f"{sku}_{option['supplier'].replace(' ', '_')}"
                        if pulp.value(procurement_vars[var_name]) > 0:
                            optimized_plan.append({
                                "sku": sku,
                                "quantity_needed": quantity_needed,
                                "supplier": option["supplier"],
                                "lead_time_days": option["lead_time_days"],
                                "unit_cost": option["unit_cost"]
                            })

        # --- Generate Non-Optimized Plan (Ignoring Constraints) ---
        else:
            for restock in restock_data:
                quantity_needed = restock["reorder_level"] - restock["current_stock"]
                if quantity_needed > 0:
                    options = [s for s in suppliers_data if s["sku"] == restock["sku"]]
                    best_option = sorted(options, key=lambda x: x["unit_cost"])[0]
                    non_optimized_plan.append({
                        "sku": restock["sku"],
                        "quantity_needed": quantity_needed,
                        "supplier": best_option["supplier"],
                        "lead_time_days": best_option["lead_time_days"],
                        "unit_cost": best_option["unit_cost"],
                    })

        return {"optimized_plan": optimized_plan, "non_optimized_plan": non_optimized_plan}

    except Exception as e:
        return {"error": str(e)}
