from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3

    from flask import Flask
    from pymongo import MongoClient

    from src.utils.logger import _Logger

    class FlaskClass(Flask):
        mongo: MongoClient
        sql: sqlite3.Connection
        log: _Logger

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
