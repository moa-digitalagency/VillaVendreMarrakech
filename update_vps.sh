#!/bin/bash

###############################################################################
# Script de Mise à Jour VPS - Villa à Vendre Marrakech
# 
# Script robuste pour mettre à jour une application déjà en production
# Gère la mise à jour du code, des dépendances et redémarre les services
#
# Usage:
#   ./update_vps.sh              # Mise à jour complète
#   ./update_vps.sh --quick      # Mise à jour rapide (sans backup)
#   ./update_vps.sh --no-restart # Mise à jour sans redémarrage
#
# Développé par: MOA Digital Agency LLC
###############################################################################

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variables globales
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-$SCRIPT_DIR}"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="$APP_DIR/backups"
DETECTED_SERVICE=""

# Fonctions utilitaires
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# Détecter le service systemd automatiquement
detect_systemd_service() {
    if ! command -v systemctl &> /dev/null; then
        return 1
    fi
    
    # Chercher les services possibles dans l'ordre de priorité
    local possible_services=(
        "villaeden.service"
        "villamarrakech.service"
        "villa.service"
        "gunicorn.service"
        "flask.service"
    )
    
    for service in "${possible_services[@]}"; do
        if systemctl list-unit-files | grep -q "^$service"; then
            DETECTED_SERVICE="$service"
            log_info "Service détecté: $service"
            return 0
        fi
    done
    
    # Chercher tous les services liés à python/flask/gunicorn
    local found_service=$(systemctl list-units --type=service --all | grep -iE "(villa|flask|gunicorn|python)" | head -1 | awk '{print $1}')
    if [ -n "$found_service" ]; then
        DETECTED_SERVICE="$found_service"
        log_info "Service détecté: $found_service"
        return 0
    fi
    
    log_warning "Aucun service systemd trouvé pour l'application"
    return 1
}

# Détecter le type d'environnement
detect_environment() {
    if [ -n "$REPL_ID" ]; then
        log_info "Environnement Replit détecté"
        export ENV_TYPE="replit"
        export NEEDS_SUDO=false
    elif command -v systemctl &> /dev/null; then
        log_info "Environnement VPS avec systemd détecté"
        export ENV_TYPE="systemd"
        export NEEDS_SUDO=true
        detect_systemd_service
    elif command -v supervisorctl &> /dev/null; then
        log_info "Environnement avec Supervisor détecté"
        export ENV_TYPE="supervisor"
        export NEEDS_SUDO=true
    else
        log_info "Environnement standard détecté"
        export ENV_TYPE="standard"
        export NEEDS_SUDO=false
    fi
}

# Vérifier si on a besoin d'être root
check_permissions() {
    if [ "$NEEDS_SUDO" = true ] && [ $EUID -ne 0 ]; then
        log_error "Ce script doit être exécuté avec sudo sur cet environnement"
        log_info "Utilisez: sudo $0 $@"
        exit 1
    fi
}

# Vérifier que le répertoire existe
check_app_dir() {
    if [ ! -d "$APP_DIR" ]; then
        log_error "Répertoire $APP_DIR non trouvé"
        exit 1
    fi
    log_success "Répertoire application: $APP_DIR"
}

# Créer un tag de rollback
create_rollback_point() {
    log_info "Création d'un point de restauration..."
    
    cd "$APP_DIR" || return 1
    
    if [ -d ".git" ]; then
        # Sauvegarder le commit actuel
        local rollback_tag="rollback_$(date +%Y%m%d_%H%M%S)"
        git tag -f "$rollback_tag" 2>/dev/null || true
        log_success "Point de restauration Git créé: $rollback_tag"
    fi
}

