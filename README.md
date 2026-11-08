# Pipeline Log Analyzer

## Présentation

Ce projet sert à lire des fichiers de logs SSH et à analyser les tentatives de connexion. Il utilise les fichiers `auth.log` placés dans le dossier `data`.

## Ce que fait le programme

- Il lit les fichiers normaux et les fichiers compressés `.gz`.
- Il cherche les connexions réussies et les connexions échouées avec les expressions régulières.
- Il récupère le pays à partir de l'adresse IP avec le service IPinfo.
- Il enregistre les informations dans PostgreSQL.
- Il prépare des graphiques à partir des données de la base.
- Il garde les erreurs dans des fichiers de logs séparés selon les modules.

## Organisation des dossiers

- `ingestion` : lecture des fichiers.
- `processing` : extraction des informations et géolocalisation.
- `storage` : connexion et enregistrement dans PostgreSQL.
- `serving` : requêtes SQL et graphiques.
- `data` : fichiers auth.log utilisés pour les tests.
- `logs` : fichiers qui enregistrent les erreurs et les informations d'exécution.
- `reports` : graphiques générés par le programme.
- `sql` : script de création de la table.

## Installation

Créer et activer un environnement virtuel, puis installer les dépendances du projet :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Sur Windows, l'activation se fait avec :

```bash
.venv\Scripts\activate
```

## Configuration de PostgreSQL

Créer une base appelée `log_analysis` dans PostgreSQL. La table `attempts` est créée automatiquement au premier lancement. Le script de création est aussi disponible dans `sql/schema.sql`.

Avant de lancer le programme, définir les informations de connexion dans le terminal. Exemple sur Mac ou Linux :

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=log_analysis
export DB_USER=postgres
export DB_PASSWORD='votre_mot_de_passe'
```

Ne pas publier le mot de passe dans GitHub.

## Lancer le programme

Depuis le dossier `log_analysis` :

```bash
python main.py
```

Le programme lit les fichiers, traite les tentatives, les enregistre dans PostgreSQL et crée les graphiques dans `reports`.

## Résultats du dashboard

Les trois graphiques générés sont :

- `failed_by_country.png` : nombre de tentatives échouées par pays.
- `success_by_user.png` : nombre de tentatives réussies par utilisateur.
- `invalid_users.png` : tentatives échouées associées à un utilisateur invalide.

Les lignes `Invalid user ...` seules sont des messages préliminaires dans les fichiers fournis. Pour éviter de compter deux fois une même tentative, le programme compte la ligne `Failed password for invalid user ...` qui contient le résultat de l'échec.

## Remarque

Les fichiers de logs ne contiennent pas l'année dans leur date. Le projet conserve donc le mois, le jour et l'heure séparément. Si les fichiers changent, il faudra vérifier que leur format correspond aux expressions régulières utilisées dans `processing/extract_transforme.py`.
