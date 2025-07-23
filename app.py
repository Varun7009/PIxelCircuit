import os
import logging
import requests
import trafilatura
from flask import Flask, render_template, flash, request, redirect
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
                    'image_url': article.get('urlToImage', ''),
                    'content': article.get('content', ''),  # Store content for scraping
                    'full_content': ''  # Will be populated by scraping
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
    
    def scrape_article_content(self, url):
        """
        Scrape full article content from URL using trafilatura with enhanced formatting
        
        Args:
            url (str): Article URL to scrape
            
        Returns:
            str: Full article content with improved formatting
        """
        try:
            app.logger.info(f"Scraping content from: {url}")
            downloaded = trafilatura.fetch_url(url)
            
            if not downloaded:
                app.logger.warning(f"Failed to download content from: {url}")
                return "Content not available"
                
            # Extract with better formatting options
            text = trafilatura.extract(
                downloaded, 
                include_links=True, 
                include_images=False,
                include_formatting=True,
                favor_precision=True,
                output_format='xml'
            )
            
            if text:
                # Convert to HTML-friendly format
                formatted_content = self.format_article_content(text)
                app.logger.info(f"Successfully scraped and formatted {len(formatted_content)} characters from: {url}")
                return formatted_content
            else:
                app.logger.warning(f"No text extracted from: {url}")
                return "Content not available"
                
        except Exception as e:
            app.logger.error(f"Error scraping content from {url}: {str(e)}")
            return "Content not available"
    
    def format_article_content(self, raw_content):
        """
        Format and structure article content for better readability
        
        Args:
            raw_content (str): Raw extracted content
            
        Returns:
            str: Formatted HTML content
        """
        import re
        
        if not raw_content or raw_content == "Content not available":
            return raw_content
        
        # Clean up the content
        content = raw_content.strip()
        
        # Convert markdown-style links to HTML links
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer" class="article-link">\1</a>', content)
        
        # Split into paragraphs and clean up
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # Clean up extra whitespace
                para = re.sub(r'\s+', ' ', para)
                
                # Format quotes
                if para.startswith('"') and para.endswith('"'):
                    para = f'<blockquote class="article-quote">{para}</blockquote>'
                
                # Format headings (if they look like headings)
                elif len(para) < 100 and para.count('.') == 0 and para.isupper():
                    para = f'<h4 class="article-heading">{para}</h4>'
                
                # Regular paragraphs
                else:
                    para = f'<p class="article-paragraph">{para}</p>'
                
                formatted_paragraphs.append(para)
        
        return '\n'.join(formatted_paragraphs)

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

@app.route('/article')
def article():
    """
    Route to display full article content
    """
    url = request.args.get('url')
    title = request.args.get('title', 'Article')
    source = request.args.get('source', 'Unknown Source')
    image_url = request.args.get('image', '')
    
    if not url:
        flash('Article URL not provided.', 'danger')
        return redirect('/')
    
    try:
        # Scrape full content
        full_content = content_fetcher.scrape_article_content(url)
        
        # Use provided image or generate a relevant fallback based on content type
        featured_image = image_url if image_url else get_fallback_image(title, source)
        
        return render_template('article.html', 
                             title=title,
                             source=source,
                             url=url,
                             content=full_content,
                             featured_image=featured_image,
                             last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    except Exception as e:
        app.logger.error(f"Error displaying article {url}: {str(e)}")
        flash('Unable to load article content.', 'danger')
        return redirect('/')

def get_fallback_image(title, source):
    """
    Generate appropriate fallback image based on article content
    """
    title_lower = title.lower()
    source_lower = source.lower()
    
    # Gaming related keywords
    gaming_keywords = ['gaming', 'game', 'steam', 'playstation', 'xbox', 'nintendo', 'esports', 'dune', 'fps', 'rpg']
    # Technology related keywords  
    tech_keywords = ['tech', 'ai', 'software', 'programming', 'samsung', 'monitor', 'cpu', 'gpu', 'smartphone', 'laptop']
    
    # Check for gaming content
    if any(keyword in title_lower for keyword in gaming_keywords):
        return "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=600&q=80"
    
    # Check for technology content
    elif any(keyword in title_lower for keyword in tech_keywords):
        return "https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=600&q=80"
    
    # Default tech image
    else:
        return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=600&q=80"

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
