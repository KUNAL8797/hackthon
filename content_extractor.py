# content_extractor.py
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from typing import Dict, Optional

class ContentExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
    
    async def extract_content(self, url: str) -> Dict[str, any]:
        """
        Extract article content and metadata from URL asynchronously.
        """
        try:
            if not self._is_valid_url(url):
                raise ValueError("Invalid URL format")
            
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    html_content = await response.text()
                    
            soup = BeautifulSoup(html_content, 'lxml')
            
            metadata = self._extract_metadata(soup, url)
            content = self._extract_main_content(soup)
            cleaned_content = self._clean_content(content)
            
            return {
                'url': url,
                'metadata': metadata,
                'content': cleaned_content,
                'raw_html_length': len(html_content),
                'extracted_length': len(cleaned_content)
            }
            
        except aiohttp.ClientError as e:
            raise Exception(f"Failed to fetch content: {str(e)}")
        except Exception as e:
            raise Exception(f"Content extraction error: {str(e)}")
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, str]:
        """Extract article metadata"""
        metadata = {
            'title': '',
            'author': '',
            'publication': '',
            'publish_date': '',
            'domain': urlparse(url).netloc
        }
        
        # Extract title
        title_elem = (soup.find('h1') or 
                     soup.find('title') or 
                     soup.find('meta', property='og:title'))
        if title_elem:
            metadata['title'] = title_elem.get_text().strip() if hasattr(title_elem, 'get_text') else title_elem.get('content', '')
        
        # Extract author
        author_selectors = [
            'meta[name="author"]',
            'meta[property="article:author"]',
            '.author',
            '.byline',
            '[rel="author"]'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                metadata['author'] = (author_elem.get('content') or 
                                    author_elem.get_text()).strip()
                break
        
        # Extract publication date
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="publishdate"]',
            'time[datetime]',
            '.publish-date',
            '.date'
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                metadata['publish_date'] = (date_elem.get('datetime') or 
                                          date_elem.get('content') or
                                          date_elem.get_text()).strip()
                break
        
        return metadata
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 
                           'aside', 'form', 'button']):
            element.decompose()
        
        # Try common article selectors
        content_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            'main',
            '.main-content'
        ]
        
        content = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem.get_text()
                break
        
        # Fallback to body if no specific content found
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text()
        
        return content
    
    def _clean_content(self, content: str) -> str:
        """Clean extracted content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove common website elements
        unwanted_patterns = [
            r'Subscribe to.*?newsletter',
            r'Follow us on.*?social media',
            r'Advertisement',
            r'Related articles?:.*',
            r'Tags?:.*',
            r'Share this article',
            r'Comments? \(\d+\)'
        ]
        
        for pattern in unwanted_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        return content.strip()
