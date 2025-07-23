# PixelCircuit - Complete Project Files

## Core Files (Required)

### 1. main.py
```python
from app import app  # noqa: F401
```

### 2. app.py
- Main Flask application with ContentFetcher class
- News API integration
- Article scraping with trafilatura
- Content filtering and duplicate removal
- Routes for homepage and article pages

### 3. pyproject.toml
- Python dependencies configuration
- Package management with uv

### 4. templates/index.html
- Homepage template
- Gaming and technology post listings
- Bootstrap responsive design
- Firebase Analytics integration

### 5. templates/article.html
- Individual article page template
- Full content display with formatting
- 3 ad positions (top, middle, bottom)
- Apple-style glass morphism design

### 6. static/css/style.css
- Custom CSS styling
- Apple-style animations and effects
- Glass morphism and blur effects
- Responsive design enhancements

## Documentation Files

### 7. replit.md
- Project overview and architecture
- Recent changes and features
- Technical decisions and preferences

### 8. ADSENSE_SETUP.md
- Google AdSense setup instructions
- Publisher ID configuration guide

### 9. ALTERNATIVE_ADS.md
- Alternative ad networks guide
- Media.net, PropellerAds, Amazon Associates

## Project Structure
```
PixelCircuit/
├── main.py                 # Entry point
├── app.py                  # Main Flask app
├── pyproject.toml          # Dependencies
├── templates/
│   ├── index.html         # Homepage
│   └── article.html       # Article page
├── static/
│   └── css/
│       └── style.css      # Custom styles
├── replit.md              # Project docs
├── ADSENSE_SETUP.md       # Ad setup guide
└── ALTERNATIVE_ADS.md     # Alternative ads
```

## To Deploy Your Website:

1. Copy all files to your hosting platform
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variable: `SESSION_SECRET`
4. Run: `python main.py` or use gunicorn
5. Your website will be live!

## Features:
- ✅ Real-time news fetching from News API
- ✅ Auto-updating content (no caching)
- ✅ Duplicate removal and category filtering
- ✅ Apple-style premium design
- ✅ 3 ad positions ready for monetization
- ✅ Mobile responsive layout
- ✅ Firebase Analytics integration
- ✅ Content scraping with clickable links