

# Create Flask app
# app/app.py (Flask app that sends logs and spans to the enricher)
from flask import Flask, jsonify
import requests
import uuid
import time

app = Flask(__name__)

@app.route("/")
def index():
    trace_id = uuid.uuid4().hex[:32]  # Simulated 32-char trace ID
    span_id = uuid.uuid4().hex[:16]   # Simulated 16-char span ID

    # Send a log
    log_payload = {
        "trace_id": trace_id,
        "message": "User failed login",
        "user_id": "user123"
    }
    requests.post("http://sidecar-enricher:8888/logs", json=log_payload)

    # Simulate a delay between log and span
    time.sleep(0.5)

    # Send a span
    span_payload = {
        "trace_id": trace_id,
        "span_id": span_id,
        "name": "GET /login",
        "attributes": {
            "http.method": "GET",
            "http.status_code": 401
        }
    }
    requests.post("http://sidecar-enricher:8888/spans", json=span_payload)

    return jsonify({"status": "sent", "trace_id": trace_id})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)