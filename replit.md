# PixelCircuit - Gaming & Technology Hub

## Overview

This is a Flask-based web application called PixelCircuit that aggregates gaming and technology content. The app fetches real news articles from News API and displays them in a user-friendly interface with Bootstrap styling and dark theme support. The site is fully functional with live content from authentic news sources.

## Recent Changes (July 2025)

- **Full Content Display**: Articles now show complete scraped content on-site instead of external redirects
- **Apple-Style Design**: Added smooth transitions, blur effects, and glass morphism throughout
- **Featured Images**: Large hero images for each article with dynamic content-based selection
- **Enhanced Ad Integration**: 3 strategically placed ad boxes per article (top, middle, bottom)
- **Advanced Animations**: Fade-in effects, hover transitions, and pulse animations
- **Content Scraping**: Integrated trafilatura for full article content extraction
- **Responsive Layout**: Optimized for all device sizes with mobile-first design
- **Premium UI Effects**: Backdrop filters, gradient overlays, and shimmer effects

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with Replit Dark Theme
- **Icons**: Font Awesome 6.4.0
- **Theme**: Dark theme optimized for Replit environment
- **Responsive Design**: Mobile-first approach with Bootstrap's grid system

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **HTTP Client**: Python requests library for Reddit API calls
- **Session Management**: Flask sessions with secret key
- **Logging**: Python's built-in logging module for debugging
- **Error Handling**: Try-catch blocks with user-friendly flash messages

### API Integration
- **News API**: Integrated NewsAPI.org for real content fetching
- **Endpoint**: `https://newsapi.org/v2/everything`
- **Authentication**: API key authentication (configured)
- **Categories**: Gaming and technology content with targeted search queries
- **Rate Limiting**: Built-in timeout (10 seconds) and proper headers
- **Data Processing**: Extracts title, URL, source, description, and timestamp from articles

## Key Components

### 1. ContentFetcher Class
- **Purpose**: Handles all content API interactions
- **Methods**: `fetch_posts()` for retrieving category content
- **Configuration**: Timeout settings, headers, and base URL management
- **Error Handling**: Graceful degradation on API failures

### 2. Firebase Analytics Integration
- **Project ID**: pixelcircuit-7555a
- **Measurement ID**: G-KPY35D2XV1
- **Purpose**: Track user engagement, page views, and site performance
- **Configuration**: Integrated via Firebase SDK v10.0.0
- **Features**: Real-time analytics, user behavior tracking

### 3. Flask Application
- **Route Structure**: Single main route for the homepage
- **Template Rendering**: Passes post data and metadata to templates
- **Flash Messaging**: User feedback for errors and status updates
- **Environment Configuration**: Development vs production settings

### 4. Template System
- **Base Template**: HTML5 structure with Bootstrap integration
- **Dynamic Content**: Post listings with metadata display
- **Social Features**: Open Graph tags for social media sharing
- **AdSense Ready**: Prepared spaces for monetization
- **Analytics Integration**: Firebase Analytics embedded for tracking

## Data Flow

1. **Request Initiation**: User visits the homepage
2. **Data Fetching**: ContentFetcher queries multiple content categories
3. **Data Processing**: Raw API JSON will be parsed and cleaned
4. **Template Rendering**: Processed data is passed to Jinja2 templates
5. **Response Delivery**: HTML page with aggregated posts is served

### Post Data Structure
Each post contains:
- Title and URL
- Author and category information
- Article description (truncated for display)
- Creation timestamp
- Thumbnail image from News API
- Fallback placeholder for missing images

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **requests**: HTTP client for API calls
- **datetime**: Timestamp handling

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme
- **Font Awesome 6**: Icon library
- **Firebase Analytics**: User tracking and analytics (v10.0.0)
- **CDN Delivery**: All frontend assets loaded from CDNs

### News API
- **Authentication**: API key based authentication
- **Rate Limiting**: Respectful API usage with proper headers
- **JSON Format**: Standard News API article format with source, title, description
- **Search Queries**: Targeted queries for gaming and technology content

## Deployment Strategy

### Development Environment
- **Host**: 0.0.0.0 (accessible from external connections)
- **Port**: 5000 (standard Flask development port)
- **Debug Mode**: Enabled for development
- **Auto-reload**: Flask development server features

### Production Considerations
- **Secret Key**: Environment variable for session security
- **Error Handling**: Production-ready error pages needed
- **WSGI Server**: Should use Gunicorn or similar for production
- **Static Files**: Consider CDN for static asset delivery

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- Development fallback: "dev-secret-key-change-in-production"

## Key Features

### Content Aggregation
- Multi-subreddit support (gaming and technology focused)
- Real-time data fetching from Reddit
- Clean, structured post presentation

### User Experience
- Dark theme optimized interface
- Responsive design for all devices
- Hover effects and smooth transitions
- Last updated timestamps

### Monetization Ready
- AdSense-ready HTML structure
- SEO optimized meta tags
- Social media sharing integration
- Strategic ad placement areas

## Technical Decisions

### Why Flask?
- **Problem**: Need lightweight, flexible web framework
- **Solution**: Flask provides minimal overhead with extensibility
- **Pros**: Simple routing, built-in templating, easy deployment
- **Cons**: Requires more manual configuration than Django

### Why Reddit JSON API?
- **Problem**: Need reliable source of gaming/tech content
- **Solution**: Reddit's public JSON endpoints
- **Pros**: No authentication required, rich metadata, active communities
- **Cons**: Rate limiting, potential API changes

### Why Bootstrap Dark Theme?
- **Problem**: Need professional, mobile-friendly UI
- **Solution**: Bootstrap with Replit's dark theme
- **Pros**: Consistent styling, responsive design, dark theme optimization
- **Cons**: Larger CSS payload, potential customization limitations