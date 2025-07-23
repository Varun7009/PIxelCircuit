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
    """Class to handle News API interactions"""
    
    def __init__(self):
        self.base_url = "https://newsapi.org/v2/everything"
        self.api_key = "e15e960b764a4f11ab348cf559ae11b9"
        self.headers = {
            'User-Agent': 'PixelCircuit Content Aggregator 1.0',
            'Accept': 'application/json'
        }
        self.timeout = 10
    
    def fetch_posts(self, category, limit=10):
        """
        Fetch posts from News API for a specific category
        
        Args:
            category (str): Content category ('gaming' or 'technology')
            limit (int): Number of posts to fetch (default: 10)
            
        Returns:
            list: List of post dictionaries or empty list on error
        """
        try:
            # Define search queries for each category
            queries = {
                'gaming': 'gaming OR "video games" OR esports OR PlayStation OR Xbox OR Nintendo OR Steam',
                'technology': 'technology OR tech OR software OR AI OR "artificial intelligence" OR startup OR programming'
            }
            
            if category not in queries:
                app.logger.error(f"Unknown category: {category}")
                return []
                
            params = {
                'q': queries[category],
                'apiKey': self.api_key,
                'pageSize': limit,
                'sortBy': 'publishedAt',
                'language': 'en'
            }
            
            app.logger.info(f"Fetching {category} posts from News API")
            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                app.logger.error(f"News API error: {data.get('message', 'Unknown error')}")
                return []
                
            posts = []
            articles = data.get('articles', [])
            
            for article in articles:
                # Skip articles with removed content
                if article.get('title') == '[Removed]' or not article.get('title'):
                    continue
                    
                post_info = {
                    'title': article.get('title', 'No Title'),
                    'url': article.get('url', ''),
                    'score': 0,  # News API doesn't provide scores, so default to 0
                    'num_comments': 0,  # News API doesn't provide comment counts
                    'author': article.get('source', {}).get('name', 'Unknown Source'),
                    'created_utc': 0,
                    'subreddit': category,
                    'external_url': article.get('url', ''),
                    'is_self': False,
                    'description': article.get('description', ''),
                    'image_url': article.get('urlToImage', '')
                }
                
                # Format creation time from publishedAt
                if article.get('publishedAt'):
                    try:
                        from datetime import datetime
                        pub_time = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                        post_info['created_time'] = pub_time.strftime('%Y-%m-%d %H:%M')
                        post_info['created_utc'] = pub_time.timestamp()
                    except:
                        post_info['created_time'] = 'Unknown'
                else:
                    post_info['created_time'] = 'Unknown'
                
                posts.append(post_info)
            
            app.logger.info(f"Successfully fetched {len(posts)} {category} posts from News API")
            return posts
            
        except requests.exceptions.Timeout:
            app.logger.error(f"Timeout error fetching {category} posts from News API")
            return []
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request error fetching {category} posts: {str(e)}")
            return []
        except Exception as e:
            app.logger.error(f"Unexpected error fetching {category} posts: {str(e)}")
            return []

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
            flash('Unable to fetch content at this time. Please try again later.', 'warning')
        elif len(gaming_posts) == 0:
            flash('Unable to fetch gaming content. Technology posts are still available.', 'info')
        elif len(technology_posts) == 0:
            flash('Unable to fetch technology content. Gaming posts are still available.', 'info')
        
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
