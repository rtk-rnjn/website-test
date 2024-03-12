import asyncio
import os

from src import app as app

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass


if __name__ == "__main__":
    app.run("0.0.0.0", 8000, debug=True)
