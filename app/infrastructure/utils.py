import logging
import time

logger = logging.getLogger("infra.repository")


def before_cursor_execute(  # type: ignore
    conn, cursor, statement, parameters, context, executemany
) -> None:
    context.start = time.perf_counter()


def after_cursor_execute(  # type: ignore
    conn, cursor, statement, parameters, context, executemany
) -> None:
    end = time.perf_counter()
    duration = (end - context.start) * 1000
    statement = statement.replace("\n", " ").strip()
    logger.info(f"[{duration:6.2f} ms] {statement}")
