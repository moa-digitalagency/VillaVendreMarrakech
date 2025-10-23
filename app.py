"""
Application Flask - Villa à Vendre Marrakech

Application web complète pour la vente de villas de luxe à Marrakech.
Comprend une interface publique pour les visiteurs et un panneau d'administration
sécurisé avec fonctionnalités d'intelligence artificielle.

Fonctionnalités principales:
- Page publique responsive avec galerie photos et informations détaillées
- Panneau d'administration sécurisé par mot de passe
- Extraction automatique de données depuis PDF via IA (Claude 3.5 Sonnet)
- Amélioration de texte via IA (Mistral Large)
- Upload et optimisation automatique d'images
- Base de données PostgreSQL pour le stockage des données

Développé par: MOA Digital Agency LLC
Développeur: Aisance KALONJI
Email: moa@myoneart.com
Web: www.myoneart.com
"""

# ========== IMPORTS ==========
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory, g
from flask_cors import CORS
from models import db, Villa
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import json
from PIL import Image
import time
import uuid
from PyPDF2 import PdfReader
from functools import wraps
import shutil

# ========== CONFIGURATION DE L'APPLICATION ==========
app = Flask(__name__)
CORS(app)  # Active CORS pour permettre les requêtes cross-origin

# ========== CONFIGURATION DE LA BASE DE DONNÉES ==========
# Configure database URL
# Essaie DATABASE_URL en premier, sinon construit l'URL depuis les variables PG* individuelles
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    # Build DATABASE_URL from individual PostgreSQL variables (for VPS deployment)
    pg_user = os.environ.get('PGUSER', 'postgres')
    pg_password = os.environ.get('PGPASSWORD', '')
    pg_host = os.environ.get('PGHOST', 'localhost')
    pg_port = os.environ.get('PGPORT', '5432')
    pg_database = os.environ.get('PGDATABASE', 'villa_sales')
    
    if pg_password:
        database_url = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
    else:
        database_url = f'postgresql://{pg_user}@{pg_host}:{pg_port}/{pg_database}'
    
    print(f"Built DATABASE_URL from PG* variables: postgresql://{pg_user}:***@{pg_host}:{pg_port}/{pg_database}")

# Fix for postgres:// vs postgresql:// (Heroku compatibility)
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.environ.get("SESSION_SECRET")

# Extensions de fichiers autorisées pour les uploads d'images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Mot de passe admin configurable via variable d'environnement
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '@4dm1n')

# Initialise SQLAlchemy avec l'application Flask
db.init_app(app)

# Crée le dossier d'upload s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ========== GESTION MULTILINGUE ==========

# Dictionnaire de traductions pour l'interface
TRANSLATIONS = {
    'fr': {
        'no_villa_available': 'Aucune Villa Disponible',
        'villa_not_configured': 'Les informations de la villa ne sont pas encore configurées.',
        'access_admin': 'Accéder à l\'administration',
        'luxury_villa': 'Villa de Prestige à Marrakech',
        'price': 'Prix',
        'location': 'Localisation',
        'distance_from_city': 'Distance du centre-ville',
        'terrain_area': 'Surface terrain',
        'built_area': 'Surface construite',
        'bedrooms': 'Chambres',
        'pool': 'Piscine',
        'features': 'Caractéristiques',
        'equipment': 'Équipements',
        'business_info': 'Exploitation commerciale',
        'investment': 'Investissement',
        'documents': 'Documents',
        'contact': 'Contact',
        'phone': 'Téléphone',
        'email': 'Email',
        'website': 'Site web',
        'login': 'Connexion',
        'password': 'Mot de passe',
        'sign_in': 'Se connecter',
        'incorrect_password': 'Mot de passe incorrect',
        'admin_panel': 'Panneau d\'administration',
        'logout': 'Déconnexion',
        'save': 'Enregistrer',
        'reference': 'Référence',
        'title': 'Titre',
        'description': 'Description',
        'upload_images': 'Télécharger des images',
        'upload_pdf': 'Télécharger un PDF',
        'enhance_with_ai': 'Améliorer avec l\'IA',
        'reset': 'Réinitialiser',
        'gallery': 'Galerie'
    },
    'en': {
        'no_villa_available': 'No Villa Available',
        'villa_not_configured': 'Villa information is not yet configured.',
        'access_admin': 'Access Administration',
        'luxury_villa': 'Luxury Villa in Marrakech',
        'price': 'Price',
        'location': 'Location',
        'distance_from_city': 'Distance from city center',
        'terrain_area': 'Land area',
        'built_area': 'Built area',
        'bedrooms': 'Bedrooms',
        'pool': 'Pool',
        'features': 'Features',
        'equipment': 'Equipment',
        'business_info': 'Business Information',
        'investment': 'Investment',
        'documents': 'Documents',
        'contact': 'Contact',
        'phone': 'Phone',
        'email': 'Email',
        'website': 'Website',
        'login': 'Login',
        'password': 'Password',
        'sign_in': 'Sign In',
        'incorrect_password': 'Incorrect password',
        'admin_panel': 'Admin Panel',
        'logout': 'Logout',
        'save': 'Save',
        'reference': 'Reference',
        'title': 'Title',
        'description': 'Description',
        'upload_images': 'Upload Images',
        'upload_pdf': 'Upload PDF',
        'enhance_with_ai': 'Enhance with AI',
        'reset': 'Reset',
        'gallery': 'Gallery'
    }
}

