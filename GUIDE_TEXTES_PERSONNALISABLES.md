# Guide - Personnaliser les Textes du Site Web

## 📝 Vue d'ensemble

Tous les textes affichés sur votre site web sont maintenant **100% modifiables** depuis le panneau d'administration. Vous pouvez personnaliser chaque titre, sous-titre et description en **français ET en anglais**.

## 🔐 Accès à l'interface d'édition

1. **Connectez-vous au panneau admin** : `https://votre-site.com/login`
2. **Entrez votre mot de passe** (défini dans ADMIN_PASSWORD)
3. **Cliquez sur "Éditer le site"** dans le menu en haut

## 📋 Sections Modifiables

### 🏡 Section Héro (Hero)
**Emplacement** : En haut de la page d'accueil, sur la grande image

**Champs disponibles** :
- **Sous-titre principal** : Le texte sous le titre de la villa
  - FR : "Découvrez cette villa d'exception à Marrakech"
  - EN : "Discover this exceptional villa in Marrakech"
  
- **Texte du bouton contact** : Le bouton principal d'action
  - FR : "Nous Contacter"
  - EN : "Contact Us"

### 📝 Section Description
**Emplacement** : Sous les statistiques rapides (surface, chambres, etc.)

**Champs disponibles** :
- **Titre de la section** :
  - FR : "Une Villa d'Exception"
  - EN : "An Exceptional Villa"
  
- **Texte du bouton WhatsApp** :
  - FR : "📱 Prendre Rendez-vous sur WhatsApp"
  - EN : "📱 Schedule a Visit on WhatsApp"

### ⭐ Section "Pourquoi Choisir Cette Villa"
**Emplacement** : Section avec 4 cartes expliquant les avantages

**Champs disponibles** :
- **Titre de la section** :
  - FR : "Pourquoi Choisir Cette Villa ?"
  - EN : "Why Choose This Villa?"

**4 Cartes personnalisables** :

1. **Carte 1 - Emplacement** 🌟
   - Titre FR : "Emplacement Premium"
   - Titre EN : "Premium Location"
   - Description FR : "Située à {location}, dans l'un des quartiers les plus prisés de Marrakech"
   - Description EN : "Located in {location}, one of Marrakech's most sought-after areas"
   
2. **Carte 2 - Architecture** 🏗️
   - Titre FR : "Architecture Moderne"
   - Titre EN : "Modern Architecture"
   - Description FR : "Design contemporain alliant luxe, confort et authenticité marocaine"
   - Description EN : "Contemporary design combining luxury, comfort and Moroccan authenticity"
   
3. **Carte 3 - Finitions** 💎
   - Titre FR : "Finitions Haut de Gamme"
   - Titre EN : "Premium Finishes"
   - Description FR : "Matériaux nobles et équipements premium pour un confort optimal"
   - Description EN : "Noble materials and premium equipment for optimal comfort"
   
4. **Carte 4 - Espaces Extérieurs** 🌴
   - Titre FR : "Espaces Extérieurs"
   - Titre EN : "Outdoor Spaces"
   - Description FR : "Jardin paysager, terrasses et espaces de vie en plein air exceptionnels"
   - Description EN : "Landscaped garden, terraces and exceptional outdoor living spaces"

### 📞 Section Contact
**Emplacement** : En bas de page, avec les coordonnées de contact

**Champs disponibles** :
- **Titre principal** :
  - FR : "Intéressé par cette Villa ?"
  - EN : "Interested in this Villa?"
  
- **Sous-titre** :
  - FR : "Contactez-nous dès aujourd'hui pour organiser une visite privée"
  - EN : "Contact us today to arrange a private viewing"

## 💡 Conseils d'utilisation

### Placeholder {location}
Dans certaines descriptions, vous verrez `{location}`. Ce placeholder est automatiquement remplacé par la localisation de votre villa (ex: "Route de Fes").

**Exemple** :
- Texte : "Située à {location}, dans l'un des quartiers..."
- Résultat : "Située à Route de Fes, dans l'un des quartiers..."

### Modification des textes

1. **Connectez-vous** à l'admin
2. **Cliquez** sur "Éditer le site"
3. **Basculez** entre 🇫🇷 Français et 🇬🇧 English avec les onglets en haut
4. **Modifiez** les textes selon vos préférences
5. **Cliquez** sur "💾 Enregistrer les Textes"
6. **Vérifiez** le résultat sur la page publique

### Bonnes pratiques

✅ **Gardez la cohérence** : Assurez-vous que les textes FR et EN transmettent le même message
✅ **Soyez concis** : Les titres courts (2-5 mots) fonctionnent mieux
✅ **Testez les deux langues** : Vérifiez toujours le rendu en FR et EN
✅ **Utilisez les emojis** : Ils rendent le site plus visuel et moderne
✅ **Personnalisez** : Adaptez les textes à votre villa spécifique

## 🔄 Retour aux valeurs par défaut

Si vous souhaitez revenir aux textes par défaut :

**Sur Replit** :
```bash
python migrate_default_texts.py
```

**Sur VPS** :
```bash
cd /var/www/villaeden
source venv/bin/activate
python migrate_default_texts.py
```

Le script ne modifie que les champs vides, donc vos textes personnalisés seront préservés.

## 🆘 Dépannage

### Les textes n'apparaissent pas en anglais
1. Vérifiez que vous avez bien rempli les champs EN (English)
2. Basculez vers l'anglais avec le toggle 🇬🇧 EN en bas à gauche du site
3. Videz le cache de votre navigateur (Ctrl+F5 ou Cmd+Shift+R)

### Les modifications ne sont pas sauvegardées
1. Vérifiez que vous êtes bien connecté
2. Assurez-vous de cliquer sur "💾 Enregistrer les Textes"
3. Vérifiez les logs de l'application pour les erreurs

### Je ne trouve pas un texte à modifier
Tous les textes modifiables sont dans `/admin/edit-website`. Les autres textes (titre de la villa, description principale, équipements) sont dans `/admin` (panneau principal).

## 📧 Support

Pour toute question :
- **Développeur** : Aisance KALONJI
- **Email** : moa@myoneart.com
- **Site web** : www.myoneart.com
