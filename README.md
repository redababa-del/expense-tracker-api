# Expense Tracker API

Une API REST permettant de gérer les dépenses de plusieurs utilisateurs : ajout, consultation, modification et suppression de dépenses, ainsi que des statistiques agrégées par catégorie et par mois.

Construite avec **FastAPI** et **PostgreSQL**.

## Configuration de la base de données

1. Installer PostgreSQL et créer une base nommée `expenses` (via pgAdmin ou en ligne de commande).
2. Créer un fichier `.env` à la racine du projet avec le contenu suivant :

```
DB_HOST=localhost
DB_NAME=expenses
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

⚠️ Ce fichier ne doit jamais être poussé sur GitHub (il est déjà exclu via `.gitignore`).

## Installation

```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv
```

## Lancer le projet

1. Créer les tables (à faire une seule fois) :
```bash
python database.py
```

2. Démarrer le serveur :
```bash
python -m uvicorn main:app --reload
```

3. Ouvrir la documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs)

## Routes disponibles

| Méthode | Route | Description |
|---|---|---|
| GET | `/depenses` | Liste toutes les dépenses |
| POST | `/depenses` | Crée une nouvelle dépense |
| PUT | `/depenses/{id}` | Modifie une dépense existante |
| DELETE | `/depenses/{id}` | Supprime une dépense |
| GET | `/stats/categorie` | Renvoie le total des dépenses par catégorie |
| GET | `/stats/mois` | Renvoie le total des dépenses par mois |

## Structure du projet

```
expense-tracker/
├── main.py        # Routes de l'API
├── database.py     # Connexion et requêtes SQL
├── models.py       # Modèles Pydantic
├── .env            # Variables d'environnement (non versionné)
└── .gitignore
```