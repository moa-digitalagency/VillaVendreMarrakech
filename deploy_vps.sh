#!/bin/bash

###############################################################################
# Script de Déploiement VPS - Villa à Vendre Marrakech
# 
# Ce script automatise le déploiement complet de l'application sur un VPS
# Il gère l'installation, la configuration et les mises à jour
#
# Usage:
#   Première installation : ./deploy_vps.sh install
#   Mise à jour           : ./deploy_vps.sh update
#   Redémarrage           : ./deploy_vps.sh restart
#   Sauvegarde DB         : ./deploy_vps.sh backup
#
# Développé par: MOA Digital Agency LLC
# Développeur: Aisance KALONJI
###############################################################################

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="villaeden"
APP_DIR="/var/www/villaeden"
APP_USER="www-data"
PYTHON_VERSION="python3.11"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="villaeden.service"

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "Ce script doit être exécuté en tant que root (utilisez sudo)"
        exit 1
    fi
}

# Vérifier les variables d'environnement
check_env_vars() {
    log_info "Vérification des variables d'environnement..."
    
    if [ ! -f "$APP_DIR/.env" ]; then
        log_error "Fichier .env non trouvé dans $APP_DIR"
        log_info "Créez un fichier .env avec les variables suivantes:"
        echo "DATABASE_URL=postgresql://user:password@localhost:5432/villaeden"
        echo "SESSION_SECRET=votre-secret-session-aleatoire"
        echo "ADMIN_PASSWORD=votre-mot-de-passe-admin"
        echo "OPENROUTER_API_KEY=votre-cle-api-openrouter (optionnel)"
        exit 1
    fi
    
    log_success "Fichier .env trouvé"
}

