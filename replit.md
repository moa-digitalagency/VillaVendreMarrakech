# Application Web de Vente de Villa de Prestige

## Vue d'ensemble
Application web complète pour la vente en ligne de villas de luxe à Marrakech avec interface d'administration sécurisée et page publique moderne ultra-immersive.

## Fonctionnalités Principales

### 🔐 Sécurité
- **Authentification admin** avec mot de passe (mot de passe par défaut: `@4dm1n`)
- **Protection par session Flask** de toutes les routes admin
- **Bouton de déconnexion** pour sécuriser l'accès

### 🎨 Interface Admin Thème Clair
- **Design professionnel moderne** avec palette claire (gold, teal, blanc)
- **Deux modes de saisie distincts** :
  - **Mode PDF + Photos** : Extraction automatique par Claude 3.5 Sonnet
  - **Mode Formulaire + Photos** : Saisie manuelle avec amélioration IA
- **Responsive** adapté à tous les écrans
- **Sections color-codées** : violet (PDF), vert (photos), doré (formulaires)

### 🚀 Intelligence Artificielle (OpenRouter)
- **Extraction automatique depuis PDF** - Claude 3.5 Sonnet analyse et extrait toutes les données
- **Amélioration de texte en temps réel** - Mistral Large améliore vos descriptions (bouton ✨ AI)
- **Modèles optimisés** pour l'extraction structurée et la génération de contenu en français

### 📸 Gestion des Médias
- **Upload de photos** avec optimisation automatique (conversion JPEG, compression)
- **Galerie interactive** avec suppression d'images
- **Preview en temps réel** des images uploadées

### 🗑️ Réinitialisation
- **Bouton de reset** pour supprimer toutes les données
- **Double confirmation** avec modale sécurisée (saisie de "SUPPRIMER")
- **Suppression complète** : données + photos

### 🌐 Frontend Public Ultra-Moderne
- **Hero Slider Automatique** : 3 photos qui défilent toutes les 5 secondes
- **Design Photo-Forward** : Images réparties partout dans la page (hero, description, galerie)
- **Section Créative** : "Pourquoi Choisir Cette Villa ?" avec 4 cards illustrées
- **Galerie Lightbox** : Toutes les photos restantes avec navigation clavier/souris
- **Intégration WhatsApp** : Tous les boutons de contact ouvrent WhatsApp avec message pré-rempli
- **Responsive Total** : Adapté mobile/tablette/desktop
- **Palette Gold/Teal** : Design luxueux professionnel

### 📱 Fonctionnalités WhatsApp
- **Lien automatique** : Numéro WhatsApp formaté automatiquement
- **Message pré-rempli** : "Bonjour, je souhaite prendre rendez-vous pour visiter la villa [TITRE] et obtenir plus d'informations. Lien: [URL]"
- **Boutons multiples** : Hero, section description, section contact
- **Ouverture externe** : WhatsApp s'ouvre dans un nouvel onglet

## Structure du Projet
```
├── app.py                  # Application Flask principale
├── models.py              # Modèles de base de données
├── templates/
│   ├── admin.html         # Interface d'administration
│   ├── login.html         # Page de connexion (thème clair)
│   └── index.html         # Page publique photo-forward moderne
├── static/
│   ├── css/
│   │   ├── style.css      # Styles frontend (design luxueux)
│   │   └── admin.css      # Styles admin (thème clair professionnel)
│   ├── js/
│   │   └── admin.js       # Scripts admin (gestion modes, event listeners)
│   └── uploads/           # Photos uploadées
├── README.md              # Documentation complète
└── replit.md              # Documentation technique
```

## Technologies
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Design moderne photo-forward)
- **IA**: OpenRouter API
  - **Claude 3.5 Sonnet** (Anthropic) - Extraction PDF structurée
  - **Mistral Large** - Amélioration de texte en français
- **Images**: Pillow pour optimisation automatique
- **Intégration**: WhatsApp Deep Links pour contact direct
- **Sécurité**: Flask Sessions, protection par mot de passe

## Routes

### Publiques
- `/` - Page publique de la villa (design photo-forward)
- `/api/villa` - Récupération des données de la villa (JSON)

### Authentification
- `/login` - Page de connexion admin (POST pour se connecter)
- `/logout` - Déconnexion admin

### Admin (Protégées par authentification)
- `/admin` - Interface d'administration
- `/admin/save` - Sauvegarde des données de la villa
- `/admin/upload` - Upload de photos (avec optimisation automatique)
- `/admin/upload-pdf` - Upload et extraction de données depuis PDF (Claude 3.5 Sonnet)
- `/admin/delete-image/<filename>` - Suppression d'une photo
- `/admin/reset` - Réinitialisation complète des données (avec confirmation)
- `/api/enhance` - Amélioration de texte par IA (Mistral Large)

## Configuration
Variables d'environnement:
- `DATABASE_URL` - URL PostgreSQL (configuré automatiquement)
- `OPENROUTER_API_KEY` - Clé API OpenRouter (requis pour les fonctionnalités IA)
- `ADMIN_PASSWORD` - Mot de passe admin (par défaut: `@4dm1n`)
- `SECRET_KEY` - Clé secrète Flask pour les sessions (généré automatiquement)

## Utilisation

### Connexion Admin
1. Accédez à `/login`
2. Entrez le mot de passe : `@4dm1n` (ou votre mot de passe personnalisé)
3. Vous êtes redirigé vers l'interface d'administration

