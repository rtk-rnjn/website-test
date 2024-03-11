import pymongo
from bson import ObjectId
from flask import render_template, request
from flask_login import current_user, login_required

from src import app

mongo_client = app.mongo
databases = mongo_client.list_database_names()

dont_capture = ["admin", "config", "local", "users_database"]

databases = [db for db in databases if db not in dont_capture]
cached_questions = {}


@app.route("/admin-page")
@login_required
async def admin_page() -> str:
    if not cached_questions:
        questions = {
            db: [col for col in mongo_client[db].list_collection_names()]
            for db in databases
        }
        cached_questions.update(questions)

    return render_template(
        "admin_page.html", user=current_user, cached_questions=cached_questions
    )

cached_count = {}
@app.route("/admin-page/<database>/<collection>")
@login_required
async def admin_page_db_col(database: str, collection: str) -> str:
    col = mongo_client[database][collection]
    skip = request.args.get("skip", 0)
    limit = request.args.get("limit", 20)
    documents = (
        col.find({}, limit=int(limit), skip=int(skip), sort=[("quesions", pymongo.ASCENDING)])
    )

    total_docs = cached_count.get(f"{database}-{collection}", col.count_documents({}))
    cached_count[f"{database}-{collection}"] = total_docs

    return render_template(
        "admin_page_db_col.html",
        user=current_user,
        database=database,
        collection=collection,
        documents=documents,
        skip=skip,
        limit=limit,
        total_docs=total_docs,
    )


@app.route("/admin-page/<database>/<collection>/<question_id>/delete", methods=["DELETE", 'GET'])
@login_required
async def admin_page_db_col_delete(
    database: str, collection: str, question_id: str
) -> str:
    col = mongo_client[database][collection]
    if request.method == "GET":
        document = col.find_one({"_id": ObjectId(question_id)}, {"_id": 0})
        return document
    # col.delete_one({"_id": ObjectId(question_id)})
    return "Deleted"


@app.route("/admin-page/<database>/<collection>/<question_id>/update")
@login_required
async def admin_page_db_col_update(
    database: str, collection: str, question_id: str
) -> str:
    col = mongo_client[database][collection]
    pass
