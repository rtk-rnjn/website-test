import asyncio
import contextlib
import os

from src import app

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    with contextlib.suppress(ImportError):
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