# Sauvegarde de la base de données
backup_database() {
    log_info "Sauvegarde de la base de données..."
    
    mkdir -p "$BACKUP_DIR/database"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/database/backup_$timestamp.sql"
    
    # Charger les variables d'environnement
    if [ -f "$APP_DIR/.env" ]; then
        set -a
        source "$APP_DIR/.env" 2>/dev/null || true
        set +a
    fi
    
    # Extraction des infos depuis DATABASE_URL
    if [ -n "$DATABASE_URL" ]; then
        # Parser l'URL PostgreSQL
        if [[ $DATABASE_URL =~ postgresql://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+) ]]; then
            local db_user="${BASH_REMATCH[1]}"
            local db_pass="${BASH_REMATCH[2]}"
            local db_host="${BASH_REMATCH[3]}"
            local db_port="${BASH_REMATCH[4]}"
            local db_name="${BASH_REMATCH[5]}"
            
            # Essayer de faire le backup
            if command -v pg_dump &> /dev/null; then
                PGPASSWORD="$db_pass" pg_dump -h "$db_host" -p "$db_port" -U "$db_user" "$db_name" > "$backup_file" 2>/dev/null && {
                    gzip "$backup_file"
                    log_success "Sauvegarde DB créée: ${backup_file}.gz"
                    
                    # Garder seulement les 10 dernières sauvegardes
                    cd "$BACKUP_DIR/database" 2>/dev/null && {
                        ls -t backup_*.sql.gz 2>/dev/null | tail -n +11 | xargs -r rm -f
                    }
                } || log_warning "Échec de la sauvegarde DB (non bloquant)"
            else
                log_warning "pg_dump non disponible, sauvegarde DB ignorée"
            fi
        else
            log_warning "Format DATABASE_URL non reconnu"
        fi
    else
        log_warning "DATABASE_URL non trouvé, sauvegarde DB ignorée"
    fi
}

# Mise à jour du code depuis Git
update_code() {
    log_info "Mise à jour du code depuis Git..."
    cd "$APP_DIR" || return 1
    
    # Vérifier si c'est un dépôt Git
    if [ ! -d ".git" ]; then
        log_warning "Pas de dépôt Git trouvé. Mise à jour du code ignorée."
        return 0
    fi
    
    # Sauvegarder les modifications locales
    if ! git diff --quiet || ! git diff --staged --quiet; then
        log_info "Sauvegarde des modifications locales..."
        git stash push -m "Auto-stash avant mise à jour $(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
    fi
    
    # Récupérer les dernières modifications
    log_info "Récupération des mises à jour depuis GitHub..."
    
    # Vérifier la branche actuelle
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    
    # Essayer de pull
    if git pull origin "$current_branch" 2>&1; then
        log_success "Code mis à jour depuis la branche $current_branch"
    else
        log_warning "Échec du pull Git, tentative de récupération..."
        git fetch origin "$current_branch" && \
        git reset --hard "origin/$current_branch" && {
            log_success "Code mis à jour via reset (modifications locales perdues)"
        } || {
            log_error "Impossible de mettre à jour le code"
            return 1
        }
    fi
}

# Détecter et installer les dépendances Python
update_dependencies() {
    log_info "Mise à jour des dépendances Python..."
    cd "$APP_DIR" || return 1
    
    # Vérifier qu'il y a un requirements.txt
    if [ ! -f "requirements.txt" ]; then
        log_warning "requirements.txt non trouvé, étape ignorée"
        return 0
    fi
    
    # Créer ou activer le venv
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Création de l'environnement virtuel..."
        python3 -m venv "$VENV_DIR" || {
            log_error "Impossible de créer l'environnement virtuel"
            return 1
        }
    fi
    
    # Activer le venv et installer les dépendances
    log_info "Installation des dépendances..."
    source "$VENV_DIR/bin/activate" || {
        log_error "Impossible d'activer l'environnement virtuel"
        return 1
    }
    
    # Mettre à jour pip silencieusement
    pip install --upgrade pip --quiet 2>/dev/null || true
    
    # Installer les dépendances avec retry
    local max_attempts=3
    for i in $(seq 1 $max_attempts); do
        if pip install -r requirements.txt --quiet 2>&1; then
            log_success "Dépendances mises à jour"
            return 0
        else
            if [ $i -lt $max_attempts ]; then
                log_warning "Tentative $i/$max_attempts échouée, nouvelle tentative..."
                sleep 2
            fi
        fi
    done
    
    log_error "Échec de l'installation des dépendances après $max_attempts tentatives"
    return 1
}

# Redémarrer l'application selon l'environnement
restart_services() {
    log_info "Redémarrage de l'application..."
    
    case "$ENV_TYPE" in
        systemd)
            if [ -z "$DETECTED_SERVICE" ]; then
                log_warning "Aucun service systemd détecté"
                log_info "Vous devrez redémarrer l'application manuellement"
                log_info "Ou créez un fichier de service dans /etc/systemd/system/"
                return 0
            fi
            
            log_info "Redémarrage du service $DETECTED_SERVICE..."
            if systemctl restart "$DETECTED_SERVICE" 2>&1; then
                sleep 3
                if systemctl is-active --quiet "$DETECTED_SERVICE"; then
                    log_success "Service $DETECTED_SERVICE redémarré avec succès"
                else
                    log_warning "Le service a redémarré mais n'est pas actif"
                    log_info "Vérifiez les logs: journalctl -u $DETECTED_SERVICE -n 30"
                fi
            else
                log_warning "Échec du redémarrage du service"
                log_info "Vérifiez: systemctl status $DETECTED_SERVICE"
            fi
            
            # Recharger nginx si présent
            if systemctl is-active --quiet nginx 2>/dev/null; then
                systemctl reload nginx 2>/dev/null && log_success "Nginx rechargé"
            fi
            ;;
            
        supervisor)
            if supervisorctl restart villaeden 2>&1; then
                sleep 2
                log_success "Application redémarrée via Supervisor"
            else
                log_warning "Vérifiez: supervisorctl status"
            fi
            ;;
            
        replit)
            log_info "Environnement Replit: redémarrage manuel requis"
            log_warning "Utilisez le bouton 'Stop' puis 'Run' dans Replit"
            ;;
            
        *)
            log_warning "Type d'environnement non reconnu"
            log_info "Redémarrez l'application manuellement"
            ;;
    esac
}

