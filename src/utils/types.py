from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    import sqlite3

    from flask import Flask
    from pymongo import MongoClient
    from bson import ObjectId

    from src.utils.logger import _Logger

    class FlaskClass(Flask):
        mongo: MongoClient
        sql: sqlite3.Connection
        log: _Logger

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

    class QuestionJsonData(TypedDict):
        _id: ObjectId
        q: str
        o: list[str]
        a: int | str
        e: str | None
        l: str | None  # noqa: E741
        t: int | None
