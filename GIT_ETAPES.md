# Historique Git et publication sur GitHub

Ce dossier contient déjà un dépôt Git local avec 10 commits organisés par étape. Il n'est donc pas nécessaire de refaire les commandes `git init`, `git add` ou `git commit`.

## 1. Créer le dépôt distant

Sur GitHub, créer un nouveau dépôt nommé `log_analysis`. Ne pas cocher les options qui ajoutent automatiquement un README, un `.gitignore` ou une licence : le projet les contient déjà.

## 2. Ouvrir le dossier du projet dans VS Code

Ouvrir le dossier `log_analysis` (celui qui contient `main.py` et le dossier caché `.git`). Ouvrir ensuite le terminal intégré.

## 3. Vérifier l'historique local

```bash
git status
git log --oneline
```

Le statut doit être propre et l'historique doit afficher les 10 commits déjà préparés.

## 4. Relier le dépôt GitHub

Remplacer `VOTRE-UTILISATEUR` par le nom de votre compte GitHub :

```bash
git remote add origin https://github.com/VOTRE-UTILISATEUR/log_analysis.git
```

Si `origin` existe déjà, utiliser plutôt :

```bash
git remote set-url origin https://github.com/VOTRE-UTILISATEUR/log_analysis.git
```

## 5. Envoyer l'historique complet

```bash
git branch -M main
git push -u origin main
```

GitHub recevra les 10 commits avec leurs messages et leur ordre. Ils apparaîtront dans l'historique du dépôt.

## 6. Vérifier sur GitHub

Ouvrir le dépôt sur GitHub, puis cliquer sur l'historique des commits. Vérifier que les dix étapes apparaissent.

## Important

Les commits sont préparés localement dans ce ZIP ; ils ne sont pas encore publiés sur GitHub. Le push ci-dessus publie l'historique complet en une seule opération. Pour montrer une progression dans le temps, il aurait fallu effectuer les commits et push à des dates différentes pendant le développement.

Avant de rendre le projet, tester les modules avec la base PostgreSQL réellement fournie par l'enseignant et adapter `sql/schema.sql` si nécessaire. Le schéma fourni ici est un schéma de départ.
