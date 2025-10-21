# Outils de Gestion de Base de Données

Ce projet inclut plusieurs outils pour initialiser et corriger la base de données PostgreSQL.

---

## 🔧 Option 1: Script Python Automatique (RECOMMANDÉ) ⭐

### `fix_database.py`

**Script intelligent** qui détecte et corrige automatiquement tous les problèmes de base de données.

### Utilisation

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le script
python fix_database.py
```

### Ce qu'il fait automatiquement

✅ **Connexion intelligente**
- Utilise DATABASE_URL si disponible
- Construit l'URL depuis les variables PG* sinon
- Affiche les informations de connexion

✅ **Vérification de la table**
- Vérifie si la table `villa` existe
- La crée si nécessaire avec toutes les colonnes

✅ **Détection des colonnes manquantes**
- Compare avec le modèle SQLAlchemy
- Liste toutes les colonnes manquantes
- Les ajoute automatiquement

✅ **Triggers et Index**
- Crée le trigger `update_updated_at_column()`
- Crée 5 index de performance

✅ **Rapport détaillé**
- Affiche le nombre de colonnes
- Liste toutes les colonnes présentes
- Compte les villas enregistrées

### Output attendu

```
🔗 Connexion à la base de données...
   Host: localhost
   Database: villa_sales

✅ Connexion établie avec succès

============================================================
🔧 SCRIPT DE CORRECTION DE BASE DE DONNÉES
   Villa à Vendre Marrakech
============================================================

✅ La table villa existe

⚠️  Colonnes manquantes détectées: 5
   business_info, documents, is_active, pool_size, reference

✅ Ajouté: business_info (TEXT)
✅ Ajouté: documents (TEXT)
✅ Ajouté: is_active (BOOLEAN)
✅ Ajouté: pool_size (VARCHAR(50))
✅ Ajouté: reference (VARCHAR(50))

⚙️  Création des triggers...
✅ Triggers créés avec succès

🚀 Création des index...
✅ villa_created_at
✅ villa_price
✅ villa_location

============================================================
📊 RÉSUMÉ DE LA BASE DE DONNÉES
============================================================
Table: villa
Nombre de colonnes: 23
Nombre de villas: 0

Colonnes présentes:
  • bedrooms
  • built_area
  • business_info
  • contact_email
  • contact_phone
  • contact_website
  • created_at
  • description
  • distance_city
  • documents
  • equipment
  • features
  • id
  • images
  • investment_benefits
  • is_active
  • location
  • pool_size
  • price
  • reference
  • terrain_area
  • title
  • updated_at
============================================================

✅ CORRECTION TERMINÉE AVEC SUCCÈS !
🚀 Vous pouvez maintenant lancer votre application:

   python app.py
   # ou
   gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### Quand l'utiliser ?

- ✅ **Premier déploiement VPS** (OBLIGATOIRE)
- ✅ Erreur `column villa.reference does not exist`
- ✅ Erreur `column does not exist` pour n'importe quelle colonne
- ✅ Après avoir modifié le modèle SQLAlchemy
- ✅ Migration d'une ancienne version

### Avantages

- 🚀 **Automatique** - Pas besoin de connaître SQL
- 🔍 **Intelligent** - Détecte les problèmes automatiquement
- 🛡️ **Sûr** - N'efface jamais les données existantes
- 📊 **Informatif** - Affiche un rapport détaillé
- ✅ **Idempotent** - Peut être exécuté plusieurs fois sans problème

---

## 📄 Option 2: Script SQL Manuel (pour référence)

### `init_database.sql`

Script SQL standard pour créer la base de données manuellement.

### Utilisation

```bash
# Méthode 1: Via psql
sudo -u postgres psql villa_sales < init_database.sql

# Méthode 2: Connexion interactive
sudo -u postgres psql
\c villa_sales
\i init_database.sql
```

### Contenu

- Création de la table `villa` avec 23 colonnes
- Fonction et trigger pour `updated_at`
- 5 index de performance
- Commentaires sur chaque colonne
- Exemple de données (commenté)

### Quand l'utiliser ?

- Si vous préférez SQL natif
- Pour documentation/référence
- Pour initialiser depuis un autre outil

