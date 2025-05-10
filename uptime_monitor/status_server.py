from aiohttp import web
import asyncio
import datetime
from typing import Dict, Optional
import logging


class StatusServer:
    def __init__(self, state: Dict, host: str = "0.0.0.0", port: int = 8080, logger: Optional[logging.Logger] = None):
        self.state = state
        self.host = host
        self.port = port
        self.logger = logger or logging.getLogger(__name__)
        self.app = web.Application()
        self.app.router.add_get("/", self.handle_status)

        # Serve static images
        import importlib.resources as pkg_resources

        try:
            img_path = pkg_resources.files('uptime_monitor').joinpath('img')
            self.app.router.add_static("/img", str(img_path))
        except Exception as e:
            self.logger.warning(f"Image directory not found: {e}")

    async def handle_status(self, request):
        html_content = self.render_html()
        return web.Response(text=html_content, content_type="text/html")

    def render_html(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cards_html = ""
        for check in self.state.get("checks", []):
            status_class = check["status"].lower()
            cards_html += f"""
            <div class="card">
                <div class="card-row"><strong>URL:</strong> {check['url']}</div>
                <div class="card-row"><strong>Status:</strong> <span class="badge {status_class}">{check['status']}</span></div>
                <div class="card-row"><strong>Latency:</strong> {check['latency_ms']} ms</div>
            </div>
            """

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>HawkUptime Monitor</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    color: #343b3f;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 960px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .logo-container{{
                   text-align: center;
                }}
                p {{
                    text-align: center;
                }}
                .card {{
                    background: #f4f4f4;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 8px;
                    box-shadow: 0 0 5px rgba(0,0,0,0.05);
                }}
                .badge {{
                    padding: 4px 8px;
                    border-radius: 12px;
                    color: #fff;
                    font-weight: bold;
                }}
                .ok {{ background-color: #4CAF50; }}
                .warning {{ background-color: #FF9800; }}
                .error {{ background-color: #F44336; }}
                footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #aaa;
                    font-size: 0.9em;
                }}
                 .card-row{{
                        margin-top:20px;
                    }}

                @media (min-width: 601px) {{
                    .card {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .card > div {{
                        flex: 1;
                        padding: 0 10px;
                    }}
                     .card-row{{
                        margin-top:3px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo-container"><img src="img/logo.png"></div>
                <p>Last updated: {timestamp}</p>
                {cards_html}
                <footer>
                    HawkUptime Monitor &copy; 2025
                </footer>
            </div>
        </body>
        </html>
        """
        return html_template

    async def run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        self.logger.info(f"Status server running on http://{self.host}:{self.port}")
        while True:
            await asyncio.sleep(3600)
