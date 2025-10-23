# Instructions de Configuration VPS - Villa à Vendre Marrakech

## Problème Résolu

Le script `update_vps.sh` fonctionnait correctement, mais l'application s'arrêtait car elle ne trouvait pas les variables d'environnement requises sur le VPS.

**Correction apportée :** Ajout du chargement automatique du fichier `.env` dans `app.py`

---

## Configuration Requise sur Votre VPS

### Étape 1 : Créer le fichier `.env`

Sur votre VPS, créez un fichier `.env` dans le répertoire de l'application :

```bash
sudo nano /root/VillaVendreMarrakech/.env
```

### Étape 2 : Ajouter les Variables d'Environnement

Copiez et modifiez ce contenu dans le fichier `.env` :

```bash
# === VARIABLES OBLIGATOIRES ===

# Clé API OpenRouter (pour les fonctionnalités IA)
# Obtenez votre clé sur : https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE_ICI

# Clé secrète de session (pour la sécurité de l'application)
# Générez-en une nouvelle avec la commande ci-dessous
SESSION_SECRET=votre_cle_secrete_longue_et_aleatoire_ici

# Mot de passe admin (pour accéder au panneau d'administration)
ADMIN_PASSWORD=VotreMotDePasseAdmin123!

# === VARIABLES DE BASE DE DONNÉES (si différentes des valeurs par défaut) ===

# URL complète de la base de données PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/villa_sales

# OU utilisez les variables individuelles :
PGUSER=postgres
PGPASSWORD=votre_mot_de_passe_postgresql
PGHOST=localhost
PGPORT=5432
PGDATABASE=villa_sales
```

### Étape 3 : Générer une Clé SESSION_SECRET Sécurisée

Générez une clé secrète aléatoire avec cette commande :

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copiez le résultat et remplacez `votre_cle_secrete_longue_et_aleatoire_ici` dans le fichier `.env`.

### Étape 4 : Sécuriser le Fichier `.env`

Définissez les bonnes permissions pour protéger vos secrets :

```bash
# Définir le propriétaire
sudo chown www-data:www-data /root/VillaVendreMarrakech/.env

# Restreindre les permissions (lecture seule pour le propriétaire)
sudo chmod 600 /root/VillaVendreMarrakech/.env
```

### Étape 5 : Mettre à Jour l'Application

Maintenant que le fichier `.env` est configuré, relancez le script de mise à jour :

```bash
cd /root/VillaVendreMarrakech
sudo ./update_vps.sh
```

---

## Vérification

Après la mise à jour, vérifiez que l'application fonctionne :

```bash
# Vérifier le statut du service
sudo systemctl status villa-vendre-marra-kech.service

# Voir les logs en temps réel
sudo journalctl -u villa-vendre-marra-kech.service -f

# Tester l'application
curl http://localhost:5000
```

---

## Variables d'Environnement Expliquées

| Variable | Description | Où l'obtenir |
|----------|-------------|--------------|
| `OPENROUTER_API_KEY` | Clé API pour les fonctionnalités IA (extraction PDF, amélioration de texte, traduction) | https://openrouter.ai/ → Créer un compte → API Keys |
| `SESSION_SECRET` | Clé secrète pour sécuriser les sessions utilisateur | Générer avec `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_PASSWORD` | Mot de passe pour accéder au panneau d'administration | Choisissez un mot de passe fort |
| `DATABASE_URL` | URL de connexion à la base de données PostgreSQL | Fourni par votre hébergeur de base de données |

---

## Fonctionnalités Nécessitant OPENROUTER_API_KEY

1. **Extraction de données depuis PDF** : Analyse automatique des documents PDF de villas
2. **Amélioration de texte** : Amélioration professionnelle des descriptions
3. **Traduction automatique** : Traduction français ↔ anglais

> **Note** : L'application peut fonctionner sans `OPENROUTER_API_KEY`, mais ces fonctionnalités IA ne seront pas disponibles.

---

## Exemple de Fichier `.env` Complet

```bash
# Production - Villa à Vendre Marrakech
OPENROUTER_API_KEY=sk-or-v1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
SESSION_SECRET=9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t9u8v7w6x5y4z3a2b1c0d9e8f7
ADMIN_PASSWORD=MonMotDePasseSecurise2024!
DATABASE_URL=postgresql://villauser:SecurePass123@localhost:5432/villa_sales
```

---

## Dépannage

### L'application s'arrête immédiatement

```bash
# Vérifiez les logs pour voir l'erreur
sudo journalctl -u villa-vendre-marra-kech.service -n 50

# Erreurs communes :
# - "Variables d'environnement manquantes" → Vérifiez votre .env
# - "Connection refused" → Vérifiez que PostgreSQL fonctionne
# - "Permission denied" → Vérifiez les permissions du .env
```

### Le fichier `.env` n'est pas chargé

```bash
# Vérifiez que le fichier existe
ls -la /root/VillaVendreMarrakech/.env

# Vérifiez le contenu (masquez les secrets sensibles !)
sudo cat /root/VillaVendreMarrakech/.env

# Redémarrez le service
sudo systemctl restart villa-vendre-marra-kech.service
```

---

## Support

Pour toute question ou problème :
- Email : moa@myoneart.com
- Web : www.myoneart.com

**Développé par MOA Digital Agency LLC**
