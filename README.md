# Le Sciøt Cial Club — Site Web & API

> Bar culturel au cœur du Cotentin — Sciotot, Normandie.
> Ce dépôt contient **le site vitrine** (HTML/CSS/JS statique) et **l'API back-end** (Django REST Framework), orchestrés par Docker Compose et hébergés sur la plateforme **Ondes HOST**.

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Architecture technique](#2-architecture-technique)
3. [Structure des fichiers](#3-structure-des-fichiers)
4. [Lancer le projet en local](#4-lancer-le-projet-en-local)
   - [Prérequis](#prérequis)
   - [Installation rapide](#installation-rapide)
   - [Installation manuelle pas à pas](#installation-manuelle-pas-à-pas)
   - [Accès en local](#accès-en-local)
5. [Lancer avec Docker Compose](#5-lancer-avec-docker-compose)
6. [Variables d'environnement](#6-variables-denvironnement)
7. [API — endpoints disponibles](#7-api--endpoints-disponibles)
8. [Interface d'administration](#8-interface-dadministration)
9. [Modifier le site — guide pratique](#9-modifier-le-site--guide-pratique)
10. [Envoyer ses modifications en ligne avec Git](#10-envoyer-ses-modifications-en-ligne-avec-git)
    - [Concepts Git en 2 minutes](#concepts-git-en-2-minutes)
    - [Workflow au quotidien](#workflow-au-quotidien)
    - [Que faire si ça se passe mal](#que-faire-si-ça-se-passe-mal)
11. [FAQ / Problèmes courants](#11-faq--problèmes-courants)

---

## 1. Vue d'ensemble

Le site du **Sciøt Cial Club** est composé de deux grandes parties qui tournent ensemble dans Docker :

| Partie | Technologie | Rôle |
|---|---|---|
| **Frontend** | HTML 5 · CSS (Bootstrap 5) · JS vanilla | Pages visibles par les visiteurs |
| **Back-end / API** | Python 3.10 · Django 5 · DRF | Données dynamiques (events, menu…) + admin |
| **Serveur web** | NGINX (Docker) | Reverse proxy entre frontend et API |

Le tout est hébergé sur un VPS géré par **Ondes HOST**. À chaque `git push` sur la branche `main`, GitHub Actions déclenche automatiquement un redéploiement.

---

## 2. Architecture technique

```
Visiteur
   │
   ▼
NGINX (port 8082 exposé au VPS)
   ├── /api/*          ──▶  conteneur Django (Gunicorn :8000)
   ├── /admin-panel/*  ──▶  conteneur Django (Gunicorn :8000)
   ├── /static/*       ──▶  fichiers statiques Django (volume Docker)
   ├── /media/*        ──▶  uploads (volume Docker)
   └── /*              ──▶  conteneur Frontend (NGINX :80, HTML statique)
```

- **3 conteneurs Docker** : `api`, `frontend`, `nginx`
- **3 volumes Docker** : `api_media`, `api_static`, `api_data` (base SQLite persistente)
- La plateforme Ondes HOST fait un second reverse proxy en amont, qui s'occupe du HTTPS et du nom de domaine.

---

## 3. Structure des fichiers

```
website_sciot/
│
├── index.html                 # Page d'accueil
├── programmation.html         # Agenda / événements
├── menu.html                  # Menu bar & restauration
├── jouerausciot.html          # Appel aux artistes
├── header.html                # Fragment HTML partagé — en-tête
├── footer.html                # Fragment HTML partagé — pied de page
│
├── css/
│   └── style.css              # Styles personnalisés (sur Bootstrap 5)
│
├── js/
│   └── api.js                 # Client API — appels fetch vers /api/*
│
├── ressources/                # Images et médias statiques du site
│
├── frontend/
│   └── Dockerfile             # Image Docker du serveur frontend (NGINX statique)
│
├── nginx/
│   └── nginx.conf             # Configuration du reverse proxy NGINX du projet
│
├── docker-compose.yml         # Définition des 3 services Docker
├── .env                       # Variables secrètes (NON versionnées — voir .env.example)
├── .env.example               # Modèle de variables d'environnement
├── .gitignore                 # Fichiers exclus de Git
│
├── .github/
│   └── workflows/
│       └── deploy.yml         # Pipeline CI/CD GitHub Actions
│
└── api/                       # Back-end Django
    ├── manage.py
    ├── requirements.txt       # Dépendances Python
    ├── setup.sh               # Script d'installation rapide
    ├── Dockerfile             # Image Docker de l'API
    │
    ├── sciot_api/             # Configuration principale Django
    │   ├── settings.py
    │   ├── urls.py            # Routage racine
    │   └── wsgi.py
    │
    ├── core/                  # Config du site (titre, réseaux sociaux, contact)
    ├── events/                # Gestion des événements / concerts
    ├── menu/                  # Gestion du menu bar & restauration
    ├── media_manager/         # Upload et gestion des images
    ├── pages/                 # Contenu éditorial des pages
    ├── admin_custom/          # Interface admin personnalisée
    ├── templates/             # Templates HTML de l'admin
    └── fixtures/
        └── initial_data.json  # Données de départ (chargées au setup)
```

---

## 4. Lancer le projet en local

### Prérequis

- **Python 3.10+** — vérifier avec `python3 --version`
- **pip** — fourni avec Python
- Un terminal (Terminal sur macOS, PowerShell ou WSL sur Windows)
- *(Optionnel pour Docker)* **Docker Desktop** — <https://www.docker.com/products/docker-desktop>

### Installation rapide

```bash
# 1. Cloner le dépôt (première fois seulement)
git clone <URL_DU_DEPOT> website_sciot
cd website_sciot

# 2. Lancer le script de setup
cd api
chmod +x setup.sh
./setup.sh
```

Le script crée l'environnement virtuel, installe les dépendances, applique les migrations,
crée le compte admin et charge les données initiales.

### Installation manuelle pas à pas

Si vous préférez comprendre chaque étape :

```bash
# Aller dans le dossier api
cd api

# Créer un environnement virtuel Python isolé
python3 -m venv venv

# L'activer (macOS / Linux)
source venv/bin/activate
# L'activer (Windows PowerShell)
# venv\Scripts\Activate.ps1

# Installer toutes les dépendances listées dans requirements.txt
pip install -r requirements.txt

# Préparer la base de données (tables, colonnes…)
python manage.py makemigrations
python manage.py migrate

# Créer un compte administrateur
python manage.py createsuperuser

# Charger les données initiales (événements, menu de démo…)
python manage.py loaddata fixtures/initial_data.json

# Démarrer le serveur de développement
python manage.py runserver
```

### Accès en local

| URL | Description |
|---|---|
| `http://localhost:8000/admin-panel/` | Interface admin personnalisée |
| `http://localhost:8000/django-admin/` | Admin Django natif (backup) |
| `http://localhost:8000/api/docs/` | Documentation interactive Swagger |
| `http://localhost:8000/api/events/` | Exemple d'endpoint API |

Pour voir le **frontend** (les pages HTML), ouvrir `index.html` directement dans le navigateur,
ou utiliser Docker Compose (voir section suivante) pour avoir le stack complet.

---

## 5. Lancer avec Docker Compose

Docker Compose démarre les 3 conteneurs (API + frontend + NGINX) en une commande, comme en production.

```bash
# Depuis la racine du projet (website_sciot/)

# 1. Copier et remplir les variables d'environnement
cp .env.example .env
# Éditez .env avec vos valeurs (voir section 6)

# 2. Construire et démarrer tous les services
docker compose up --build

# 3. (Optionnel) Démarrer en arrière-plan
docker compose up --build -d

# 4. Créer le superutilisateur Django (première fois)
docker compose exec api python manage.py createsuperuser

# 5. Charger les données initiales (première fois)
docker compose exec api python manage.py loaddata fixtures/initial_data.json
```

Le site est alors accessible sur **`http://localhost:8082`**.

```bash
# Arrêter les conteneurs
docker compose down

# Arrêter ET supprimer les volumes (⚠️ efface la base de données)
docker compose down -v

# Voir les logs en temps réel
docker compose logs -f

# Voir les logs d'un seul service
docker compose logs -f api
```

---

## 6. Variables d'environnement

Copiez `.env.example` en `.env` et remplissez chaque valeur.
**Le fichier `.env` ne doit jamais être commité** (il est listé dans `.gitignore`).

| Variable | Exemple | Description |
|---|---|---|
| `SECRET_KEY` | `abc123...` | Clé secrète Django. Générer avec : `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | `False` | Mettre `True` uniquement en développement local |
| `DJANGO_ALLOWED_HOSTS` | `sciot.fr,www.sciot.fr` | Domaines autorisés (séparés par des virgules) |
| `DB_PATH` | `/app/data/db.sqlite3` | Chemin vers la base SQLite (volume Docker en prod) |
| `CORS_ALLOWED_ORIGINS` | `https://sciot.fr` | Origines autorisées à appeler l'API (prod uniquement) |

---

## 7. API — endpoints disponibles

La documentation complète et interactive est disponible à `/api/docs/` (Swagger UI).

### Configuration & contact
| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/config/` | Titre, description, infos générales du bar |
| GET | `/api/social-links/` | Liens réseaux sociaux |
| POST | `/api/contact/` | Envoyer un message de contact |

### Événements
| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | Liste de tous les événements |
| GET | `/api/events/upcoming/` | Prochains événements |
| GET | `/api/events/week/` | Événements de la semaine |
| GET | `/api/events/calendar/` | Vue calendrier |
| GET | `/api/events/categories/` | Catégories d'événements |

### Menu
| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/menu/full/` | Menu complet (plats + boissons) |
| GET | `/api/menu/categories/` | Catégories de plats |
| GET | `/api/menu/items/` | Plats |
| GET | `/api/menu/drinks/categories/` | Catégories de boissons |
| GET | `/api/menu/drinks/items/` | Boissons |
| GET | `/api/menu/specials/` | Menus spéciaux / formules |

### Médias & pages
| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/media/` | Galerie d'images |
| GET | `/api/pages/` | Contenu éditorial des pages |

---

## 8. Interface d'administration

L'interface admin personnalisée est accessible à `/admin-panel/`.
Elle permet de gérer sans toucher au code :

- Les **événements** (concerts, soirées, expositions…)
- Le **menu** (plats, boissons, formules)
- Les **images** de la galerie
- La **configuration** du site (textes, réseaux sociaux…)
- Les **pages** éditoriales

L'admin Django natif (pour les opérations avancées) est accessible à `/django-admin/`.

---

## 9. Modifier le site — guide pratique

### Modifier une page HTML

Les pages sont des fichiers `.html` à la racine du projet.
Ouvrez-les dans n'importe quel éditeur de texte (VS Code recommandé).

- **Textes / titres** : chercher directement dans le fichier HTML et modifier.
- **Navigation** : elle est dupliquée dans chaque page (pas de système de composants côté frontend). Modifier `header.html` ne suffit pas — il faut mettre à jour la balise `<nav>` dans chaque fichier `.html`.
- **Styles** : tout est dans `css/style.css`. Bootstrap 5 est chargé depuis un CDN.
- **Appels API** : la logique de récupération des données est dans `js/api.js`.

### Ajouter une image

1. Copier l'image dans le dossier `ressources/`.
2. La référencer dans le HTML : `<img src="ressources/mon-image.jpg" alt="...">`.
3. Ou la télécharger via l'admin (`/admin-panel/` → Médias) pour qu'elle soit servie par Django.

### Modifier des données (événements, menu…)

Passer par l'interface admin — pas besoin de toucher au code.

---

## 10. Envoyer ses modifications en ligne avec Git

### Concepts Git en 2 minutes

Git est un outil qui **sauvegarde l'historique de vos fichiers** et permet de travailler à plusieurs sans se marcher dessus.

| Terme | Explication simple |
|---|---|
| **dépôt (repository)** | Le dossier du projet, suivi par Git |
| **commit** | Une "photo" de l'état du projet à un instant T, avec un message |
| **branche (branch)** | Une version parallèle du projet. La branche principale s'appelle `main` |
| **remote** | La copie du dépôt hébergée en ligne (sur GitHub) |
| **push** | Envoyer vos commits locaux vers GitHub |
| **pull** | Récupérer les commits de GitHub vers votre machine |

### Workflow au quotidien

Voici les commandes à connaître pour travailler sur le site.

#### Étape 1 — Récupérer les dernières modifications

Avant de commencer à travailler, toujours synchroniser :

```bash
git pull
```

#### Étape 2 — Modifier les fichiers

Éditez les fichiers de votre choix (`index.html`, `css/style.css`, etc.) avec votre éditeur.

#### Étape 3 — Vérifier ce qui a changé

```bash
# Voir quels fichiers ont été modifiés
git status

# Voir le détail des changements ligne par ligne
git diff
```

#### Étape 4 — Préparer le commit (staging)

```bash
# Ajouter un fichier précis
git add index.html

# Ajouter tous les fichiers modifiés d'un coup
git add .
```

> ⚠️ Ne jamais faire `git add .env` — le fichier `.env` contient des secrets et ne doit pas être envoyé sur GitHub.

#### Étape 5 — Créer le commit

```bash
git commit -m "feat: ajout de la date du prochain concert"
```

Le message de commit doit être **court et clair**. Conventions utilisées dans ce projet :

| Préfixe | Quand l'utiliser |
|---|---|
| `feat:` | Ajout d'une nouvelle fonctionnalité |
| `fix:` | Correction d'un bug |
| `chore:` | Mise à jour de dépendances, réorganisation |
| `docs:` | Modification de documentation |
| `refactor:` | Réécriture de code sans changer le comportement |

#### Étape 6 — Envoyer sur GitHub

```bash
git push
```

C'est tout ! Le site sera mis à jour en ligne.

---

### Commandes Git complètes en un coup d'oeil

```bash
# ── Quotidien ────────────────────────────────────────────────────────────────
git pull                          # Récupérer les dernières modifs
git status                        # Voir les fichiers modifiés
git diff                          # Voir les changements en détail

git add nom_du_fichier.html       # Préparer un fichier
git add .                         # Préparer tous les fichiers modifiés
git commit -m "feat: ma modif"    # Créer le commit
git push                          # Envoyer sur GitHub → met le site à jour

# ── Historique ───────────────────────────────────────────────────────────────
git log --oneline                 # Voir l'historique des commits
git diff HEAD~1                   # Voir ce qui a changé depuis le dernier commit

# ── Annuler ──────────────────────────────────────────────────────────────────
git restore nom_du_fichier.html   # Annuler les modifs d'un fichier (avant le commit)
git restore .                     # Annuler TOUTES les modifs locales non commitées
```

---

### Que faire si ça se passe mal

**"J'ai commité par erreur un fichier que je ne voulais pas"**

```bash
# Annuler le dernier commit en gardant les modifications locales
git reset --soft HEAD~1

# Retirer le fichier du staging, puis recommiter sans lui
git restore --staged .env
git commit -m "feat: ma modif sans le .env"
git push
```

**"Mon push est rejeté (rejected)"**

Il y a probablement des commits sur GitHub que vous n'avez pas en local. Faites d'abord :

```bash
git pull --rebase
# Résoudre les éventuels conflits, puis :
git push
```

---

## 11. FAQ / Problèmes courants

**Le site ne se charge pas après `docker compose up`**

Attendre quelques secondes que Django applique les migrations au démarrage, puis recharger.
Vérifier les logs : `docker compose logs -f api`

**"ModuleNotFoundError" au démarrage de l'API**

L'environnement virtuel n'est pas activé ou les dépendances ne sont pas installées :

```bash
cd api
source venv/bin/activate
pip install -r requirements.txt
```

**Les images uploadées via l'admin ont disparu**

En local, les médias sont dans `api/media/` (ignoré par Git). En production, ils sont dans le volume Docker `api_media`. Si vous recréez les conteneurs avec `docker compose down -v`, les médias sont effacés.

**Je vois "CORS error" dans la console du navigateur**

En production, vérifier que `CORS_ALLOWED_ORIGINS` dans `.env` contient bien l'URL du frontend (avec `https://`).

**Comment voir la doc API ?**

En local : `http://localhost:8000/api/docs/`
En production : `https://votre-domaine.fr/api/docs/`

---

*Projet développé avec ❤️ pour le Sciøt Cial Club — Sciotot, Normandie.*

## 🔗 Accès

| Service | URL |
|---------|-----|
| Admin personnalisé | http://localhost:8000/admin-panel/ |
| Admin Django | http://localhost:8000/admin/ |
| Documentation API (Swagger) | http://localhost:8000/api/docs/ |
| API Événements | http://localhost:8000/api/events/ |
| API Menu | http://localhost:8000/api/menu/ |
| API Médias | http://localhost:8000/api/media/ |
| API Pages | http://localhost:8000/api/pages/ |

## 📡 Endpoints API

### Événements
- `GET /api/events/` - Liste des événements
- `GET /api/events/{id}/` - Détail d'un événement
- `GET /api/events/week/` - Événements de la semaine
- `GET /api/events/upcoming/` - Événements à venir
- `GET /api/events/calendar/` - Format calendrier (FullCalendar)
- `GET /api/events/stats/` - Statistiques
- `GET /api/events/categories/` - Catégories

### Menu
- `GET /api/menu/full/` - Menu complet
- `GET /api/menu/categories/` - Catégories de plats
- `GET /api/menu/items/` - Tous les plats
- `GET /api/menu/drinks/categories/` - Catégories de boissons
- `GET /api/menu/drinks/items/` - Toutes les boissons
- `GET /api/menu/specials/` - Formules spéciales

### Configuration
- `GET /api/config/` - Configuration du site
- `GET /api/social-links/` - Liens réseaux sociaux
- `POST /api/contact/` - Envoyer un message

### Médias
- `GET /api/media/images/` - Galerie d'images
- `POST /api/media/images/bulk_upload/` - Upload multiple
- `GET /api/media/carousel/` - Slides du carrousel
- `GET /api/media/hero/` - Bannières hero

### Pages
- `GET /api/pages/pages/` - Pages du site
- `GET /api/pages/menu/` - Pages du menu navigation
- `GET /api/pages/faq/` - FAQ

## 🎨 Interface Admin Personnalisée

L'interface admin (`/admin-panel/`) utilise le même design que le site public :
- Même palette de couleurs (#1a1a2e)
- Police Jost
- Style glass-bar

### Fonctionnalités
- **Dashboard** : Vue d'ensemble avec statistiques
- **Événements** : CRUD + Calendrier interactif (FullCalendar)
- **Menu** : Gestion plats, boissons, formules
- **Médias** : Galerie avec upload drag & drop
- **Messages** : Gestion des messages de contact
- **Paramètres** : Configuration site et réseaux sociaux

## 🛠️ Technologies

### Frontend (Site public)
- HTML5 / CSS3
- Bootstrap 5
- Bootstrap Icons
- Google Fonts (Jost)

### Backend (API)
- Django 5.x
- Django REST Framework
- Django CORS Headers
- Django Filter
- DRF Spectacular (Swagger)
- Pillow (images)
- SQLite (dev) / PostgreSQL (prod)

### Admin personnalisé
- Bootstrap 5
- FullCalendar 6.x
- Vanilla JS

## 📝 License

Propriétaire - Le Sciøt Cial Club © 2024

---

## 🚀 Déploiement sur Ondes HOST

### Architecture Docker

Le `docker-compose.yml` contient trois services :

| Service | Rôle |
|---------|------|
| `api` | Django 5 + Gunicorn (port 8000, interne) |
| `frontend` | NGINX servant les fichiers HTML/CSS/JS statiques (port 80, interne) |
| `nginx` | Reverse-proxy interne exposé sur le **port 8082** → routé par Ondes HOST |

> Le port 8082 est un port non-plateforme : Ondes HOST le détecte comme routeur interne et ne le supprime **pas** au déploiement.

### Variables d'environnement à configurer dans Ondes HOST

Dans le panneau **Stack Detail → Environment Variables**, renseigner :

```
SECRET_KEY=<générer avec : python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
DJANGO_ALLOWED_HOSTS=votre-domaine.fr,www.votre-domaine.fr
DB_PATH=/app/data/db.sqlite3
CORS_ALLOWED_ORIGINS=https://votre-domaine.fr,https://www.votre-domaine.fr
```

> Le fichier `.env` est écrit automatiquement par le pipeline Ondes HOST depuis ces variables.

### CI/CD automatique (webhook)

Le workflow `.github/workflows/deploy.yml` déclenche un redéploiement à chaque push sur `main`.  
Configurer trois secrets GitHub (**Settings → Secrets → Actions**) :

| Secret | Valeur |
|--------|--------|
| `ONDES_API_URL` | URL de l'instance Ondes HOST, ex. `https://ondes.monvps.fr` |
| `ONDES_STACK_ID` | ID numérique du stack (visible dans l'URL du dashboard) |
| `ONDES_WEBHOOK_TOKEN` | UUID affiché dans le panneau Stack Detail de l'app Flutter |

### Premier déploiement

1. Connecter le repo GitHub dans Ondes HOST (onglet GitHub Integration).
2. Créer un nouveau stack pointant sur ce repo / branche `main`.
3. Renseigner toutes les variables d'environnement ci-dessus.
4. Cliquer **Deploy** — le pipeline clone, écrit `.env`, strip les conflits plateforme, et lance `docker compose up -d --build`.
5. Configurer le vhost dans Ondes HOST pour pointer le domaine vers le port 8082.