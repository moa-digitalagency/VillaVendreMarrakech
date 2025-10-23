#!/bin/bash

###############################################################################
# Script de Mise à Jour VPS - Villa à Vendre Marrakech
# 
# Script robuste pour mettre à jour une application déjà en production
# Gère la mise à jour du code, des dépendances et redémarre les services
# Avec gestion complète des erreurs et rollback automatique
#
# Usage:
#   ./update_vps.sh              # Mise à jour complète
#   ./update_vps.sh --quick      # Mise à jour rapide (sans backup)
#   ./update_vps.sh --restart    # Redémarrage uniquement
#   ./update_vps.sh --rollback   # Annuler la dernière mise à jour
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
SERVICE_NAME="${SERVICE_NAME:-villaeden.service}"
BACKUP_DIR="$APP_DIR/backups"
ROLLBACK_TAG=""
UPDATE_FAILED=0

# Fonctions utilitaires
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# Fonction de nettoyage en cas d'erreur
cleanup_on_error() {
    if [ $UPDATE_FAILED -eq 1 ] && [ -n "$ROLLBACK_TAG" ]; then
        log_error "Mise à jour échouée. Tentative de rollback..."
        rollback_update
    fi
}

trap cleanup_on_error EXIT

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
        ROLLBACK_TAG="rollback_$(date +%Y%m%d_%H%M%S)"
        git tag -f "$ROLLBACK_TAG" 2>/dev/null || true
        log_success "Point de restauration créé: $ROLLBACK_TAG"
    else
        log_warning "Pas de dépôt Git, création d'un backup fichier..."
        mkdir -p "$BACKUP_DIR/code"
        BACKUP_FILE="$BACKUP_DIR/code/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar -czf "$BACKUP_FILE" \
            --exclude='venv' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='node_modules' \
            --exclude='backups' \
            . 2>/dev/null || true
        log_success "Backup créé: $BACKUP_FILE"
    fi
}

# Rollback en cas d'erreur
rollback_update() {
    log_warning "=== ROLLBACK EN COURS ==="
    
    cd "$APP_DIR" || return 1
    
    if [ -d ".git" ] && [ -n "$ROLLBACK_TAG" ]; then
        log_info "Retour au commit précédent..."
        git reset --hard "$ROLLBACK_TAG" 2>/dev/null || {
            log_error "Impossible de restaurer le code"
            return 1
        }
        git tag -d "$ROLLBACK_TAG" 2>/dev/null || true
    fi
    
    # Redémarrer les services
    restart_services
    
    log_success "Rollback effectué"
}

