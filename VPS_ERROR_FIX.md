# VPS Deployment Error Fix Guide

**Quick guide to fix common PostgreSQL errors during VPS deployment using automated scripts.**

---

## 🔴 Common Errors You May Encounter

### Error 1: `column villa.reference does not exist`
```
psycopg2.errors.UndefinedColumn: column villa.reference does not exist
LINE 2: FROM (SELECT villa.id AS villa_id, villa.reference AS villa...
```

### Error 2: `permission denied for schema public`
```
psycopg2.errors.InsufficientPrivilege: permission denied for schema public
LINE 2: CREATE TABLE IF NOT EXISTS villa (
```

### Error 3: `relation "villa" does not exist`
```
psycopg2.errors.UndefinedTable: relation "villa" does not exist
```

---

## ✅ Quick Fix (3 Steps)

### Step 1: Fix PostgreSQL Permissions

Run the automatic permission script:

```bash
sudo bash setup_postgres_permissions.sh
```

**What it does:**
- Creates PostgreSQL user `villa_user`
- Creates database `villa_sales`
- Grants ALL necessary permissions
- Fixes "permission denied" errors
- Tests connection automatically

**Expected output:**
```
✅ Utilisateur villa_user configuré
✅ Base de données villa_sales créée
✅ Permissions configurées avec succès
✅ Connexion réussie !
```

---

### Step 2: Fix Database Structure

Run the automatic database fix script:

```bash
cd /var/www/villaavendremarrakech
source venv/bin/activate
python fix_database.py
```

**What it does:**
- Creates `villa` table if missing
- Detects missing columns
- Adds all 23 required columns automatically
- Creates database triggers
- Creates performance indexes

**Expected output:**
```
🔗 Connexion à la base de données...
✅ Connexion établie avec succès

✅ La table villa existe
⚠️  Colonnes manquantes détectées: 5
✅ Ajouté: reference (VARCHAR(50))
✅ Ajouté: business_info (TEXT)
✅ Ajouté: documents (TEXT)
✅ Ajouté: pool_size (VARCHAR(50))
✅ Ajouté: is_active (BOOLEAN)

⚙️  Création des triggers...
✅ Triggers créés avec succès

🚀 Création des index...
✅ villa_created_at
✅ villa_price
✅ villa_location

📊 RÉSUMÉ DE LA BASE DE DONNÉES
Table: villa
Nombre de colonnes: 23
Nombre de villas: 0

✅ CORRECTION TERMINÉE AVEC SUCCÈS !
```

---

### Step 3: Start Application

```bash
python app.py
```

**Expected output:**
```
✅ Database tables initialized successfully
📊 Current villas in database: 0
 * Running on http://0.0.0.0:5000
```

---

## 🎯 Complete VPS Deployment Sequence

```bash
# 1. Install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# 2. Clone your project
cd /var/www
sudo git clone <your-repo-url> villaavendremarrakech
cd villaavendremarrakech

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
nano .env  # Edit with your values

# 5. FIX POSTGRES PERMISSIONS ⭐
sudo bash setup_postgres_permissions.sh

# 6. FIX DATABASE STRUCTURE ⭐
python fix_database.py

# 7. Test the application
python app.py

# If everything works, press Ctrl+C and continue with:
# - Gunicorn setup
# - Nginx configuration
# - SSL certificate
```

---

## 📋 Script Descriptions

### `setup_postgres_permissions.sh`

**Purpose:** Automatically configures PostgreSQL with correct permissions

**Usage:**
```bash
sudo bash setup_postgres_permissions.sh
```

**Fixes:**
- ✅ `permission denied for schema public`
- ✅ `permission denied for table villa`
- ✅ `must be owner of schema public`

**What it configures:**
- Creates user with CREATEDB privilege
- Creates database with correct owner
- Grants ALL PRIVILEGES on database
- Grants ALL PRIVILEGES on schema public
- Grants CREATE on schema public
- Sets user as schema owner
- Configures default privileges for future tables

---

### `fix_database.py`

**Purpose:** Automatically detects and fixes database structure issues

**Usage:**
```bash
source venv/bin/activate
python fix_database.py
```

**Fixes:**
- ✅ `column villa.reference does not exist`
- ✅ `column villa.business_info does not exist`
- ✅ `column villa.pool_size does not exist`
- ✅ `column villa.is_active does not exist`
- ✅ `relation "villa" does not exist`

**What it does:**
- Connects to PostgreSQL using PG* environment variables
- Checks if `villa` table exists (creates if missing)
- Compares existing columns with required columns
- Adds missing columns automatically
- Creates trigger for `updated_at` field
- Creates 5 performance indexes
- Shows detailed summary

**Safe to run multiple times:** Yes, it only adds what's missing

---

## 🔧 Troubleshooting

### Script not found
```bash
# Make sure you're in the project directory
cd /var/www/villaavendremarrakech

# Make scripts executable
chmod +x setup_postgres_permissions.sh
chmod +x fix_database.py
```

### Permission denied when running scripts
```bash
# setup_postgres_permissions.sh requires sudo
sudo bash setup_postgres_permissions.sh

# fix_database.py requires venv activation
source venv/bin/activate
python fix_database.py
```

### Connection failed
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if stopped
sudo systemctl start postgresql

# Check .env file has correct values
cat .env | grep PG
```

### Still getting errors after running scripts

1. Check environment variables are loaded:
```bash
source venv/bin/activate
python -c "import os; print(os.getenv('PGHOST'), os.getenv('PGDATABASE'))"
```

2. Test manual PostgreSQL connection:
```bash
psql -U villa_user -d villa_sales -h localhost
```

3. Re-run both scripts in order:
```bash
sudo bash setup_postgres_permissions.sh
python fix_database.py
```

---

## 📌 Quick Reference

**Fix permissions error:**
```bash
sudo bash setup_postgres_permissions.sh
```

**Fix column missing error:**
```bash
python fix_database.py
```

**Fix both (recommended order):**
```bash
sudo bash setup_postgres_permissions.sh
python fix_database.py
```

**Verify everything works:**
```bash
python app.py
```

---

## ✅ Success Indicators

After running the scripts, you should see:

1. ✅ No more `permission denied` errors
2. ✅ No more `column does not exist` errors  
3. ✅ No more `relation does not exist` errors
4. ✅ Application starts without crashes
5. ✅ Database has 23 columns
6. ✅ All triggers and indexes created

**Application startup message:**
```
✅ Database tables initialized successfully
📊 Current villas in database: 0
 * Running on http://0.0.0.0:5000
```

**Database fix script completion:**
```
✅ CORRECTION TERMINÉE AVEC SUCCÈS !
🚀 Vous pouvez maintenant lancer votre application
```

---

## 🚀 After Successful Fix

Once both scripts complete successfully, continue with production deployment:

1. Configure Gunicorn service
2. Setup Nginx reverse proxy  
3. Install SSL certificate with Let's Encrypt
4. Configure firewall
5. Enable auto-start on boot

**See full deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

**See quick VPS guide:** [VPS_QUICK_START.md](VPS_QUICK_START.md)

---

## 💡 Key Points

- **Always run `setup_postgres_permissions.sh` first** - Fixes permissions before creating tables
- **Then run `fix_database.py`** - Creates/fixes table structure
- **Both scripts are safe** - They only add what's missing, never delete data
- **Can be run multiple times** - Idempotent operations
- **No manual SQL needed** - Everything is automated

---

**These two scripts solve 99% of VPS deployment database errors. Run them before troubleshooting manually.**
