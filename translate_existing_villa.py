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
        
        french_data = {
            'title': villa.title or '',
            'description': villa.description or '',
            'features': villa.features or '',
            'equipment': villa.equipment or '',
            'business_info': villa.business_info or '',
            'investment_benefits': villa.investment_benefits or '',
            'documents': villa.documents or ''
        }
        
        non_empty = {k: v for k, v in french_data.items() if v and v.strip()}
        
        if not non_empty:
            print("⚠️  Aucune donnée française à traduire")
            return False
        
        print(f"📝 Champs français trouvés: {', '.join(non_empty.keys())}")
        print()
        print("🌍 Traduction en cours vers l'anglais...")
        print("⏳ Cela peut prendre 60-90 secondes...")
        print()
        
        english_translations = translate_villa_data_to_english(french_data)
        
        if not english_translations:
            print("❌ La traduction a échoué")
            return False
        
        print(f"✅ Traduction réussie de {len(english_translations)} champs")
        print()
        
        if 'title_en' in english_translations:
            villa.title_en = english_translations['title_en']
            print(f"  ✓ Titre: {english_translations['title_en'][:60]}...")
        
        if 'description_en' in english_translations:
            villa.description_en = english_translations['description_en']
            print(f"  ✓ Description: {len(english_translations['description_en'])} caractères")
        
        if 'features_en' in english_translations:
            villa.features_en = english_translations['features_en']
            features_count = len([f for f in english_translations['features_en'].split('\n') if f.strip()])
            print(f"  ✓ Caractéristiques: {features_count} items")
        
        if 'equipment_en' in english_translations:
            villa.equipment_en = english_translations['equipment_en']
            equipment_count = len([e for e in english_translations['equipment_en'].split('\n') if e.strip()])
            print(f"  ✓ Équipements: {equipment_count} items")
        
        if 'business_info_en' in english_translations:
            villa.business_info_en = english_translations['business_info_en']
            print(f"  ✓ Informations commerciales: {len(english_translations['business_info_en'])} caractères")
        
        if 'investment_benefits_en' in english_translations:
            villa.investment_benefits_en = english_translations['investment_benefits_en']
            benefits_count = len([b for b in english_translations['investment_benefits_en'].split('\n') if b.strip()])
            print(f"  ✓ Atouts investissement: {benefits_count} items")
        
        if 'documents_en' in english_translations:
            villa.documents_en = english_translations['documents_en']
            print(f"  ✓ Documents: traduit")
        
        try:
            db.session.commit()
            print()
            print("💾 Traductions sauvegardées dans la base de données")
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
