from __future__ import annotations

from flask import redirect, render_template, request, url_for, session
from flask_login import current_user

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

    # _id = 0 means we don't want to include the _id field in the response
    return list(col.aggregate([{"$sample": {"size": count}}, {"$project": {"_id": 0}}]))

@app.route("/competitive-reasoning", methods=["GET"])
async def competitive_reasoning():
    if topic_arg := request.args.get("topic"):
        questions = get_random_questions(database="competitive_reasoning", collection=topic_arg)
        session["questions"] = questions
        return redirect(url_for("start_test"))

    topics = await get_topics("competitive_reasoning")
    return render_template("section.html", title="Competitive Reasoning", current_user=current_user, topics=topics)


@app.route("/competitive-english", methods=["GET"])
async def competitive_english():
    if topic_arg := request.args.get("topic"):
        questions = get_random_questions(database="competitive_english", collection=topic_arg)
        session["questions"] = questions
        return redirect(url_for("start_test"))

    topics = await get_topics("competitive_english")
    return render_template("section.html", title="Competitive English", current_user=current_user, topics=topics)


@app.route("/arithmetic-ability", methods=["GET"])
async def arithmetic_ability():
    if topic_arg := request.args.get("topic"):
        questions = get_random_questions(database="arithmetic_ability", collection=topic_arg)
        session["questions"] = questions
        return redirect(url_for("start_test"))

    topics = await get_topics("arithmetic_ability")
    return render_template("section.html", title="Arithmetic Ability", current_user=current_user, topics=topics)


@app.route("/test")
async def start_test():
    questions = session.get("questions", [])
    print(len(questions))
    return render_template("mcq.html", current_user=current_user, questions=questions)
