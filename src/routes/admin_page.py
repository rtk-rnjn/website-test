import json

from bson import ObjectId
from flask import render_template, request
from flask_login import current_user, login_required

from src import app, csrf

mongo_client = app.mongo
databases = mongo_client.list_database_names()

dont_capture = ["admin", "config", "local", "users_database"]

databases = [db for db in databases if db not in dont_capture]


@app.route("/admin-page")
@login_required
async def admin_page() -> str:
    questions = {
        db: mongo_client[db].list_collection_names()
        for db in databases
    }

    return render_template(
        "admin_page.html", user=current_user, cached_questions=questions
    )


@app.route("/admin-page/<database>/<collection>")
@login_required
async def admin_page_db_col(database: str, collection: str) -> str:
    col = mongo_client[database][collection]
    skip = request.args.get("skip", 0)
    limit = request.args.get("limit", 20)
    documents = col.find(
        {}, limit=int(limit), skip=int(skip)
    )

    total_docs = col.count_documents({})

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


csrf.exempt(admin_page_db_col)


@app.route(
    "/admin-page/<database>/<collection>/<question_id>/delete",
    methods=["DELETE", "GET"],
)
@login_required
async def admin_page_db_col_delete(
    database: str, collection: str, question_id: str
) -> str:
    col = mongo_client[database][collection]
    if request.method == "GET":
        document = col.find_one({"_id": ObjectId(question_id)}, {"_id": 0})

        return (
            "Method GET not allowed\n" + f"<pre>{json.dumps(document, indent=4)}</pre>"
        )

    if request.method == "DELETE":
        print("Deleted")

    # col.delete_one({"_id": ObjectId(question_id)})
    return


@app.route(
    "/admin-page/<database>/<collection>/<question_id>/update", methods=["GET", "PATCH"]
)
@login_required
async def admin_page_db_col_update(
    database: str, collection: str, question_id: str
) -> str:
    col = mongo_client[database][collection]
    if request.method == "GET":
        document = col.find_one({"_id": ObjectId(question_id)}, {"_id": 0})

        return (
            "Method GET not allowed\n" + f"<pre>{json.dumps(document, indent=4)}</pre>"
        )

    if request.method == "PATCH":
        json_object = request.data
        if json_object is None:
            return
        json_data = json.loads(json_object)
        print(json_data)

        payload = {
            "questions": json_data["question"],
            "options": json_data["options"],
            "answer": json_data["answer"],
        }

        print(payload)
        # col.update_one({"_id": question_id}, {"$set": payload})
    return


csrf.exempt(admin_page_db_col_update)
