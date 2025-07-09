from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(description="Generate procurement plan by matching SKUs needing restock with the best supplier.")
def generate_procurement_plan() -> list:
    """
    Match SKUs needing restock with the best supplier (based on cost and lead time).

    Returns:
    - List of procurement plans, each with:
        - 'sku'
        - 'quantity_needed'
        - 'supplier'
        - 'lead_time_days'
        - 'unit_cost'
    """
    try:
        # Hardcoded restock data
        restock_data = [
            {"sku": "SKU001", "current_stock": 5, "reorder_level": 15},
            {"sku": "SKU002", "current_stock": 20, "reorder_level": 25},
            {"sku": "SKU003", "current_stock": 2, "reorder_level": 10},
        ]

        # Hardcoded supplier data
        suppliers_data = [
            {"sku": "SKU001", "supplier": "Supplier A", "lead_time_days": 3, "unit_cost": 10.5},
            {"sku": "SKU001", "supplier": "Supplier B", "lead_time_days": 2, "unit_cost": 11.0},
            {"sku": "SKU002", "supplier": "Supplier C", "lead_time_days": 5, "unit_cost": 9.0},
            {"sku": "SKU003", "supplier": "Supplier A", "lead_time_days": 1, "unit_cost": 15.0},
            {"sku": "SKU003", "supplier": "Supplier B", "lead_time_days": 2, "unit_cost": 14.5},
        ]

        plan_rows = []

        for restock in restock_data:
            quantity_needed = restock["reorder_level"] - restock["current_stock"]
            if quantity_needed <= 0:
                continue

            options = [s for s in suppliers_data if s["sku"] == restock["sku"]]
            if options:
                best_option = sorted(options, key=lambda x: (x["unit_cost"], x["lead_time_days"]))[0]
                plan_rows.append({
                    "sku": restock["sku"],
                    "quantity_needed": quantity_needed,
                    "supplier": best_option["supplier"],
                    "lead_time_days": best_option["lead_time_days"],
                    "unit_cost": best_option["unit_cost"],
                })

        return plan_rows

    except Exception as e:
        return [{"error": str(e)}]
