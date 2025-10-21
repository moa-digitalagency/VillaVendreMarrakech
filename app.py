from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from models import db, Villa
import os
from werkzeug.utils import secure_filename
import requests
import json
from PIL import Image
import time
import uuid

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

db.init_app(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

def enhance_text_with_ai(text, context=""):
    openrouter_key = os.environ.get('OPENROUTER_API_KEY')
    if not openrouter_key:
        return text
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Améliore ce texte pour une annonce immobilière de luxe. {context}\n\nTexte: {text}\n\nRéponds uniquement avec le texte amélioré, sans explication."
                    }
                ]
            },
            timeout=30
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

@app.route('/admin')
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
        
        return redirect(url_for('admin'))
    except Exception as e:
        db.session.rollback()
        return f"Erreur lors de la sauvegarde: {str(e)}", 500

@app.route('/admin/upload', methods=['POST'])
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

@app.route('/api/enhance', methods=['POST'])
def enhance():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    text = data.get('text', '')
    field = data.get('field', '')
    
    enhanced = enhance_text_with_ai(text, f"Contexte: {field}")
    
    return jsonify({'enhanced': enhanced})

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
