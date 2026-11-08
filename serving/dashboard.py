import logging
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

def create_dashboard(failed_by_country, success_by_user, invalid_users):
    """Creer trois graphiques PNG avec les resultats venant de PostgreSQL."""
    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    try:
        _create_bar_chart(
            [str(row[0]) for row in failed_by_country],
            [int(row[1]) for row in failed_by_country],
            "Tentatives echouees par pays", "Pays", "Nombre de tentatives",
            reports / "failed_by_country.png"
        )
        _create_bar_chart(
            [str(row[0]) for row in success_by_user],
            [int(row[1]) for row in success_by_user],
            "Tentatives reussies par utilisateur", "Utilisateur", "Nombre de tentatives",
            reports / "success_by_user.png"
        )
        invalid_labels = [str(row[0]) + " - " + str(row[2]) for row in invalid_users]
        invalid_values = [int(row[3]) for row in invalid_users]
        _create_bar_chart(
            invalid_labels, invalid_values,
            "Tentatives echouees avec utilisateur invalide", "Utilisateur - IP", "Nombre de tentatives",
            reports / "invalid_users.png"
        )
        logger.info("Dashboard genere dans le dossier reports")
    except Exception:
        logger.exception("Erreur pendant la creation du dashboard")
        raise

def _create_bar_chart(labels, values, title, xlabel, ylabel, output_file):
    plt.figure(figsize=(11, 6))
    if labels:
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
    else:
        plt.text(0.5, 0.5, "Aucune donnee", ha="center", va="center")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
