from aiohttp import web
import asyncio

app = web.Application()

async def hello(request):
    return web.Response(text="Hello, world!")

app.router.add_get('/', hello)

async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("Server running on http://0.0.0.0:8080")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
