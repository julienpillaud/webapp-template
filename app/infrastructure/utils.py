import logging
import time
from typing import Any

from sqlalchemy.engine import Connection
from sqlalchemy.engine.interfaces import DBAPICursor, ExecutionContext

logger = logging.getLogger("infra.repository")


class TimedExecutionContext(ExecutionContext):
    start: float


def before_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: dict[str, Any],
    context: TimedExecutionContext,
    executemany: bool,
) -> None:
    context.start = time.perf_counter()


def after_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: dict[str, Any],
    context: TimedExecutionContext,
    executemany: bool,
) -> None:
    end = time.perf_counter()
    duration = (end - context.start) * 1000
    statement = statement.replace("\n", " ").strip()
    logger.info(f"[{duration:6.2f} ms] {statement}")
