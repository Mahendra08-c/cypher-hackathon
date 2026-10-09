"""
Gadgetbay Supplier Quality Detection
Identifies repeated faults in returned products.
"""


def analyse_return_patterns(returns, minimum_returns=5, alert_rate=30):
    """
    Each return should contain:
    sku, supplier_batch, reason_code
    """

    if minimum_returns < 1:
        raise ValueError("minimum_returns must be at least 1")

    if not 0 <= alert_rate <= 100:
        raise ValueError("alert_rate must be between 0 and 100")

    groups = {}

    for item in returns:
        key = (
            item.get("sku", "UNKNOWN"),
            item.get("supplier_batch", "UNKNOWN"),
        )

        groups.setdefault(key, []).append(item)

    alerts = []

    for (sku, batch), items in groups.items():
        total = len(items)
        reasons = {}

        for item in items:
            reason = item.get("reason_code", "UNKNOWN")
            reasons[reason] = reasons.get(reason, 0) + 1

        if total < minimum_returns:
            continue

        for reason, count in reasons.items():
            rate = count / total * 100

            if rate >= alert_rate:
                alerts.append({
                    "sku": sku,
                    "supplier_batch": batch,
                    "return_count": total,
                    "fault": reason,
                    "fault_count": count,
                    "fault_rate_percent": round(rate, 2),
                    "severity": (
                        "HIGH" if rate >= 60 else "REVIEW"
                    ),
                    "recommendation": (
                        "Investigate supplier batch and review "
                        "further returns before taking action."
                    ),
                })

    return alerts


if __name__ == "__main__":
    sample_returns = [
        {
            "sku": "HEADPHONE-01",
            "supplier_batch": "HB-09",
            "reason_code": "AUDIO_FAILURE",
        }
        for _ in range(28)
    ]

    sample_returns.extend([
        {
            "sku": "HEADPHONE-01",
            "supplier_batch": "HB-09",
            "reason_code": "OTHER",
        }
        for _ in range(12)
    ])

    for alert in analyse_return_patterns(sample_returns):
        print("\nSUPPLIER QUALITY ALERT")
        for key, value in alert.items():
            print(f"{key}: {value}")
