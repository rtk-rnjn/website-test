from __future__ import annotations

from flask import render_template, request, session, url_for
from flask_login import current_user

from bson import ObjectId

from src import app
from src import mongo_client as mongo
from src.utils.caching import cache_function_result


@cache_function_result
async def get_topics(database: str) -> list[str]:
    db = mongo[database]
    collections = db.list_collection_names()

    return [str(collection).replace("_", " ").capitalize() for collection in collections]


def get_random_questions(*, database: str, collection: str, count: int = 10) -> list[dict]:
    db = mongo[database]
    col = db[collection]

    return sorted(col.aggregate([{"$sample": {"size": count}}]), key=lambda x: x["_id"])


@app.route("/competitive-reasoning", methods=["GET"])
async def competitive_reasoning():
    if topic_arg := request.args.get("topic"):
        questions = get_random_questions(database="competitive_reasoning", collection=topic_arg)
        return render_template("mcq.html", current_user=current_user, questions=questions)

    topics = await get_topics("competitive_reasoning")
    return render_template("section.html", title="Competitive Reasoning", current_user=current_user, topics=topics)


@app.route("/competitive-english", methods=["GET"])
async def competitive_english():
    if topic_arg := request.args.get("topic"):
        questions = get_random_questions(database="competitive_english", collection=topic_arg)
        return render_template("mcq.html", current_user=current_user, questions=questions)

    topics = await get_topics("competitive_english")
    return render_template("section.html", title="Competitive English", current_user=current_user, topics=topics)


@app.route("/arithmetic-ability", methods=["GET"])
async def arithmetic_ability():
    if topic_arg := request.args.get("topic"):
        questions = get_random_questions(database="arithmetic_ability", collection=topic_arg)
        return render_template("mcq.html", current_user=current_user, questions=questions)

    topics = await get_topics("arithmetic_ability")
    return render_template("section.html", title="Arithmetic Ability", current_user=current_user, topics=topics)


@app.route("/check-answer", methods=["POST", "GET"])
def check_answer():
    data = request.json
    if questions := session.pop("ABC", None):
        return render_template("check_answer.html", current_user=current_user, questions=questions)

    if not data:
        return {"error": "No data provided"}, 400

    database = data.pop("database").strip("/")
    collection = data.pop("collection")

    db = mongo[database.replace("-", "_")]
    col = db[collection.replace("-", "_")]

    questions = sorted(col.find({"_id": {"$in": list(data.keys())}}), key=lambda x: x["_id"])
    session["ABC"] = [
        {
            "_id": str(question.pop("_id")),
            **question,
        }
        for question in questions
    ]
    return {"redirect": url_for("check_answer", abc="ABC")}
