# Application Web de Vente de Villa de Prestige

## Vue d'ensemble
Application web complète pour la vente en ligne de villas de luxe avec interface d'administration sécurisée et page publique moderne.

## Fonctionnalités Principales

### 🔐 Sécurité
- **Authentification admin** avec mot de passe (mot de passe par défaut: `@4dm1n`)
- **Protection par session Flask** de toutes les routes admin
- **Bouton de déconnexion** pour sécuriser l'accès

### 🎨 Interface Admin Dark Mode
- **Design professionnel** avec palette sombre (charcoal, gold, teal)
- **Interface moderne** avec effets de survol et transitions fluides
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

## Structure du Projet
```
├── app.py                  # Application Flask principale
├── models.py              # Modèles de base de données
├── templates/
│   ├── admin.html         # Interface d'administration
│   └── index.html         # Page publique de présentation
├── static/
│   ├── css/
│   │   ├── style.css      # Styles frontend
│   │   └── admin.css      # Styles admin
│   ├── js/
│   │   └── admin.js       # Scripts admin
│   └── uploads/           # Photos uploadées
└── replit.md              # Documentation
```

## Technologies
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Design Dark Mode professionnel)
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

### Méthode 1 : Extraction automatique depuis PDF (Recommandé)
1. Connectez-vous à `/admin`
2. Dans la section "🚀 Remplissage Automatique par IA" (violet), uploadez un PDF de la villa
3. **Claude 3.5 Sonnet** analyse le PDF et remplit automatiquement tous les champs (60-90 secondes)
4. Dans la section "📸 Photos de la Villa" (vert), uploadez les photos
5. Vérifiez et ajustez les données extraites si nécessaire
6. Cliquez sur "💾 Enregistrer"
7. Consultez `/` pour voir le résultat

### Méthode 2 : Saisie manuelle
1. Connectez-vous à `/admin`
2. Ignorez la section PDF
3. Uploadez directement vos photos dans la section verte
4. Remplissez manuellement les informations dans le formulaire
5. Utilisez les boutons ✨ AI pour améliorer vos textes avec **Mistral Large**
6. Cliquez sur "💾 Enregistrer"
7. Consultez `/` pour voir le résultat

### Réinitialisation des données
1. Dans l'admin, cliquez sur "🗑️ Réinitialiser"
2. Une modale s'ouvre avec un avertissement
3. Tapez exactement "SUPPRIMER" pour confirmer
4. Toutes les données et photos sont supprimées définitivement

### Déconnexion
- Cliquez sur "Déconnexion" dans le header de l'admin

## Date de Création
21 octobre 2025
