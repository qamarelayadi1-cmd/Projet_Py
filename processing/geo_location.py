import logging
import requests
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

URL_IPINFO = "https://ipinfo.io/"

# Cache simple : une IP deja demandee ne sera pas redemandee pendant l'execution.
_locations = {}

def get_location(ip: str):
    if ip in _locations:
        return _locations[ip]

    try:
        response = requests.get(URL_IPINFO + ip + "/json", timeout=10)
        response.raise_for_status()
        result = response.json()
        country = result.get("country", "Unknown")
        _locations[ip] = country
        return country
    except requests.exceptions.Timeout:
        logger.error("Timeout pendant la geolocalisation de %s", ip)
    except requests.exceptions.RequestException:
        logger.exception("Erreur reseau ou HTTP pour l'IP %s", ip)
    except ValueError:
        logger.exception("Reponse JSON incorrecte pour l'IP %s", ip)

    _locations[ip] = "Unknown"
    return "Unknown"

if __name__ == "__main__":
    print(get_location("45.156.87.204"))