# Vérifier les permissions des fichiers
fix_permissions() {
    log_info "Vérification des permissions..."
    cd "$APP_DIR" || return 1
    
    if [ "$ENV_TYPE" = "systemd" ] && [ $EUID -eq 0 ]; then
        # Assurer que www-data possède les fichiers
        if id -u www-data &>/dev/null; then
            chown -R www-data:www-data "$APP_DIR" 2>/dev/null || true
            chmod -R 755 "$APP_DIR" 2>/dev/null || true
            
            # Permissions spéciales pour les uploads
            if [ -d "$APP_DIR/static/uploads" ]; then
                mkdir -p "$APP_DIR/static/uploads"
                chmod -R 775 "$APP_DIR/static/uploads"
                chown -R www-data:www-data "$APP_DIR/static/uploads"
            fi
            
            log_success "Permissions mises à jour (propriétaire: www-data)"
        else
            log_warning "Utilisateur www-data non trouvé, permissions non modifiées"
        fi
    else
        log_info "Permissions non modifiées (environnement non-VPS ou sans root)"
    fi
}

# Test de santé de l'application
health_check() {
    log_info "Test de santé de l'application..."
    
    # Attendre un peu que l'app démarre
    sleep 3
    
    # Vérifier si l'app répond
    if command -v curl &> /dev/null; then
        for i in {1..5}; do
            if curl -s -f http://localhost:5000 > /dev/null 2>&1 || \
               curl -s -f http://127.0.0.1:5000 > /dev/null 2>&1; then
                log_success "L'application répond correctement ✓"
                return 0
            fi
            log_info "Tentative $i/5..."
            sleep 2
        done
        log_warning "L'application ne répond pas sur le port 5000"
        log_info "Vérifiez manuellement que l'application fonctionne"
    else
        log_info "Test de santé ignoré (curl non disponible)"
    fi
}

# Afficher le statut
show_status() {
    log_info "=== STATUT DE L'APPLICATION ==="
    
    case "$ENV_TYPE" in
        systemd)
            if [ -n "$DETECTED_SERVICE" ]; then
                systemctl status "$DETECTED_SERVICE" --no-pager -l
            else
                log_warning "Aucun service détecté"
            fi
            ;;
        supervisor)
            supervisorctl status villaeden
            ;;
        *)
            log_info "Vérification manuelle requise"
            if [ -d ".git" ]; then
                echo "Branche Git: $(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
                echo "Dernier commit: $(git log -1 --oneline 2>/dev/null)"
            fi
            ;;
    esac
}

# Afficher les logs
show_logs() {
    log_info "=== DERNIERS LOGS DE L'APPLICATION ==="
    
    case "$ENV_TYPE" in
        systemd)
            if [ -n "$DETECTED_SERVICE" ]; then
                journalctl -u "$DETECTED_SERVICE" -n 50 --no-pager
            else
                log_warning "Aucun service détecté, impossible d'afficher les logs"
            fi
            ;;
        supervisor)
            supervisorctl tail -50 villaeden
            ;;
        *)
            log_warning "Logs non disponibles automatiquement"
            ;;
    esac
}

