from __future__ import annotations

from flask import render_template
from flask_login import current_user

from src import app
from src.utils.caching import cache_function_result


@cache_function_result
async def get_topics(databse: str) -> list[str]:
    db = app.mongo[databse]
    collections = db.list_collection_names()

    return [str(collection).replace("_", " ").capitalize() for collection in collections]


@app.route("/competitive-reasoning", methods=["GET"])
async def competitive_reasoning():
    topics = await get_topics("competitive_reasoning")
    return render_template("section.html", title="Competitive Reasoning", current_user=current_user, topics=topics)


@app.route("/competitive-english", methods=["GET"])
async def competitive_english():
    topics = await get_topics("competitive_english")
    return render_template("section.html", title="Competitive English", current_user=current_user, topics=topics)


@app.route("/arithmetic-ability", methods=["GET"])
async def arithmetic_ability():
    topics = await get_topics("arithmetic_ability")
    return render_template("section.html", title="Arithmetic Ability", current_user=current_user, topics=topics)
