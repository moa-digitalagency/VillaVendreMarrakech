#!/usr/bin/env python3
"""
Script de correction/migration automatique de la base de données
Ajoute toutes les colonnes manquantes à la table villa
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la connexion à la base de données
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    # Construire depuis les variables PG*
    pg_user = os.environ.get('PGUSER', 'postgres')
    pg_password = os.environ.get('PGPASSWORD', '')
    pg_host = os.environ.get('PGHOST', 'localhost')
    pg_port = os.environ.get('PGPORT', '5432')
    pg_database = os.environ.get('PGDATABASE', 'villa_sales')
    
    if pg_password:
        database_url = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
    else:
        database_url = f'postgresql://{pg_user}@{pg_host}:{pg_port}/{pg_database}'

# Fix pour postgres:// vs postgresql://
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

print(f"🔗 Connexion à la base de données...")
print(f"   Host: {os.environ.get('PGHOST', 'localhost')}")
print(f"   Database: {os.environ.get('PGDATABASE', 'villa_sales')}")
print()

# Créer la connexion
try:
    engine = create_engine(database_url)
    conn = engine.connect()
    print("✅ Connexion établie avec succès\n")
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
    sys.exit(1)

# Définition de toutes les colonnes requises (correspondant au modèle SQLAlchemy)
REQUIRED_COLUMNS = {
    'id': 'SERIAL PRIMARY KEY',
    'reference': 'VARCHAR(50) UNIQUE NOT NULL',
    'title': 'VARCHAR(200) NOT NULL',
    'price': 'INTEGER NOT NULL',
    'location': 'VARCHAR(200) NOT NULL',
    'distance_city': 'VARCHAR(100)',
    'description': 'TEXT NOT NULL',
    'terrain_area': 'INTEGER',
    'built_area': 'INTEGER',
    'bedrooms': 'INTEGER',
    'pool_size': 'VARCHAR(50)',
    'features': 'TEXT',
    'equipment': 'TEXT',
    'business_info': 'TEXT',
    'investment_benefits': 'TEXT',
    'documents': 'TEXT',
    'images': 'TEXT',
    'contact_phone': 'VARCHAR(50)',
    'contact_email': 'VARCHAR(100)',
    'contact_website': 'VARCHAR(200)',
    'is_active': 'BOOLEAN DEFAULT TRUE',
    'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
}

def check_table_exists():
    """Vérifie si la table villa existe"""
    result = conn.execute(text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'villa'
        );
    """))
    return result.scalar()

