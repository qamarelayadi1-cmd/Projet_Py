import logging
import re
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = RotatingFileHandler("logs/processing.log", maxBytes=500000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    ))
    logger.addHandler(handler)

# Format general des lignes auth.log du jeu de donnees fourni.
HEADER_PATTERN = re.compile(
    r"(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<server>\S+)\s+"
    r"(?P<service>\w+)\[(?P<pid>\d+)\]:\s+(?P<message>.*)"
)

# Les logs peuvent regrouper plusieurs messages identiques dans une seule ligne.
REPEATED_PATTERN = re.compile(r"message repeated (?P<count>\d+) times: \[ (?P<message>.*) \]")
SUCCESS_PATTERN = re.compile(
    r"Accepted (?:password|publickey) for (?P<username>\S+) from "
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) port (?P<port>\d+)"
)
FAILED_PATTERN = re.compile(
    r"Failed password for (?:(?P<invalid>invalid user)\s+)?(?P<username>\S+) from "
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) port (?P<port>\d+)"
)

def extract_from_row(row: str):
    """Extraire une tentative SSH. Retourner None si la ligne n'est pas une tentative."""
    header = HEADER_PATTERN.search(row)
    if not header:
        return None

    values = header.groupdict()
    message = values["message"]
    attempt_count = 1

    repeated = REPEATED_PATTERN.search(message)
    if repeated:
        attempt_count = int(repeated.group("count"))
        message = repeated.group("message")

    success = SUCCESS_PATTERN.search(message)
    failed = FAILED_PATTERN.search(message)

    if success:
        details = success.groupdict()
        status = "SUCCESS"
        invalid_user = False
    elif failed:
        details = failed.groupdict()
        status = "FAILED"
        invalid_user = details.get("invalid") is not None
    else:
        # Une ligne "Invalid user ..." seule est une information preliminaire.
        # On compte la tentative sur la ligne "Failed password for invalid user ..."
        return None

    try:
        result = {
            "month": values["month"],
            "day": int(values["day"]),
            "time": values["time"],
            "server": values["server"],
            "service": values["service"],
            "pid": int(values["pid"]),
            "username": details["username"],
            "ip": details["ip"],
            "port": int(details["port"]),
            "status": status,
            "invalid_user": invalid_user,
            "attempt_count": attempt_count,
            "raw_line": row.strip()
        }
        return result
    except (KeyError, ValueError):
        logger.exception("Erreur de transformation pour la ligne : %s", row.strip())
        return None

if __name__ == "__main__":
    example = "May 24 00:28:00 ns sshd[1351222]: Failed password for invalid user test from 45.156.87.204 port 41740 ssh2"
    print(extract_from_row(example))
