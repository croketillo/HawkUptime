<p align="center">
  <img src="uptime_monitor/img/logo.png" alt="Uptime Monitor Logo" width="300"/>
</p>

A containerized tool to monitor the uptime and latency of your websites.

## Features

- Periodic HTTP health checks on your defined URLs.
- Latency threshold alerts.
- Real-time **web dashboard** for live status visualization.
- Telegram notifications.
- Configurable log retention.
- Persistent logs outside the container.
- Dockerized and production-ready.

---

## Getting Started

### Requirements

- Docker
- Docker Compose

---

## Configuration

Create or edit `uptime_monitor/config.yaml`:

```yaml
interval_minutes: 5
latency_threshold_ms: 500
log_retention_days: 30

urls:
  - https://example.com
  - https://your-service.com

notifier:
  telegram:
    token: "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id: "YOUR_TELEGRAM_CHAT_ID"

status_api:
  enabled: true
  host: "0.0.0.0"
  port: 8080
```

---

## Building and Running

1. **Build the Docker image:**

   ```bash
   docker-compose build
   ```

2. **Run the monitor as a service:**

   ```bash
   docker-compose up -d
   ```

3. **View live logs:**

   ```bash
   docker-compose logs -f
   ```

4. **Access the Real-Time Web Dashboard:**

   Open your browser and visit:

   ```
   http://localhost:8080
   ```

   This dashboard shows the current status of all monitored URLs with color-coded indicators and auto-refresh every 5 seconds.

---

## Persistent Logs

Logs are written to `uptime_monitor/logs/uptime_monitor.log`  
They are mapped to your host machine and persist after container restarts.

---

## Reloading Configuration

After changing `config.yaml`, restart the container to apply changes:

```bash
docker restart uptime-monitor
```

---

## Stopping the Service

```bash
docker-compose down
```

---

## License

MIT License