# Gestion des logs

Chaque partie du programme utilise le module `logging` de Python.

- `ingestion/raw.py` écrit dans `logs/ingestion.log`.
- `processing/extract_transforme.py` et `processing/geo_location.py` écrivent dans `logs/processing.log`.
- `storage/database.py` et `storage/save.py` écrivent dans `logs/storage.log`.
- `serving/queries.py` et `serving/dashboard.py` écrivent dans `logs/serving.log`.

Les fichiers de logs sont créés pendant l'exécution. Ils ne sont pas envoyés sur GitHub, car `.gitignore` exclut `logs/*.log`.

Pour consulter les erreurs, ouvrir le fichier du module concerné après avoir lancé le programme.
