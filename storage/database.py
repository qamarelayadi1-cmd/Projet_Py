import logging
import os
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

def get_connection():
    """Connexion PostgreSQL avec les variables d'environnement."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "log_analysis"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            port=os.getenv("DB_PORT", "5432")
        )
        logger.info("Connexion PostgreSQL reussie")
        return connection
    except psycopg2.Error:
        logger.exception("Impossible de se connecter a PostgreSQL")
        return None

def create_tables(connection):
    sql = """
    CREATE TABLE IF NOT EXISTS attempts (
        id BIGSERIAL PRIMARY KEY,
        log_month VARCHAR(3) NOT NULL,
        log_day INTEGER NOT NULL,
        log_time TIME NOT NULL,
        server VARCHAR(100),
        service VARCHAR(50),
        process_id INTEGER,
        username VARCHAR(255),
        ip INET NOT NULL,
        port INTEGER,
        status VARCHAR(10) NOT NULL CHECK (status IN ('SUCCESS', 'FAILED')),
        invalid_user BOOLEAN NOT NULL DEFAULT FALSE,
        country VARCHAR(10) NOT NULL DEFAULT 'Unknown',
        attempt_count INTEGER NOT NULL DEFAULT 1,
        raw_line TEXT NOT NULL UNIQUE
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        logger.info("Table attempts verifiee")
    except psycopg2.Error:
        connection.rollback()
        logger.exception("Erreur pendant la creation de la table")
        raise
