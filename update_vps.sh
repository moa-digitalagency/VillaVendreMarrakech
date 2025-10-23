#!/bin/bash

###############################################################################
# Script de Mise à Jour VPS - Villa à Vendre Marrakech
# 
# Script simplifié pour mettre à jour une application déjà en production
# Gère la mise à jour du code, des dépendances et redémarre les services
#
# Usage:
#   ./update_vps.sh              # Mise à jour complète
#   ./update_vps.sh --quick      # Mise à jour rapide (sans backup)
#   ./update_vps.sh --restart    # Redémarrage uniquement
#
# Développé par: MOA Digital Agency LLC
###############################################################################

set -e  # Arrêter en cas d'erreur

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration (ajustez selon votre configuration)
APP_DIR="/var/www/villaeden"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="villaeden.service"
BACKUP_DIR="$APP_DIR/backups"

# Fonctions utilitaires
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# Vérifier si on est root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "Ce script doit être exécuté en tant que root (utilisez sudo)"
        exit 1
    fi
}

# Vérifier que le répertoire existe
check_app_dir() {
    if [ ! -d "$APP_DIR" ]; then
        log_error "Répertoire $APP_DIR non trouvé. L'application n'est pas installée ici."
        exit 1
    fi
}

# Sauvegarde de la base de données
backup_database() {
    log_info "Sauvegarde de la base de données..."
    
    mkdir -p $BACKUP_DIR
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"
    
    # Charger les variables d'environnement
    if [ -f "$APP_DIR/.env" ]; then
        export $(cat $APP_DIR/.env | grep -v '^#' | xargs)
    fi
    
    # Extraction des infos depuis DATABASE_URL
    if [ -n "$DATABASE_URL" ]; then
        DB_INFO=$(echo $DATABASE_URL | sed -e 's/postgresql:\/\///' -e 's/@/ /' -e 's/:/ /g' -e 's/\// /g')
        DB_USER=$(echo $DB_INFO | awk '{print $1}')
        DB_PASS=$(echo $DB_INFO | awk '{print $2}')
        DB_HOST=$(echo $DB_INFO | awk '{print $3}')
        DB_PORT=$(echo $DB_INFO | awk '{print $4}')
        DB_NAME=$(echo $DB_INFO | awk '{print $5}')
        
        PGPASSWORD=$DB_PASS pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME > $BACKUP_FILE 2>/dev/null
        gzip $BACKUP_FILE
        
        log_success "Sauvegarde créée: ${BACKUP_FILE}.gz"
        
        # Garder seulement les 10 dernières sauvegardes
        cd $BACKUP_DIR
        ls -t backup_*.sql.gz 2>/dev/null | tail -n +11 | xargs -r rm
    else
        log_warning "DATABASE_URL non trouvé, sauvegarde ignorée"
    fi
}

# Mise à jour du code
update_code() {
    log_info "Mise à jour du code depuis Git..."
    cd $APP_DIR
    
    # Vérifier si c'est un dépôt Git
    if [ -d ".git" ]; then
        # Sauvegarder les modifications locales
        git stash push -m "Auto-stash avant mise à jour $(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
        
        # Récupérer les dernières modifications
        git pull origin main
        
        log_success "Code mis à jour"
    else
        log_warning "Pas de dépôt Git trouvé. Mettez à jour le code manuellement."
    fi
}

# Mise à jour des dépendances Python
update_dependencies() {
    log_info "Mise à jour des dépendances Python..."
    cd $APP_DIR
    
    # Vérifier que le venv existe
    if [ ! -d "$VENV_DIR" ]; then
        log_error "Environnement virtuel non trouvé à $VENV_DIR"
        exit 1
    fi
    
    # Activer le venv et installer les dépendances
    source $VENV_DIR/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    
    log_success "Dépendances mises à jour"
}

