# Deployment Guide / Guide de Déploiement

## 🇬🇧 English Version

### Overview
This is a Flask-based luxury villa sales platform for Marrakech with AI-powered features, PostgreSQL database, and WhatsApp integration.

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- OpenRouter API key (for AI features)

### Database Schema

#### Table: `villa`
```sql
CREATE TABLE villa (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    price DECIMAL(15, 2),
    location VARCHAR(200),
    area DECIMAL(10, 2),
    land_area DECIMAL(10, 2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT,
    features TEXT,
    equipment TEXT,
    investment_benefits TEXT,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_website VARCHAR(200),
    images TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_villa_updated_at 
    BEFORE UPDATE ON villa 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### Database Initialization Script

```sql
-- init_database.sql
-- Create database (if not exists)
-- Note: Run this as postgres superuser

CREATE DATABASE villa_sales;

\c villa_sales

-- Create villa table
CREATE TABLE IF NOT EXISTS villa (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    price DECIMAL(15, 2),
    location VARCHAR(200),
    area DECIMAL(10, 2),
    land_area DECIMAL(10, 2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT,
    features TEXT,
    equipment TEXT,
    investment_benefits TEXT,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_website VARCHAR(200),
    images TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create update trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_villa_updated_at 
    BEFORE UPDATE ON villa 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create uploads directory (handled by application)
-- Ensure static/uploads/ directory exists with write permissions

-- Default admin credentials
-- Username: admin
-- Default Password: @4dm1n (change this in production!)
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/villa_sales
PGHOST=localhost
PGPORT=5432
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGDATABASE=villa_sales

# Flask Configuration
SECRET_KEY=your-very-secret-random-key-change-this-in-production
FLASK_ENV=production
FLASK_DEBUG=0

# Admin Authentication
ADMIN_PASSWORD=@4dm1n

# OpenRouter API (for AI features)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Application Settings
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd villa-sales-platform
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create uploads directory**
```bash
mkdir -p static/uploads
chmod 755 static/uploads
```

5. **Initialize database**
```bash
# Option 1: Using psql
psql -U postgres -f init_database.sql

# Option 2: Using Python (automatic on first run)
python app.py
```

6. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
nano .env
```

7. **Run the application**
```bash
# Development
python app.py

# Production with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Production Deployment (VPS - Ubuntu/Debian)

#### Prerequisites
- Ubuntu 20.04+ or Debian 11+ VPS
- Root or sudo access
- Domain name pointed to your VPS IP (e.g., villaavendremarrakech.com)

#### Step-by-Step VPS Deployment

**1. Update system and install dependencies**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

**2. Create PostgreSQL database and user**
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL console:
CREATE DATABASE villa_sales;
CREATE USER villa_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE villa_sales TO villa_user;
\q
```

**3. Clone and setup application**
```bash
# Create app directory
sudo mkdir -p /var/www/villaavendremarrakech
cd /var/www/villaavendremarrakech

# Clone your repository
sudo git clone <your-repo-url> .

# Set permissions
sudo chown -R $USER:www-data /var/www/villaavendremarrakech
chmod -R 755 /var/www/villaavendremarrakech

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**4. Create uploads directory**
```bash
mkdir -p static/uploads
chmod 775 static/uploads
sudo chown -R $USER:www-data static/uploads
```

**5. Configure environment variables**
```bash
# Create .env file
nano .env
```

Add the following content (replace with your values):
```env
# Database Configuration (REQUIRED for VPS)
PGHOST=localhost
PGPORT=5432
PGUSER=villa_user
PGPASSWORD=your_secure_password_here
PGDATABASE=villa_sales

# Flask Configuration (REQUIRED)
SECRET_KEY=generate_with_python_secrets_token_hex_32
FLASK_ENV=production
FLASK_DEBUG=0

# Admin Authentication (REQUIRED)
ADMIN_PASSWORD=your_secure_admin_password

# OpenRouter API (REQUIRED for AI features)
OPENROUTER_API_KEY=your_openrouter_api_key

# Application Settings (Optional)
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**6. Fix/Initialize the database** ⭐ IMPORTANT
```bash
# Activate virtual environment
source venv/bin/activate

# Run the database fix script (ajoute toutes les colonnes manquantes)
python fix_database.py

# You should see:
# 🔗 Connexion à la base de données...
# ✅ Connexion établie avec succès
# ✅ La table villa existe
# ⚠️  Colonnes manquantes détectées: X
# ✅ Ajouté: reference (VARCHAR(50))
# ✅ Ajouté: title (VARCHAR(200))
# ... (toutes les colonnes)
# ✅ Triggers créés avec succès
# 🚀 Création des index...
# ✅ CORRECTION TERMINÉE AVEC SUCCÈS !
```

**Note**: Ce script est **OBLIGATOIRE** lors du premier déploiement. Il :
- Crée la table `villa` si elle n'existe pas
- Ajoute toutes les colonnes manquantes
- Crée les triggers pour `updated_at`
- Crée les index pour optimiser les performances

**7. Test the application**
```bash
# Test avec Flask dev server
python app.py

# You should see:
# ✅ Database tables initialized successfully
# 📊 Current villas in database: 0
```

Press `Ctrl+C` to stop.

**8. Create systemd service for auto-start**
```bash
sudo nano /etc/systemd/system/villaavendremarrakech.service
```

Add this content:
```ini
[Unit]
Description=Villa à Vendre Marrakech - Flask Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/villaavendremarrakech
Environment="PATH=/var/www/villaavendremarrakech/venv/bin"
EnvironmentFile=/var/www/villaavendremarrakech/.env
ExecStart=/var/www/villaavendremarrakech/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile - app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**9. Start and enable the service**
```bash
sudo systemctl daemon-reload
sudo systemctl start villaavendremarrakech
sudo systemctl enable villaavendremarrakech
sudo systemctl status villaavendremarrakech
```

**10. Configure Nginx reverse proxy**
```bash
sudo nano /etc/nginx/sites-available/villaavendremarrakech
```

Add this content:
```nginx
server {
    listen 80;
    server_name villaavendremarrakech.com www.villaavendremarrakech.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logs
    access_log /var/log/nginx/villaavendremarrakech_access.log;
    error_log /var/log/nginx/villaavendremarrakech_error.log;

    # Max upload size (16MB)
    client_max_body_size 16M;

    # Static files
    location /static/ {
        alias /var/www/villaavendremarrakech/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Flask app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }
}
```

**Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/villaavendremarrakech /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**11. Install SSL certificate (HTTPS) with Let's Encrypt**
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d villaavendremarrakech.com -d www.villaavendremarrakech.com

# Follow prompts and select option 2 (redirect HTTP to HTTPS)
```

**12. Configure firewall**
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

**13. Verify deployment**
```bash
# Check service status
sudo systemctl status villaavendremarrakech

# Check logs
sudo journalctl -u villaavendremarrakech -f

# Test locally
curl http://localhost:8000/

# Test domain
curl https://villaavendremarrakech.com/
```

**Access your application:**
- Public page: `https://villaavendremarrakech.com/`
- Admin login: `https://villaavendremarrakech.com/login`

#### VPS Maintenance Commands

**Restart application:**
```bash
sudo systemctl restart villaavendremarrakech
```

**View logs:**
```bash
# Application logs
sudo journalctl -u villaavendremarrakech -n 100 -f

# Nginx access logs
sudo tail -f /var/log/nginx/villaavendremarrakech_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/villaavendremarrakech_error.log
```

**Update application:**
```bash
cd /var/www/villaavendremarrakech
source venv/bin/activate
git pull
pip install -r requirements.txt
sudo systemctl restart villaavendremarrakech
```

**Database backup:**
```bash
# Backup
sudo -u postgres pg_dump villa_sales > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
sudo -u postgres psql villa_sales < backup_20251021_120000.sql
```

### Production Deployment (Replit)

1. **Set environment secrets** in Replit:
   - `DATABASE_URL` - Provided automatically by Replit PostgreSQL
   - `OPENROUTER_API_KEY` - Your OpenRouter API key
   - `ADMIN_PASSWORD` - Your custom admin password
   - `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

2. **Database setup**:
   - Replit automatically creates PostgreSQL database
   - Tables are created automatically on first run
   - No manual initialization needed

3. **Run configuration**:
   - Default workflow: `python app.py`
   - Server binds to `0.0.0.0:5000`

4. **Access**:
   - Public page: `https://your-repl-url.repl.co/`
   - Admin login: `https://your-repl-url.repl.co/login`

### Security Recommendations

1. **Change default admin password**
   - Set strong password via `ADMIN_PASSWORD` environment variable

2. **Use strong SECRET_KEY**
   - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`

3. **HTTPS only in production**
   - Replit provides HTTPS by default

4. **Database backups**
   - Regular automated backups recommended
   - Replit provides checkpoint/rollback features

5. **API key security**
   - Never commit API keys to repository
   - Use environment variables only

### Troubleshooting

**Database connection issues:**
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL
```

**Upload permission errors:**
```bash
# Fix upload directory permissions
chmod 755 static/uploads
```

**Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

---

## 🇫🇷 Version Française

### Vue d'ensemble
Plateforme de vente de villas de luxe à Marrakech basée sur Flask avec fonctionnalités IA, base de données PostgreSQL et intégration WhatsApp.

### Prérequis
- Python 3.8+
- PostgreSQL 12+
- Clé API OpenRouter (pour les fonctionnalités IA)

### Schéma de Base de Données

#### Table : `villa`
```sql
CREATE TABLE villa (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    price DECIMAL(15, 2),
    location VARCHAR(200),
    area DECIMAL(10, 2),
    land_area DECIMAL(10, 2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT,
    features TEXT,
    equipment TEXT,
    investment_benefits TEXT,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_website VARCHAR(200),
    images TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer le trigger de mise à jour pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_villa_updated_at 
    BEFORE UPDATE ON villa 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### Script d'Initialisation de la Base de Données

```sql
-- init_database.sql
-- Créer la base de données (si elle n'existe pas)
-- Note : Exécuter en tant que superutilisateur postgres

CREATE DATABASE villa_sales;

\c villa_sales

-- Créer la table villa
CREATE TABLE IF NOT EXISTS villa (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    price DECIMAL(15, 2),
    location VARCHAR(200),
    area DECIMAL(10, 2),
    land_area DECIMAL(10, 2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT,
    features TEXT,
    equipment TEXT,
    investment_benefits TEXT,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_website VARCHAR(200),
    images TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer le trigger de mise à jour
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_villa_updated_at 
    BEFORE UPDATE ON villa 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Créer le répertoire uploads (géré par l'application)
-- S'assurer que le répertoire static/uploads/ existe avec permissions d'écriture

-- Identifiants admin par défaut
-- Nom d'utilisateur : admin
-- Mot de passe par défaut : @4dm1n (à changer en production !)
```

### Variables d'Environnement

Créer un fichier `.env` dans le répertoire racine :

```env
# Configuration Base de Données
DATABASE_URL=postgresql://username:password@localhost:5432/villa_sales
PGHOST=localhost
PGPORT=5432
PGUSER=votre_utilisateur_db
PGPASSWORD=votre_mot_de_passe_db
PGDATABASE=villa_sales

# Configuration Flask
SECRET_KEY=votre-cle-secrete-aleatoire-a-changer-en-production
FLASK_ENV=production
FLASK_DEBUG=0

# Authentification Admin
ADMIN_PASSWORD=@4dm1n

# API OpenRouter (pour fonctionnalités IA)
OPENROUTER_API_KEY=votre_cle_api_openrouter_ici

# Paramètres Application
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Étapes d'Installation

1. **Cloner le dépôt**
```bash
git clone <url-du-depot>
cd villa-sales-platform
```

2. **Créer l'environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Créer le répertoire uploads**
```bash
mkdir -p static/uploads
chmod 755 static/uploads
```

5. **Initialiser la base de données**
```bash
# Option 1 : Utiliser psql
psql -U postgres -f init_database.sql

# Option 2 : Utiliser Python (automatique au premier lancement)
python app.py
```

6. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos valeurs réelles
nano .env
```

7. **Lancer l'application**
```bash
# Développement
python app.py

# Production avec Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Déploiement en Production (Replit)

1. **Définir les secrets d'environnement** dans Replit :
   - `DATABASE_URL` - Fourni automatiquement par PostgreSQL Replit
   - `OPENROUTER_API_KEY` - Votre clé API OpenRouter
   - `ADMIN_PASSWORD` - Votre mot de passe admin personnalisé
   - `SECRET_KEY` - Générer avec : `python -c "import secrets; print(secrets.token_hex(32))"`

2. **Configuration de la base de données** :
   - Replit crée automatiquement la base PostgreSQL
   - Les tables sont créées automatiquement au premier lancement
   - Aucune initialisation manuelle nécessaire

3. **Configuration d'exécution** :
   - Workflow par défaut : `python app.py`
   - Le serveur écoute sur `0.0.0.0:5000`

4. **Accès** :
   - Page publique : `https://votre-url-repl.repl.co/`
   - Connexion admin : `https://votre-url-repl.repl.co/login`

### Recommandations de Sécurité

1. **Changer le mot de passe admin par défaut**
   - Définir un mot de passe fort via la variable `ADMIN_PASSWORD`

2. **Utiliser une SECRET_KEY forte**
   - Générer : `python -c "import secrets; print(secrets.token_hex(32))"`

3. **HTTPS uniquement en production**
   - Replit fournit HTTPS par défaut

4. **Sauvegardes de base de données**
   - Sauvegardes automatiques régulières recommandées
   - Replit fournit des fonctionnalités de checkpoint/rollback

5. **Sécurité des clés API**
   - Ne jamais commiter les clés API dans le dépôt
   - Utiliser uniquement les variables d'environnement

### Dépannage

**Problèmes de connexion à la base de données :**
```bash
# Vérifier que PostgreSQL fonctionne
pg_isready

# Vérifier la chaîne de connexion
echo $DATABASE_URL
```

**Erreurs de permissions d'upload :**
```bash
# Corriger les permissions du répertoire uploads
chmod 755 static/uploads
```

**Dépendances manquantes :**
```bash
pip install -r requirements.txt --upgrade
```

---

## API Endpoints Documentation

### Public Endpoints

#### `GET /`
- **Description**: Main villa display page
- **Response**: HTML page with villa details
- **Authentication**: None

#### `GET /api/villa`
- **Description**: Get villa data in JSON format
- **Response**: 
```json
{
  "title": "Villa Title",
  "price": 5000000.00,
  "location": "Marrakech",
  "area": 450.0,
  "land_area": 800.0,
  "bedrooms": 5,
  "bathrooms": 4,
  "description": "...",
  "features": "...",
  "equipment": "...",
  "investment_benefits": "...",
  "contact_phone": "+212 6 80 76 03 52",
  "contact_email": "contact@example.com",
  "images": ["img1.jpg", "img2.jpg"]
}
```

### Admin Endpoints (Authentication Required)

#### `GET /login`
- **Description**: Admin login page
- **Response**: HTML login form

#### `POST /login`
- **Description**: Authenticate admin
- **Parameters**: `password` (form data)
- **Response**: Redirect to `/admin` on success

#### `GET /logout`
- **Description**: Logout admin
- **Response**: Redirect to `/login`

#### `GET /admin`
- **Description**: Admin dashboard
- **Response**: HTML admin interface
- **Authentication**: Session required

#### `POST /admin/save`
- **Description**: Save villa data
- **Parameters**: All villa fields (form data)
- **Response**: JSON success/error message

#### `POST /admin/upload`
- **Description**: Upload villa photos
- **Parameters**: `photos[]` (multipart/form-data)
- **Response**: JSON with uploaded filenames

#### `POST /admin/upload-pdf`
- **Description**: Upload PDF and extract data using AI
- **Parameters**: `pdf` (multipart/form-data)
- **Response**: JSON with extracted villa data

#### `DELETE /admin/delete-image/<filename>`
- **Description**: Delete uploaded image
- **Response**: JSON success/error message

#### `POST /admin/reset`
- **Description**: Reset all villa data and images
- **Response**: JSON success message

#### `POST /api/enhance`
- **Description**: AI text enhancement
- **Parameters**: `text` (JSON)
- **Response**: JSON with enhanced text

---

## Database Field Descriptions

| Field | Type | Description (EN) | Description (FR) |
|-------|------|------------------|------------------|
| `id` | Integer | Primary key | Clé primaire |
| `title` | String(200) | Villa title | Titre de la villa |
| `price` | Decimal(15,2) | Price in MAD | Prix en MAD |
| `location` | String(200) | Location/Address | Localisation/Adresse |
| `area` | Decimal(10,2) | Living area in m² | Surface habitable en m² |
| `land_area` | Decimal(10,2) | Land area in m² | Surface terrain en m² |
| `bedrooms` | Integer | Number of bedrooms | Nombre de chambres |
| `bathrooms` | Integer | Number of bathrooms | Nombre de salles de bain |
| `description` | Text | Full description | Description complète |
| `features` | Text | Features list (newline-separated) | Liste caractéristiques (séparées par retour ligne) |
| `equipment` | Text | Equipment list | Liste équipements |
| `investment_benefits` | Text | Investment benefits | Avantages investissement |
| `contact_phone` | String(50) | Contact phone number | Numéro de téléphone |
| `contact_email` | String(100) | Contact email | Email de contact |
| `contact_website` | String(200) | Contact website | Site web de contact |
| `images` | Text | Comma-separated image filenames | Noms fichiers images (séparés par virgule) |
| `created_at` | Timestamp | Creation timestamp | Date de création |
| `updated_at` | Timestamp | Last update timestamp | Date dernière modification |

---

## Dependencies / Dépendances

```txt
flask>=2.3.0
flask-cors>=4.0.0
flask-sqlalchemy>=3.0.0
pillow>=10.0.0
psycopg2-binary>=2.9.0
pypdf2>=3.0.0
python-dotenv>=1.0.0
requests>=2.31.0
werkzeug>=2.3.0
gunicorn>=21.0.0
```

---

## Support

For issues or questions:
- Email: support@example.com
- Documentation: This file

Pour des problèmes ou questions :
- Email : support@example.com
- Documentation : Ce fichier