def get_browser_language():
    """Détecte la langue du navigateur depuis l'en-tête Accept-Language."""
    accept_language = request.headers.get('Accept-Language', '')
    if accept_language:
        languages = accept_language.split(',')
        for lang in languages:
            lang_code = lang.split(';')[0].strip().lower()
            if lang_code.startswith('fr'):
                return 'fr'
            elif lang_code.startswith('en'):
                return 'en'
    return 'fr'

def get_current_language():
    """Retourne la langue courante (depuis la session ou détection auto)."""
    if 'language' not in session:
        session['language'] = get_browser_language()
    return session.get('language', 'fr')

def get_translations():
    """Retourne les traductions pour la langue courante."""
    lang = get_current_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr'])

@app.before_request
def before_request():
    """Exécuté avant chaque requête pour initialiser la langue."""
    g.lang = get_current_language()
    g.t = get_translations()

@app.route('/set-language/<lang>')
def set_language(lang):
    """Change la langue de l'interface."""
    if lang in ['fr', 'en']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

# ========== VALIDATION DES VARIABLES D'ENVIRONNEMENT ==========
def validate_required_env_vars():
    """
    Vérifie que toutes les variables d'environnement obligatoires sont définies.
    Arrête l'application avec un message clair si une variable manque.
    """
    required_vars = {
        'OPENROUTER_API_KEY': 'Clé API OpenRouter requise pour les fonctionnalités IA (extraction PDF, amélioration de texte)',
        'SESSION_SECRET': 'Clé secrète de session requise pour la sécurité de l\'application'
    }
    
    missing_vars = []
    for var_name, description in required_vars.items():
        if not os.environ.get(var_name):
            missing_vars.append(f"  ❌ {var_name}: {description}")
    
    if missing_vars:
        print("\n" + "="*80)
        print("🚨 ERREUR: Variables d'environnement manquantes")
        print("="*80)
        print("\nLes variables suivantes sont obligatoires mais non définies:\n")
        for var in missing_vars:
            print(var)
        print("\n" + "="*80)
        print("💡 Configurez ces variables dans les Secrets Replit")
        print("="*80 + "\n")
        raise SystemExit("Application arrêtée: variables d'environnement manquantes")
    
    print("✅ All required environment variables are configured")

