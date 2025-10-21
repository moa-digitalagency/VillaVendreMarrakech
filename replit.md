# Application Web de Vente de Villa de Prestige

## Vue d'ensemble
Application web complète pour la vente en ligne de villas de luxe avec interface d'administration et page publique moderne.

## Fonctionnalités
- **Backend Python (Flask)** avec PostgreSQL
- **Interface Admin** pour gérer toutes les informations de la villa
- **🚀 Extraction automatique depuis PDF** - Uploadez un PDF et l'IA extrait toutes les données
- **Upload de photos** avec optimisation automatique (conversion en JPEG, compression)
- **Intégration OpenRouter AI** pour :
  - Extraction intelligente de données depuis PDF
  - Amélioration de texte en temps réel (bouton ✨ AI)
- **Frontend moderne** avec effets parallaxe et design responsive
- **Galerie photo** avec lightbox et navigation
- **Design luxueux** adapté aux propriétés de prestige

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
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: OpenRouter API (Llama 3.1)
- **Images**: Pillow pour optimisation

## Routes
- `/` - Page publique de la villa
- `/admin` - Interface d'administration
- `/admin/save` - Sauvegarde des données de la villa
- `/admin/upload` - Upload de photos (avec optimisation automatique)
- `/admin/upload-pdf` - Upload et extraction de données depuis PDF
- `/admin/delete-image/<filename>` - Suppression d'une photo
- `/api/enhance` - Amélioration de texte par IA
- `/api/villa` - Récupération des données de la villa (JSON)

## Configuration
Variables d'environnement nécessaires:
- `DATABASE_URL` - URL PostgreSQL (automatique)
- `OPENROUTER_API_KEY` - Clé API OpenRouter (optionnel)

## Utilisation

### Méthode 1 : Extraction automatique depuis PDF (Recommandé)
1. Accédez à `/admin`
2. Dans la section "🚀 Remplissage Automatique par IA", uploadez un PDF de la villa
3. L'IA analyse le PDF et remplit automatiquement tous les champs (30-60 secondes)
4. Vérifiez et ajustez les données extraites si nécessaire
5. Uploadez les photos de la villa
6. Sauvegardez
7. Consultez `/` pour voir le résultat

### Méthode 2 : Saisie manuelle
1. Accédez à `/admin`
2. Remplissez manuellement les informations (titre, prix, description, etc.)
3. Utilisez le bouton ✨ AI pour améliorer vos textes
4. Uploadez des photos
5. Sauvegardez
6. Consultez `/` pour voir le résultat

## Date de Création
21 octobre 2025
