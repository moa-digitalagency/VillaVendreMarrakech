# VPS Deployment Quick Start Guide

## 🚀 Quick Deploy for villaavendremarrakech.com

This guide will get your application running on a VPS in **15 minutes**.

### Prerequisites
- Ubuntu 20.04+ or Debian 11+ VPS
- Root access via SSH
- Domain name pointed to your VPS IP

---

## Step-by-Step Commands

### 1️⃣ Install System Dependencies (2 min)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

### 2️⃣ Setup PostgreSQL Database (1 min)
```bash
sudo -u postgres psql << EOF
CREATE DATABASE villa_sales;
CREATE USER villa_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE villa_sales TO villa_user;
\q
EOF
```

### 3️⃣ Clone and Setup Application (3 min)
```bash
# Create directory
sudo mkdir -p /var/www/villaavendremarrakech
cd /var/www/villaavendremarrakech

# Clone repository
sudo git clone https://github.com/your-username/villa-marrakech.git .

# Set permissions
sudo chown -R $USER:www-data .
chmod -R 755 .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create uploads directory
mkdir -p static/uploads
chmod 775 static/uploads
sudo chown -R $USER:www-data static/uploads
```

### 4️⃣ Configure Environment Variables (2 min)
```bash
cat > .env << 'EOF'
# Database (REQUIRED)
PGHOST=localhost
PGPORT=5432
PGUSER=villa_user
PGPASSWORD=CHANGE_THIS_PASSWORD
PGDATABASE=villa_sales

# Flask (REQUIRED)
SECRET_KEY=GENERATE_WITH_COMMAND_BELOW
FLASK_ENV=production
FLASK_DEBUG=0

# Admin (REQUIRED)
ADMIN_PASSWORD=CHANGE_THIS_TO_SECURE_PASSWORD

# OpenRouter API (REQUIRED for AI features)
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY_HERE
EOF

# Generate SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env.temp
# Copy the generated key to .env file
nano .env  # Edit and paste the SECRET_KEY
```

### 5️⃣ Fix/Initialize Database (1 min) ⭐ OBLIGATOIRE
```bash
source venv/bin/activate

# Lancer le script de correction de la base de données
python fix_database.py

# Output attendu:
# 🔗 Connexion à la base de données...
# ✅ Connexion établie avec succès
# ✅ La table villa existe (ou sera créée)
# ⚠️  Colonnes manquantes détectées: XX
# ✅ Ajouté: reference (VARCHAR(50))
# ✅ Ajouté: title (VARCHAR(200))
# ... (toutes les colonnes manquantes)
# ✅ Triggers créés avec succès
# 🚀 Création des index...
# ✅ CORRECTION TERMINÉE AVEC SUCCÈS !
```

**Ce script est OBLIGATOIRE** - Il crée/corrige automatiquement :
- La table `villa` si elle n'existe pas
- Toutes les colonnes manquantes
- Les triggers pour `updated_at`
- Les index pour la performance

### 6️⃣ Test Application (1 min)
```bash
# Test avec Flask dev server
python app.py

# You should see:
# ✅ Database tables initialized successfully
# 📊 Current villas in database: 0

# Press Ctrl+C to stop
```

### 7️⃣ Create Systemd Service (2 min)
```bash
sudo cat > /etc/systemd/system/villaavendremarrakech.service << 'EOF'
[Unit]
Description=Villa à Vendre Marrakech
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/villaavendremarrakech
Environment="PATH=/var/www/villaavendremarrakech/venv/bin"
EnvironmentFile=/var/www/villaavendremarrakech/.env
ExecStart=/var/www/villaavendremarrakech/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start villaavendremarrakech
sudo systemctl enable villaavendremarrakech
sudo systemctl status villaavendremarrakech
```

### 8️⃣ Configure Nginx (2 min)
```bash
sudo cat > /etc/nginx/sites-available/villaavendremarrakech << 'EOF'
server {
    listen 80;
    server_name villaavendremarrakech.com www.villaavendremarrakech.com;

    client_max_body_size 16M;

    location /static/ {
        alias /var/www/villaavendremarrakech/static/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/villaavendremarrakech /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9️⃣ Install SSL Certificate (2 min)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d villaavendremarrakech.com -d www.villaavendremarrakech.com

# Follow prompts and select option 2 (redirect HTTP to HTTPS)
```

### 🔟 Configure Firewall (1 min)
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

---

## ✅ Verification

```bash
# Check service
sudo systemctl status villaavendremarrakech

# Check logs
sudo journalctl -u villaavendremarrakech -n 50

# Test locally
curl http://localhost:8000/

# Test domain
curl https://villaavendremarrakech.com/
```

---

## 🎉 Access Your Site

- **Public page**: https://villaavendremarrakech.com/
- **Admin login**: https://villaavendremarrakech.com/login
- **Default password**: The one you set in ADMIN_PASSWORD

---

## 🔧 Common Commands

**Restart app:**
```bash
sudo systemctl restart villaavendremarrakech
```

**View logs:**
```bash
sudo journalctl -u villaavendremarrakech -f
```

**Update code:**
```bash
cd /var/www/villaavendremarrakech
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart villaavendremarrakech
```

**Database backup:**
```bash
sudo -u postgres pg_dump villa_sales > backup_$(date +%Y%m%d).sql
```

---

## 🆘 Troubleshooting

**Error: Database connection failed**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check credentials in .env file
cat .env | grep PG

# Test connection
sudo -u postgres psql -d villa_sales -c "SELECT 1;"
```

**Error: Permission denied on uploads**
```bash
sudo chown -R www-data:www-data /var/www/villaavendremarrakech/static/uploads
chmod 775 /var/www/villaavendremarrakech/static/uploads
```

**Error: Port 8000 already in use**
```bash
sudo systemctl stop villaavendremarrakech
sudo systemctl start villaavendremarrakech
```

---

## 📚 Full Documentation

For complete documentation, see [DEPLOYMENT.md](DEPLOYMENT.md)
