from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3

    from flask import Flask
    from pymongo import MongoClient

    class FlaskClass(Flask):
        mongo: MongoClient
        sql: sqlite3.Connection

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
