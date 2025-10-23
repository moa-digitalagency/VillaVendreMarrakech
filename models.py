"""
Modèles de Base de Données - Application Villa à Vendre Marrakech

Ce fichier définit les modèles SQLAlchemy pour la base de données PostgreSQL.
Actuellement, il contient le modèle Villa qui représente une villa de luxe à vendre.

Développé par: MOA Digital Agency LLC
Développeur: Aisance KALONJI
Email: moa@myoneart.com
Web: www.myoneart.com
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()


class Villa(db.Model):
    """
    Modèle de données pour une Villa de luxe à Marrakech
    
    Ce modèle stocke toutes les informations nécessaires pour présenter
    une villa de prestige sur le site, incluant:
    - Informations générales (référence, titre, prix, localisation)
    - Caractéristiques techniques (surfaces, chambres, piscine)
    - Détails marketing (équipements, avantages investisseurs)
    - Médias (images)
    - Coordonnées de contact
    """
    
    __tablename__ = 'villa'
    
    # ========== IDENTIFIANT UNIQUE ==========
    id = db.Column(db.Integer, primary_key=True)
    
    # ========== INFORMATIONS PRINCIPALES ==========
    reference = db.Column(db.String(50), unique=True, nullable=False)  # Référence unique de la villa (ex: "VL-001")
    title = db.Column(db.String(200), nullable=False)  # Titre attractif de l'annonce (français)
    title_en = db.Column(db.String(200))  # Titre en anglais
    price = db.Column(db.Integer, nullable=False)  # Prix en euros
    location = db.Column(db.String(200), nullable=False)  # Localisation (quartier, zone)
    distance_city = db.Column(db.String(100))  # Distance depuis le centre-ville
    description = db.Column(db.Text, nullable=False)  # Description complète et détaillée (français)
    description_en = db.Column(db.Text)  # Description en anglais
    
    # ========== CARACTÉRISTIQUES TECHNIQUES ==========
    terrain_area = db.Column(db.Integer)  # Surface du terrain en m²
    built_area = db.Column(db.Integer)  # Surface construite en m²
    bedrooms = db.Column(db.Integer)  # Nombre de chambres/suites
    pool_size = db.Column(db.String(50))  # Dimensions de la piscine (ex: "12m x 6m")
    
    # ========== DÉTAILS MARKETING ==========
    features = db.Column(db.Text)  # Équipements principaux (un par ligne) - français
    features_en = db.Column(db.Text)  # Équipements principaux - anglais
    equipment = db.Column(db.Text)  # Équipement et confort (un par ligne) - français
    equipment_en = db.Column(db.Text)  # Équipement et confort - anglais
    business_info = db.Column(db.Text)  # Informations sur l'exploitation commerciale - français
    business_info_en = db.Column(db.Text)  # Informations sur l'exploitation commerciale - anglais
    investment_benefits = db.Column(db.Text)  # Atouts pour investisseurs - français
    investment_benefits_en = db.Column(db.Text)  # Atouts pour investisseurs - anglais
    documents = db.Column(db.Text)  # Documents disponibles (titre de propriété, etc.) - français
    documents_en = db.Column(db.Text)  # Documents disponibles - anglais
    
    # ========== MÉDIAS ==========
    images = db.Column(db.Text)  # Liste des noms de fichiers d'images (format JSON)
    
    # ========== CONTACT ==========
    contact_phone = db.Column(db.String(50))  # Numéro de téléphone
    contact_email = db.Column(db.String(100))  # Email de contact
    contact_website = db.Column(db.String(200))  # Site web de l'agence
    
    # ========== TEXTES PERSONNALISABLES DU SITE WEB ==========
    # Section Héro
    hero_subtitle_fr = db.Column(db.String(200))  # Sous-titre héro (français)
    hero_subtitle_en = db.Column(db.String(200))  # Sous-titre héro (anglais)
    contact_button_fr = db.Column(db.String(100))  # Texte bouton contact (français)
    contact_button_en = db.Column(db.String(100))  # Texte bouton contact (anglais)
    
    # Section Description
    description_title_fr = db.Column(db.String(200))  # Titre section description (français)
    description_title_en = db.Column(db.String(200))  # Titre section description (anglais)
    whatsapp_button_fr = db.Column(db.String(100))  # Texte bouton WhatsApp (français)
    whatsapp_button_en = db.Column(db.String(100))  # Texte bouton WhatsApp (anglais)
    
    # Section "Pourquoi Choisir Cette Villa"
    why_choose_title_fr = db.Column(db.String(200))  # Titre section (français)
    why_choose_title_en = db.Column(db.String(200))  # Titre section (anglais)
    
    # Carte 1 - Emplacement
    why_card1_title_fr = db.Column(db.String(200))
    why_card1_title_en = db.Column(db.String(200))
    why_card1_desc_fr = db.Column(db.Text)
    why_card1_desc_en = db.Column(db.Text)
    
    # Carte 2 - Architecture
    why_card2_title_fr = db.Column(db.String(200))
    why_card2_title_en = db.Column(db.String(200))
    why_card2_desc_fr = db.Column(db.Text)
    why_card2_desc_en = db.Column(db.Text)
    
    # Carte 3 - Finitions
    why_card3_title_fr = db.Column(db.String(200))
    why_card3_title_en = db.Column(db.String(200))
    why_card3_desc_fr = db.Column(db.Text)
    why_card3_desc_en = db.Column(db.Text)
    
    # Carte 4 - Espaces Extérieurs
    why_card4_title_fr = db.Column(db.String(200))
    why_card4_title_en = db.Column(db.String(200))
    why_card4_desc_fr = db.Column(db.Text)
    why_card4_desc_en = db.Column(db.Text)
    
    # Section Contact
    contact_title_fr = db.Column(db.String(200))  # Titre contact (français)
    contact_title_en = db.Column(db.String(200))  # Titre contact (anglais)
    contact_subtitle_fr = db.Column(db.String(200))  # Sous-titre contact (français)
    contact_subtitle_en = db.Column(db.String(200))  # Sous-titre contact (anglais)
    
    # ========== MÉTADONNÉES ==========
    is_active = db.Column(db.Boolean, default=True)  # Villa active/visible sur le site
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date de dernière mise à jour
    
    # ========== MÉTHODES UTILITAIRES ==========
    
    def get_images_list(self):
        """
        Retourne la liste des images sous forme de liste Python
        
        Les images sont stockées en JSON dans la base de données.
        Cette méthode décode le JSON et retourne une liste utilisable.
        
        Returns:
            list: Liste des noms de fichiers d'images
        """
        if self.images:
            return json.loads(self.images)
        return []
    
    def set_images_list(self, images_list):
        """
        Enregistre une liste d'images en JSON dans la base de données
        
        Args:
            images_list (list): Liste des noms de fichiers d'images
        """
        self.images = json.dumps(images_list)
    
    def get_features_list(self):
        """
        Retourne les équipements sous forme de liste
        
        Les équipements sont stockés avec un élément par ligne.
        Cette méthode sépare les lignes et retourne une liste.
        
        Returns:
            list: Liste des équipements
        """
        if self.features:
            return self.features.split('\n')
        return []
    
    def to_dict(self, lang='fr'):
        """
        Convertit l'objet Villa en dictionnaire pour l'API JSON
        
        Utile pour les endpoints API qui doivent retourner les données
        de la villa en format JSON.
        
        IMPORTANT: Pour la langue anglaise, les champs retournent None si la traduction
        n'existe pas (pas de fallback vers le français) pour garantir une expérience
        bilingue pure sans mélange de langues.
        
        Args:
            lang (str): Langue souhaitée ('fr' ou 'en')
        
        Returns:
            dict: Dictionnaire contenant toutes les données de la villa
        """
        if lang == 'en':
            return {
                'id': self.id,
                'reference': self.reference,
                'title': self.title_en,
                'price': self.price,
                'location': self.location,
                'distance_city': self.distance_city,
                'description': self.description_en,
                'terrain_area': self.terrain_area,
                'built_area': self.built_area,
                'bedrooms': self.bedrooms,
                'pool_size': self.pool_size,
                'features': self.features_en,
                'equipment': self.equipment_en,
                'business_info': self.business_info_en,
                'investment_benefits': self.investment_benefits_en,
                'documents': self.documents_en,
                'images': self.get_images_list(),
                'contact_phone': self.contact_phone,
                'contact_email': self.contact_email,
                'contact_website': self.contact_website,
                'is_active': self.is_active
            }
        else:
            return {
                'id': self.id,
                'reference': self.reference,
                'title': self.title,
                'price': self.price,
                'location': self.location,
                'distance_city': self.distance_city,
                'description': self.description,
                'terrain_area': self.terrain_area,
                'built_area': self.built_area,
                'bedrooms': self.bedrooms,
                'pool_size': self.pool_size,
                'features': self.features,
                'equipment': self.equipment,
                'business_info': self.business_info,
                'investment_benefits': self.investment_benefits,
                'documents': self.documents,
                'images': self.get_images_list(),
                'contact_phone': self.contact_phone,
                'contact_email': self.contact_email,
                'contact_website': self.contact_website,
                'is_active': self.is_active
            }
