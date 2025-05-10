import pytest
import asyncio
import logging
from aiohttp import ClientSession
from uptime_monitor.monitor import check_url
from uptime_monitor.notifier import TelegramNotifier


@pytest.mark.asyncio
async def test_check_url_ok(monkeypatch):
    """Simulate a successful URL check."""

    class MockResponse:
        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class MockSession:
        async def get(self, url):
            return MockResponse()

    logger = logging.getLogger("test_logger")
    notifier = TelegramNotifier(None, None, logger)

    await check_url(MockSession(), "https://example.com", 500, logger, notifier)
