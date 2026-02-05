#!/bin/bash
# Script de configuration initiale pour Le Sciøt Cial Club API

echo "🍺 Configuration du Sciøt Cial Club API..."
echo ""

# Se placer dans le dossier api
cd "$(dirname "$0")"

# Créer l'environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Créer les migrations
echo "🗃️  Création des migrations..."
python manage.py makemigrations core events menu media_manager pages

# Appliquer les migrations
echo "⚡ Application des migrations..."
python manage.py migrate

# Créer le superutilisateur
echo ""
echo "👤 Création du compte administrateur..."
python manage.py createsuperuser

# Charger les données initiales
echo ""
echo "📊 Chargement des données initiales..."
python manage.py loaddata fixtures/initial_data.json

echo ""
echo "✅ Configuration terminée !"
echo ""
echo "Pour démarrer le serveur :"
echo "  cd api && source venv/bin/activate && python manage.py runserver"
echo ""
echo "Accès à l'admin personnalisé : http://localhost:8000/admin-panel/"
echo "Accès à la documentation API : http://localhost:8000/api/docs/"
echo ""
