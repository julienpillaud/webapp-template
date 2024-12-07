import logging

logger = logging.getLogger("infra.repository")


def log_sql_statement(  # type: ignore
    conn, cursor, statement, parameters, context, executemany
) -> None:
    statement = statement.replace("\n", " ").strip()
    logger.debug(statement)
