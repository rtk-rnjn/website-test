from __future__ import annotations

from flask import render_template

from src import app
from src.utils.error_codes import ERROR_CODES


@app.errorhandler(400)
def error_handler_400(error: Exception) -> tuple:
    return render_template(
        "400-500.html",
        title=f"400 - {ERROR_CODES[400]['short_desc']}",
        error_code=400,
        error_short_desc=ERROR_CODES[400]["short_desc"],
        error_long_desc=ERROR_CODES[400]["long_desc"],
    ), 400


@app.errorhandler(404)
def error_handler_404(error: Exception) -> tuple:
    return render_template(
        "400-500.html",
        title=f"404 - {ERROR_CODES[404]['short_desc']}",
        error_code=404,
        error_short_desc=ERROR_CODES[404]["short_desc"],
        error_long_desc=ERROR_CODES[404]["long_desc"],
    ), 404
