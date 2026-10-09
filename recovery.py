"""
Gadgetbay Recovery Engine
Calculates recovery values for returned products.
"""


def calculate_recovery(
    selling_price,
    cost_price,
    refurb_cost,
    resale_pct,
    vendor_credit_pct,
    liquidation_pct,
):
    # Refurbishment
    refurbished_sale = selling_price * resale_pct / 100
    refurb_net = refurbished_sale - refurb_cost

    # Vendor return credit
    vendor_recovery = cost_price * vendor_credit_pct / 100

    # Liquidation
    liquidation_recovery = cost_price * liquidation_pct / 100

    return [
        {
            "route": "Refurbish",
            "recovery_per_unit": round(refurb_net, 2),
            "time_to_cash_days": 5,
            "note": "Subject to resale demand",
        },
        {
            "route": "Vendor Return",
            "recovery_per_unit": round(vendor_recovery, 2),
            "time_to_cash_days": None,
            "note": "Only eligible units; credit timing unspecified",
        },
        {
            "route": "Liquidation",
            "recovery_per_unit": round(liquidation_recovery, 2),
            "time_to_cash_days": None,
            "note": "Liquidation timing unspecified",
        },
    ]


def recommend_batch(total_units, eligible_units):
    if total_units < 0 or eligible_units < 0:
        raise ValueError("Unit quantities cannot be negative")

    if eligible_units > total_units:
        raise ValueError("Eligible units cannot exceed total units")

    return {
        "vendor_return_units": eligible_units,
        "refurbish_units": total_units - eligible_units,
    }


if __name__ == "__main__":
    routes = calculate_recovery(
        selling_price=2500,
        cost_price=1400,
        refurb_cost=250,
        resale_pct=75,
        vendor_credit_pct=60,
        liquidation_pct=35,
    )

    print("GADGETBAY RECOVERY COMPARISON")
    for route in routes:
        print(
            f"{route['route']}: "
            f"Rs. {route['recovery_per_unit']} per unit"
        )

    plan = recommend_batch(40, 24)
    print("\nSUGGESTED BATCH SPLIT")
    print(plan)
