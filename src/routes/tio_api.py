from flask import request

from src import app, csrf
from src.utils.tio import Tio, parse_output


@app.route("/api/tio", methods=["POST"])
async def tio():
    lang: str = request.get_json().get("language", "")
    code: str = request.get_json().get("code", "")

    print(lang, code)
    if not lang or not code:
        return "Invalid request", 401

    tio = Tio(lang, code)
    st: str = await tio.send()

    return {"language": lang, "code": code, **parse_output(st)}


csrf.exempt(tio)
