# Changelog - Villa à Vendre Marrakech

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-10-23

### 🌍 Added - Full Bilingual Support
- **Complete website text customization**: All text on the public website is now fully editable from the admin panel
- **New admin interface**: Added dedicated "Edit Website" page (`/admin/edit-website`) for customizing all website text
- **Bilingual text fields** added to the database:
  - Hero section (subtitle, contact button)
  - Description section (title, WhatsApp button)
  - "Why Choose This Villa" section (title, 4 cards with titles and descriptions)
  - Contact section (title, subtitle)
- **Migration script**: `migrate_default_texts.py` to automatically populate default English and French text
- **No more hardcoded text**: All text previously hardcoded in templates now comes from the database

### 🔧 Changed - Configuration
- **SESSION_SECRET**: Application now uses `SESSION_SECRET` environment variable instead of `SECRET_KEY`
- **Environment validation**: Added proper checks for required environment variables
- **Bilingual defaults**: All default text now available in both French and English

### 📝 Improved - Admin Panel
- **Better organization**: Separated villa data editing from website text editing
- **User-friendly interface**: Clear sections for each part of the website
- **Real-time preview**: Changes can be immediately seen on the public site
- **Language toggle**: Easy switching between French and English when editing

### 🐛 Fixed
- **Language detection**: Fixed issues where French text appeared on English version
- **Default values**: All default text now properly translated in both languages
- **Database consistency**: Ensured all text fields are properly stored and retrieved

### 📚 Documentation
- Added comprehensive CHANGELOG.md
- Added VPS deployment script (`deploy_vps.sh`)
- Updated progress tracker for migration status

## [1.0.0] - 2025-10-XX

### Initial Release
- Flask web application for luxury villa sales in Marrakech
- PostgreSQL database integration
- AI-powered PDF data extraction (Claude 3.5 Sonnet)
- AI-powered text enhancement (Mistral Large)
- Image upload and optimization
- Responsive design with modern UI
- Admin panel with authentication
- Basic bilingual support (FR/EN)

---

## Migration Guide from 1.0.0 to 2.0.0

### For Replit Environment:
1. The migration is automatic - environment variables are already configured
2. Run the migration script to set default text: `python migrate_default_texts.py`
3. Access `/admin/edit-website` to customize all website text

### For VPS Environment:
1. Pull the latest code: `git pull origin main`
2. Ensure all environment variables are set:
   - `DATABASE_URL` or `PG*` variables
   - `SESSION_SECRET`
   - `ADMIN_PASSWORD`
   - `OPENROUTER_API_KEY` (optional, for AI features)
3. Run migrations: `python migrate_default_texts.py`
4. Restart the application: `sudo systemctl restart villaeden`

### Breaking Changes:
- Environment variable `SECRET_KEY` renamed to `SESSION_SECRET` (for consistency with Replit)
- Database schema extended with 24 new text fields for customization

### Database Changes:
New columns added to `villa` table:
```sql
-- Hero section
hero_subtitle_fr, hero_subtitle_en
contact_button_fr, contact_button_en

-- Description section  
description_title_fr, description_title_en
whatsapp_button_fr, whatsapp_button_en

-- Why Choose section
why_choose_title_fr, why_choose_title_en
why_card1_title_fr/en, why_card1_desc_fr/en
why_card2_title_fr/en, why_card2_desc_fr/en
why_card3_title_fr/en, why_card3_desc_fr/en
why_card4_title_fr/en, why_card4_desc_fr/en

-- Contact section
contact_title_fr, contact_title_en
contact_subtitle_fr, contact_subtitle_en
```

## Support

For issues or questions:
- Developer: Aisance KALONJI
- Email: moa@myoneart.com
- Website: www.myoneart.com
