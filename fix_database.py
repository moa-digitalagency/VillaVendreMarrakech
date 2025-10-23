#!/usr/bin/env python3
"""
Script de réparation de la base de données
Ajoute les colonnes manquantes si nécessaire

Usage:
    python fix_database.py
    ou
    python3 fix_database.py
"""

import os
from sqlalchemy import create_engine, text, inspect
from models import Villa, db
from app import app

def check_and_fix_database():
    """Vérifie et répare le schéma de la base de données"""
    
    print("="*80)
    print("🔧 Vérification et réparation de la base de données")
    print("="*80)
    
    with app.app_context():
        try:
            # Créer toutes les tables si elles n'existent pas
            print("\n1️⃣ Création des tables manquantes...")
            db.create_all()
            print("✅ Tables vérifiées/créées")
            
            # Vérifier les colonnes de la table Villa
            engine = db.engine
            inspector = inspect(engine)
            
            if inspector.has_table('villa'):
                print("\n2️⃣ Vérification des colonnes de la table 'villa'...")
                
                existing_columns = {col['name'] for col in inspector.get_columns('villa')}
                print(f"   Colonnes existantes: {len(existing_columns)}")
                
                # Définir toutes les colonnes qui devraient exister
                required_columns = {
                    # Colonnes de base
                    'id', 'reference', 'title', 'price', 'location', 'distance_city',
                    'description', 'terrain_area', 'built_area', 'bedrooms', 'pool_size',
                    'features', 'equipment', 'business_info', 'investment_benefits',
                    'documents', 'contact_phone', 'contact_email', 'contact_website',
                    'is_active', 'created_at', 'updated_at',
                    
                    # Colonnes pour les images
                    'images',
                    
                    # Colonnes pour les traductions anglaises
                    'title_en', 'description_en', 'features_en', 'equipment_en',
                    'business_info_en', 'investment_benefits_en', 'documents_en',
                    
                    # Nouvelles colonnes pour les textes personnalisables du site (FR)
                    'hero_subtitle_fr', 'contact_button_fr', 'description_title_fr',
                    'whatsapp_button_fr', 'why_choose_title_fr',
                    'why_card1_title_fr', 'why_card1_desc_fr',
                    'why_card2_title_fr', 'why_card2_desc_fr',
                    'why_card3_title_fr', 'why_card3_desc_fr',
                    'why_card4_title_fr', 'why_card4_desc_fr',
                    'contact_title_fr', 'contact_subtitle_fr',
                    
                    # Nouvelles colonnes pour les textes personnalisables du site (EN)
                    'hero_subtitle_en', 'contact_button_en', 'description_title_en',
                    'whatsapp_button_en', 'why_choose_title_en',
                    'why_card1_title_en', 'why_card1_desc_en',
                    'why_card2_title_en', 'why_card2_desc_en',
                    'why_card3_title_en', 'why_card3_desc_en',
                    'why_card4_title_en', 'why_card4_desc_en',
                    'contact_title_en', 'contact_subtitle_en'
                }
                
                missing_columns = required_columns - existing_columns
                
                if missing_columns:
                    print(f"\n⚠️  Colonnes manquantes détectées: {len(missing_columns)}")
                    print(f"   Colonnes à ajouter: {', '.join(sorted(missing_columns))}")
                    
                    print("\n3️⃣ Ajout des colonnes manquantes...")
                    
                    # Dictionnaire des types de colonnes
                    column_types = {
                        # Colonnes texte courtes
                        'reference': 'VARCHAR(100)',
                        'title': 'VARCHAR(500)',
                        'title_en': 'TEXT',
                        'location': 'VARCHAR(200)',
                        'distance_city': 'VARCHAR(100)',
                        'pool_size': 'VARCHAR(100)',
                        'contact_phone': 'VARCHAR(50)',
                        'contact_email': 'VARCHAR(200)',
                        'contact_website': 'VARCHAR(500)',
                        
                        # Colonnes numériques
                        'price': 'INTEGER DEFAULT 0',
                        'terrain_area': 'INTEGER DEFAULT 0',
                        'built_area': 'INTEGER DEFAULT 0',
                        'bedrooms': 'INTEGER DEFAULT 0',
                        
                        # Colonnes texte longues
                        'description': 'TEXT',
                        'description_en': 'TEXT',
                        'features': 'TEXT',
                        'features_en': 'TEXT',
                        'equipment': 'TEXT',
                        'equipment_en': 'TEXT',
                        'business_info': 'TEXT',
                        'business_info_en': 'TEXT',
                        'investment_benefits': 'TEXT',
                        'investment_benefits_en': 'TEXT',
                        'documents': 'TEXT',
                        'documents_en': 'TEXT',
                        'images': 'TEXT',
                        
                        # Textes personnalisables FR
                        'hero_subtitle_fr': 'TEXT',
                        'contact_button_fr': 'VARCHAR(100)',
                        'description_title_fr': 'VARCHAR(200)',
                        'whatsapp_button_fr': 'VARCHAR(100)',
                        'why_choose_title_fr': 'VARCHAR(200)',
                        'why_card1_title_fr': 'VARCHAR(200)',
                        'why_card1_desc_fr': 'TEXT',
                        'why_card2_title_fr': 'VARCHAR(200)',
                        'why_card2_desc_fr': 'TEXT',
                        'why_card3_title_fr': 'VARCHAR(200)',
                        'why_card3_desc_fr': 'TEXT',
                        'why_card4_title_fr': 'VARCHAR(200)',
                        'why_card4_desc_fr': 'TEXT',
                        'contact_title_fr': 'VARCHAR(200)',
                        'contact_subtitle_fr': 'TEXT',
                        
                        # Textes personnalisables EN
                        'hero_subtitle_en': 'TEXT',
                        'contact_button_en': 'VARCHAR(100)',
                        'description_title_en': 'VARCHAR(200)',
                        'whatsapp_button_en': 'VARCHAR(100)',
                        'why_choose_title_en': 'VARCHAR(200)',
                        'why_card1_title_en': 'VARCHAR(200)',
                        'why_card1_desc_en': 'TEXT',
                        'why_card2_title_en': 'VARCHAR(200)',
                        'why_card2_desc_en': 'TEXT',
                        'why_card3_title_en': 'VARCHAR(200)',
                        'why_card3_desc_en': 'TEXT',
                        'why_card4_title_en': 'VARCHAR(200)',
                        'why_card4_desc_en': 'TEXT',
                        'contact_title_en': 'VARCHAR(200)',
                        'contact_subtitle_en': 'TEXT'
                    }
                    
                    # Ajouter chaque colonne manquante
                    for column in sorted(missing_columns):
                        if column in column_types:
                            column_type = column_types[column]
                            try:
                                with engine.begin() as conn:
                                    sql = f'ALTER TABLE villa ADD COLUMN IF NOT EXISTS {column} {column_type}'
                                    conn.execute(text(sql))
                                print(f"   ✅ Ajouté: {column} ({column_type})")
                            except Exception as e:
                                print(f"   ⚠️  Impossible d'ajouter {column}: {e}")
                        else:
                            print(f"   ⚠️  Type inconnu pour la colonne: {column}")
                    
                    print("\n✅ Colonnes ajoutées avec succès")
                else:
                    print("   ✅ Toutes les colonnes requises existent déjà")
                
                # Vérifier qu'on peut lire les données
                print("\n4️⃣ Test de lecture de la base de données...")
                villa_count = Villa.query.count()
                print(f"   ✅ Nombre de villas: {villa_count}")
                
                if villa_count > 0:
                    villa = Villa.query.first()
                    print(f"   ✅ Villa de test chargée: {villa.title if villa.title else '(sans titre)'}")
                
            else:
                print("\n⚠️  La table 'villa' n'existe pas, création...")
                db.create_all()
                print("✅ Table 'villa' créée")
            
            print("\n" + "="*80)
            print("✅ Base de données vérifiée et réparée avec succès!")
            print("="*80)
            print("\n💡 Vous pouvez maintenant redémarrer l'application")
            print()
            
        except Exception as e:
            print("\n" + "="*80)
            print("❌ Erreur lors de la réparation de la base de données")
            print("="*80)
            print(f"\nErreur: {e}")
            print("\n💡 Vérifiez que:")
            print("   - PostgreSQL est en cours d'exécution")
            print("   - Les variables d'environnement DATABASE_URL ou PG* sont correctes")
            print("   - L'utilisateur a les permissions nécessaires")
            print()
            raise

if __name__ == '__main__':
    check_and_fix_database()
