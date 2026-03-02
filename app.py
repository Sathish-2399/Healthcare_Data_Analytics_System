import json
import time

from flask import Flask, Response, render_template, request, jsonify
from model import predict_disease
from simulator import RealTimeSimulator

app = Flask(__name__)
simulator = RealTimeSimulator()


def get_age_group(age):
    age = int(age)
    if age <= 12:
        return "Child"
    elif age <= 30:
        return "Young Adult"
    elif age <= 60:
        return "Adult"
    else:
        return "Senior"


@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        symptoms = request.form["symptoms"]
        age_group = get_age_group(age)
        output = predict_disease(age, gender, age_group, symptoms)

    return render_template("index.html", output=output)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", total=simulator.get_total_rows())


@app.route("/api/stream")
def stream():
    """SSE endpoint that pushes new records as they arrive."""
    def event_stream():
        last_count = 0
        while True:
            current_count = simulator.get_count()
            if current_count > last_count:
                new_records = simulator.get_latest(current_count - last_count)
                for record in new_records:
                    clean = {k: (None if pd_isnan(v) else v) for k, v in record.items()}
                    payload = json.dumps({
                        "record": clean,
                        "count": current_count,
                        "total": simulator.get_total_rows(),
                        "running": simulator.is_running(),
                    })
                    yield f"data: {payload}\n\n"
                last_count = current_count
            else:
                status = json.dumps({
                    "heartbeat": True,
                    "count": current_count,
                    "total": simulator.get_total_rows(),
                    "running": simulator.is_running(),
                })
                yield f"data: {status}\n\n"
            time.sleep(2)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/api/records")
def get_records():
    records = simulator.get_all_inserted()
    return jsonify({"count": len(records), "records": records})


def pd_isnan(val):
    try:
        import math
        return isinstance(val, float) and math.isnan(val)
    except Exception:
        return False


if __name__ == "__main__":
    simulator.start(interval=10)
    app.run(debug=True, threaded=True, use_reloader=False)
