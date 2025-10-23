"""
Migration script to add website text customization columns to the Villa table.
Run this once to add the new columns to existing databases.
"""

import os
from sqlalchemy import create_engine, text

# Get database URL from environment
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    pg_user = os.environ.get('PGUSER', 'postgres')
    pg_password = os.environ.get('PGPASSWORD', '')
    pg_host = os.environ.get('PGHOST', 'localhost')
    pg_port = os.environ.get('PGPORT', '5432')
    pg_database = os.environ.get('PGDATABASE', 'villa_sales')
    
    if pg_password:
        database_url = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
    else:
        database_url = f'postgresql://{pg_user}@{pg_host}:{pg_port}/{pg_database}'

# Fix for postgres:// vs postgresql://
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

print(f"Connecting to database...")
engine = create_engine(database_url)

# List of new columns to add
new_columns = [
    ('hero_subtitle_fr', 'VARCHAR(200)'),
    ('hero_subtitle_en', 'VARCHAR(200)'),
    ('contact_button_en', 'VARCHAR(100)'),
    ('description_title_fr', 'VARCHAR(200)'),
    ('description_title_en', 'VARCHAR(200)'),
    ('whatsapp_button_fr', 'VARCHAR(100)'),
    ('whatsapp_button_en', 'VARCHAR(100)'),
    ('why_choose_title_fr', 'VARCHAR(200)'),
    ('why_choose_title_en', 'VARCHAR(200)'),
    ('why_card1_title_fr', 'VARCHAR(200)'),
    ('why_card1_title_en', 'VARCHAR(200)'),
    ('why_card1_desc_fr', 'TEXT'),
    ('why_card1_desc_en', 'TEXT'),
    ('why_card2_title_fr', 'VARCHAR(200)'),
    ('why_card2_title_en', 'VARCHAR(200)'),
    ('why_card2_desc_fr', 'TEXT'),
    ('why_card2_desc_en', 'TEXT'),
    ('why_card3_title_fr', 'VARCHAR(200)'),
    ('why_card3_title_en', 'VARCHAR(200)'),
    ('why_card3_desc_fr', 'TEXT'),
    ('why_card3_desc_en', 'TEXT'),
    ('why_card4_title_fr', 'VARCHAR(200)'),
    ('why_card4_title_en', 'VARCHAR(200)'),
    ('why_card4_desc_fr', 'TEXT'),
    ('why_card4_desc_en', 'TEXT'),
    ('contact_title_fr', 'VARCHAR(200)'),
    ('contact_title_en', 'VARCHAR(200)'),
    ('contact_subtitle_fr', 'VARCHAR(200)'),
    ('contact_subtitle_en', 'VARCHAR(200)'),
]

with engine.connect() as conn:
    for column_name, column_type in new_columns:
        try:
            # Check if column exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='villa' AND column_name=:col_name
            """)
            result = conn.execute(check_query, {"col_name": column_name})
            
            if result.fetchone() is None:
                # Column doesn't exist, add it
                add_column_query = text(f"ALTER TABLE villa ADD COLUMN {column_name} {column_type}")
                conn.execute(add_column_query)
                conn.commit()
                print(f"✅ Added column: {column_name}")
            else:
                print(f"⏭️  Column already exists: {column_name}")
        except Exception as e:
            print(f"❌ Error adding column {column_name}: {e}")
            conn.rollback()

print("\n✅ Migration completed!")
