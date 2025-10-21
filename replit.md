# Application Web de Vente de Villa de Prestige

## Vue d'ensemble
Application web complète pour la vente en ligne de villas de luxe à Marrakech avec interface d'administration sécurisée et page publique moderne.

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

### 🌐 Frontend Public
- **Design luxueux** avec effets parallaxe
- **Galerie photo** avec lightbox et navigation
- **Responsive** adapté mobile/tablette/desktop
- **Spécialisé** pour les villas à vendre à Marrakech

## Structure du Projet
```
├── app.py                  # Application Flask principale
├── models.py              # Modèles de base de données
├── templates/
│   ├── admin.html         # Interface d'administration
│   ├── login.html         # Page de connexion (thème clair)
│   └── index.html         # Page publique de présentation
├── static/
│   ├── css/
│   │   ├── style.css      # Styles frontend
│   │   └── admin.css      # Styles admin (thème clair professionnel)
│   ├── js/
│   │   └── admin.js       # Scripts admin (gestion modes, event listeners)
│   └── uploads/           # Photos uploadées
├── README.md              # Documentation complète
└── replit.md              # Documentation technique
```

## Technologies
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Design thème clair professionnel)
- **IA**: OpenRouter API
  - **Claude 3.5 Sonnet** (Anthropic) - Extraction PDF structurée
  - **Mistral Large** - Amélioration de texte en français
- **Images**: Pillow pour optimisation automatique
- **Sécurité**: Flask Sessions, protection par mot de passe

## Routes

### Publiques
- `/` - Page publique de la villa
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
5. Ajoutez les photos dans la section verte
6. Cliquez sur "💾 Enregistrer la Villa"
7. Consultez `/` pour voir le résultat

#### Mode 2 : Formulaire + Photos
1. Connectez-vous à `/admin`
2. Cliquez sur **"Mode Formulaire + Photos"** dans le sélecteur de mode
3. Remplissez manuellement tous les champs du formulaire
4. Utilisez les boutons ✨ AI pour améliorer vos textes avec **Mistral Large**
5. Ajoutez les photos dans la section verte
6. Cliquez sur "💾 Enregistrer la Villa"
7. Consultez `/` pour voir le résultat

### Réinitialisation des données
1. Dans l'admin (peu importe le mode), cliquez sur "🗑️ Réinitialiser"
2. Une modale s'ouvre avec un avertissement
3. Tapez exactement "SUPPRIMER" pour confirmer
4. Toutes les données et photos sont supprimées définitivement

### Déconnexion
- Cliquez sur "Déconnexion" dans le header de l'admin

## Workflow des Modes

### Mode PDF + Photos
```
Sélection mode → Upload PDF → Extraction IA (60-90s) → 
Upload photos → Enregistrer → Terminé
```

### Mode Formulaire + Photos
```
Sélection mode → Saisie manuelle → (Optionnel: Amélioration IA) → 
Upload photos → Enregistrer → Terminé
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

## Date de Création
21 octobre 2025

## Plateforme
Villas à Vendre Marrakech - Immobilier de luxe
