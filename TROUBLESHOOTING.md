# Guide de Dépannage - Villa à Vendre Marrakech

Ce guide résout les erreurs courantes lors du déploiement VPS.

---

## 🔴 Erreur: `column villa.reference does not exist`

### Symptôme
```
psycopg2.errors.UndefinedColumn: column villa.reference does not exist
LINE 2: FROM (SELECT villa.id AS villa_id, villa.reference AS villa...
```

### Cause
La table `villa` existe mais n'a pas toutes les colonnes (migration incomplète depuis une ancienne version).

### Solution ⭐
```bash
cd /var/www/villaavendremarrakech
source venv/bin/activate
python fix_database.py
```

Le script détecte et ajoute automatiquement les 5 colonnes manquantes :
- `reference`
- `business_info`
- `documents`
- `pool_size`
- `is_active`

---

## 🔴 Erreur: `permission denied for schema public`

### Symptôme
```
psycopg2.errors.InsufficientPrivilege: permission denied for schema public
LINE 2: CREATE TABLE IF NOT EXISTS villa (
```

### Cause
L'utilisateur PostgreSQL n'a pas les permissions nécessaires pour créer des tables dans le schéma public.

### Solution A: Script automatique (RECOMMANDÉ) ⭐
```bash
sudo bash setup_postgres_permissions.sh
```

### Solution B: Commandes manuelles
```bash
sudo -u postgres psql << EOF
\c villa_sales
GRANT ALL PRIVILEGES ON SCHEMA public TO villa_user;
GRANT CREATE ON SCHEMA public TO villa_user;
ALTER SCHEMA public OWNER TO villa_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO villa_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO villa_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO villa_user;
\q
EOF
```

Puis relancez :
```bash
python fix_database.py
```

---

## 🔴 Erreur: `relation "villa" does not exist`

### Symptôme
```
psycopg2.errors.UndefinedTable: relation "villa" does not exist
```

### Cause
La table `villa` n'a jamais été créée.

### Solution
```bash
source venv/bin/activate
python fix_database.py
```

Le script crée automatiquement la table avec toutes les colonnes.

---

## 🔴 Erreur: `FATAL: password authentication failed`

### Symptôme
```
psycopg2.OperationalError: FATAL: password authentication failed for user "villa_user"
```

### Cause
Identifiants PostgreSQL incorrects dans `.env`.

### Solution
1. Vérifiez votre fichier `.env` :
```bash
cat .env | grep PG
```

2. Testez la connexion manuellement :
```bash
psql -U villa_user -d villa_sales -h localhost
```

3. Si le mot de passe est incorrect, réinitialisez-le :
```bash
sudo -u postgres psql << EOF
ALTER USER villa_user WITH PASSWORD 'nouveau_mot_de_passe';
\q
EOF
```

4. Mettez à jour `.env` avec le nouveau mot de passe.

---

## 🔴 Erreur: `could not connect to server`

### Symptôme
```
psycopg2.OperationalError: could not connect to server: Connection refused
```

### Cause
PostgreSQL n'est pas démarré ou n'écoute pas sur le bon port.

### Solution
```bash
# Vérifier le statut
sudo systemctl status postgresql

# Démarrer PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Vérifier que PostgreSQL écoute
sudo netstat -plnt | grep 5432
```

---

## 🔴 Erreur: `App crashes on startup`

### Symptôme
L'application Flask crash immédiatement après le démarrage.

### Solution
1. **Vérifiez les logs** :
```bash
sudo journalctl -u villaavendremarrakech -n 100 --no-pager
```

2. **Vérifiez que toutes les colonnes existent** :
```bash
source venv/bin/activate
python fix_database.py
```

3. **Testez manuellement** :
```bash
python app.py
```

4. **Vérifiez les variables d'environnement** :
```bash
cat .env
```

Variables requises :
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`
- `SECRET_KEY`
- `ADMIN_PASSWORD`
- `OPENROUTER_API_KEY`

---

## 🔴 Erreur: `ModuleNotFoundError`

### Symptôme
```
ModuleNotFoundError: No module named 'flask'
```

### Cause
Les dépendances Python ne sont pas installées.

### Solution
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔴 Erreur: `Port 8000 already in use`

### Symptôme
```
OSError: [Errno 98] Address already in use
```

### Cause
Un autre processus utilise déjà le port 8000.

### Solution
```bash
# Trouver le processus
sudo lsof -i :8000

# Tuer le processus
sudo kill -9 <PID>

