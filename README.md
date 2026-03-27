# Le Sciøt Cial Club - Site Web & API

Bar culturel au cœur du Cotentin - Sciotot, Normandie.

## 🌐 Structure du projet

```
website_sciot/
├── index.html              # Page d'accueil
├── programmation.html      # Page des événements
├── menu.html               # Page du menu restaurant
├── jouerausciot.html       # Page artistes
├── css/style.css           # Styles personnalisés
├── ressources/             # Images et médias
└── api/                    # API Django + Admin personnalisé
    ├── sciot_api/          # Configuration Django
    ├── core/               # App config site & contact
    ├── events/             # App gestion événements
    ├── menu/               # App gestion menu
    ├── media_manager/      # App gestion médias
    ├── pages/              # App gestion pages
    ├── admin_custom/       # Interface admin personnalisée
    └── templates/          # Templates admin
```

## 🚀 Installation de l'API

### Prérequis
- Python 3.10+
- pip

### Installation rapide

```bash
cd api
chmod +x setup.sh
./setup.sh
```

### Installation manuelle

```bash
# Créer l'environnement virtuel
cd api
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Charger les données initiales
python manage.py loaddata fixtures/initial_data.json

# Lancer le serveur
python manage.py runserver
```

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