Here's the revised **README.md**, fully Docker‑Compose‑based with Splunk branding and references. It integrates the SpanMetrics workshop into a containerized Splunk OpenTelemetry (OTel) Collector environment.

---

# 🔍 Splunk SpanMetrics Workshop (Docker‑Compose)

Convert OpenTelemetry spans into actionable R.E.D. (Request, Error, Duration) metrics using Splunk’s downstream distribution of the SpanMetrics connector. This hands-on workshop containerizes the full pipeline—OTLP trace ingestion, span → metric conversion, and Prometheus export—all orchestrated via Docker‑Compose.

---

## 🚀 Why Use Splunk SpanMetrics?

* **Automatic Span→Metric conversion**: No need to add metrics instrumentation to your app.
* **Seamless Splunk integration**: Ingest metrics into Splunk Observability Cloud or Enterprise via HEC or Splunk APM exporters.
* **Branded & supported**: Built on the Splunk OpenTelemetry Collector distribution for full support and enterprise-grade reliability ([GitHub][1], [Grafana Labs][2], [Splunk Community][3]).

---

## 🧩 Structure

```
/
├── docker-compose.yaml        # Defines Collector + Prometheus stack
├── collector/
│   └── config.yaml           # OTLP span receiver + spanmetrics + Splunk exporter
├── sample/
│   └── send-traces.sh        # BASH script using curl & OTLP
└── README.md                 # This file
```

---

## ⚙️ Docker‑Compose Setup

**docker-compose.yaml**:

```yaml
version: "3.8"
services:
  otelcol:
    image: “splunk/otel-collector:latest”
    volumes:
      - ./collector/config.yaml:/etc/otel/config.yaml
    ports:
      - 4317:4317     # OTLP gRPC
      - 8888:8888     # Prometheus metrics
    command: ["--config=/etc/otel/config.yaml"]

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./collector/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
```

**collector/config.yaml**:

```yaml
receivers:
  otlp:
    protocols:
      grpc:

connectors:
  spanmetrics:
    histogram:
      explicit:
        buckets: [100ms,500ms,1s,2s,5s]
    dimensions:
      - name: http.method
      - name: http.status_code
      - name: span.name
    exemplars:
      enabled: true
    resource_metrics_key_attributes:
      - service.name
      - telemetry.sdk.language

exporters:
  prometheus:
    endpoint: "0.0.0.0:8888"
  splunk_hec:
    endpoint: "${SPLUNK_HEC_ENDPOINT}"
    token: "${SPLUNK_HEC_TOKEN}"
    metric_endpoint: `${SPLUNK_HEC_ENDPOINT}/services/collector`
    metrics_index: "otel-metrics"

processors:
  batch:

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [spanmetrics, splunk_hec]
    metrics:
      receivers: [spanmetrics]
      processors: [batch]
      exporters: [prometheus, splunk_hec]
```

* The **Splunk OTel Collector** image provides enterprise‑supported pipelines ([GitHub][1], [Grafana Labs][2]).
* Metrics are exported both via Prometheus (local testing at `localhost:8888/metrics`) and to Splunk via HEC.
* Environment variables are used for Splunk credentials: `SPLUNK_HEC_ENDPOINT`, `SPLUNK_HEC_TOKEN`.

---

## 🧪 Run the Workshop Locally

1. **Export Splunk credentials** (replace with your real tokens):

   ```bash
   export SPLUNK_HEC_ENDPOINT="https://splunk-hec.example.com:8088"
   export SPLUNK_HEC_TOKEN="YOUR_HEC_TOKEN"
   ```

2. **Start services**:

   ```bash
   docker-compose up -d
   ```

3. **Send sample data**:

  chmod +x curl.sh
  #in a separte term window run ./curl.sh

4.**View metrics in Splunk Observability**:


   Those same `calls_total` and `duration_bucket` metrics should also appear in your Splunk Observability Cloud or Enterprise.

---

## 🛠️ Customization

* **Latency buckets & dimensions**: Adjust `explicit.buckets` and attribute sets to reflect your tracing style.
* **Splunk exporters**: Consider using `sapm` exporter for APM spans or `signalfx` for legacy Splunk Infra Cloud ([Last9][4], [konst.fish][5], [GitHub][1]).
* **Cardinality management**: Use `exemplars.enabled`, `resource_metrics_key_attributes`, and cache settings to control high-cardinality behavior ([Grafana Labs][2]).

---

## ✅ Troubleshooting

* Check Collector logs:

  ```bash
  docker-compose logs otelcol
  ```
* Confirm Prometheus scraping at `/metrics`:

  ```
  curl http://localhost:8888/metrics
  ```
* Verify Splunk ingestion via logs or metric dashboards.
* Adjust connector settings to manage label explosion or exemplar volume.

---

## 📚 Learn More & Splunk Resources

* \[Splunk OTel Collector Helm & enterprise guide] ([Artifact Hub][6], [Last9][4], [GitHub][1])
* \[Splunk SpanMetrics connector docs (Grafana Alloy)] ([Grafana Labs][2])
* \[SpanMetrics in action: convert traces to R.E.D metrics] (Splunk blog/guides)

---

## 📝 License

Licensed under MIT. See `LICENSE` in repo root.

---

**Enjoy exploring SpanMetrics with Splunk!** Let me know if you’d like Kotlin, Python, or service instrumentation examples added.

