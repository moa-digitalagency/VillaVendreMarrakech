# 🚀 Configuration VPS - Villa à Vendre Marrakech

## ✅ Améliorations du Script `update_vps.sh`

Le script a été amélioré pour **gérer automatiquement la configuration VPS** :

- ✅ **Détection automatique de l'environnement** (Replit vs VPS)
- ✅ **Création automatique du fichier `.env`** s'il n'existe pas
- ✅ **Vérification des variables obligatoires** si `.env` existe déjà
- ✅ **Génération automatique de `SESSION_SECRET`** sécurisée
- ✅ **Skip automatique sur Replit** (aucune interférence)

---

## 🎯 Utilisation Simplifiée sur VPS

### Première utilisation

```bash
cd /root/VillaVendreMarrakech
sudo ./update_vps.sh
```

**Le script va automatiquement :**
1. ✅ Détecter que vous êtes sur VPS (pas sur Replit)
2. ✅ Créer le fichier `.env` s'il n'existe pas
3. ✅ Générer une `SESSION_SECRET` sécurisée
4. ⏸️ **Pause** et vous demander de configurer 2 variables
5. ✅ Continuer la mise à jour après configuration

---

## 📝 Configuration du Fichier `.env`

### Lorsque le script crée `.env` automatiquement

Le script s'arrête et affiche :

```
⚠️  CONFIGURATION REQUISE ⚠️

Le fichier .env a été créé avec des valeurs par défaut.
Vous devez modifier les variables suivantes :

  1. OPENROUTER_API_KEY  (obligatoire pour l'IA)
  2. ADMIN_PASSWORD      (pour la sécurité)
  3. DATABASE_URL ou PGPASSWORD (connexion base de données)

Commandes :
  nano /root/VillaVendreMarrakech/.env

Appuyez sur Entrée pour continuer après avoir configuré .env...
```

### Éditez le fichier `.env`

```bash
sudo nano /root/VillaVendreMarrakech/.env
```

**Complétez ces variables :**

```bash
# 1. Clé API OpenRouter (pour l'IA)
# Obtenez-la sur : https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE_ICI

# 2. SESSION_SECRET (déjà générée automatiquement - ne pas modifier)
SESSION_SECRET=e4f8a2b9c1d3e5f7g9h1i3j5k7l9m1n3...

# 3. Mot de passe admin (changez @4dm1n)
ADMIN_PASSWORD=VotreMotDePasseSecurise2024!

# 4. Base de données PostgreSQL
DATABASE_URL=postgresql://postgres:votre_password@localhost:5432/villa_sales
```

**Sauvegardez** le fichier (Ctrl+O puis Ctrl+X) et **appuyez sur Entrée** dans le terminal.

Le script continuera automatiquement la mise à jour.

---

## 🔄 Mises à jour suivantes

Les fois suivantes, le script **vérifie automatiquement** que `.env` est bien configuré :

```bash
cd /root/VillaVendreMarrakech
sudo ./update_vps.sh
```

**Si tout est OK :**
```
✅ Fichier .env détecté
✅ Toutes les variables obligatoires sont présentes
```

**Si des variables manquent :**
```
⚠️ Variables manquantes dans .env:
  ❌ OPENROUTER_API_KEY
```

→ Éditez `.env` pour compléter les variables manquantes.

---

## 📋 Variables d'Environnement

| Variable | Description | Obligatoire | Où l'obtenir |
|----------|-------------|-------------|--------------|
| `OPENROUTER_API_KEY` | Clé API pour l'IA (extraction PDF, traduction) | ✅ Oui | https://openrouter.ai/ |
| `SESSION_SECRET` | Clé secrète pour sécuriser les sessions | ✅ Oui | **Générée automatiquement** |
| `ADMIN_PASSWORD` | Mot de passe du panneau admin | ⚠️ Recommandé | Votre choix (changez `@4dm1n`) |
| `DATABASE_URL` | URL PostgreSQL complète | ✅ Oui | Votre configuration DB |

---

## 🛠️ Commandes Utiles

### Vérifier le fichier `.env`
```bash
cat /root/VillaVendreMarrakech/.env
```

### Éditer le fichier `.env`
```bash
sudo nano /root/VillaVendreMarrakech/.env
```

### Vérifier le statut de l'application
```bash
sudo systemctl status villa-vendre-marra-kech.service
```

### Voir les logs en temps réel
```bash
sudo journalctl -u villa-vendre-marra-kech.service -f
```

### Redémarrer uniquement l'application
```bash
cd /root/VillaVendreMarrakech
sudo ./update_vps.sh --restart
```

---

## 🚨 Dépannage

### L'application s'arrête après mise à jour

**Vérifiez les logs :**
```bash
sudo journalctl -u villa-vendre-marra-kech.service -n 100
```

**Erreurs communes :**

| Erreur | Solution |
|--------|----------|
| `Variables d'environnement manquantes` | Complétez le fichier `.env` |
| `Connection refused` (PostgreSQL) | Vérifiez que PostgreSQL fonctionne |
| `Permission denied` | Vérifiez les permissions : `chmod 600 .env` |
| `OPENROUTER_API_KEY invalid` | Vérifiez votre clé sur openrouter.ai |

### Le fichier `.env` ne se charge pas

```bash
# Vérifiez qu'il existe
ls -la /root/VillaVendreMarrakech/.env

# Vérifiez les permissions
chmod 600 /root/VillaVendreMarrakech/.env

# Redémarrez
sudo systemctl restart villa-vendre-marra-kech.service
```

---

## 📖 Workflow Complet de Mise à Jour VPS

```bash
# 1. Se connecter au VPS
ssh root@votre-vps.com

# 2. Aller dans le répertoire de l'application
cd /root/VillaVendreMarrakech

# 3. Lancer la mise à jour
sudo ./update_vps.sh

# 4. Si c'est la première fois : configurer .env
#    (le script vous guidera)

# 5. C'est tout ! L'application est à jour
```

---

## 🎯 Différences Replit vs VPS

| Aspect | Replit | VPS |
|--------|--------|-----|
| Variables d'environnement | Secrets Replit | Fichier `.env` |
| Gestion automatique | ✅ Oui | ✅ Oui (via script) |
| Fichier `.env` | ❌ Non requis | ✅ Requis |
| Script `update_vps.sh` | ⏭️ Skip création `.env` | ✅ Crée/vérifie `.env` |

---

## 📞 Support

**Développé par MOA Digital Agency LLC**
- Email : moa@myoneart.com
- Web : www.myoneart.com
