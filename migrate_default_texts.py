"""
Script de migration - Définir les textes par défaut bilingues
Ce script met à jour la villa existante avec tous les textes par défaut en français et anglais
pour rendre le site entièrement modifiable depuis le panneau d'administration.

Exécutez ce script une fois après le déploiement :
python migrate_default_texts.py
"""

import os
from app import app, db
from models import Villa

def migrate_default_texts():
    """Migre les textes par défaut pour la villa existante"""
    with app.app_context():
        villa = Villa.query.first()
        
        if not villa:
            print("❌ Aucune villa trouvée dans la base de données")
            print("💡 Créez d'abord une villa depuis le panneau d'administration")
            return
        
        print(f"🔄 Migration des textes par défaut pour la villa: {villa.reference}")
        
        # Section Héro
        if not villa.hero_subtitle_fr:
            villa.hero_subtitle_fr = "Découvrez cette villa d'exception à Marrakech"
        if not villa.hero_subtitle_en:
            villa.hero_subtitle_en = "Discover this exceptional villa in Marrakech"
        
        if not villa.contact_button_fr:
            villa.contact_button_fr = "Nous Contacter"
        if not villa.contact_button_en:
            villa.contact_button_en = "Contact Us"
        
        # Section Description
        if not villa.description_title_fr:
            villa.description_title_fr = "Une Villa d'Exception"
        if not villa.description_title_en:
            villa.description_title_en = "An Exceptional Villa"
        
        if not villa.whatsapp_button_fr:
            villa.whatsapp_button_fr = "📱 Prendre Rendez-vous sur WhatsApp"
        if not villa.whatsapp_button_en:
            villa.whatsapp_button_en = "📱 Schedule a Visit on WhatsApp"
        
        # Section "Pourquoi Choisir Cette Villa"
        if not villa.why_choose_title_fr:
            villa.why_choose_title_fr = "Pourquoi Choisir Cette Villa ?"
        if not villa.why_choose_title_en:
            villa.why_choose_title_en = "Why Choose This Villa?"
        
        # Carte 1 - Emplacement
        if not villa.why_card1_title_fr:
            villa.why_card1_title_fr = "Emplacement Premium"
        if not villa.why_card1_title_en:
            villa.why_card1_title_en = "Premium Location"
        if not villa.why_card1_desc_fr:
            villa.why_card1_desc_fr = f"Située à {villa.location}, dans l'un des quartiers les plus prisés de Marrakech"
        if not villa.why_card1_desc_en:
            villa.why_card1_desc_en = f"Located in {villa.location}, one of Marrakech's most sought-after areas"
        
        # Carte 2 - Architecture
        if not villa.why_card2_title_fr:
            villa.why_card2_title_fr = "Architecture Moderne"
        if not villa.why_card2_title_en:
            villa.why_card2_title_en = "Modern Architecture"
        if not villa.why_card2_desc_fr:
            villa.why_card2_desc_fr = "Design contemporain alliant luxe, confort et authenticité marocaine"
        if not villa.why_card2_desc_en:
            villa.why_card2_desc_en = "Contemporary design combining luxury, comfort and Moroccan authenticity"
        
        # Carte 3 - Finitions
        if not villa.why_card3_title_fr:
            villa.why_card3_title_fr = "Finitions Haut de Gamme"
        if not villa.why_card3_title_en:
            villa.why_card3_title_en = "Premium Finishes"
        if not villa.why_card3_desc_fr:
            villa.why_card3_desc_fr = "Matériaux nobles et équipements premium pour un confort optimal"
        if not villa.why_card3_desc_en:
            villa.why_card3_desc_en = "Noble materials and premium equipment for optimal comfort"
        
        # Carte 4 - Espaces Extérieurs
        if not villa.why_card4_title_fr:
            villa.why_card4_title_fr = "Espaces Extérieurs"
        if not villa.why_card4_title_en:
            villa.why_card4_title_en = "Outdoor Spaces"
        if not villa.why_card4_desc_fr:
            villa.why_card4_desc_fr = "Jardin paysager, terrasses et espaces de vie en plein air exceptionnels"
        if not villa.why_card4_desc_en:
            villa.why_card4_desc_en = "Landscaped garden, terraces and exceptional outdoor living spaces"
        
        # Section Contact
        if not villa.contact_title_fr:
            villa.contact_title_fr = "Intéressé par cette Villa ?"
        if not villa.contact_title_en:
            villa.contact_title_en = "Interested in this Villa?"
        
        if not villa.contact_subtitle_fr:
            villa.contact_subtitle_fr = "Contactez-nous dès aujourd'hui pour organiser une visite privée"
        if not villa.contact_subtitle_en:
            villa.contact_subtitle_en = "Contact us today to arrange a private viewing"
        
        try:
            db.session.commit()
            print("✅ Migration réussie !")
            print("📝 Tous les textes par défaut ont été définis")
            print("💡 Vous pouvez maintenant modifier tous ces textes depuis le panneau d'administration")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la migration: {e}")

if __name__ == '__main__':
    migrate_default_texts()
