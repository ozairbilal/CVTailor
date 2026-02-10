"""
Web scraper for extracting job descriptions from various sources
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_job_description(url):
    """
    Extract job description text from a given URL
    Supports LinkedIn, company career pages, and general job posting sites
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Use html.parser (built-in, no dependencies needed)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find job description based on common patterns
        job_desc = None
        
        # LinkedIn specific selectors
        if 'linkedin.com' in url:
            job_desc = soup.find('div', class_='description__text')
            if not job_desc:
                job_desc = soup.find('div', {'class': lambda x: x and 'job-description' in x.lower()})
        
        # General job description patterns
        if not job_desc:
            # Try common class names
            patterns = [
                {'class': lambda x: x and any(term in x.lower() for term in ['job-description', 'description', 'job-details', 'posting-description'])},
                {'id': lambda x: x and any(term in x.lower() for term in ['job-description', 'description', 'job-details'])},
            ]
            
            for pattern in patterns:
                job_desc = soup.find(['div', 'section', 'article'], pattern)
                if job_desc:
                    break
        
        # If still not found, get main content
        if not job_desc:
            job_desc = soup.find('main') or soup.find('article') or soup.body
        
        if job_desc:
            # Extract text and clean it
            text = job_desc.get_text(separator='\n', strip=True)
            # Remove excessive newlines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)
            
            if len(cleaned_text) > 100:  # Ensure we got substantial content
                return cleaned_text
        
        return "Unable to extract job description. Please ensure the URL is correct and accessible."
        
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error parsing job description: {str(e)}"

def validate_url(url):
    """
    Validate if the provided string is a valid URL
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
