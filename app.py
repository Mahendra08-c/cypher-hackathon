
from flask import Flask, render_template, jsonify

from recovery import calculate_recovery, recommend_batch
from quality import analyse_return_patterns

app = Flask(__name__)


def get_demo_data():
    """Build the challenge's sample return scenario."""

    total_units = 40
    eligible_units = 24

    routes = calculate_recovery(
        selling_price=2500,
        cost_price=1400,
        refurb_cost=250,
        resale_pct=75,
        vendor_credit_pct=60,
        liquidation_pct=35,
    )

    batch_plan = recommend_batch(total_units, eligible_units)

    # Demonstration data based on the challenge scenario.
    sample_returns = [
        {
            "sku": "HEADPHONE-01",
            "supplier_batch": "HB-09",
            "reason_code": (
                "AUDIO_FAILURE" if i < 28 else "OTHER"
            ),
        }
        for i in range(40)
    ]

    alerts = analyse_return_patterns(sample_returns)

    return {
        "total_units": total_units,
        "eligible_units": batch_plan["vendor_return_units"],
        "refurbish_units": batch_plan["refurbish_units"],
        "routes": routes,
        "alerts": alerts,
    }


@app.route("/")
def home():
    data = get_demo_data()
    return render_template("index.html", **data)


@app.route("/api/recovery")
def recovery_api():
    return jsonify(get_demo_data())


@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "Gadgetbay"})


if __name__ == "__main__":
    app.run(debug=True)
