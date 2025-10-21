from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
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

app = Flask(__name__)
CORS(app)

# Configure database URL
# Try DATABASE_URL first, then build from PG* variables if not available
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
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '@4dm1n')

db.init_app(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database tables automatically on startup
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

# Initialize database on startup
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_image(filepath):
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

@app.route('/')
def index():
    villa = Villa.query.filter_by(is_active=True).first()
    return render_template('index.html', villa=villa)

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/admin')
@login_required
def admin():
    villa = Villa.query.first()
    return render_template('admin.html', villa=villa)

def safe_int(value, default=0):
    try:
        if value is None or value == '':
            return default
        return int(value)
    except (ValueError, TypeError):
        return default

@app.route('/admin/save', methods=['POST'])
@login_required
def admin_save():
    data = request.form
    
    try:
        villa = Villa.query.first()
        if not villa:
            villa = Villa()
            db.session.add(villa)
        
        villa.reference = data.get('reference', '')
        villa.title = data.get('title', '')
        villa.price = safe_int(data.get('price'), 0)
        villa.location = data.get('location', '')
        villa.distance_city = data.get('distance_city', '')
        villa.description = data.get('description', '')
        villa.terrain_area = safe_int(data.get('terrain_area'), 0)
        villa.built_area = safe_int(data.get('built_area'), 0)
        villa.bedrooms = safe_int(data.get('bedrooms'), 0)
        villa.pool_size = data.get('pool_size', '')
        villa.features = data.get('features', '')
        villa.equipment = data.get('equipment', '')
        villa.business_info = data.get('business_info', '')
        villa.investment_benefits = data.get('investment_benefits', '')
        villa.documents = data.get('documents', '')
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
        
        pdf_text = extract_text_from_pdf(temp_filepath)
        
        os.remove(temp_filepath)
        
        if not pdf_text:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        villa_data = extract_villa_data_with_ai(pdf_text)
        
        if not villa_data:
            return jsonify({'error': 'Could not extract villa data. Make sure OPENROUTER_API_KEY is configured.'}), 400
        
        return jsonify({'success': True, 'data': villa_data})
    
    except Exception as e:
        if temp_filepath and os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

@app.route('/api/enhance', methods=['POST'])
@login_required
def enhance():
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

@app.route('/api/villa', methods=['GET'])
def get_villa():
    villa = Villa.query.filter_by(is_active=True).first()
    if villa:
        return jsonify(villa.to_dict())
    return jsonify({'error': 'No villa found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
