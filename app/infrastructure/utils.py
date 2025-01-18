import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Self

from pydantic import BaseModel
from sqlalchemy import Engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.engine.interfaces import DBAPICursor, ExecutionContext

logger = logging.getLogger("infra.repository")


class TimedExecutionContext(ExecutionContext):
    start: float


class QueryInfo(BaseModel):
    statement: str
    parameters: dict[str, Any]
    duration: float


class SQLAlchemyInstrument:
    def __init__(self, engine: Engine):
        self._enabled = False
        self.queries: list[QueryInfo] = []
        self.engine = engine

        event.listen(Engine, "before_cursor_execute", self.before_cursor_execute)
        event.listen(Engine, "after_cursor_execute", self.after_cursor_execute)

    def __del__(self) -> None:
        event.remove(Engine, "before_cursor_execute", self.before_cursor_execute)
        event.remove(Engine, "after_cursor_execute", self.after_cursor_execute)

    @property
    def queries_count(self) -> int:
        return len(self.queries)

    @contextmanager
    def record(self) -> Iterator[Self]:
        self._enabled = True
        self.queries = []
        try:
            yield self
        finally:
            self._enabled = False

    def before_cursor_execute(
        self,
        conn: Connection,
        cursor: DBAPICursor,
        statement: str,
        parameters: dict[str, Any],
        context: TimedExecutionContext,
        executemany: bool,
    ) -> None:
        if not self._enabled:
            return

        context.start = time.perf_counter()

    def after_cursor_execute(
        self,
        conn: Connection,
        cursor: DBAPICursor,
        statement: str,
        parameters: dict[str, Any],
        context: TimedExecutionContext,
        executemany: bool,
    ) -> None:
        if not self._enabled:
            return

        duration = (time.perf_counter() - context.start) * 1000
        statement = statement.replace("\n", " ").strip()
        logger.info(f"[{duration:6.2f} ms] {statement}")

        query_info = QueryInfo(
            statement=statement, parameters=parameters, duration=duration
        )
        self.queries.append(query_info)
