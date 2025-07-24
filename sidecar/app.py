from flask import Flask, request
from threading import Lock
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

app = Flask(__name__)
log_cache = {}
lock = Lock()

# Setup OTEL tracing
resource = Resource(attributes={
    "service.name": "log-enricher",
    "service.version": "1.0.0",
    "deployment.environment": "curtis"
})
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer("log-enricher")

@app.route("/logs", methods=["POST"])
def receive_log():
    data = request.json
    trace_id = data.get("trace_id")
    if trace_id:
        with lock:
            log_cache[trace_id] = data
    return "ok"

@app.route("/spans", methods=["POST"])
def receive_span():
    span_data = request.json
    trace_id = span_data.get("trace_id")
    span_name = span_data.get("name", "unknown-operation")
    with tracer.start_as_current_span(span_name) as span:
        span.set_attribute("span_id", span_data.get("span_id"))

        for k, v in span_data.get("attributes", {}).items():
            span.set_attribute(k, v)
        with lock:
            if trace_id in log_cache:
                log_data = log_cache[trace_id]
                span.set_attribute("log.message", log_data.get("message"))
                span.set_attribute("user_id", log_data.get("user_id"))


    return "ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)

