from __future__ import annotations

import functools
import logging
import logging.handlers
import sqlite3
from datetime import datetime

from colorama import Fore


def handler(filename: str) -> logging.handlers.RotatingFileHandler:
    return logging.handlers.RotatingFileHandler(
        filename=filename,
        encoding="utf-8",
        maxBytes=1 * 1024 * 1024,  # 1 MiB
        backupCount=1,  # Rotate through 1 files
    )


DT_FMT = "%Y-%m-%d %H:%M:%S"


class CustomFormatter(logging.Formatter):
    GRAY = f"{Fore.LIGHTBLACK_EX}"
    GREY = GRAY

    RED = f"{Fore.RED}"
    YELLOW = f"{Fore.YELLOW}"
    GREEN = f"{Fore.GREEN}"
    WHITE = f"{Fore.WHITE}"
    BLUE = f"{Fore.BLUE}"
    CYAN = f"{Fore.CYAN}"

    RESET = f"{Fore.RESET}"

    fmt = "{} %(asctime)s {} - {} %(name)s {} - {} %(levelname)s {} - {} %(message)s {} ({}%(filename)s/%(module)s.%(funcName)s{}:{}%(lineno)d{}){}"

    # fmt: off
    formats = {
        logging.DEBUG   : fmt.format(WHITE, WHITE, YELLOW, WHITE, GRAY  , WHITE, BLUE, WHITE, CYAN, YELLOW, GREEN, WHITE, RESET),
        logging.INFO    : fmt.format(WHITE, WHITE, YELLOW, WHITE, GREEN , WHITE, BLUE, WHITE, CYAN, YELLOW, GREEN, WHITE, RESET),
        logging.WARNING : fmt.format(WHITE, WHITE, YELLOW, WHITE, YELLOW, WHITE, BLUE, WHITE, CYAN, YELLOW, GREEN, WHITE, RESET),
        logging.ERROR   : fmt.format(WHITE, WHITE, YELLOW, WHITE, RED   , WHITE, BLUE, WHITE, CYAN, YELLOW, GREEN, WHITE, RESET),
        logging.CRITICAL: fmt.format(WHITE, WHITE, YELLOW, WHITE, RED   , WHITE, BLUE, WHITE, CYAN, YELLOW, GREEN, WHITE, RESET),
    }
    # fmt: on

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt, DT_FMT)
        return formatter.format(record)


_log = logging.getLogger("")
_log.setLevel(logging.DEBUG)
file_handler = handler("logs.log")
file_handler.setLevel(logging.DEBUG)
file_handler_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", DT_FMT)
file_handler.setFormatter(file_handler_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(CustomFormatter())

_log.addHandler(stream_handler)
_log.addHandler(file_handler)


def auto_commit_deco(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            self.sql.commit()

    return wrapper


class _Logger:
    def __init__(self, con: sqlite3.Connection, logger: logging.Logger) -> None:
        self.__query = """INSERT INTO LOGS (log_level, log_message, log_created_at) VALUES ('{}', ?, %s)""" % (
            datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")
        )
        self.__sql = con
        self.__logger = logger

    @property
    def sql(self) -> sqlite3.Connection:
        return self.__sql

    @auto_commit_deco
    def info(self, msg: str, *args, **kwargs) -> None:
        self.__logger.info(msg, *args, **kwargs)
        self.__sql.execute(self.__query.format("INFO"), (msg,))

    @auto_commit_deco
    def debug(self, msg: str, *args, **kwargs) -> None:
        self.__logger.debug(msg, *args, **kwargs)
        self.__sql.execute(self.__query.format("DEBUG"), (msg,))

    @auto_commit_deco
    def warning(self, msg: str, *args, **kwargs) -> None:
        self.__logger.warning(msg, *args, **kwargs)
        self.__sql.execute(self.__query.format("WARNING"), (msg,))

    @auto_commit_deco
    def error(self, msg: str, *args, **kwargs) -> None:
        self.__logger.error(msg, *args, **kwargs)
        self.__sql.execute(self.__query.format("ERROR"), (msg,))

    @auto_commit_deco
    def critical(self, msg: str, *args, **kwargs) -> None:
        self.__logger.critical(msg, *args, **kwargs)
        self.__sql.execute(self.__query.format("CRITICAL"), (msg,))


log = _Logger(sqlite3.connect("logs.sqlite"), _log)
