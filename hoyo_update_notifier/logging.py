import contextlib
import logging
import logging.handlers
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Generator

__all__ = ("setup_logging",)


@contextlib.contextmanager
def setup_logging() -> "Generator[Any, Any, Any]":
    log = logging.getLogger()

    try:
        # __enter__
        log.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter("[{asctime}] [{levelname}] {name}: {message}", dt_fmt, style="{")
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)
