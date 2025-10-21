-- ============================================================
-- Script d'initialisation de la base de données PostgreSQL
-- Villa à Vendre Marrakech - Immobilier de Luxe
-- ============================================================
-- 
-- Ce script crée la table villa avec toutes les colonnes nécessaires,
-- les triggers pour updated_at et les index pour optimiser les performances.
--
-- UTILISATION:
-- psql -U postgres -d villa_sales -f init_database.sql
-- ou
-- sudo -u postgres psql villa_sales < init_database.sql
--
-- ⚠️  IMPORTANT: Ce script est maintenu pour compatibilité.
--     Pour VPS, utilisez plutôt le script Python automatique:
--     python fix_database.py
--
-- ============================================================

-- Supprimer la table si elle existe (attention: perte de données!)
-- DROP TABLE IF EXISTS villa CASCADE;

-- Créer la table villa avec toutes les colonnes (correspondant au modèle SQLAlchemy)
CREATE TABLE IF NOT EXISTS villa (
    -- Identifiant et référence
    id SERIAL PRIMARY KEY,
    reference VARCHAR(50) UNIQUE NOT NULL,
    
    -- Informations principales
    title VARCHAR(200) NOT NULL,
    price INTEGER NOT NULL,
    location VARCHAR(200) NOT NULL,
    distance_city VARCHAR(100),
    description TEXT NOT NULL,
    
    -- Caractéristiques techniques
    terrain_area INTEGER,
    built_area INTEGER,
    bedrooms INTEGER,
    pool_size VARCHAR(50),
    
    -- Détails et équipements
    features TEXT,
    equipment TEXT,
    business_info TEXT,
    investment_benefits TEXT,
    documents TEXT,
    
    -- Médias
    images TEXT,
    
    -- Contact
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_website VARCHAR(200),
    
    -- Statut et dates
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Fonction pour mettre à jour automatiquement updated_at
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- Trigger pour appeler la fonction avant chaque UPDATE
-- ============================================================

DROP TRIGGER IF EXISTS update_villa_updated_at ON villa;

CREATE TRIGGER update_villa_updated_at
    BEFORE UPDATE ON villa
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- Index pour optimiser les performances
-- ============================================================

-- Index sur created_at pour trier par date de création
CREATE INDEX IF NOT EXISTS idx_villa_created_at ON villa(created_at);

-- Index sur price pour filtrer par prix
CREATE INDEX IF NOT EXISTS idx_villa_price ON villa(price);

-- Index sur location pour rechercher par localisation
CREATE INDEX IF NOT EXISTS idx_villa_location ON villa(location);

-- Index sur is_active pour filtrer les villas actives
CREATE INDEX IF NOT EXISTS idx_villa_is_active ON villa(is_active);

-- Index sur reference pour recherche rapide
CREATE INDEX IF NOT EXISTS idx_villa_reference ON villa(reference);

-- ============================================================
-- Commentaires sur la table et les colonnes
-- ============================================================

COMMENT ON TABLE villa IS 'Table principale contenant toutes les villas à vendre';
COMMENT ON COLUMN villa.reference IS 'Référence unique de la villa (ex: VILLA-2025-001)';
COMMENT ON COLUMN villa.title IS 'Titre de l''annonce de la villa';
COMMENT ON COLUMN villa.price IS 'Prix de vente en MAD (Dirhams marocains)';
COMMENT ON COLUMN villa.location IS 'Localisation de la villa à Marrakech';
COMMENT ON COLUMN villa.distance_city IS 'Distance depuis le centre-ville';
COMMENT ON COLUMN villa.description IS 'Description détaillée de la villa';
COMMENT ON COLUMN villa.terrain_area IS 'Surface du terrain en m²';
COMMENT ON COLUMN villa.built_area IS 'Surface construite en m²';
COMMENT ON COLUMN villa.bedrooms IS 'Nombre de chambres';
COMMENT ON COLUMN villa.pool_size IS 'Dimensions de la piscine';
COMMENT ON COLUMN villa.features IS 'Caractéristiques principales';
COMMENT ON COLUMN villa.equipment IS 'Équipements et installations';
COMMENT ON COLUMN villa.business_info IS 'Informations commerciales';
COMMENT ON COLUMN villa.investment_benefits IS 'Avantages de l''investissement';
COMMENT ON COLUMN villa.documents IS 'Documents disponibles';
COMMENT ON COLUMN villa.images IS 'JSON array des chemins des images';
COMMENT ON COLUMN villa.contact_phone IS 'Numéro de téléphone de contact (WhatsApp)';
COMMENT ON COLUMN villa.contact_email IS 'Email de contact';
COMMENT ON COLUMN villa.contact_website IS 'Site web (optionnel)';
COMMENT ON COLUMN villa.is_active IS 'Indique si la villa est active (visible)';
COMMENT ON COLUMN villa.created_at IS 'Date de création de l''enregistrement';
COMMENT ON COLUMN villa.updated_at IS 'Date de dernière modification';

-- ============================================================
-- Vérification et affichage du résultat
-- ============================================================

DO $$
DECLARE
    col_count INTEGER;
    rec_count INTEGER;
BEGIN
    -- Compter les colonnes
    SELECT COUNT(*) INTO col_count
    FROM information_schema.columns
    WHERE table_name = 'villa';
    
    -- Compter les enregistrements
    SELECT COUNT(*) INTO rec_count FROM villa;
    
    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS !';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Structure de la base de données:';
    RAISE NOTICE '  • Table villa créée';
    RAISE NOTICE '  • % colonnes configurées', col_count;
    RAISE NOTICE '  • 5 index de performance';
    RAISE NOTICE '  • 1 trigger automatique (updated_at)';
    RAISE NOTICE '';
    RAISE NOTICE 'Données:';
    RAISE NOTICE '  • % villas enregistrées', rec_count;
    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'PROCHAINES ÉTAPES:';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';
    RAISE NOTICE '1. Créer le répertoire uploads:';
    RAISE NOTICE '   mkdir -p static/uploads';
    RAISE NOTICE '   chmod 775 static/uploads';
    RAISE NOTICE '';
    RAISE NOTICE '2. Configurer les variables d''environnement (.env):';
    RAISE NOTICE '   cp .env.example .env';
    RAISE NOTICE '   nano .env  # Éditer avec vos valeurs';
    RAISE NOTICE '';
    RAISE NOTICE '3. Lancer l''application:';
    RAISE NOTICE '   python app.py';
    RAISE NOTICE '   # ou pour production:';
    RAISE NOTICE '   gunicorn --bind 0.0.0.0:8000 --workers 4 app:app';
    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';
END $$;

-- ============================================================
-- Exemple de données (optionnel - décommentez pour tester)
-- ============================================================

/*
INSERT INTO villa (
    reference, title, price, location, distance_city, description,
    terrain_area, built_area, bedrooms, pool_size,
    features, equipment, investment_benefits,
    contact_phone, contact_email,
    images, is_active
) VALUES (
    'VILLA-2025-001',
    'Villa de Luxe avec Piscine - Route de Fès',
    4500000,
    'Route de Fès, Marrakech',
    '10 minutes du centre-ville',
    'Magnifique villa de prestige située sur la Route de Fès, dans un quartier calme et résidentiel. Cette propriété exceptionnelle allie modernité et confort avec ses espaces généreux et ses finitions haut de gamme.',
    500,
    350,
    5,
    '12m x 6m',
    E'Piscine chauffée\nArchitecture moderne\nJardin paysagé\nVue panoramique\nTerrasse spacieuse',
    E'Climatisation centrale\nChauffage au sol\nCuisine équipée Siemens\nDomotique complète\nPortail automatique',
    E'Emplacement stratégique\nFort potentiel de valorisation\nQuartier résidentiel en développement\nProximité écoles internationales',
    '+212 6 XX XX XX XX',
    'contact@villaavendremarrakech.com',
    '[]',
    TRUE
);

RAISE NOTICE '📝 Exemple de villa inséré pour test';
*/

-- ============================================================
-- FIN DU SCRIPT
-- ============================================================
