from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Villa(db.Model):
    __tablename__ = 'villa'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    distance_city = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    
    terrain_area = db.Column(db.Integer)
    built_area = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    pool_size = db.Column(db.String(50))
    
    features = db.Column(db.Text)
    equipment = db.Column(db.Text)
    business_info = db.Column(db.Text)
    investment_benefits = db.Column(db.Text)
    documents = db.Column(db.Text)
    
    images = db.Column(db.Text)
    
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(100))
    contact_website = db.Column(db.String(200))
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_images_list(self):
        if self.images:
            return json.loads(self.images)
        return []
    
    def set_images_list(self, images_list):
        self.images = json.dumps(images_list)
    
    def get_features_list(self):
        if self.features:
            return self.features.split('\n')
        return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'title': self.title,
            'price': self.price,
            'location': self.location,
            'distance_city': self.distance_city,
            'description': self.description,
            'terrain_area': self.terrain_area,
            'built_area': self.built_area,
            'bedrooms': self.bedrooms,
            'pool_size': self.pool_size,
            'features': self.features,
            'equipment': self.equipment,
            'business_info': self.business_info,
            'investment_benefits': self.investment_benefits,
            'documents': self.documents,
            'images': self.get_images_list(),
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'contact_website': self.contact_website,
            'is_active': self.is_active
        }
