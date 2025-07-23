import os
import logging
import requests
from flask import Flask, render_template, flash
from datetime import datetime

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

class ContentFetcher:
    """Class to handle content API interactions"""
    
    def __init__(self):
        self.base_url = "https://api.pixelcircuit.com/v1/{category}"  # Placeholder for future API
        self.headers = {
            'User-Agent': 'PixelCircuit Content Aggregator 1.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json'
        }
        self.timeout = 10
    
    def fetch_posts(self, category, limit=10):
        """
        Fetch posts from a specific category (gaming or technology)
        
        Args:
            category (str): Content category ('gaming' or 'technology')
            limit (int): Number of posts to fetch (default: 10)
            
        Returns:
            list: List of post dictionaries or empty list on error
        """
        # Placeholder method - will be implemented when API is provided
        app.logger.info(f"API not configured yet for {category} content")
        return []
        
        # Future implementation when API is available:
        # try:
        #     url = self.base_url.format(category=category)
        #     params = {'limit': limit}
        #     
        #     app.logger.info(f"Fetching {category} posts")
        #     response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
        #     response.raise_for_status()
        #     
        #     data = response.json()
        #     posts = []
        #     
        #     # Process API response data here
        #     # Expected format will be provided with API documentation
        #     
        #     return posts
        #     
        # except Exception as e:
        #     app.logger.error(f"Error fetching {category} posts: {str(e)}")
        #     return []

# Initialize content fetcher
content_fetcher = ContentFetcher()

@app.route('/')
def index():
    """
    Main route that displays aggregated posts from gaming and technology categories
    """
    try:
        # Use content fetcher when API is configured
        gaming_posts = content_fetcher.fetch_posts('gaming', limit=10)
        technology_posts = content_fetcher.fetch_posts('technology', limit=10)
        
        # Check if we got any posts
        total_posts = len(gaming_posts) + len(technology_posts)
        
        if total_posts == 0:
            flash('Content API is not configured yet. Waiting for API setup.', 'info')
        elif len(gaming_posts) == 0:
            flash('Gaming content API is not configured yet. Technology posts will be available soon.', 'info')
        elif len(technology_posts) == 0:
            flash('Technology content API is not configured yet. Gaming posts will be available soon.', 'info')
        
        # Prepare data for template
        template_data = {
            'gaming_posts': gaming_posts,
            'technology_posts': technology_posts,
            'total_posts': total_posts,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        app.logger.info(f"Rendering index page with {total_posts} total posts")
        return render_template('index.html', **template_data)
        
    except Exception as e:
        app.logger.error(f"Unexpected error in index route: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        
        # Return empty data to prevent template errors
        return render_template('index.html', 
                             gaming_posts=[], 
                             technology_posts=[], 
                             total_posts=0,
                             last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('index.html', 
                         gaming_posts=[], 
                         technology_posts=[], 
                         total_posts=0,
                         last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    flash('An internal server error occurred. Please try again later.', 'danger')
    return render_template('index.html', 
                         gaming_posts=[], 
                         technology_posts=[], 
                         total_posts=0,
                         last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
