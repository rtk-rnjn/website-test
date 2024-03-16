import asyncio
import contextlib
import os

from src import app
from src.utils.logger import log

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    with contextlib.suppress(ImportError):
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


if __name__ == "__main__":
    log.info("Starting server")
    app.run("0.0.0.0", 8000, debug=True)