# ========== INITIALISATION DE LA BASE DE DONNÉES ==========
def init_db():
    """Initialize database tables if they don't exist"""
    with app.app_context():
        try:
            # Import all models to ensure they're registered
            from models import Villa
            
            # Create all tables
            db.create_all()
            print("✅ Database tables initialized successfully")
            
            # Try to count villas, but don't fail if there's an error
            try:
                villa_count = Villa.query.count()
                print(f"📊 Current villas in database: {villa_count}")
            except Exception as count_error:
                print(f"⚠️  Could not count villas (table may need migration): {count_error}")
                print("💡 Run 'python fix_database.py' to fix missing columns")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            print("⚠️  Make sure PostgreSQL is running and credentials are correct")
            print("💡 If you see 'column does not exist', run: python fix_database.py")
            # Don't raise - allow app to continue
            pass

# Valide les variables d'environnement requises au démarrage
validate_required_env_vars()

# Initialise la base de données au démarrage de l'application
init_db()

# ========== DÉCORATEURS ET FONCTIONS UTILITAIRES ==========

def login_required(f):
    """
    Décorateur pour protéger les routes admin.
    Redirige vers la page de login si l'utilisateur n'est pas authentifié.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_image(filepath):
    """
    Optimise une image pour le web:
    - Convertit en RGB si nécessaire
    - Redimensionne à max 1920x1080
    - Convertit en JPEG avec qualité 85
    - Supprime le fichier original
    """
    try:
        img = Image.open(filepath)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        base, ext = os.path.splitext(filepath)
        new_filepath = base + '.jpg'
        img.save(new_filepath, 'JPEG', quality=85, optimize=True)
        
        if filepath != new_filepath and os.path.exists(filepath):
            os.remove(filepath)
        
        return new_filepath
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return filepath

def extract_text_from_pdf(pdf_path):
    """Extrait tout le texte d'un fichier PDF en utilisant PyPDF2."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def extract_villa_data_with_ai(pdf_text):
    """
    Extrait les données structurées d'une villa depuis du texte PDF via IA.
    Utilise Claude 3.5 Sonnet via OpenRouter pour analyser le texte et
    extraire toutes les informations dans un format JSON structuré.
    Temps d'exécution: 60-90 secondes.
    """
    openrouter_key = os.environ.get('OPENROUTER_API_KEY')
    if not openrouter_key:
        return None
    
    try:
        prompt = f"""Analyse ce texte extrait d'un PDF de vente de villa et extrait les informations structurées.

Texte du PDF:
{pdf_text}

Réponds UNIQUEMENT avec un objet JSON valide contenant ces champs (mets des valeurs vides "" ou 0 si l'information n'est pas disponible):
{{
    "reference": "référence de la villa",
    "title": "titre court et attractif de la villa",
    "price": nombre entier du prix en euros,
    "location": "ville ou région",
    "distance_city": "distance depuis la ville principale",
    "description": "description complète et attractive",
    "terrain_area": nombre entier de la surface du terrain en m²,
    "built_area": nombre entier de la surface construite en m²,
    "bedrooms": nombre de chambres/suites,
    "pool_size": "dimensions de la piscine",
    "features": "liste des caractéristiques principales, une par ligne",
    "equipment": "liste des équipements et confort, une par ligne",
    "business_info": "informations sur l'exploitation commerciale",
    "investment_benefits": "atouts pour investisseurs",
    "documents": "documents disponibles",
    "contact_phone": "numéro de téléphone",
    "contact_email": "email",
    "contact_website": "site web"
}}"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://villaeden.replit.app",
                "X-Title": "Villa Eden Admin"
            },
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            return data
        else:
            print(f"OpenRouter API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"AI extraction error: {e}")
        return None

def enhance_text_with_ai(text, context=""):
    """
    Améliore un texte via IA pour l'immobilier de luxe.
    Utilise Mistral Large via OpenRouter pour améliorer le texte
    en français avec un style professionnel adapté au luxe.
    """
    openrouter_key = os.environ.get('OPENROUTER_API_KEY')
    if not openrouter_key:
        return text
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://villaeden.replit.app",
                "X-Title": "Villa Eden Admin"
            },
            json={
                "model": "mistralai/mistral-large-latest",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Améliore ce texte pour une annonce immobilière de luxe en français. {context}\n\nTexte: {text}\n\nRéponds uniquement avec le texte amélioré, sans explication ni commentaire."
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"OpenRouter API error: {response.status_code}")
            return text
    except Exception as e:
        print(f"AI enhancement error: {e}")
        return text

def translate_villa_data_to_english(french_data):
    """
    Traduit automatiquement toutes les données d'une villa du français vers l'anglais.
    Utilise Claude 3.5 Sonnet via OpenRouter pour des traductions de haute qualité
    adaptées au contexte de l'immobilier de luxe à Marrakech.
    
    Args:
        french_data: Dictionnaire contenant les données en français
    
    Returns:
        Dictionnaire avec les mêmes clés mais suffixées par _en avec les traductions
    """
    openrouter_key = os.environ.get('OPENROUTER_API_KEY')
    if not openrouter_key:
        return {}
    
    try:
        fields_to_translate = {
            'title': french_data.get('title', ''),
            'description': french_data.get('description', ''),
            'features': french_data.get('features', ''),
            'equipment': french_data.get('equipment', ''),
            'business_info': french_data.get('business_info', ''),
            'investment_benefits': french_data.get('investment_benefits', ''),
            'documents': french_data.get('documents', '')
        }
        
        non_empty_fields = {k: v for k, v in fields_to_translate.items() if v and v.strip()}
        
        if not non_empty_fields:
            return {}
        
        prompt = f"""Translate the following luxury villa real estate content from French to English. 