# Installation initiale complète
install() {
    log_info "=== INSTALLATION INITIALE DE L'APPLICATION ==="
    
    check_root
    
    # 1. Mise à jour du système
    log_info "Mise à jour du système..."
    apt update && apt upgrade -y
    log_success "Système mis à jour"
    
    # 2. Installation des dépendances système
    log_info "Installation des dépendances système..."
    apt install -y python3.11 python3.11-venv python3-pip postgresql nginx git curl
    apt install -y python3.11-dev libpq-dev build-essential
    log_success "Dépendances système installées"
    
    # 3. Configuration PostgreSQL
    log_info "Configuration de PostgreSQL..."
    sudo -u postgres psql -c "CREATE DATABASE villaeden;" 2>/dev/null || log_warning "Database déjà existante"
    sudo -u postgres psql -c "CREATE USER villauser WITH PASSWORD 'changeme';" 2>/dev/null || log_warning "User déjà existant"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE villaeden TO villauser;" 
    sudo -u postgres psql -c "ALTER DATABASE villaeden OWNER TO villauser;"
    log_success "PostgreSQL configuré"
    log_warning "N'oubliez pas de changer le mot de passe PostgreSQL dans votre .env!"
    
    # 4. Création du répertoire de l'application
    log_info "Création du répertoire de l'application..."
    mkdir -p $APP_DIR
    cd $APP_DIR
    log_success "Répertoire créé: $APP_DIR"
    
    # 5. Clonage du code (ou copie si déjà présent)
    if [ -d ".git" ]; then
        log_info "Dépôt Git déjà présent, mise à jour..."
        git pull origin main
    else
        log_warning "Copiez votre code dans $APP_DIR"
        log_info "Ou clonez depuis Git: git clone <votre-repo> ."
    fi
    
    # 6. Création de l'environnement virtuel Python
    log_info "Création de l'environnement virtuel Python..."
    $PYTHON_VERSION -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    log_success "Environnement virtuel créé"
    
    # 7. Installation des packages Python
    log_info "Installation des packages Python..."
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Packages Python installés"
    
    # 8. Création du fichier .env si non existant
    if [ ! -f ".env" ]; then
        log_info "Création du fichier .env template..."
        cat > .env << 'EOL'
# Configuration de la base de données PostgreSQL
DATABASE_URL=postgresql://villauser:changeme@localhost:5432/villaeden

# Clé secrète pour les sessions Flask (générez une clé aléatoire forte)
SESSION_SECRET=changeme-generate-random-secret-key

# Mot de passe administrateur
ADMIN_PASSWORD=changeme-admin-password

# Clé API OpenRouter pour les fonctionnalités IA (optionnel)
# OPENROUTER_API_KEY=sk-or-v1-xxxxx
EOL
        log_warning "Fichier .env créé - MODIFIEZ LES VALEURS AVANT DE CONTINUER!"
        log_error "Éditez $APP_DIR/.env et relancez le script"
        exit 1
    fi
    
    # 9. Création du fichier systemd service
    log_info "Création du service systemd..."
    cat > /etc/systemd/system/$SERVICE_NAME << EOL
[Unit]
Description=Villa Eden - Application Flask
After=network.target postgresql.service

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV_DIR/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 --timeout 120 main:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOL
    log_success "Service systemd créé"
    
    # 10. Configuration de Nginx
    log_info "Configuration de Nginx..."
    cat > /etc/nginx/sites-available/$APP_NAME << 'EOL'
server {
    listen 80;
    server_name villaavendremarrakech.com www.villaavendremarrakech.com;
    
    client_max_body_size 16M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    location /static {
        alias /var/www/villaeden/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOL
    
    # Activer le site
    ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t
    log_success "Nginx configuré"
    
    # 11. Permissions
    log_info "Configuration des permissions..."
    chown -R $APP_USER:$APP_USER $APP_DIR
    chmod -R 755 $APP_DIR
    mkdir -p $APP_DIR/static/uploads
    chown -R $APP_USER:$APP_USER $APP_DIR/static/uploads
    log_success "Permissions configurées"
    
    # 12. Initialisation de la base de données
    log_info "Initialisation de la base de données..."
    cd $APP_DIR
    source $VENV_DIR/bin/activate
    python migrate_default_texts.py || log_warning "Migration ignorée si aucune villa"
    log_success "Base de données initialisée"
    
    # 13. Démarrage des services
    log_info "Démarrage des services..."
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    systemctl start $SERVICE_NAME
    systemctl restart nginx
    log_success "Services démarrés"
    
    # 14. Configuration SSL avec Let's Encrypt (optionnel)
    log_info "Pour configurer SSL avec Let's Encrypt, exécutez:"
    echo "sudo apt install certbot python3-certbot-nginx"
    echo "sudo certbot --nginx -d villaavendremarrakech.com -d www.villaavendremarrakech.com"
    
    log_success "=== INSTALLATION TERMINÉE AVEC SUCCÈS ==="
    log_info "Votre application est accessible sur: http://votre-ip-vps"
    log_info "Connectez-vous à l'admin: http://votre-ip-vps/login"
}

# Mise à jour de l'application
update() {
    log_info "=== MISE À JOUR DE L'APPLICATION ==="
    
    check_root
    check_env_vars
    
    # 1. Sauvegarde de la base de données
    backup
    
    # 2. Mise à jour du code
    log_info "Mise à jour du code depuis Git..."
    cd $APP_DIR
    git stash  # Sauvegarder les modifications locales
    git pull origin main
    log_success "Code mis à jour"
    
    # 3. Mise à jour des dépendances Python
    log_info "Mise à jour des dépendances Python..."
    source $VENV_DIR/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Dépendances mises à jour"
    
    # 4. Exécution des migrations de base de données
    log_info "Exécution des migrations..."
    python migrate_default_texts.py
    log_success "Migrations exécutées"
    
    # 5. Mise à jour des permissions
    log_info "Mise à jour des permissions..."
    chown -R $APP_USER:$APP_USER $APP_DIR
    log_success "Permissions mises à jour"
    
    # 6. Redémarrage de l'application
    restart
    
    log_success "=== MISE À JOUR TERMINÉE AVEC SUCCÈS ==="
}

# Redémarrage de l'application
restart() {
    log_info "Redémarrage de l'application..."
    
    check_root
    
    systemctl restart $SERVICE_NAME
    systemctl restart nginx
    
    # Attendre que l'application démarre
    sleep 3
    
    # Vérifier le statut
    if systemctl is-active --quiet $SERVICE_NAME; then
        log_success "Application redémarrée avec succès"
        systemctl status $SERVICE_NAME --no-pager
    else
        log_error "Échec du redémarrage de l'application"
        journalctl -u $SERVICE_NAME -n 50 --no-pager
        exit 1
    fi
}

# Sauvegarde de la base de données
backup() {
    log_info "Sauvegarde de la base de données..."
    
    BACKUP_DIR="$APP_DIR/backups"
    mkdir -p $BACKUP_DIR
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/villaeden_backup_$TIMESTAMP.sql"
    
    # Charger les variables d'environnement
    if [ -f "$APP_DIR/.env" ]; then
        export $(cat $APP_DIR/.env | grep -v '^#' | xargs)
    fi
    
    # Extraction des infos de connexion depuis DATABASE_URL
    # Format: postgresql://user:password@host:port/database
    DB_INFO=$(echo $DATABASE_URL | sed -e 's/postgresql:\/\///' -e 's/@/ /' -e 's/:/ /g' -e 's/\// /g')
    DB_USER=$(echo $DB_INFO | awk '{print $1}')
    DB_PASS=$(echo $DB_INFO | awk '{print $2}')
    DB_HOST=$(echo $DB_INFO | awk '{print $3}')
    DB_PORT=$(echo $DB_INFO | awk '{print $4}')
    DB_NAME=$(echo $DB_INFO | awk '{print $5}')
    
    PGPASSWORD=$DB_PASS pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME > $BACKUP_FILE
    
    # Compression de la sauvegarde
    gzip $BACKUP_FILE
    
    log_success "Sauvegarde créée: ${BACKUP_FILE}.gz"
    
    # Nettoyage des anciennes sauvegardes (garder les 30 dernières)
    log_info "Nettoyage des anciennes sauvegardes..."
    cd $BACKUP_DIR
    ls -t villaeden_backup_*.sql.gz | tail -n +31 | xargs -r rm
    log_success "Anciennes sauvegardes nettoyées"
}

# Affichage des logs
logs() {
    log_info "Affichage des logs de l'application..."
    journalctl -u $SERVICE_NAME -f
}

# Vérification du statut
status() {
    log_info "Statut de l'application:"
    systemctl status $SERVICE_NAME --no-pager
    
    log_info "\nStatut Nginx:"
    systemctl status nginx --no-pager
    
    log_info "\nStatut PostgreSQL:"
    systemctl status postgresql --no-pager
}

# Menu d'aide
help() {
    echo "=========================================="
    echo "Script de Déploiement - Villa à Vendre"
    echo "=========================================="
    echo ""
    echo "Usage: $0 {install|update|restart|backup|logs|status|help}"
    echo ""
    echo "Commandes disponibles:"
    echo "  install  - Installation initiale complète de l'application"
    echo "  update   - Mise à jour de l'application (code + dépendances + DB)"
    echo "  restart  - Redémarrage de l'application et Nginx"
    echo "  backup   - Sauvegarde de la base de données"
    echo "  logs     - Affichage des logs en temps réel"
    echo "  status   - Vérification du statut des services"
    echo "  help     - Affichage de cette aide"
    echo ""
    echo "Exemples:"
    echo "  sudo ./deploy_vps.sh install"
    echo "  sudo ./deploy_vps.sh update"
    echo "  sudo ./deploy_vps.sh backup"
    echo ""
}

# Menu principal
case "$1" in
    install)
        install
        ;;
    update)
        update
        ;;
    restart)
        restart
        ;;
    backup)
        backup
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    help)
        help
        ;;
    *)
        log_error "Commande invalide: $1"
        help
        exit 1
        ;;
esac
