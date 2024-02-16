from flask import request

from src import app
from src.utils.tio import Tio


@app.route("/api/tio", methods=["POST"])
async def tio():
    lang: str = request.get_json().get("language", "")
    code: str = request.get_json().get("code", "")

    if not lang or not code:
        return "Invalid request", 400

    tio = Tio(lang, code)
    st: str = await tio.send()
    return {"output": st, "language": lang, "code": code}
