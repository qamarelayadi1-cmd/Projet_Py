import logging
import psycopg2
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = RotatingFileHandler("logs/storage.log", maxBytes=500000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    ))
    logger.addHandler(handler)

INSERT_SQL = """
INSERT INTO attempts
(log_month, log_day, log_time, server, service, process_id, username,
 ip, port, status, invalid_user, country, attempt_count, raw_line)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (raw_line) DO NOTHING;
"""

def save_attempts(connection, attempts):
    """Inserer les tentatives. Les lignes deja importees sont ignorees."""
    inserted = 0
    try:
        with connection.cursor() as cursor:
            for attempt in attempts:
                values = (
                    attempt["month"], attempt["day"], attempt["time"],
                    attempt["server"], attempt["service"], attempt["pid"],
                    attempt["username"], attempt["ip"], attempt["port"],
                    attempt["status"], attempt["invalid_user"],
                    attempt.get("country", "Unknown"), attempt["attempt_count"],
                    attempt["raw_line"]
                )
                cursor.execute(INSERT_SQL, values)
                inserted += cursor.rowcount
        connection.commit()
        logger.info("Tentatives ajoutees : %d", inserted)
        return inserted
    except (psycopg2.Error, KeyError, ValueError):
        connection.rollback()
        logger.exception("Erreur pendant l'insertion des tentatives")
        raise