### ⚠️ Limitations

- Ne détecte PAS les colonnes manquantes
- Ne corrige PAS une table existante incomplète
- Nécessite des connaissances SQL
- Moins flexible que le script Python

---

## 🗂️ Structure de la Table `villa`

### 23 Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Identifiant unique auto-incrémenté |
| `reference` | VARCHAR(50) | UNIQUE NOT NULL | Référence unique (ex: VILLA-2025-001) |
| `title` | VARCHAR(200) | NOT NULL | Titre de l'annonce |
| `price` | INTEGER | NOT NULL | Prix en MAD |
| `location` | VARCHAR(200) | NOT NULL | Localisation à Marrakech |
| `distance_city` | VARCHAR(100) | | Distance du centre-ville |
| `description` | TEXT | NOT NULL | Description détaillée |
| `terrain_area` | INTEGER | | Surface terrain en m² |
| `built_area` | INTEGER | | Surface construite en m² |
| `bedrooms` | INTEGER | | Nombre de chambres |
| `pool_size` | VARCHAR(50) | | Dimensions piscine |
| `features` | TEXT | | Caractéristiques |
| `equipment` | TEXT | | Équipements |
| `business_info` | TEXT | | Infos commerciales |
| `investment_benefits` | TEXT | | Avantages investissement |
| `documents` | TEXT | | Documents disponibles |
| `images` | TEXT | | JSON array des images |
| `contact_phone` | VARCHAR(50) | | Téléphone WhatsApp |
| `contact_email` | VARCHAR(100) | | Email de contact |
| `contact_website` | VARCHAR(200) | | Site web (optionnel) |
| `is_active` | BOOLEAN | DEFAULT TRUE | Villa active/visible |
| `created_at` | TIMESTAMP | DEFAULT NOW | Date création |
| `updated_at` | TIMESTAMP | DEFAULT NOW | Date modification |

### 5 Index de Performance

1. `idx_villa_created_at` - Tri par date de création
2. `idx_villa_price` - Filtrage par prix
3. `idx_villa_location` - Recherche par localisation
4. `idx_villa_is_active` - Filtrage actif/inactif
5. `idx_villa_reference` - Recherche rapide par référence

### 1 Trigger Automatique

- `update_villa_updated_at` - Met à jour `updated_at` avant chaque UPDATE

---

## 🆘 Résolution de Problèmes

### Erreur: `column villa.reference does not exist`

**Solution**: Lancez le script Python
```bash
python fix_database.py
```

### Erreur: `relation "villa" does not exist`

**Solution**: La table n'existe pas, lancez le script Python
```bash
python fix_database.py
```

### Erreur: `connection refused`

**Vérifications**:
1. PostgreSQL est-il démarré ?
   ```bash
   sudo systemctl status postgresql
   ```

2. Les identifiants dans `.env` sont-ils corrects ?
   ```bash
   cat .env | grep PG
   ```

3. Testez la connexion manuellement :
   ```bash
   psql -U villa_user -d villa_sales -h localhost
   ```

### Erreur: `permission denied`

**Solution**: Donnez les bonnes permissions
```bash
sudo chown -R $USER:www-data .
chmod 755 fix_database.py
```

---

## 📋 Checklist de Déploiement

- [ ] PostgreSQL installé et démarré
- [ ] Base de données `villa_sales` créée
- [ ] Utilisateur PostgreSQL `villa_user` créé
- [ ] Variables d'environnement configurées dans `.env`
- [ ] **Script `fix_database.py` exécuté avec succès** ⭐
- [ ] Répertoire `static/uploads` créé avec permissions
- [ ] Application testée avec `python app.py`
- [ ] Service systemd configuré (pour production)
- [ ] Nginx configuré (pour production)
- [ ] SSL/HTTPS activé (pour production)

---

## 🔗 Liens Utiles

- **Guide complet**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Guide rapide VPS**: [VPS_QUICK_START.md](VPS_QUICK_START.md)
- **Documentation technique**: [replit.md](replit.md)
- **Variables d'environnement**: [.env.example](.env.example)

---

**Recommandation**: Utilisez toujours `fix_database.py` pour garantir une base de données complète et correcte ! ✅