### Deux Modes Distincts

#### Mode 1 : PDF + Photos (Recommandé)
1. Connectez-vous à `/admin`
2. Cliquez sur **"Mode PDF + Photos"** dans le sélecteur de mode
3. Uploadez un PDF de la villa dans la section violette
4. **Claude 3.5 Sonnet** analyse le PDF et extrait automatiquement toutes les données (60-90 secondes)
5. Ajoutez au moins **5 photos** dans la section verte (3 pour le slider, 2 pour description, reste en galerie)
6. Cliquez sur "💾 Enregistrer la Villa"
7. Consultez `/` pour voir le résultat

#### Mode 2 : Formulaire + Photos
1. Connectez-vous à `/admin`
2. Cliquez sur **"Mode Formulaire + Photos"** dans le sélecteur de mode
3. Remplissez manuellement tous les champs du formulaire
4. Utilisez les boutons ✨ AI pour améliorer vos textes avec **Mistral Large**
5. Ajoutez au moins **5 photos** dans la section verte
6. Cliquez sur "💾 Enregistrer la Villa"
7. Consultez `/` pour voir le résultat

### Réinitialisation des données
1. Dans l'admin (peu importe le mode), cliquez sur "🗑️ Réinitialiser"
2. Une modale s'ouvre avec un avertissement
3. Tapez exactement "SUPPRIMER" pour confirmer
4. Toutes les données et photos sont supprimées définitivement

### Déconnexion
- Cliquez sur "Déconnexion" dans le header de l'admin

## Architecture Frontend (Page Publique)

### Distribution des Photos
- **Photos 1-3** : Hero slider automatique (rotation 5s)
- **Photos 4-5** : Section description (double image block)
- **Photos 6+** : Galerie complète avec lightbox

### Sections de la Page
1. **Hero Slider** : 3 photos en rotation + titre + prix + bouton WhatsApp
2. **Quick Stats** : Cards avec icônes (terrain, surface, chambres, piscine)
3. **Description** : Texte + double image + bouton WhatsApp "Prendre Rendez-vous"
4. **Pourquoi Choisir** : 4 cards créatives (emplacement, architecture, finitions, extérieurs)
5. **Caractéristiques** : 3 cards (équipements, confort, avantages)
6. **Galerie Photos** : Grid masonry responsive avec lightbox
7. **Contact** : Box centrale + bouton WhatsApp principal

### Fonctionnalités JavaScript
- **Hero Slider** : Auto-rotation toutes les 5 secondes
- **Lightbox** : Navigation clavier (←/→/Escape) et clics
- **Smooth Scroll** : Défilement fluide vers sections
- **Responsive** : Adaptation automatique aux breakpoints

## Workflow des Modes

### Mode PDF + Photos
```
Sélection mode → Upload PDF → Extraction IA (60-90s) → 
Upload photos (min. 5) → Enregistrer → Terminé
```

### Mode Formulaire + Photos
```
Sélection mode → Saisie manuelle → (Optionnel: Amélioration IA) → 
Upload photos (min. 5) → Enregistrer → Terminé
```

## Architecture Technique

### Event Listeners (JavaScript)
- Tous les événements sont gérés via `addEventListener` (plus de `onclick` inline)
- Délégation d'événements pour les boutons dynamiques (suppression d'images)
- Gestion centralisée des modes PDF vs Formulaire
- Stockage temporaire des données extraites du PDF dans `window.pdfExtractedData`

### Modes Distincts
- Sélecteur de mode en haut de l'interface
- Basculement CSS avec classes `.active` sur les divs `.mode-content`
- Mode PDF : formulaire simplifié avec extraction automatique
- Mode Formulaire : formulaire complet avec tous les champs éditables

### WhatsApp Deep Links
- Format : `https://wa.me/PHONE?text=MESSAGE`
- Nettoyage automatique du numéro (suppression +, espaces, tirets)
- Message URL-encodé avec titre villa + lien site
- Ouverture en nouvel onglet (`target="_blank"`)

## Documentation de Déploiement

Le projet inclut une documentation complète de déploiement :

### Fichiers de Déploiement
- **DEPLOYMENT.md** : Guide complet bilingue (EN/FR) avec schémas DB, scripts init, env vars
- **init_database.sql** : Script PostgreSQL d'initialisation automatique avec triggers et index
- **requirements.txt** : Liste complète des dépendances Python
- **.env.example** : Template de configuration des variables d'environnement

### Schéma de Base de Données
- Table `villa` avec 18 colonnes (titre, prix, localisation, surface, etc.)
- Triggers automatiques pour `updated_at`
- Index optimisés pour performance (created_at, price, location)
- Support PostgreSQL 12+

### Variables d'Environnement Requises
- `DATABASE_URL` : Connexion PostgreSQL (auto sur Replit)
- `OPENROUTER_API_KEY` : Clé API pour fonctionnalités IA
- `ADMIN_PASSWORD` : Mot de passe admin (défaut: @4dm1n)
- `SECRET_KEY` : Clé secrète Flask pour sessions

## Date de Création
21 octobre 2025

## Dernière Mise à Jour
21 octobre 2025 - Design photo-forward + intégration WhatsApp + Documentation déploiement

## Plateforme
Villas à Vendre Marrakech - Immobilier de luxe
