#!/bin/bash
# Script pour configurer les permissions PostgreSQL correctement
# Setup PostgreSQL permissions for villa_sales database

set -e

echo "============================================================"
echo "🔧 Configuration des Permissions PostgreSQL"
echo "   Villa à Vendre Marrakech"
echo "============================================================"
echo ""

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier si on est root ou avec sudo
if [ "$EUID" -ne 0 ] && ! sudo -n true 2>/dev/null; then 
    echo -e "${RED}❌ Ce script doit être exécuté avec sudo${NC}"
    echo "Usage: sudo bash setup_postgres_permissions.sh"
    exit 1
fi

# Variables (modifiez si nécessaire)
DB_NAME=${PGDATABASE:-villa_sales}
DB_USER=${PGUSER:-villa_user}
DB_PASS=${PGPASSWORD:-changeme}

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo ""

# Vérifier si PostgreSQL est installé et en cours d'exécution
echo "🔍 Vérification de PostgreSQL..."
if ! systemctl is-active --quiet postgresql; then
    echo -e "${RED}❌ PostgreSQL n'est pas en cours d'exécution${NC}"
    echo "Démarrage de PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    echo -e "${GREEN}✅ PostgreSQL démarré${NC}"
fi

# Créer l'utilisateur s'il n'existe pas
echo ""
echo "👤 Configuration de l'utilisateur PostgreSQL..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_user WHERE usename = '$DB_USER'" | grep -q 1 || \
sudo -u postgres psql << EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
ALTER USER $DB_USER CREATEDB;
EOF

echo -e "${GREEN}✅ Utilisateur $DB_USER configuré${NC}"

# Créer la base de données si elle n'existe pas
echo ""
echo "🗄️  Configuration de la base de données..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME OWNER $DB_USER;
EOF

echo -e "${GREEN}✅ Base de données $DB_NAME créée${NC}"

# Donner tous les privilèges
echo ""
echo "🔐 Attribution des permissions..."
sudo -u postgres psql << EOF
-- Se connecter à la base de données
\c $DB_NAME

-- Donner tous les privilèges sur la base de données
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Donner les privilèges sur le schéma public
GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;
GRANT CREATE ON SCHEMA public TO $DB_USER;

-- Donner les privilèges sur toutes les tables existantes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;

-- Donner les privilèges sur les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO $DB_USER;

-- Rendre l'utilisateur propriétaire du schéma public (pour éviter les erreurs de permission)
ALTER SCHEMA public OWNER TO $DB_USER;

-- Afficher les privilèges
\du $DB_USER
EOF

echo -e "${GREEN}✅ Permissions configurées avec succès${NC}"

# Tester la connexion
echo ""
echo "🧪 Test de connexion..."
if PGPASSWORD=$DB_PASS psql -U $DB_USER -d $DB_NAME -h localhost -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Connexion réussie !${NC}"
else
    echo -e "${RED}❌ Échec de la connexion${NC}"
    exit 1
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✅ CONFIGURATION TERMINÉE AVEC SUCCÈS !${NC}"
echo "============================================================"
echo ""
echo "Variables d'environnement à ajouter dans .env:"
echo ""
echo "PGHOST=localhost"
echo "PGPORT=5432"
echo "PGUSER=$DB_USER"
echo "PGPASSWORD=$DB_PASS"
echo "PGDATABASE=$DB_NAME"
echo ""
echo "Prochaines étapes:"
echo "1. Mettre à jour votre fichier .env avec les valeurs ci-dessus"
echo "2. Lancer: python fix_database.py"
echo "3. Lancer: python app.py"
echo ""
