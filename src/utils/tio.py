from __future__ import annotations

import zlib
from functools import partial

import aiohttp

from src.utils.caching import Cache, cache_function_result

to_bytes = partial(bytes, encoding="utf-8")


def _split_with_limit(text: str, limit: int = 5) -> list[str]:
    lines: list[str] = text.splitlines()
    return lines[-limit:] + ["\n".join(lines[:-limit])] if lines else []


def _parse_split_text_tio(texts: list[str]) -> dict[str, str]:
    real_time: float = float(texts[0].split(":")[1][:-1])
    user_time: float = float(texts[1].split(":")[1][:-1])
    sys_time: float = float(texts[2].split(":")[1][:-1])
    cpu_share: float = float(texts[3].split(":")[1][:-1])
    exit_code: int = int(texts[4].split(":")[1])

    output: str = texts[-1]

    return {
        "real_time": real_time,
        "user_time": user_time,
        "sys_time": sys_time,
        "cpu_share": cpu_share,
        "exit_code": exit_code,
        "output": output,
    }


def parse_output(text: str) -> dict[str, str]:
    texts = _split_with_limit(text)
    return _parse_split_text_tio(texts)


def _to_tio_string(couple):
    name, obj = couple[0], couple[1]
    if not obj:
        return b""
    if isinstance(obj, list):
        content = [f"V{name}", str(len(obj))] + obj
        return to_bytes("\x00".join(content) + "\x00")
    return to_bytes(f"F{name}\x00{len(to_bytes(obj))}\x00{obj}\x00")


class Tio:
    def __init__(
        self,
        language: str,
        code: str,
        inputs="",
        compiler_flags=None,
        command_line_options=None,
        args=None,
    ) -> None:
        compiler_flags = compiler_flags or []
        command_line_options = command_line_options or []
        args = args or []
        self.backend = "https://tio.run/cgi-bin/run/api/"
        self.json = "https://tio.run/languages.json"

        strings = {
            "lang": [language],
            ".code.tio": code,
            ".input.tio": inputs,
            "TIO_CFLAGS": compiler_flags,
            "TIO_OPTIONS": command_line_options,
            "args": args,
        }
        self.__string = strings

        bytes_ = (
            b"".join(
                map(_to_tio_string, zip(strings.keys(), strings.values(), strict=False)),
            )
            + b"R"
        )

        # This returns a DEFLATE-compressed bytestring, which is what the API requires
        self.request = zlib.compress(bytes_, 9)[2:-4]

    def __repr__(self) -> str:
        return Cache.fromdict(d=self.__string).__repr__()

    @cache_function_result
    async def send(self):
        async with aiohttp.ClientSession() as client_session:
            res = await client_session.post(self.backend, data=self.request)
            if res.status != 200:
                raise aiohttp.ClientError(res.status)

            data = await res.read()
            data: str = data.decode("utf-8")
            data = data.replace(data[:16], "")

            return data


# TODO: Caching, Timeout, Rate Limiting, Logging
