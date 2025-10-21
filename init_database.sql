-- Database Initialization Script for Villa Sales Platform
-- Script d'Initialisation de Base de Données pour Plateforme de Vente de Villas

-- Create database (if not exists)
-- Note: Run this as postgres superuser or skip if database already exists
-- Créer la base de données (si elle n'existe pas)
-- Note : Exécuter en tant que superutilisateur postgres ou ignorer si la base existe déjà

-- CREATE DATABASE villa_sales;
-- \c villa_sales

-- Create villa table
-- Créer la table villa
CREATE TABLE IF NOT EXISTS villa (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    price DECIMAL(15, 2),
    location VARCHAR(200),
    area DECIMAL(10, 2),
    land_area DECIMAL(10, 2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT,
    features TEXT,
    equipment TEXT,
    investment_benefits TEXT,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_website VARCHAR(200),
    images TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create update trigger for updated_at column
-- Créer le trigger de mise à jour pour la colonne updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_villa_updated_at ON villa;

CREATE TRIGGER update_villa_updated_at 
    BEFORE UPDATE ON villa 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better performance
-- Créer des index pour meilleures performances
CREATE INDEX IF NOT EXISTS idx_villa_created_at ON villa(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_villa_price ON villa(price);
CREATE INDEX IF NOT EXISTS idx_villa_location ON villa(location);

-- Success message
-- Message de succès
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully! / Base de données initialisée avec succès !';
    RAISE NOTICE 'Table "villa" created with triggers and indexes.';
    RAISE NOTICE 'Table "villa" créée avec triggers et index.';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps / Prochaines étapes :';
    RAISE NOTICE '1. Create static/uploads directory / Créer le répertoire static/uploads';
    RAISE NOTICE '2. Configure .env file / Configurer le fichier .env';
    RAISE NOTICE '3. Run the application / Lancer l''application : python app.py';
END $$;