def create_table():
    """Crée la table villa si elle n'existe pas"""
    print("📋 Création de la table villa...")
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS villa (
        id SERIAL PRIMARY KEY,
        reference VARCHAR(50) UNIQUE NOT NULL,
        title VARCHAR(200) NOT NULL,
        price INTEGER NOT NULL,
        location VARCHAR(200) NOT NULL,
        distance_city VARCHAR(100),
        description TEXT NOT NULL,
        terrain_area INTEGER,
        built_area INTEGER,
        bedrooms INTEGER,
        pool_size VARCHAR(50),
        features TEXT,
        equipment TEXT,
        business_info TEXT,
        investment_benefits TEXT,
        documents TEXT,
        images TEXT,
        contact_phone VARCHAR(50),
        contact_email VARCHAR(100),
        contact_website VARCHAR(200),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    conn.execute(text(create_table_sql))
    conn.commit()
    print("✅ Table villa créée\n")

def get_existing_columns():
    """Récupère la liste des colonnes existantes"""
    inspector = inspect(engine)
    columns = inspector.get_columns('villa')
    return {col['name']: col for col in columns}

def add_missing_columns():
    """Ajoute les colonnes manquantes"""
    existing_cols = get_existing_columns()
    existing_col_names = set(existing_cols.keys())
    required_col_names = set(REQUIRED_COLUMNS.keys())
    
    missing_cols = required_col_names - existing_col_names
    
    if not missing_cols:
        print("✅ Toutes les colonnes sont présentes !\n")
        return
    
    print(f"⚠️  Colonnes manquantes détectées: {len(missing_cols)}")
    print(f"   {', '.join(sorted(missing_cols))}\n")
    
    for col_name in sorted(missing_cols):
        col_type_full = REQUIRED_COLUMNS[col_name]
        
        # Extraire le type sans les contraintes NOT NULL, UNIQUE, etc.
        # Pour les colonnes manquantes, on ajoute sans contraintes strictes
        col_type = col_type_full.split('NOT NULL')[0].split('UNIQUE')[0].split('DEFAULT')[0].strip()
        
        # Construire la commande ALTER TABLE
        alter_sql = f"ALTER TABLE villa ADD COLUMN IF NOT EXISTS {col_name} {col_type};"
        
        # Si il y a une valeur par défaut, l'extraire
        if 'DEFAULT' in col_type_full:
            default_part = 'DEFAULT ' + col_type_full.split('DEFAULT')[1].strip()
            alter_sql = f"ALTER TABLE villa ADD COLUMN IF NOT EXISTS {col_name} {col_type} {default_part};"
        
        try:
            conn.execute(text(alter_sql))
            conn.commit()
            print(f"✅ Ajouté: {col_name} ({col_type})")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'ajout de {col_name}: {e}")
            # Continuer avec les autres colonnes même en cas d'erreur
    
    print()

def create_triggers():
    """Crée les triggers pour updated_at"""
    print("⚙️  Création des triggers...")
    
    # Fonction pour mettre à jour updated_at
    function_sql = """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    
    # Trigger
    trigger_sql = """
    DROP TRIGGER IF EXISTS update_villa_updated_at ON villa;
    CREATE TRIGGER update_villa_updated_at 
        BEFORE UPDATE ON villa 
        FOR EACH ROW 
        EXECUTE FUNCTION update_updated_at_column();
    """
    
    try:
        conn.execute(text(function_sql))
        conn.execute(text(trigger_sql))
        conn.commit()
        print("✅ Triggers créés avec succès\n")
    except Exception as e:
        print(f"⚠️  Erreur lors de la création des triggers: {e}\n")

def create_indexes():
    """Crée les index pour optimiser les performances"""
    print("🚀 Création des index...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_villa_created_at ON villa(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_villa_price ON villa(price);",
        "CREATE INDEX IF NOT EXISTS idx_villa_location ON villa(location);"
    ]
    
    for index_sql in indexes:
        try:
            conn.execute(text(index_sql))
            conn.commit()
            print(f"✅ {index_sql.split('idx_')[1].split(' ')[0]}")
        except Exception as e:
            print(f"⚠️  Erreur: {e}")
    
    print()

def show_table_info():
    """Affiche les informations sur la table"""
    result = conn.execute(text("SELECT COUNT(*) FROM villa;"))
    count = result.scalar()
    
    columns = get_existing_columns()
    
    print("=" * 60)
    print("📊 RÉSUMÉ DE LA BASE DE DONNÉES")
    print("=" * 60)
    print(f"Table: villa")
    print(f"Nombre de colonnes: {len(columns)}")
    print(f"Nombre de villas: {count}")
    print("\nColonnes présentes:")
    for col_name in sorted(columns.keys()):
        print(f"  • {col_name}")
    print("=" * 60)
    print()

def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("🔧 SCRIPT DE CORRECTION DE BASE DE DONNÉES")
    print("   Villa à Vendre Marrakech")
    print("=" * 60)
    print()
    
    try:
        # 1. Vérifier/Créer la table
        if not check_table_exists():
            print("⚠️  La table villa n'existe pas\n")
            create_table()
        else:
            print("✅ La table villa existe\n")
        
        # 2. Ajouter les colonnes manquantes
        add_missing_columns()
        
        # 3. Créer les triggers
        create_triggers()
        
        # 4. Créer les index
        create_indexes()
        
        # 5. Afficher le résumé
        show_table_info()
        
        print("✅ CORRECTION TERMINÉE AVEC SUCCÈS !")
        print("🚀 Vous pouvez maintenant lancer votre application:\n")
        print("   python app.py")
        print("   # ou")
        print("   gunicorn --bind 0.0.0.0:8000 --workers 4 app:app\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
