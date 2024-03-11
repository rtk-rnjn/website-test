from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, Iterator, TypeVar

if TYPE_CHECKING:
    from typing_extensions import Self

from functools import wraps

from lru import LRU

KT = TypeVar("KT")
VT = TypeVar("VT")
LRU_CACHE: int = 2 ** 10


def lru_callback(key: KT, value: VT) -> None:
    pass


class Cache(Generic[KT, VT]):
    def __init__(
        self,
        cache_size: int | None = 2 ** 5,
        *,
        callback: Callable[[KT, VT], None] | None = None,
    ) -> None:
        self.cache_size: int = cache_size or LRU_CACHE
        self.__internal_cache: LRU = LRU(
            self.cache_size, callback=callback or lru_callback
        )

        self.items: Callable[[], list[tuple[int, Any]]] = self.__internal_cache.items
        self.peek_first_item: Callable[
            [], tuple[int, Any] | None
        ] = self.__internal_cache.peek_first_item
        self.peek_last_item: Callable[
            [], tuple[int, Any] | None
        ] = self.__internal_cache.peek_last_item
        self.get_size: Callable[[], int] = self.__internal_cache.get_size
        self.set_size: Callable[[int], None] = self.__internal_cache.set_size
        self.has_key: Callable[[object], bool] = self.__internal_cache.has_key
        self.values: Callable[[], list[Any]] = self.__internal_cache.values
        self.keys: Callable[[], list[Any]] = self.__internal_cache.keys
        self.get: Callable[[object], Any] = self.__internal_cache.get
        self.pop: Callable[[object], Any] = self.__internal_cache.pop
        self.popitem: Callable[[], tuple[int, Any]] = self.__internal_cache.popitem

        self.get_stats: Callable[[], tuple[int, int]] = self.__internal_cache.get_stats
        self.set_callback: Callable[
            [Callable[[KT, VT], Any]], None
        ] = self.__internal_cache.set_callback

    def __repr__(self) -> str:
        return repr(self.__internal_cache)

    def __len__(self) -> int:
        return len(self.__internal_cache)

    def __getitem__(self, __k: KT) -> VT:
        return self.__internal_cache[__k]

    def __delitem__(self, __v: KT) -> None:
        del self.__internal_cache[__v]

    def __contains__(self, __o: object) -> bool:
        return self.has_key(__o)

    def __setitem__(self, __k: KT, __v: VT) -> None:
        self.__internal_cache[__k] = __v

    def clear(self) -> None:
        return self.__internal_cache.clear()

    def update(self, *args, **kwargs) -> None:
        return self.__internal_cache.update(*args, **kwargs)

    def setdefault(self, *args, **kwargs) -> None:
        return self.__internal_cache.setdefault(*args, **kwargs)

    def __iter__(self) -> Iterator:
        return iter(self.__internal_cache)

    @classmethod
    def fromdict(
        cls: Self[Cache[KT, VT]],
        cache_size: int = LRU_CACHE,
        callback: Callable[[KT, VT], None] | None = None,
        *,
        d: dict[KT, VT] | None = None,
    ) -> Cache[KT, VT]:
        if d is None:
            d = {}

        cache: Self[Cache[KT, VT]] = cls(cache_size, callback=callback)
        cache.__from_dict(d)
        return cache

    def __from_dict(self, d: dict[KT, VT]) -> None:
        self.__internal_cache = LRU(self.cache_size)
        for k, v in d.items():
            self.__internal_cache[k] = v

    def __hash_repr__(self) -> str:
        d = {}
        for k, v in self.__internal_cache.items():
            d[hash(k)] = hash(v)
        return repr(d)


_GLOBAL_CACHE: Cache[KT, VT] = Cache(LRU_CACHE)


def cache_function_result(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        key = str((func.__name__, args, frozenset(kwargs.items())))
        if key in _GLOBAL_CACHE:
            return _GLOBAL_CACHE[key]
        result = await func(*args, **kwargs)
        _GLOBAL_CACHE[key] = result
        print(_GLOBAL_CACHE.__hash_repr__())
        return result

    return wrapper
