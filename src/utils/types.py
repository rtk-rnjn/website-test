from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask
    from pymongo import MongoClient

    class FlaskClass(Flask):
        mongo: MongoClient

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
