# Monitoring system

> System to monitor Linux server metrics, including CPU, memory, and disk usage.

- Collect Linux system metrics using Python.
- Store metrics in a time-series database.
- Visualize data with customizable Grafana dashboards.
- Version-controlled dashboards using YAML provisioning.
- Easy deployment with Docker Compose.


## Getting started

```bash
docker compose up -d
virtualenv .venv & source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Stack

### Data collection
<!-- `psutil` -->

### Data storage
<!-- TimescaleDB -->

### Data visualization

<!-- Grafana
Dashboard -->
