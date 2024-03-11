from flask import render_template
from flask_login import current_user, login_required

from src import app

data = {
    "_id": {"$oid": "65eac2ea4c91edad8e0149ce"},
    "questions": '<div class="question-main">The average age of seven boys sitting in a row facing North is 26 years. If the average age of the first three boys is 19 years and the average age of the last three boys is 32 years, <sup>1</sup> what is the age of the boy who is sitting in the middle of the row?</div>',
    "options": ["24 years", "28 years", "29 years", "31 years"],
    "answer": "3",
}


@app.route("/admin-page")
@login_required
def admin_page() -> str:
    return render_template("admin_page.html", user=current_user, data=data)