# Ou redémarrer le service
sudo systemctl restart villaavendremarrakech
```

---

## 🔴 Erreur: `500 Internal Server Error`

### Symptôme
Page blanche ou erreur 500 dans le navigateur.

### Solution
1. **Consultez les logs Nginx** :
```bash
sudo tail -f /var/log/nginx/villaavendremarrakech_error.log
```

2. **Consultez les logs de l'application** :
```bash
sudo journalctl -u villaavendremarrakech -f
```

3. **Vérifiez que Gunicorn fonctionne** :
```bash
sudo systemctl status villaavendremarrakech
```

4. **Testez localement** :
```bash
curl http://localhost:8000/
```

---

## 🔴 Erreur: `Static files not loading`

### Symptôme
CSS/JS/Images ne se chargent pas (erreurs 404).

### Cause
Permissions incorrectes ou configuration Nginx incorrecte.

### Solution
```bash
# Vérifier les permissions
ls -la static/

# Corriger les permissions
sudo chown -R www-data:www-data static/
chmod -R 755 static/

# Redémarrer Nginx
sudo systemctl restart nginx
```

---

## 🔴 Erreur: `Upload failed`

### Symptôme
Impossible d'uploader des photos.

### Cause
Permissions incorrectes sur le dossier `static/uploads`.

### Solution
```bash
# Créer le dossier
mkdir -p static/uploads

# Donner les bonnes permissions
sudo chown -R www-data:www-data static/uploads
chmod 775 static/uploads

# Vérifier
ls -la static/
```

---

## 🔴 Erreur: `SSL certificate error`

### Symptôme
Erreur SSL lors de l'accès HTTPS.

### Cause
Certificat Let's Encrypt expiré ou mal configuré.

### Solution
```bash
# Renouveler le certificat
sudo certbot renew

# Tester le renouvellement
sudo certbot renew --dry-run

# Redémarrer Nginx
sudo systemctl restart nginx
```

---

## 📋 Checklist de Démarrage Rapide

Si rien ne fonctionne, suivez cette checklist dans l'ordre :

1. ✅ **PostgreSQL fonctionne** ?
   ```bash
   sudo systemctl status postgresql
   ```

2. ✅ **Base de données créée** ?
   ```bash
   sudo -u postgres psql -l | grep villa_sales
   ```

3. ✅ **Permissions configurées** ?
   ```bash
   sudo bash setup_postgres_permissions.sh
   ```

4. ✅ **Table et colonnes créées** ?
   ```bash
   python fix_database.py
   ```

5. ✅ **Variables d'environnement configurées** ?
   ```bash
   cat .env
   ```

6. ✅ **Dépendances Python installées** ?
   ```bash
   source venv/bin/activate && pip list
   ```

7. ✅ **Application démarre** ?
   ```bash
   python app.py
   ```

8. ✅ **Service systemd fonctionne** ?
   ```bash
   sudo systemctl status villaavendremarrakech
   ```

9. ✅ **Nginx configuré** ?
   ```bash
   sudo nginx -t
   ```

10. ✅ **Firewall autorise le trafic** ?
    ```bash
    sudo ufw status
    ```

---

## 🆘 Commandes de Debug Utiles

### Tester la connexion PostgreSQL
```bash
PGPASSWORD=your_password psql -U villa_user -d villa_sales -h localhost -c "SELECT 1;"
```

### Lister les tables
```bash
PGPASSWORD=your_password psql -U villa_user -d villa_sales -h localhost -c "\dt"
```

### Voir les colonnes de la table villa
```bash
PGPASSWORD=your_password psql -U villa_user -d villa_sales -h localhost -c "\d villa"
```

### Compter les villas
```bash
PGPASSWORD=your_password psql -U villa_user -d villa_sales -h localhost -c "SELECT COUNT(*) FROM villa;"
```

### Voir toutes les permissions
```bash
sudo -u postgres psql -d villa_sales -c "\z"
```

---

## 📞 Besoin d'Aide ?

Si le problème persiste après avoir suivi ce guide :

1. **Vérifiez les logs détaillés** :
   ```bash
   sudo journalctl -u villaavendremarrakech -n 200 --no-pager
   ```

2. **Partagez les informations** suivantes :
   - Message d'erreur complet
   - Output de `python fix_database.py`
   - Output de `sudo systemctl status villaavendremarrakech`
   - Contenu de `.env` (SANS les mots de passe)

---

**La plupart des erreurs sont résolues par :**
```bash
sudo bash setup_postgres_permissions.sh
python fix_database.py
sudo systemctl restart villaavendremarrakech
```
