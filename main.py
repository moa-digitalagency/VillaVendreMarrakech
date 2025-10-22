"""
Main Entry Point - Application Flask Villa à Vendre Marrakech

Ce fichier sert de point d'entrée principal pour l'application Flask.
Il importe l'application depuis app.py et la rend disponible pour gunicorn.

Développé par: MOA Digital Agency LLC
Développeur: Aisance KALONJI
Email: moa@myoneart.com
Web: www.myoneart.com
"""

# Import de l'application Flask depuis le module app
from app import app

# Point d'entrée pour l'exécution directe en développement
if __name__ == '__main__':
    # Lance le serveur de développement Flask
    # host='0.0.0.0' permet d'accepter les connexions de toutes les interfaces réseau
    # port=5000 est le port par défaut pour Replit
    # debug=True active le mode debug avec rechargement automatique
    app.run(host='0.0.0.0', port=5000, debug=True)
