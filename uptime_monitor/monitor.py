import asyncio
import time
import logging
from pathlib import Path
from typing import List
from aiohttp import ClientSession, ClientTimeout

from .config import Config
from .notifier import TelegramNotifier
from .status_server import StatusServer

def purge_old_logs(log_path: Path, retention_days: int = 30) -> None:
    now = time.time()
    retention_seconds = retention_days * 86400
    for log_file in log_path.glob("*.log"):
        if (now - log_file.stat().st_mtime) > retention_seconds:
            log_file.unlink()

def setup_logger(log_dir: str = "logs", log_retention_days: int = 30) -> logging.Logger:
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    purge_old_logs(log_path, log_retention_days)
    log_file = log_path / "uptime_monitor.log"

    logger = logging.getLogger("uptime_monitor")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger

# Shared state for the status server
shared_state = {
    "status": "starting",
    "checks": []
}

async def check_url(session: ClientSession, url: str, latency_threshold_ms: int,
                    logger: logging.Logger, notifier: TelegramNotifier) -> None:
    start_time = time.monotonic()
    try:
        async with session.get(url) as response:
            duration_ms = (time.monotonic() - start_time) * 1000
            status_code = response.status

            if status_code == 200 and duration_ms <= latency_threshold_ms:
                result_status = "OK"
                logger.info(f"[OK] {url} responded in {duration_ms:.2f} ms")
            elif status_code == 200:
                result_status = "WARNING"
                msg = f"[WARNING] {url} responded in {duration_ms:.2f} ms (above threshold {latency_threshold_ms} ms)"
                logger.warning(msg)
                notifier.send_message(msg)
            else:
                result_status = "ERROR"
                msg = f"[ERROR] {url} returned status {status_code}"
                logger.error(msg)
                notifier.send_message(msg)

            shared_state["checks"].append({
                "url": url,
                "status": result_status,
                "latency_ms": round(duration_ms)
            })
    except Exception as e:
        result_status = "ERROR"
        msg = f"[ERROR] {url} request failed: {e}"
        logger.error(msg)
        notifier.send_message(msg)
        shared_state["checks"].append({
            "url": url,
            "status": result_status,
            "latency_ms": -1
        })

async def monitoring_loop(config: Config, logger: logging.Logger, notifier: TelegramNotifier):
    timeout = ClientTimeout(total=10)
    async with ClientSession(timeout=timeout) as session:
        while True:
            shared_state["checks"] = []
            tasks: List[asyncio.Task] = [
                asyncio.create_task(check_url(session, url, config.latency_threshold_ms, logger, notifier))
                for url in config.urls
            ]
            await asyncio.gather(*tasks)
            shared_state["status"] = "running"
            logger.info(f"Waiting for {config.interval_minutes} minutes before next check...\n")
            await asyncio.sleep(config.interval_minutes * 60)

async def run_monitor_and_server(config: Config, logger: logging.Logger, notifier: TelegramNotifier):
    status_api_config = getattr(config, "status_api", {})
    host = status_api_config.get("host", "0.0.0.0")
    port = status_api_config.get("port", 8080)

    status_server = StatusServer(shared_state, host, port, logger)
    server_task = asyncio.create_task(status_server.run())

    monitor_task = asyncio.create_task(monitoring_loop(config, logger, notifier))

    await asyncio.gather(server_task, monitor_task)

def run_monitor() -> None:
    try:
        config = Config.load_from_file()
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return

    logger = setup_logger(log_retention_days=getattr(config, "log_retention_days", 30))
    notifier = TelegramNotifier(config.telegram_token, config.telegram_chat_id)

    try:
        asyncio.run(run_monitor_and_server(config, logger, notifier))
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
