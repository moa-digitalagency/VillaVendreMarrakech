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
- **Multilingual Support:** Automatic browser language detection (French/English) with a discreet floating toggle. All content can be input in both languages, with a fallback to French if English translation is absent.

### Technical Implementations
- **AI Integration:** Utilizes OpenRouter API. Claude 3.5 Sonnet for automated PDF data extraction. Mistral Large for real-time text enhancement in French.
- **Media Management:** Automatic photo optimization (JPEG conversion, compression) upon upload. Interactive gallery with image deletion and real-time previews.
- **Authentication:** Secure admin login with Flask session protection for all admin routes.
- **WhatsApp Integration:** Automatic formatting of WhatsApp numbers and pre-filled messages for direct communication with potential buyers.
- **Database Management:** PostgreSQL with a `villa` table containing 23 columns, automatic `updated_at` triggers, and 5 optimized indexes for performance.
- **SEO:** Optimized meta tags, Open Graph, Twitter Cards, structured data (Schema.org), descriptive alt tags, and dedicated SEO files (robots.txt, sitemap.xml).

### Feature Specifications
- **Admin Modes:** Two distinct input modes: "PDF + Photos" for AI-powered extraction and "Formulaire + Photos" for manual entry with AI text enhancement.
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
  - **Claude 3.5 Sonnet (Anthropic):** Structured PDF extraction.
  - **Mistral Large:** French text enhancement.
- **PostgreSQL:** Primary database for storing villa data.
- **Pillow:** Python Imaging Library for automatic image optimization.
- **WhatsApp Deep Links:** For direct communication integration.