Maintain the professional, luxurious tone appropriate for high-end Marrakech real estate.
Preserve all line breaks and formatting exactly as shown.

French content to translate:
{json.dumps(non_empty_fields, ensure_ascii=False, indent=2)}

Respond ONLY with a valid JSON object containing the translations, using the same keys with "_en" suffix:
{{
    "title_en": "English translation of title",
    "description_en": "English translation of description",
    "features_en": "English translation of features (preserve line breaks)",
    "equipment_en": "English translation of equipment (preserve line breaks)",
    "business_info_en": "English translation of business_info",
    "investment_benefits_en": "English translation of investment_benefits (preserve line breaks)",
    "documents_en": "English translation of documents"
}}

Only include fields that were provided in the French content."""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://villaeden.replit.app",
                "X-Title": "Villa Eden Admin - Translation"
            },
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            translations = json.loads(content)
            print(f"✅ Successfully translated {len(translations)} fields to English")
            return translations
        else:
            print(f"OpenRouter translation API error: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Translation error: {e}")
        return {}

# ========== ROUTES PUBLIQUES ==========

@app.route('/')
def index():
    """Page d'accueil publique affichant la villa active."""
    villa = Villa.query.filter_by(is_active=True).first()
    return render_template('index.html', villa=villa)

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

# ========== ROUTES D'AUTHENTIFICATION ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion administrateur avec vérification du mot de passe."""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Mot de passe incorrect')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

# ========== ROUTES ADMIN (PROTÉGÉES) ==========

@app.route('/admin')
@login_required
def admin():
    """Panneau d'administration pour gérer la villa."""
    villa = Villa.query.first()
    return render_template('admin.html', villa=villa)

def safe_int(value, default=0):
    """Convertit une valeur en entier de manière sécurisée, retourne default si échec."""
    try:
        if value is None or value == '':
            return default
        return int(value)
    except (ValueError, TypeError):
        return default