# Sauvegarde de la base de données
backup_database() {
    log_info "Sauvegarde de la base de données..."
    
    mkdir -p "$BACKUP_DIR/database"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/database/backup_$TIMESTAMP.sql"
    
    # Charger les variables d'environnement
    if [ -f "$APP_DIR/.env" ]; then
        set -a
        source "$APP_DIR/.env"
        set +a
    fi
    
    # Extraction des infos depuis DATABASE_URL
    if [ -n "$DATABASE_URL" ]; then
        # Parser l'URL PostgreSQL
        if [[ $DATABASE_URL =~ postgresql://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+) ]]; then
            DB_USER="${BASH_REMATCH[1]}"
            DB_PASS="${BASH_REMATCH[2]}"
            DB_HOST="${BASH_REMATCH[3]}"
            DB_PORT="${BASH_REMATCH[4]}"
            DB_NAME="${BASH_REMATCH[5]}"
            
            # Essayer de faire le backup
            if command -v pg_dump &> /dev/null; then
                PGPASSWORD="$DB_PASS" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE" 2>/dev/null && {
                    gzip "$BACKUP_FILE"
                    log_success "Sauvegarde DB créée: ${BACKUP_FILE}.gz"
                    
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
        git stash push -m "Auto-stash avant mise à jour $(date +%Y%m%d_%H%M%S)" 2>/dev/null || {
            log_warning "Impossible de sauvegarder les modifications locales"
        }
    fi
    
    # Récupérer les dernières modifications
    log_info "Récupération des mises à jour depuis GitHub..."
    
    # Vérifier la branche actuelle
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    
    # Essayer de pull
    if git pull origin "$CURRENT_BRANCH" 2>&1 | tee /tmp/git_pull.log; then
        log_success "Code mis à jour depuis la branche $CURRENT_BRANCH"
        
        # Vérifier s'il y a eu des changements
        if grep -q "Already up to date" /tmp/git_pull.log; then
            log_info "Le code était déjà à jour"
        fi
    else
        log_error "Échec de la mise à jour Git"
        
        # Vérifier s'il y a des conflits
        if git status | grep -q "both modified"; then
            log_error "Conflits Git détectés. Résolvez-les manuellement."
            log_info "Fichiers en conflit:"
            git diff --name-only --diff-filter=U
            UPDATE_FAILED=1
            return 1
        fi
        
        # Tenter une récupération
        log_info "Tentative de récupération..."
        git fetch origin "$CURRENT_BRANCH" && \
        git reset --hard "origin/$CURRENT_BRANCH" && {
            log_warning "Reset forcé effectué. Modifications locales perdues."
        } || {
            log_error "Impossible de mettre à jour le code"
            UPDATE_FAILED=1
            return 1
        }
    fi
    
    rm -f /tmp/git_pull.log
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
            UPDATE_FAILED=1
            return 1
        }
    fi
    
    # Activer le venv et installer les dépendances
    log_info "Installation des dépendances..."
    source "$VENV_DIR/bin/activate" || {
        log_error "Impossible d'activer l'environnement virtuel"
        UPDATE_FAILED=1
        return 1
    }
    
    # Mettre à jour pip
    pip install --upgrade pip --quiet 2>/dev/null || true
    
    # Installer les dépendances avec retry
    for i in 1 2 3; do
        if pip install -r requirements.txt --quiet 2>&1 | tee /tmp/pip_install.log; then
            log_success "Dépendances mises à jour"
            rm -f /tmp/pip_install.log
            return 0
        else
            log_warning "Tentative $i/3 échouée"
            sleep 2
        fi
    done
    
    log_error "Échec de l'installation des dépendances"
    if [ -f /tmp/pip_install.log ]; then
        log_info "Dernières lignes d'erreur:"
        tail -20 /tmp/pip_install.log
        rm -f /tmp/pip_install.log
    fi
    UPDATE_FAILED=1
    return 1
}

# Redémarrer l'application selon l'environnement
restart_services() {
    log_info "Redémarrage de l'application..."
    
    case "$ENV_TYPE" in
        systemd)
            systemctl restart "$SERVICE_NAME" || {
                log_error "Échec du redémarrage de $SERVICE_NAME"
                UPDATE_FAILED=1
                return 1
            }
            sleep 3
            if systemctl is-active --quiet "$SERVICE_NAME"; then
                log_success "Service $SERVICE_NAME redémarré"
            else
                log_error "Le service ne démarre pas correctement"
                log_info "Logs du service:"
                journalctl -u "$SERVICE_NAME" -n 20 --no-pager
                UPDATE_FAILED=1
                return 1
            fi
            
            # Recharger nginx si présent
            if systemctl is-active --quiet nginx 2>/dev/null; then
                systemctl reload nginx && log_success "Nginx rechargé"
            fi
            ;;
            
        supervisor)
            supervisorctl restart villaeden || {
                log_error "Échec du redémarrage via Supervisor"
                UPDATE_FAILED=1
                return 1
            }
            sleep 2
            if supervisorctl status villaeden | grep -q RUNNING; then
                log_success "Application redémarrée via Supervisor"
            else
                log_error "L'application ne démarre pas"
                supervisorctl status villaeden
                UPDATE_FAILED=1
                return 1
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
        chown -R www-data:www-data "$APP_DIR" 2>/dev/null || true
        chmod -R 755 "$APP_DIR" 2>/dev/null || true
        
        # Permissions spéciales pour les uploads
        if [ -d "$APP_DIR/static/uploads" ]; then
            mkdir -p "$APP_DIR/static/uploads"
            chmod -R 775 "$APP_DIR/static/uploads"
            chown -R www-data:www-data "$APP_DIR/static/uploads"
        fi
        
        log_success "Permissions mises à jour"
    else
        log_info "Permissions non modifiées (environnement non-VPS)"
    fi
}