# Redémarrer l'application
restart_services() {
    log_info "Redémarrage de l'application..."
    
    systemctl restart $SERVICE_NAME
    
    # Attendre que le service démarre
    sleep 2
    
    # Vérifier le statut
    if systemctl is-active --quiet $SERVICE_NAME; then
        log_success "Application redémarrée avec succès"
    else
        log_error "Échec du redémarrage de l'application"
        log_info "Vérifiez les logs: journalctl -u $SERVICE_NAME -n 50"
        exit 1
    fi
    
    # Redémarrer nginx si nécessaire
    if systemctl is-active --quiet nginx; then
        systemctl reload nginx
        log_success "Nginx rechargé"
    fi
}

# Vérifier les permissions
fix_permissions() {
    log_info "Vérification des permissions..."
    cd $APP_DIR
    
    # S'assurer que www-data possède les fichiers
    chown -R www-data:www-data $APP_DIR
    chmod -R 755 $APP_DIR
    
    # Permissions spéciales pour les uploads
    if [ -d "$APP_DIR/static/uploads" ]; then
        chmod -R 775 $APP_DIR/static/uploads
    fi
    
    log_success "Permissions vérifiées"
}

# Afficher le statut
show_status() {
    log_info "Statut de l'application:"
    systemctl status $SERVICE_NAME --no-pager -l
}

# Afficher les logs
show_logs() {
    log_info "Derniers logs de l'application:"
    journalctl -u $SERVICE_NAME -n 30 --no-pager
}

# Mise à jour complète
full_update() {
    log_info "=== MISE À JOUR COMPLÈTE DE L'APPLICATION ==="
    
    check_root
    check_app_dir
    
    # 1. Sauvegarde
    backup_database
    
    # 2. Mise à jour du code
    update_code
    
    # 3. Mise à jour des dépendances
    update_dependencies
    
    # 4. Permissions
    fix_permissions
    
    # 5. Redémarrage
    restart_services
    
    log_success "=== MISE À JOUR TERMINÉE AVEC SUCCÈS ==="
    log_info "Votre site est à jour et en ligne !"
}

# Mise à jour rapide (sans backup)
quick_update() {
    log_info "=== MISE À JOUR RAPIDE ==="
    
    check_root
    check_app_dir
    
    update_code
    update_dependencies
    fix_permissions
    restart_services
    
    log_success "=== MISE À JOUR RAPIDE TERMINÉE ==="
}

# Redémarrage simple
restart_only() {
    log_info "=== REDÉMARRAGE DE L'APPLICATION ==="
    
    check_root
    restart_services
    
    log_success "=== REDÉMARRAGE TERMINÉ ==="
}

# Aide
show_help() {
    cat << EOF
========================================
Script de Mise à Jour VPS
Villa à Vendre Marrakech
========================================

Usage: sudo $0 [OPTION]

Options:
  (aucune)      Mise à jour complète (avec backup DB)
  --quick       Mise à jour rapide (sans backup DB)
  --restart     Redémarrage uniquement
  --status      Afficher le statut de l'application
  --logs        Afficher les derniers logs
  --help        Afficher cette aide

Exemples:
  sudo $0                    # Mise à jour complète
  sudo $0 --quick            # Mise à jour rapide
  sudo $0 --restart          # Redémarrer l'application
  sudo $0 --status           # Voir le statut
  sudo $0 --logs             # Voir les logs

Remarques:
  - Le script doit être exécuté avec sudo
  - Une sauvegarde automatique de la DB est créée (sauf avec --quick)
  - Les 10 dernières sauvegardes sont conservées
  - Le code Git local est automatiquement sauvegardé avant pull

EOF
}

# Menu principal
case "${1:-}" in
    --quick)
        quick_update
        ;;
    --restart)
        restart_only
        ;;
    --status)
        check_root
        show_status
        ;;
    --logs)
        check_root
        show_logs
        ;;
    --help|-h)
        show_help
        ;;
    "")
        full_update
        ;;
    *)
        log_error "Option invalide: $1"
        show_help
        exit 1
        ;;
esac
