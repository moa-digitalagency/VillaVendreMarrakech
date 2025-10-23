#!/usr/bin/env python3
"""
Script pour traduire automatiquement les données existantes de la villa
du français vers l'anglais en utilisant l'API OpenRouter.

Usage: python translate_existing_villa.py
"""

import os
import sys

if not os.environ.get('OPENROUTER_API_KEY'):
    print("❌ Erreur: OPENROUTER_API_KEY non définie")
    print("💡 Configurez cette variable dans les Secrets Replit")
    sys.exit(1)

from app import app, db, translate_villa_data_to_english
from models import Villa

def translate_villa():
    """Traduit automatiquement la villa existante du français vers l'anglais."""
    with app.app_context():
        villa = Villa.query.first()
        
        if not villa:
            print("❌ Aucune villa trouvée dans la base de données")
            return False
        
        print("🏡 Villa trouvée:", villa.title or "Sans titre")
        print()
        
        # Collecte de TOUS les champs français disponibles
        french_data = {
            # Contenu principal
            'title': villa.title or '',
            'description': villa.description or '',
            'features': villa.features or '',
            'equipment': villa.equipment or '',
            'business_info': villa.business_info or '',
            'investment_benefits': villa.investment_benefits or '',
            'documents': villa.documents or '',
            # Textes personnalisables du site web
            'hero_subtitle_fr': villa.hero_subtitle_fr or '',
            'contact_button_fr': villa.contact_button_fr or '',
            'description_title_fr': villa.description_title_fr or '',
            'whatsapp_button_fr': villa.whatsapp_button_fr or '',
            # Section "Why Choose This Villa"
            'why_choose_title_fr': villa.why_choose_title_fr or '',
            'why_card1_title_fr': villa.why_card1_title_fr or '',
            'why_card1_desc_fr': villa.why_card1_desc_fr or '',
            'why_card2_title_fr': villa.why_card2_title_fr or '',
            'why_card2_desc_fr': villa.why_card2_desc_fr or '',
            'why_card3_title_fr': villa.why_card3_title_fr or '',
            'why_card3_desc_fr': villa.why_card3_desc_fr or '',
            'why_card4_title_fr': villa.why_card4_title_fr or '',
            'why_card4_desc_fr': villa.why_card4_desc_fr or '',
            # Section Contact
            'contact_title_fr': villa.contact_title_fr or '',
            'contact_subtitle_fr': villa.contact_subtitle_fr or ''
        }
        
        non_empty = {k: v for k, v in french_data.items() if v and v.strip()}
        
        if not non_empty:
            print("⚠️  Aucune donnée française à traduire")
            return False
        
        print(f"📝 {len(non_empty)} champs français trouvés")
        print()
        print("🌍 Traduction en cours vers l'anglais...")
        print("⏳ Cela peut prendre 90-120 secondes...")
        print()
        
        english_translations = translate_villa_data_to_english(french_data)
        
        if not english_translations:
            print("❌ La traduction a échoué")
            return False
        
        print(f"✅ Traduction réussie de {len(english_translations)} champs")
        print()
        
        # Appliquer toutes les traductions
        field_mapping = {
            'title_en': 'title_en',
            'description_en': 'description_en',
            'features_en': 'features_en',
            'equipment_en': 'equipment_en',
            'business_info_en': 'business_info_en',
            'investment_benefits_en': 'investment_benefits_en',
            'documents_en': 'documents_en',
            'hero_subtitle_en': 'hero_subtitle_en',
            'contact_button_en': 'contact_button_en',
            'description_title_en': 'description_title_en',
            'whatsapp_button_en': 'whatsapp_button_en',
            'why_choose_title_en': 'why_choose_title_en',
            'why_card1_title_en': 'why_card1_title_en',
            'why_card1_desc_en': 'why_card1_desc_en',
            'why_card2_title_en': 'why_card2_title_en',
            'why_card2_desc_en': 'why_card2_desc_en',
            'why_card3_title_en': 'why_card3_title_en',
            'why_card3_desc_en': 'why_card3_desc_en',
            'why_card4_title_en': 'why_card4_title_en',
            'why_card4_desc_en': 'why_card4_desc_en',
            'contact_title_en': 'contact_title_en',
            'contact_subtitle_en': 'contact_subtitle_en'
        }
        
        translated_count = 0
        for trans_key, villa_attr in field_mapping.items():
            if trans_key in english_translations:
                setattr(villa, villa_attr, english_translations[trans_key])
                translated_count += 1
                
                # Affichage selon le type de champ
                if trans_key == 'title_en':
                    print(f"  ✓ Titre: {english_translations[trans_key][:60]}...")
                elif trans_key == 'description_en':
                    print(f"  ✓ Description: {len(english_translations[trans_key])} caractères")
                elif trans_key in ['features_en', 'equipment_en', 'investment_benefits_en']:
                    items_count = len([item for item in english_translations[trans_key].split('\n') if item.strip()])
                    field_name = trans_key.replace('_en', '').replace('_', ' ').title()
                    print(f"  ✓ {field_name}: {items_count} items")
                elif trans_key.endswith('_en') and len(english_translations[trans_key]) > 50:
                    field_name = trans_key.replace('_en', '').replace('_', ' ').title()
                    print(f"  ✓ {field_name}: {english_translations[trans_key][:50]}...")
                elif trans_key.endswith('_en'):
                    field_name = trans_key.replace('_en', '').replace('_', ' ').title()
                    print(f"  ✓ {field_name}: {english_translations[trans_key]}")
        
        try:
            db.session.commit()
            print()
            print(f"💾 {translated_count} traductions sauvegardées dans la base de données")
            print()
            print("✅ Traduction terminée avec succès!")
            print()
            print("📌 Prochaine étape:")
            print("   Allez sur /admin pour vérifier et éditer les traductions si besoin")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False

if __name__ == '__main__':
    print("="*80)
    print("🌍 TRADUCTION AUTOMATIQUE FRANÇAIS → ANGLAIS")
    print("="*80)
    print()
    
    success = translate_villa()
    
    print()
    print("="*80)
    
    sys.exit(0 if success else 1)
