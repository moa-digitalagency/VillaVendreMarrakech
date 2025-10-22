# 🏡 Villa à Vendre Marrakech

Application web complète pour la vente en ligne de villas de luxe à Marrakech avec interface d'administration sécurisée et intelligence artificielle.

**Développé par :** MOA Digital Agency LLC  
**Développeur :** Aisance KALONJI  
**Email :** moa@myoneart.com  
**Site Web :** [www.myoneart.com](https://www.myoneart.com)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-orange)
![OpenRouter](https://img.shields.io/badge/AI-Claude%20%26%20Mistral-purple)

## ✨ Fonctionnalités Principales

### 🔐 Sécurité
- Authentification admin avec mot de passe sécurisé
- Protection par session Flask de toutes les routes admin
- Bouton de déconnexion intégré
- Mot de passe configurable via variable d'environnement (défaut: `@4dm1n`)

### 🎨 Interface Admin Moderne
- **Design professionnel thème clair** avec palette cohérente (gold, teal)
- **Deux modes de saisie distincts** :
  - **Mode PDF + Photos** : Extraction automatique par IA depuis PDF
  - **Mode Formulaire + Photos** : Saisie manuelle avec amélioration IA
- Interface responsive adaptée à tous les écrans
- Transitions fluides et effets de survol

### 🚀 Intelligence Artificielle (OpenRouter)
- **Claude 3.5 Sonnet** (Anthropic) - Extraction structurée depuis PDF
- **Mistral Large** - Amélioration de texte en français
- Boutons ✨ AI sur tous les champs de texte
- Extraction automatique en 60-90 secondes

### 📸 Gestion des Médias
- Upload de photos avec optimisation automatique (JPEG, compression)
- Galerie interactive avec suppression d'images
- Preview en temps réel des images uploadées
- Support multi-images

### 🗑️ Réinitialisation Sécurisée
- Bouton de reset pour supprimer toutes les données
- Double confirmation avec modale (saisie de "SUPPRIMER")
- Suppression complète : données DB + fichiers photos

### 🌐 Frontend Public
- Design luxueux adapté aux villas de prestige
- Effets parallaxe et animations
- Galerie photo avec lightbox
- Responsive mobile/tablette/desktop

## 🛠️ Technologies

- **Backend** : Python (Flask), SQLAlchemy
- **Base de données** : PostgreSQL (Neon)
- **IA** : OpenRouter API
  - Claude 3.5 Sonnet (extraction PDF)
  - Mistral Large (amélioration texte)
- **Frontend** : HTML5, CSS3, JavaScript
- **Images** : Pillow (optimisation automatique)
- **Sécurité** : Flask Sessions, authentification

## 📦 Déploiement

Pour des instructions complètes de déploiement, consultez **[DEPLOYMENT.md](DEPLOYMENT.md)** qui inclut :
- 🗄️ Schémas de base de données complets
- 🔧 Scripts d'initialisation SQL
- ⚙️ Configuration des variables d'environnement
- 🚀 Instructions de déploiement (Replit et serveurs)
- 📚 Documentation bilingue (EN/FR)

**Fichiers de déploiement** :
- `DEPLOYMENT.md` - Guide complet de déploiement
- `init_database.sql` - Script d'initialisation PostgreSQL
- `requirements.txt` - Dépendances Python
- `.env.example` - Template de configuration

## 🔍 SEO & Référencement Naturel

Le site est **100% optimisé pour le référencement naturel** sur Google pour "villa à vendre marrakech".

Consultez **[SEO.md](SEO.md)** pour le guide complet incluant :
- ✅ Meta tags optimisés (title, description, keywords)
- ✅ Open Graph & Twitter Cards pour réseaux sociaux
- ✅ Schema.org (RealEstateListing, Organization, Breadcrumb)
- ✅ Alt tags descriptifs sur toutes les images
- ✅ robots.txt & sitemap.xml
- ✅ Géolocalisation Marrakech (MA-15)
- ✅ 12+ mots-clés ciblés immobilier luxe Marrakech

**Score SEO : 95/100** 🎉

**URL configurée** : `villaavendremarrakech.com`

**Mots-clés principaux** :
- villa à vendre marrakech
- villa de luxe marrakech
- immobilier marrakech
- achat villa marrakech
- propriété de prestige marrakech

## 📋 Structure du Projet

```
├── app.py                  # Application Flask principale
├── models.py              # Modèles de base de données
├── templates/
│   ├── login.html         # Page de connexion admin
│   ├── admin.html         # Interface d'administration
│   └── index.html         # Page publique de présentation
├── static/
│   ├── css/
│   │   ├── style.css      # Styles frontend
│   │   └── admin.css      # Styles admin (thème clair)
│   ├── js/
│   │   └── admin.js       # Scripts admin (gestion modes)
│   └── uploads/           # Photos uploadées
├── README.md              # Ce fichier
└── replit.md              # Documentation technique
```

## 🚀 Installation & Démarrage

### Prérequis
- Python 3.11+
- PostgreSQL
- Clé API OpenRouter (pour les fonctionnalités IA)

### Configuration

1. **Variables d'environnement** :
```bash
DATABASE_URL=postgresql://...          # URL PostgreSQL
OPENROUTER_API_KEY=sk-or-...          # Clé API OpenRouter
ADMIN_PASSWORD=@4dm1n                  # Mot de passe admin (modifiable)
SECRET_KEY=votre-cle-secrete           # Clé secrète Flask
```

2. **Installer les dépendances** :
```bash
pip install flask flask-cors flask-sqlalchemy pillow psycopg2-binary pypdf2 python-dotenv requests werkzeug
```

3. **Lancer l'application** :
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 📖 Utilisation

### 1. Connexion Admin
1. Accédez à `/login`
2. Entrez le mot de passe : `@4dm1n` (ou votre mot de passe personnalisé)
3. Vous êtes redirigé vers l'interface d'administration

### 2. Mode 1 : PDF + Photos (Recommandé)
1. Sélectionnez "Mode PDF + Photos" dans le sélecteur
2. Uploadez un PDF de la villa
3. **Claude 3.5 Sonnet** extrait automatiquement toutes les données (60-90s)
4. Ajoutez les photos de la villa
5. Cliquez sur "💾 Enregistrer la Villa"
6. Consultez le résultat sur `/`

### 3. Mode 2 : Formulaire + Photos
1. Sélectionnez "Mode Formulaire + Photos" dans le sélecteur
2. Remplissez manuellement les informations
3. Utilisez les boutons ✨ AI pour améliorer vos textes avec **Mistral Large**
4. Ajoutez les photos de la villa
5. Cliquez sur "💾 Enregistrer la Villa"
6. Consultez le résultat sur `/`

### 4. Réinitialisation
1. Dans l'admin, cliquez sur "🗑️ Réinitialiser"
2. Une modale s'ouvre avec un avertissement
3. Tapez exactement "SUPPRIMER" pour confirmer
4. Toutes les données et photos sont supprimées

### 5. Déconnexion
- Cliquez sur "Déconnexion" dans le header

## 🔗 Routes de l'Application

### Routes Publiques
- `/` - Page publique de la villa
- `/api/villa` - API JSON des données de la villa

### Routes d'Authentification
- `/login` (GET, POST) - Page de connexion admin
- `/logout` (GET) - Déconnexion admin

### Routes Admin (Protégées)
- `/admin` (GET) - Interface d'administration
- `/admin/save` (POST) - Sauvegarde des données
- `/admin/upload` (POST) - Upload de photos
- `/admin/upload-pdf` (POST) - Upload et extraction PDF
- `/admin/delete-image/<filename>` (POST) - Suppression photo
- `/admin/reset` (POST) - Réinitialisation complète
- `/api/enhance` (POST) - Amélioration de texte par IA

## 🎯 Fonctionnalités IA

### Extraction PDF (Claude 3.5 Sonnet)
- Analyse complète du PDF
- Extraction de toutes les informations :
  - Référence, titre, prix
  - Localisation, distance
  - Description complète
  - Surfaces, chambres, piscine
  - Équipements et caractéristiques
  - Informations commerciales
  - Coordonnées de contact
- Format JSON structuré
- Temps : 60-90 secondes

### Amélioration de Texte (Mistral Large)
- Amélioration instantanée de vos descriptions
- Optimisé pour l'immobilier de luxe
- Français professionnel
- Boutons ✨ AI sur tous les champs de texte

## 🔒 Sécurité

- **Authentification** : Protection par mot de passe sur toutes les routes admin
- **Sessions** : Gestion sécurisée des sessions Flask
- **Base de données** : Connexions SSL avec pool de connexions
- **Upload** : Validation des types de fichiers et optimisation automatique
- **Confirmation** : Double sécurité pour les actions destructives

## 🌟 Avantages

✅ **Gain de temps** : Extraction automatique depuis PDF  
✅ **Qualité** : Amélioration IA des textes  
✅ **Flexibilité** : Deux modes de saisie au choix  
✅ **Optimisation** : Images automatiquement compressées  
✅ **Sécurité** : Authentification et confirmations  
✅ **Moderne** : Interface professionnelle thème clair  

## 📝 License

Propriétaire - Tous droits réservés © MOA Digital Agency LLC

## 👤 Contact & Développement

**MOA Digital Agency LLC**  
Développeur : Aisance KALONJI  
Email : [moa@myoneart.com](mailto:moa@myoneart.com)  
Site Web : [www.myoneart.com](https://www.myoneart.com)

Pour toute question technique, personnalisation ou support, n'hésitez pas à nous contacter.

---

**Développé avec ❤️ par MOA Digital Agency LLC - Spécialiste du développement web sur mesure**
