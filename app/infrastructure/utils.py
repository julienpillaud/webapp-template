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
    _instance: Self | None = None
    _enabled: bool
    _queries: list[QueryInfo]

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._enabled = False
            cls._instance._queries = []

            event.listen(
                Engine,
                "before_cursor_execute",
                cls._instance._before_cursor_execute,
            )
            event.listen(
                Engine,
                "after_cursor_execute",
                cls._instance._after_cursor_execute,
            )

        return cls._instance

    @property
    def queries_count(self) -> int:
        return len(self._queries)

    @classmethod
    @contextmanager
    def record(cls) -> Iterator[Self]:
        instance = cls()
        instance._enabled = True
        instance._queries = []
        try:
            yield instance
        finally:
            instance._enabled = False

    def _before_cursor_execute(
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

    def _after_cursor_execute(
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
        self._queries.append(query_info)
