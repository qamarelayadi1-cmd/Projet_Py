import gzip
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Logger du module ingestion (notions vues dans le cours logging)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = RotatingFileHandler("logs/ingestion.log", maxBytes=500000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    ))
    logger.addHandler(handler)

"""Lire les fichiers de logs du dossier indique et retourner toutes les lignes."""
def to_rows(path: str) -> list[str]:
    data_dir = Path(path)
    rows = []

    try:
        files = os.listdir(data_dir)
    except FileNotFoundError:
        logger.error("Dossier introuvable : %s", path)
        return rows
    except PermissionError:
        logger.exception("Acces refuse au dossier : %s", path)
        return rows
    except OSError:
        logger.exception("Impossible de lire le dossier : %s", path)
        return rows

    for file in sorted(files):
        file_path = data_dir / file
        if not file_path.is_file():
            continue
        try:
            if file.endswith(".gz"):
                open_type = gzip.open(file_path, mode="rt", encoding="utf-8", errors="replace")
            else:
                open_type = open(file_path, mode="rt", encoding="utf-8", errors="replace")
            with open_type as f:
                rows.extend(f.readlines())
            logger.info("Fichier lu : %s", file)
        except (OSError, EOFError, gzip.BadGzipFile):
            logger.exception("Erreur pendant la lecture du fichier : %s", file)

    logger.info("Nombre total de lignes lues : %d", len(rows))
    return rows

if __name__ == "__main__":
    data = to_rows("./data")
    print("Nombre de lignes :", len(data))
    print(data[:10])
