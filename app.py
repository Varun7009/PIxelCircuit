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

class RedditFetcher:
    """Class to handle Reddit API interactions"""
    
    def __init__(self):
        self.base_url = "https://www.reddit.com/r/{subreddit}.json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.timeout = 10
    
    def fetch_posts(self, subreddit, limit=10):
        """
        Fetch posts from a specific subreddit
        
        Args:
            subreddit (str): Name of the subreddit
            limit (int): Number of posts to fetch (default: 10)
            
        Returns:
            list: List of post dictionaries or empty list on error
        """
        try:
            url = self.base_url.format(subreddit=subreddit)
            params = {'limit': limit}
            
            app.logger.info(f"Fetching posts from r/{subreddit}")
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post_data in data['data']['children']:
                post = post_data['data']
                
                # Extract relevant post information
                post_info = {
                    'title': post.get('title', 'No Title'),
                    'url': f"https://www.reddit.com{post.get('permalink', '')}",
                    'score': post.get('score', 0),
                    'num_comments': post.get('num_comments', 0),
                    'author': post.get('author', 'Unknown'),
                    'created_utc': post.get('created_utc', 0),
                    'subreddit': subreddit,
                    'external_url': post.get('url', ''),
                    'is_self': post.get('is_self', False)
                }
                
                # Format creation time
                if post_info['created_utc']:
                    post_info['created_time'] = datetime.fromtimestamp(post_info['created_utc']).strftime('%Y-%m-%d %H:%M')
                else:
                    post_info['created_time'] = 'Unknown'
                
                posts.append(post_info)
            
            app.logger.info(f"Successfully fetched {len(posts)} posts from r/{subreddit}")
            return posts
            
        except requests.exceptions.Timeout:
            app.logger.error(f"Timeout error fetching posts from r/{subreddit}")
            return []
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request error fetching posts from r/{subreddit}: {str(e)}")
            return []
        except KeyError as e:
            app.logger.error(f"Data parsing error for r/{subreddit}: {str(e)}")
            return []
        except Exception as e:
            app.logger.error(f"Unexpected error fetching posts from r/{subreddit}: {str(e)}")
            return []

# Initialize Reddit fetcher
reddit_fetcher = RedditFetcher()

@app.route('/')
def index():
    """
    Main route that displays aggregated posts from gaming and technology subreddits
    """
    try:
        # Fetch posts from both subreddits
        gaming_posts = reddit_fetcher.fetch_posts('gaming', limit=10)
        technology_posts = reddit_fetcher.fetch_posts('technology', limit=10)
        
        # Check if we got any posts
        total_posts = len(gaming_posts) + len(technology_posts)
        
        if total_posts == 0:
            flash('Unable to fetch posts from Reddit at this time. Please try again later.', 'warning')
        elif len(gaming_posts) == 0:
            flash('Unable to fetch posts from r/gaming. Technology posts are still available.', 'info')
        elif len(technology_posts) == 0:
            flash('Unable to fetch posts from r/technology. Gaming posts are still available.', 'info')
        
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
