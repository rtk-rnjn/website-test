import asyncio
import contextlib
import os

from dotenv import load_dotenv

from src import app

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    with contextlib.suppress(ImportError):
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 80))  # noqa: PLW1508

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