# Mise à jour complète
full_update() {
    log_info "╔════════════════════════════════════════╗"
    log_info "║  MISE À JOUR COMPLÈTE DE L'APPLICATION ║"
    log_info "╚════════════════════════════════════════╝"
    echo ""
    
    detect_environment
    check_permissions
    check_app_dir
    
    # Point de restauration
    create_rollback_point
    
    # Sauvegarde DB
    backup_database
    
    # Mise à jour du code
    if ! update_code; then
        log_error "Échec de la mise à jour du code"
        log_warning "Continuez en mode manuel ou corrigez les erreurs Git"
        exit 1
    fi
    
    # Mise à jour des dépendances
    if ! update_dependencies; then
        log_error "Échec de la mise à jour des dépendances"
        log_warning "Vérifiez requirements.txt et l'environnement virtuel"
        exit 1
    fi
    
    # Permissions
    fix_permissions
    
    # Redémarrage
    restart_services
    
    # Test de santé
    health_check
    
    echo ""
    log_success "╔════════════════════════════════════════╗"
    log_success "║  MISE À JOUR TERMINÉE AVEC SUCCÈS ✓    ║"
    log_success "╚════════════════════════════════════════╝"
    log_info "Votre site est à jour !"
}

# Mise à jour rapide (sans backup)
quick_update() {
    log_info "=== MISE À JOUR RAPIDE ==="
    
    detect_environment
    check_permissions
    check_app_dir
    
    create_rollback_point
    update_code
    update_dependencies
    fix_permissions
    restart_services
    health_check
    
    log_success "=== MISE À JOUR RAPIDE TERMINÉE ==="
}

# Mise à jour sans redémarrage
update_no_restart() {
    log_info "=== MISE À JOUR SANS REDÉMARRAGE ==="
    
    detect_environment
    check_permissions
    check_app_dir
    
    create_rollback_point
    backup_database
    update_code
    update_dependencies
    fix_permissions
    
    log_success "=== MISE À JOUR TERMINÉE (sans redémarrage) ==="
    log_warning "N'oubliez pas de redémarrer l'application manuellement !"
}

# Redémarrage simple
restart_only() {
    log_info "=== REDÉMARRAGE DE L'APPLICATION ==="
    
    detect_environment
    check_permissions
    restart_services
    health_check
    
    log_success "=== REDÉMARRAGE TERMINÉ ==="
}

# Aide
show_help() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════╗
║        Script de Mise à Jour VPS                       ║
║        Villa à Vendre Marrakech                        ║
╚════════════════════════════════════════════════════════╝

Usage: ./update_vps.sh [OPTION]

Options:
  (aucune)        Mise à jour complète (avec backup DB)
  --quick         Mise à jour rapide (sans backup DB)
  --no-restart    Mise à jour sans redémarrage automatique
  --restart       Redémarrage uniquement
  --status        Afficher le statut de l'application
  --logs          Afficher les derniers logs
  --help          Afficher cette aide

Exemples:
  ./update_vps.sh                # Mise à jour complète
  sudo ./update_vps.sh           # Sur VPS (avec sudo)
  ./update_vps.sh --quick        # Mise à jour rapide
  ./update_vps.sh --no-restart   # MAJ sans redémarrer
  ./update_vps.sh --restart      # Redémarrer seulement
  ./update_vps.sh --status       # Voir le statut
  ./update_vps.sh --logs         # Voir les logs

Workflow typique:
  1. cd /chemin/vers/VillaVendreMarrakech
  2. sudo ./update_vps.sh
  3. C'est tout ! Le script gère automatiquement:
     ✓ Backup de la base de données
     ✓ git pull depuis GitHub
     ✓ Installation des dépendances Python
     ✓ Redémarrage de l'application
     ✓ Test de santé

Fonctionnalités:
  ✓ Détection automatique de l'environnement
  ✓ Détection automatique du service systemd
  ✓ Sauvegarde automatique de la DB
  ✓ Gestion des conflits Git
  ✓ Retry automatique pour pip
  ✓ Test de santé de l'application
  ✓ Support Replit, VPS, Supervisor

Remarques:
  - Sur VPS, utilisez sudo
  - Sur Replit, sudo n'est pas nécessaire
  - Le script détecte automatiquement l'environnement
  - Une sauvegarde automatique est créée avant MAJ
  - Si aucun service systemd n'est trouvé, le script
    continue mais vous devrez redémarrer manuellement

EOF
}

# Menu principal
case "${1:-}" in
    --quick)
        quick_update
        ;;
    --no-restart)
        update_no_restart
        ;;
    --restart)
        restart_only
        ;;
    --status)
        detect_environment
        check_permissions
        show_status
        ;;
    --logs)
        detect_environment
        check_permissions
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

exit 0
