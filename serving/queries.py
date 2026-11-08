import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = RotatingFileHandler("logs/serving.log", maxBytes=500000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    ))
    logger.addHandler(handler)

def get_failed_by_country(connection):
    sql = """
    SELECT country, SUM(attempt_count) AS total
    FROM attempts
    WHERE status = 'FAILED'
    GROUP BY country
    ORDER BY total DESC;
    """
    return _fetch_all(connection, sql)

def get_success_by_user(connection):
    sql = """
    SELECT username, SUM(attempt_count) AS total
    FROM attempts
    WHERE status = 'SUCCESS'
    GROUP BY username
    ORDER BY total DESC;
    """
    return _fetch_all(connection, sql)

def get_invalid_users(connection):
    sql = """
    SELECT username, country, ip::text, SUM(attempt_count) AS total
    FROM attempts
    WHERE status = 'FAILED' AND invalid_user = TRUE
    GROUP BY username, country, ip
    ORDER BY total DESC;
    """
    return _fetch_all(connection, sql)

def _fetch_all(connection, sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception:
        logger.exception("Erreur pendant l'execution d'une requete SQL")
        raise
