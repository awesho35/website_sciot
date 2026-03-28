# Le Sciøt Cial Club — Site Web & API

Bar culturel au cœur du Cotentin — Sciotot, Normandie.

---

## Structure

```
website_sciot/
├── index.html / programmation.html / menu.html / jouerausciot.html
├── css/style.css          # Styles (Bootstrap 5)
├── js/api.js              # Appels vers l'API
├── ressources/            # Images
├── docker-compose.yml     # 3 services : api + frontend + nginx
└── api/                   # Back-end Django 5 + DRF
    ├── core/              # Config site & contact
    ├── events/            # Événements
    ├── menu/              # Menu bar
    ├── media_manager/     # Galerie
    └── pages/             # Contenu éditorial
```

---

## Lancer en local

### API seulement (développement)

```bash
cd api
chmod +x setup.sh && ./setup.sh   # Première fois
source venv/bin/activate
python manage.py runserver
```

- Admin : `http://localhost:8000/admin-panel/`
- Docs API : `http://localhost:8000/api/docs/`

### Stack complet avec Docker

```bash
cp .env.example .env   # Remplir les variables
docker compose up --build
```

Site accessible sur `http://localhost:8082`.

---

## Variables d'environnement

Copier `.env.example` → `.env`. Ne jamais commiter `.env`.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Clé secrète Django |
| `DEBUG` | `True` en dev, `False` en prod |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés (ex. `sciot.fr`) |
| `DB_PATH` | Chemin SQLite (ex. `/app/data/db.sqlite3`) |
| `CORS_ALLOWED_ORIGINS` | URL du frontend autorisé à appeler l'API |

---

## Modifier et envoyer en ligne

### Modifier le site

- **Pages HTML** : éditer directement `index.html`, `menu.html`, etc.
- **Styles** : `css/style.css`
- **Données** (événements, menu…) : passer par `/admin-panel/`, pas besoin de toucher au code.

### Envoyer avec Git

```bash
git pull                        # Récupérer les dernières modifs
# … modifier les fichiers …
git add .                       # Préparer les fichiers modifiés
git commit -m "feat: ma modif"  # Sauvegarder
git push                        # Envoyer en ligne → le site se met à jour
```

> ⚠️ Ne jamais faire `git add .env`.

**Si le push est rejeté :**

```bash
git pull --rebase
git push
```

---

*Projet développé avec ❤️ pour le Sciøt Cial Club.*
