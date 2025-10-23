# Application Web de Vente de Villa de Prestige

## Overview
This project is a comprehensive web application designed for the online sale of luxury villas in Marrakech. It features a modern, immersive public-facing site and a secure, professional administration interface. The application aims to streamline the process of listing and managing high-end properties, leveraging AI for data extraction and content enhancement, and providing a seamless user experience for potential buyers. The business vision is to establish a leading online platform for luxury real estate in Marrakech, offering advanced features for both administrators and public users.

## User Preferences
- I prefer simple language.
- I want iterative development.
- Ask before making major changes.
- I prefer detailed explanations.
- Do not make changes to the folder `Z`.
- Do not make changes to the file `Y`.

## System Architecture

### UI/UX Decisions
- **Admin Interface:** Professional, modern design with a light theme (gold, teal, white). Color-coded sections: violet (PDF), green (photos), gold (forms). Responsive across devices.
- **Public Frontend:** Ultra-modern, photo-forward design with a luxurious Gold/Teal palette. Features include an automatic hero slider, creative sections, a lightbox gallery, and integrated WhatsApp contact buttons. Fully responsive for mobile, tablet, and desktop.
- **Multilingual Support:** Pure bilingual experience with automatic browser language detection (French/English) and a discreet floating toggle. English version displays only English content (no French fallback) with default placeholder messages when translations are missing. French version displays French content exclusively.

### Technical Implementations
- **AI Integration:** Utilizes OpenRouter API for three key functions:
  - **Claude 3.5 Sonnet (Anthropic):** Automated PDF data extraction in French + automatic translation to English (21 fields translated)
  - **Mistral Large:** Real-time text enhancement in French
  - **Automatic Translation:** Complete French-to-English translation covering main content, UI text, "Why Choose" cards, and contact sections
- **Bilingual Data Management:** Separate database columns for French and English versions of all content. No fallback to French in English mode for pure bilingual experience.
- **Media Management:** Automatic photo optimization (JPEG conversion, compression) upon upload. Interactive gallery with image deletion and real-time previews.
- **Authentication:** Secure admin login with Flask session protection for all admin routes.
- **WhatsApp Integration:** Automatic formatting of WhatsApp numbers and pre-filled messages for direct communication with potential buyers.
- **Database Management:** PostgreSQL with a `villa` table containing bilingual columns for all user-facing content, automatic `updated_at` triggers, and optimized indexes for performance.
- **SEO:** Language-aware meta tags (separate for FR/EN), Open Graph, Twitter Cards, structured data (Schema.org), descriptive alt tags, and dedicated SEO files (robots.txt, sitemap.xml).

### Feature Specifications
- **Admin Modes:** Two distinct input modes:
  - **"PDF + Photos":** AI-powered extraction in French + automatic translation to English for all 21 bilingual fields
  - **"Formulaire + Photos":** Manual bilingual entry with AI text enhancement
- **Automatic Translation:** When uploading a PDF, the system:
  1. Extracts French content using Claude 3.5 Sonnet
  2. Automatically translates ALL fields to English (title, description, features, equipment, business info, investment benefits, documents, UI text, "Why Choose" cards, contact sections)
  3. Populates both French and English database fields
  4. Allows manual editing of both language versions independently
- **Translation Script:** `translate_existing_villa.py` utility to translate existing villa data from French to English (for legacy data or re-translation)
- **Data Reset:** Secure data reset functionality with double confirmation to delete all data and photos.
- **Frontend Photo Distribution:** Specific allocation of photos for the hero slider, description section, and the main gallery.
- **JavaScript Features:** Hero slider auto-rotation, keyboard/click navigation for lightbox, smooth scrolling, and responsive adaptations.

### System Design Choices
- **Backend:** Flask, SQLAlchemy, PostgreSQL.
- **Frontend:** HTML5, CSS3, JavaScript.
- **Deployment:** Comprehensive deployment guides for Replit and VPS, including a `fix_database.py` script for automatic database schema correction and migration.
- **Environment Variables:** Configuration via `DATABASE_URL`, `OPENROUTER_API_KEY`, `ADMIN_PASSWORD`, and `SESSION_SECRET`.
- **Security:** Mandatory validation of required environment variables (`OPENROUTER_API_KEY`, `SESSION_SECRET`) at application startup. The application will refuse to start with a clear error message if any required variable is missing.

## External Dependencies
- **OpenRouter API:** For AI functionalities, specifically:
  - **Claude 3.5 Sonnet (Anthropic):** Structured PDF extraction in French AND automatic French-to-English translation (comprehensive bilingual support)
  - **Mistral Large:** French text enhancement
- **PostgreSQL:** Primary database for storing bilingual villa data (separate columns for FR/EN).
- **Pillow:** Python Imaging Library for automatic image optimization.
- **WhatsApp Deep Links:** For direct communication integration.

## Bilingual Translation Workflow

### PDF Upload → Automatic Translation
1. Admin uploads PDF via "📄 PDF + Photos" mode
2. System extracts French text using Claude 3.5 Sonnet (60-90 seconds)
3. System automatically translates ALL French content to English (additional 90-120 seconds)
4. Both French and English fields are populated in database
5. Admin can review and edit both languages independently in admin panel

### Manual Translation of Existing Data
Run `python translate_existing_villa.py` to translate existing villa data:
- Loads all French fields from database
- Translates to English using Claude 3.5 Sonnet
- Updates all English (_en) fields
- Shows progress and confirms successful translation

### Fields Automatically Translated (21 total)
- **Main Content:** title, description, features, equipment, business_info, investment_benefits, documents
- **Website UI:** hero_subtitle, contact_button, description_title, whatsapp_button
- **"Why Choose" Section:** why_choose_title, 4 card titles and descriptions (why_card1-4)
- **Contact Section:** contact_title, contact_subtitle