# Test de santé de l'application
health_check() {
    log_info "Vérification de la santé de l'application..."
    
    # Attendre un peu que l'app démarre
    sleep 3
    
    # Vérifier si l'app répond (si on a curl)
    if command -v curl &> /dev/null; then
        for i in {1..5}; do
            if curl -s -f http://localhost:5000 > /dev/null 2>&1; then
                log_success "L'application répond correctement"
                return 0
            fi
            log_info "Tentative $i/5..."
            sleep 2
        done
        log_warning "L'application ne répond pas sur le port 5000"
        log_info "Vérifiez manuellement que l'application fonctionne"
    else
        log_info "curl non disponible, test de santé ignoré"
    fi
}

# Afficher le statut
show_status() {
    log_info "=== STATUT DE L'APPLICATION ==="
    
    case "$ENV_TYPE" in
        systemd)
            systemctl status "$SERVICE_NAME" --no-pager -l
            ;;
        supervisor)
            supervisorctl status villaeden
            ;;
        *)
            log_info "Vérification manuelle requise"
            if [ -d ".git" ]; then
                echo "Branche Git: $(git rev-parse --abbrev-ref HEAD)"
                echo "Dernier commit: $(git log -1 --oneline)"
            fi
            ;;
    esac
}

# Afficher les logs
show_logs() {
    log_info "=== DERNIERS LOGS DE L'APPLICATION ==="
    
    case "$ENV_TYPE" in
        systemd)
            journalctl -u "$SERVICE_NAME" -n 50 --no-pager
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
    update_code || {
        log_error "Échec de la mise à jour du code"
        return 1
    }
    
    # Mise à jour des dépendances
    update_dependencies || {
        log_error "Échec de la mise à jour des dépendances"
        return 1
    }
    
    # Permissions
    fix_permissions
    
    # Redémarrage
    restart_services || {
        log_error "Échec du redémarrage"
        return 1
    }
    
    # Test de santé
    health_check
    
    echo ""
    log_success "╔════════════════════════════════════════╗"
    log_success "║  MISE À JOUR TERMINÉE AVEC SUCCÈS ✓    ║"
    log_success "╚════════════════════════════════════════╝"
    log_info "Votre site est à jour et en ligne !"
    
    # Tout s'est bien passé, pas de rollback nécessaire
    UPDATE_FAILED=0
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
    UPDATE_FAILED=0
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
  (aucune)      Mise à jour complète (avec backup DB)
  --quick       Mise à jour rapide (sans backup DB)
  --restart     Redémarrage uniquement
  --rollback    Annuler la dernière mise à jour
  --status      Afficher le statut de l'application
  --logs        Afficher les derniers logs
  --help        Afficher cette aide

Exemples:
  ./update_vps.sh                # Mise à jour complète
  sudo ./update_vps.sh           # Sur VPS (avec sudo)
  ./update_vps.sh --quick        # Mise à jour rapide
  ./update_vps.sh --restart      # Redémarrer l'application
  ./update_vps.sh --status       # Voir le statut
  ./update_vps.sh --logs         # Voir les logs
  ./update_vps.sh --rollback     # Annuler la MAJ

Workflow typique:
  1. git pull (ou le script le fait automatiquement)
  2. ./update_vps.sh
  3. Le script gère tout automatiquement !

Fonctionnalités:
  ✓ Détection automatique de l'environnement
  ✓ Sauvegarde automatique de la DB
  ✓ Point de restauration avant MAJ
  ✓ Rollback automatique en cas d'erreur
  ✓ Gestion des conflits Git
  ✓ Retry automatique pour pip
  ✓ Test de santé de l'application
  ✓ Support Replit, VPS, Supervisor

Remarques:
  - Sur VPS, utilisez sudo
  - Sur Replit, sudo n'est pas nécessaire
  - Le script détecte automatiquement l'environnement
  - Une sauvegarde automatique est créée avant MAJ
  - En cas d'erreur, rollback automatique

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
    --rollback)
        detect_environment
        check_permissions
        rollback_update
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
