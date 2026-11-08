import logging
from pathlib import Path

from ingestion import raw
from processing import extract_transforme, geo_location
from storage import database, save
from serving import queries, dashboard


def main():
    # Les dossiers de sortie doivent exister avant de creer les fichiers de logs.
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO)

    print("Lecture des fichiers logs...")
    rows = raw.to_rows("./data")
    print("Lignes lues :", len(rows))

    print("Extraction des tentatives SSH...")
    attempts = []
    for row in rows:
        result = extract_transforme.extract_from_row(row)
        if result is not None:
            attempts.append(result)
    print("Tentatives trouvees :", len(attempts))

    if not attempts:
        print("Aucune tentative reconnue. Verifiez les fichiers dans data/.")
        return

    print("Geolocalisation des adresses IP...")
    location_cache = {}
    for attempt in attempts:
        ip = attempt["ip"]
        if ip not in location_cache:
            location_cache[ip] = geo_location.get_location(ip)
        attempt["country"] = location_cache[ip]

    print("Connexion a PostgreSQL...")
    connection = database.get_connection()
    if connection is None:
        print("Connexion PostgreSQL impossible. Verifiez les variables DB_*. ")
        return

    try:
        database.create_tables(connection)
        inserted = save.save_attempts(connection, attempts)
        print("Nouvelles tentatives enregistrees :", inserted)

        failed_by_country = queries.get_failed_by_country(connection)
        success_by_user = queries.get_success_by_user(connection)
        invalid_users = queries.get_invalid_users(connection)

        dashboard.create_dashboard(failed_by_country, success_by_user, invalid_users)
        print("Dashboard cree dans le dossier reports/.")
        print("- reports/failed_by_country.png")
        print("- reports/success_by_user.png")
        print("- reports/invalid_users.png")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
