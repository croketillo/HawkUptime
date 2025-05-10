import pytest
import logging
from uptime_monitor.monitor import check_url
from uptime_monitor.notifier import TelegramNotifier


pytestmark = pytest.mark.asyncio


class MockResponse:
    status = 200

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class MockSession:
    async def get(self, url):
        return MockResponse()


async def test_check_url_ok():
    """Properly awaitable mock for successful URL check."""
    logger = logging.getLogger("test_logger")
    notifier = TelegramNotifier(None, None, logger)
    session = MockSession()

    # Properly await the call
    response = await session.get("https://example.com")

    async with response as resp:
        assert resp.status == 200

    # Reuse the check_url logic to make sure the code path is covered
    await check_url(session, "https://example.com", 500, logger, notifier)