@app.route('/admin/save', methods=['POST'])
@login_required
def admin_save():
    """Enregistre ou met à jour les données de la villa."""
    data = request.form
    
    try:
        villa = Villa.query.first()
        if not villa:
            villa = Villa()
            db.session.add(villa)
        
        villa.reference = data.get('reference', '')
        villa.title = data.get('title', '')
        villa.title_en = data.get('title_en', '')
        villa.price = safe_int(data.get('price'), 0)
        villa.location = data.get('location', '')
        villa.distance_city = data.get('distance_city', '')
        villa.description = data.get('description', '')
        villa.description_en = data.get('description_en', '')
        villa.terrain_area = safe_int(data.get('terrain_area'), 0)
        villa.built_area = safe_int(data.get('built_area'), 0)
        villa.bedrooms = safe_int(data.get('bedrooms'), 0)
        villa.pool_size = data.get('pool_size', '')
        villa.features = data.get('features', '')
        villa.features_en = data.get('features_en', '')
        villa.equipment = data.get('equipment', '')
        villa.equipment_en = data.get('equipment_en', '')
        villa.business_info = data.get('business_info', '')
        villa.business_info_en = data.get('business_info_en', '')
        villa.investment_benefits = data.get('investment_benefits', '')
        villa.investment_benefits_en = data.get('investment_benefits_en', '')
        villa.documents = data.get('documents', '')
        villa.documents_en = data.get('documents_en', '')
        villa.contact_phone = data.get('contact_phone', '')
        villa.contact_email = data.get('contact_email', '')
        villa.contact_website = data.get('contact_website', '')
        villa.is_active = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Villa enregistrée avec succès !'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la sauvegarde: {str(e)}'
        }), 500

@app.route('/admin/upload', methods=['POST'])
@login_required
def upload_image():
    """Upload et optimise une image de villa."""
    if 'image' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        timestamp = str(int(time.time() * 1000))
        base_name = os.path.splitext(original_filename)[0]
        temp_filename = f"{timestamp}_{unique_id}_{base_name}.tmp"
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        file.save(temp_filepath)
        
        final_filepath = optimize_image(temp_filepath)
        final_filename = os.path.basename(final_filepath)
        
        villa = Villa.query.first()
        if villa:
            images = villa.get_images_list()
            images.append(final_filename)
            villa.set_images_list(images)
            db.session.commit()
        
        return jsonify({'success': True, 'filename': final_filename})
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/admin/delete-image/<filename>', methods=['POST'])
@login_required
def delete_image(filename):
    """Supprime une image de la base de données et du système de fichiers."""
    villa = Villa.query.first()
    if villa:
        images = villa.get_images_list()
        if filename in images:
            images.remove(filename)
            villa.set_images_list(images)
            db.session.commit()
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return jsonify({'success': True})
    
    return jsonify({'error': 'Image not found'}), 404

@app.route('/admin/upload-pdf', methods=['POST'])
@login_required
def upload_pdf():
    """
    Upload un PDF, extrait le texte et utilise l'IA pour extraire les données de villa.
    Traduit automatiquement le contenu français vers l'anglais pour remplir les deux langues.
    """
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file'}), 400
    
    file = request.files['pdf']
    if not file.filename or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    temp_filepath = None
    try:
        temp_filename = f"temp_{uuid.uuid4()}.pdf"
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        file.save(temp_filepath)
        
        print("📄 Extracting text from PDF...")
        pdf_text = extract_text_from_pdf(temp_filepath)
        
        os.remove(temp_filepath)
        
        if not pdf_text:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        print("🤖 Extracting French villa data with AI...")
        villa_data = extract_villa_data_with_ai(pdf_text)
        
        if not villa_data:
            return jsonify({'error': 'Could not extract villa data. Make sure OPENROUTER_API_KEY is configured.'}), 400
        
        print("🌍 Translating French content to English...")
        english_translations = translate_villa_data_to_english(villa_data)
        
        if english_translations:
            villa_data.update(english_translations)
            print(f"✅ Added {len(english_translations)} English translations to villa data")
        else:
            print("⚠️  Translation failed or returned no data - English fields will be empty")
        
        return jsonify({'success': True, 'data': villa_data})
    
    except Exception as e:
        if temp_filepath and os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

