# 🏡 Villa à Vendre Marrakech

Application web complète pour la vente en ligne de villas de luxe à Marrakech avec support bilingue complet et intelligence artificielle.

**Développé par :** MOA Digital Agency LLC  
**Développeur :** Aisance KALONJI  
**Email :** moa@myoneart.com  
**Site Web :** [www.myoneart.com](https://www.myoneart.com)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-orange)
![Version](https://img.shields.io/badge/Version-2.0.0-purple)

## ✨ Nouveautés Version 2.0.0

### 🌍 Support Bilingue Complet
- **Tous les textes modifiables** depuis le panneau d'administration
- **Interface d'édition dédiée** pour personnaliser chaque section du site
- **24 nouveaux champs bilingues** (FR/EN) pour une personnalisation totale
- **Détection automatique** de la langue du navigateur

### ✏️ Édition Facile
- Section Héro (sous-titre, bouton contact)
- Section Description (titre, bouton WhatsApp)
- Section "Pourquoi Choisir" (titre + 4 cartes personnalisables)
- Section Contact (titre, sous-titre)

📘 **Guide complet** : Consultez `GUIDE_TEXTES_PERSONNALISABLES.md`

## 🚀 Déploiement & Mise à Jour

### Sur Replit
✅ Déjà configuré - Cliquez simplement sur "Run" !

### Sur VPS (En Production)

#### Mise à jour de l'application
```bash
# Mise à jour complète (recommandé)
sudo ./update_vps.sh

# Mise à jour rapide (sans backup DB)
sudo ./update_vps.sh --quick

# Redémarrage uniquement
sudo ./update_vps.sh --restart

# Afficher le statut
sudo ./update_vps.sh --status

# Voir les logs
sudo ./update_vps.sh --logs
```

Le script `update_vps.sh` gère automatiquement :
- ✅ Sauvegarde automatique de la base de données
- ✅ Mise à jour du code depuis Git
- ✅ Installation des dépendances Python
- ✅ Vérification et correction des permissions
- ✅ Redémarrage des services

## 🎨 Fonctionnalités Principales

### 🔐 Interface Admin Sécurisée
- Connexion par mot de passe
- **Deux modes de saisie** :
  - **PDF + Photos** : Extraction IA automatique (Claude 3.5 Sonnet)
  - **Formulaire Bilingue** : Saisie manuelle avec amélioration IA (Mistral Large)
- **Édition des textes du site** : Personnalisez tous les textes en FR/EN
- Gestion complète des photos avec optimisation automatique

### 🌐 Site Public Ultra-Moderne
- Design luxueux responsive
- Slider automatique en page d'accueil
- Galerie photos avec lightbox
- Support bilingue FR/EN automatique
- Intégration WhatsApp directe
- SEO optimisé (Score 95/100)

### 🤖 Intelligence Artificielle
- **Claude 3.5 Sonnet** : Extraction structurée de données PDF
- **Mistral Large** : Amélioration de texte en français
- Traitement en 60-90 secondes

## 📖 Utilisation

### 1. Connexion Admin
1. Accédez à `/login`
2. Entrez votre mot de passe administrateur
3. Vous êtes redirigé vers le panneau d'administration

### 2. Ajouter une Villa

#### Option A : Mode PDF + Photos (Recommandé)
1. Uploadez le PDF de la villa
2. L'IA extrait automatiquement toutes les informations
3. Ajoutez les photos
4. Enregistrez

#### Option B : Mode Formulaire Bilingue
1. Remplissez les informations en français et anglais
2. Utilisez les boutons ✨ AI pour améliorer les textes
3. Ajoutez les photos
4. Enregistrez

### 3. Personnaliser le Site
1. Cliquez sur "**Éditer le site**" dans le menu admin
2. Modifiez tous les textes en français et anglais :
   - Sous-titres et boutons
   - Titres de sections
   - Descriptions des 4 cartes "Pourquoi Choisir"
   - Textes de contact
3. Enregistrez vos modifications
4. Les changements sont immédiatement visibles sur le site public

## 🔧 Configuration

### Variables d'Environnement

Créez un fichier `.env` avec :

```bash
# Base de données PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/villaeden

# Clé secrète pour les sessions Flask
SESSION_SECRET=votre-cle-secrete-aleatoire-forte

# Mot de passe administrateur
ADMIN_PASSWORD=votre-mot-de-passe-admin

# Clé API OpenRouter pour IA (optionnel)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
```

## 📂 Structure du Projet

```
.
├── app.py                              # Application Flask principale
├── main.py                             # Point d'entrée
├── models.py                           # Modèles de base de données
├── requirements.txt                    # Dépendances Python
├── update_vps.sh                       # Script de mise à jour VPS
├── static/
│   ├── css/
│   │   ├── admin.css                   # Styles admin
│   │   └── style.css                   # Styles frontend
│   ├── js/
│   │   └── admin.js                    # Scripts admin
│   └── uploads/                        # Photos uploadées
├── templates/
│   ├── admin.html                      # Interface admin principale
│   ├── edit_website.html               # Édition textes du site
│   ├── index.html                      # Page publique
│   └── login.html                      # Page de connexion
├── CHANGELOG.md                        # Historique des versions
├── GUIDE_TEXTES_PERSONNALISABLES.md   # Guide utilisateur
└── SEO.md                              # Guide SEO complet
```

## 🔒 Sécurité

- ✅ Authentification admin par mot de passe
- ✅ Protection par sessions Flask
- ✅ Variables d'environnement pour les secrets
- ✅ Validation stricte des uploads
- ✅ Optimisation automatique des images
- ✅ Double confirmation pour actions destructives

## 🌟 Technologies

- **Backend** : Flask, SQLAlchemy, PostgreSQL
- **Frontend** : HTML5, CSS3, JavaScript
- **IA** : OpenRouter (Claude 3.5, Mistral Large)
- **Déploiement** : Gunicorn, Nginx
- **Images** : Pillow (optimisation automatique)

## 🔄 Historique des Versions

### Version 2.0.0 (Actuelle)
- ✨ Tous les textes du site sont modifiables
- 🌍 Support bilingue complet (24 nouveaux champs)
- 📝 Interface d'édition dédiée
- 🔧 Script de mise à jour VPS simplifié
- 🐛 Corrections de bugs de langue

### Version 1.0.0
- Release initiale avec extraction PDF et amélioration IA

Voir `CHANGELOG.md` pour l'historique complet.

## 📚 Documentation

- **GUIDE_TEXTES_PERSONNALISABLES.md** : Guide complet pour personnaliser tous les textes
- **SEO.md** : Guide d'optimisation SEO (Score 95/100)
- **CHANGELOG.md** : Historique détaillé des versions
- **replit.md** : Documentation technique du projet

## 📞 Support

**MOA Digital Agency LLC**  
Développeur : Aisance KALONJI  
Email : [moa@myoneart.com](mailto:moa@myoneart.com)  
Site Web : [www.myoneart.com](https://www.myoneart.com)

## 📄 Licence

Propriétaire - Tous droits réservés © 2025 MOA Digital Agency LLC

---

**Développé avec ❤️ pour l'immobilier de luxe à Marrakech**
