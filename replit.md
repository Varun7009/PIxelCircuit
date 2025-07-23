# PixelCircuit - Gaming & Technology Hub

## Overview

This is a Flask-based web application called PixelCircuit that will aggregate gaming and technology content. The app is designed to fetch posts from external APIs and display them in a user-friendly interface with Bootstrap styling and dark theme support. Currently waiting for API configuration to enable content fetching.

## Recent Changes (July 2025)

- **Rebranding Complete**: Changed from "Reddit Aggregator" to "PixelCircuit"
- **API Preparation**: Updated ContentFetcher class to be ready for external API integration
- **UI Updates**: Removed all platform-specific references, updated branding throughout
- **Ready for Integration**: Framework prepared for API configuration when provided

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
- **Content API**: Placeholder for external content API (to be configured)
- **Endpoint Pattern**: `https://api.pixelcircuit.com/v1/{category}` (pending configuration)
- **Rate Limiting**: Built-in timeout (10 seconds) and proper headers
- **Data Processing**: Ready to extract relevant post information from API response

## Key Components

### 1. ContentFetcher Class
- **Purpose**: Handles all content API interactions
- **Methods**: `fetch_posts()` for retrieving category content
- **Configuration**: Timeout settings, headers, and base URL management
- **Error Handling**: Graceful degradation on API failures

### 2. Flask Application
- **Route Structure**: Single main route for the homepage
- **Template Rendering**: Passes post data and metadata to templates
- **Flash Messaging**: User feedback for errors and status updates
- **Environment Configuration**: Development vs production settings

### 3. Template System
- **Base Template**: HTML5 structure with Bootstrap integration
- **Dynamic Content**: Post listings with metadata display
- **Social Features**: Open Graph tags for social media sharing
- **AdSense Ready**: Prepared spaces for monetization

## Data Flow

1. **Request Initiation**: User visits the homepage
2. **Data Fetching**: ContentFetcher queries multiple content categories
3. **Data Processing**: Raw API JSON will be parsed and cleaned
4. **Template Rendering**: Processed data is passed to Jinja2 templates
5. **Response Delivery**: HTML page with aggregated posts is served

### Post Data Structure
Each post will contain:
- Title and URL
- Author and category information
- Score (engagement metrics)
- Creation timestamp
- Number of comments
- Post type indicators

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **requests**: HTTP client for API calls
- **datetime**: Timestamp handling

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme
- **Font Awesome 6**: Icon library
- **CDN Delivery**: All frontend assets loaded from CDNs

### Content API
- **Authentication**: To be configured when API details are provided
- **Rate Limiting**: Respectful API usage with proper headers
- **JSON Format**: API response structure to be documented

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