@app.route('/api/enhance', methods=['POST'])
@login_required
def enhance():
    """API pour améliorer un texte via IA (Mistral Large)."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    text = data.get('text', '')
    field = data.get('field', '')
    
    enhanced = enhance_text_with_ai(text, f"Contexte: {field}")
    
    return jsonify({'enhanced': enhanced})

@app.route('/admin/reset', methods=['POST'])
@login_required
def reset_data():
    """Réinitialise complètement: supprime toutes les données et images."""
    try:
        confirmation = request.form.get('confirmation')
        if confirmation != 'SUPPRIMER':
            return jsonify({'error': 'Confirmation incorrecte'}), 400
        
        Villa.query.delete()
        db.session.commit()
        
        upload_dir = app.config['UPLOAD_FOLDER']
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                file_path = os.path.join(upload_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        return jsonify({'success': True, 'message': 'Toutes les données ont été supprimées'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/admin/edit-website')
@login_required
def edit_website():
    """Page d'édition des textes personnalisables du site web."""
    villa = Villa.query.first()
    return render_template('edit_website.html', villa=villa)

@app.route('/admin/save-website-text', methods=['POST'])
@login_required
def save_website_text():
    """Enregistre les textes personnalisés du site web."""
    try:
        villa = Villa.query.first()
        if not villa:
            return jsonify({'success': False, 'error': 'Aucune villa trouvée. Créez d\'abord une villa.'}), 404
        
        # French texts
        villa.hero_subtitle_fr = request.form.get('hero_subtitle_fr', '')
        villa.contact_button_fr = request.form.get('contact_button_fr', '')
        villa.description_title_fr = request.form.get('description_title_fr', '')
        villa.whatsapp_button_fr = request.form.get('whatsapp_button_fr', '')
        villa.why_choose_title_fr = request.form.get('why_choose_title_fr', '')
        villa.why_card1_title_fr = request.form.get('why_card1_title_fr', '')
        villa.why_card1_desc_fr = request.form.get('why_card1_desc_fr', '')
        villa.why_card2_title_fr = request.form.get('why_card2_title_fr', '')
        villa.why_card2_desc_fr = request.form.get('why_card2_desc_fr', '')
        villa.why_card3_title_fr = request.form.get('why_card3_title_fr', '')
        villa.why_card3_desc_fr = request.form.get('why_card3_desc_fr', '')
        villa.why_card4_title_fr = request.form.get('why_card4_title_fr', '')
        villa.why_card4_desc_fr = request.form.get('why_card4_desc_fr', '')
        villa.contact_title_fr = request.form.get('contact_title_fr', '')
        villa.contact_subtitle_fr = request.form.get('contact_subtitle_fr', '')
        
        # English texts
        villa.hero_subtitle_en = request.form.get('hero_subtitle_en', '')
        villa.contact_button_en = request.form.get('contact_button_en', '')
        villa.description_title_en = request.form.get('description_title_en', '')
        villa.whatsapp_button_en = request.form.get('whatsapp_button_en', '')
        villa.why_choose_title_en = request.form.get('why_choose_title_en', '')
        villa.why_card1_title_en = request.form.get('why_card1_title_en', '')
        villa.why_card1_desc_en = request.form.get('why_card1_desc_en', '')
        villa.why_card2_title_en = request.form.get('why_card2_title_en', '')
        villa.why_card2_desc_en = request.form.get('why_card2_desc_en', '')
        villa.why_card3_title_en = request.form.get('why_card3_title_en', '')
        villa.why_card3_desc_en = request.form.get('why_card3_desc_en', '')
        villa.why_card4_title_en = request.form.get('why_card4_title_en', '')
        villa.why_card4_desc_en = request.form.get('why_card4_desc_en', '')
        villa.contact_title_en = request.form.get('contact_title_en', '')
        villa.contact_subtitle_en = request.form.get('contact_subtitle_en', '')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Textes enregistrés avec succès !'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Erreur lors de la sauvegarde: {str(e)}'}), 500

# ========== API JSON ==========

@app.route('/api/villa', methods=['GET'])
def get_villa():
    """API JSON pour récupérer les données de la villa active."""
    villa = Villa.query.filter_by(is_active=True).first()
    if villa:
        return jsonify(villa.to_dict())
    return jsonify({'error': 'No villa found'}), 404

# ========== POINT D'ENTRÉE DÉVELOPPEMENT ==========
if __name__ == '__main__':
    # Crée les tables de la base de données si elles n'existent pas
    with app.app_context():
        db.create_all()
    # Lance le serveur de développement Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
