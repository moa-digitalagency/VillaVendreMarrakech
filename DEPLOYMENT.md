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
