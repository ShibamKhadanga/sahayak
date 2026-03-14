"""
Web Scraper Module
Searches the internet for government forms and extracts requirements
Uses Google Custom Search API + BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# Google Custom Search API (Get free key from: https://developers.google.com/custom-search)
# For demo, we'll use DuckDuckGo scraping (no API key needed)

def search_government_forms(query, state='india', max_results=5):
    """
    Search the internet for government forms
    
    Args:
        query: Search query (e.g., "learning license application")
        state: State name (e.g., "chhattisgarh")
        max_results: Number of results to return
    
    Returns:
        List of search results with title, URL, snippet
    """
    try:
        # Build search query
        search_query = f"{query} {state} government official application form"
        
        # Method 1: DuckDuckGo search (no API key needed)
        results = search_duckduckgo(search_query, max_results)
        
        # Filter for official government websites
        official_results = []
        gov_domains = ['.gov.in', '.nic.in', '.gov', 'uidai.gov.in', 'nsdl.com']
        
        for result in results:
            # Prioritize official domains
            is_official = any(domain in result['url'] for domain in gov_domains)
            result['source'] = 'official' if is_official else 'general'
            
            if is_official:
                official_results.insert(0, result)  # Add to beginning
            else:
                official_results.append(result)
        
        return official_results[:max_results]
        
    except Exception as e:
        logger.error(f"Error in search_government_forms: {e}")
        return []

def search_duckduckgo(query, max_results=5):
    """
    Search using DuckDuckGo (no API key needed)
    """
    try:
        # DuckDuckGo HTML search
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # Parse DuckDuckGo results
        for result_div in soup.find_all('div', class_='result'):
            try:
                title_elem = result_div.find('a', class_='result__a')
                snippet_elem = result_div.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
                    
                    if len(results) >= max_results:
                        break
            except:
                continue
        
        return results
        
    except Exception as e:
        logger.error(f"DuckDuckGo search error: {e}")
        
        # Fallback: Return common government portals
        return get_common_portals(query)

def get_common_portals(query):
    """
    Fallback: Return common government portals based on query
    """
    query_lower = query.lower()
    
    portals = {
        'learning license': {
            'title': 'Learning License - Sarathi Parivahan',
            'url': 'https://sarathi.parivahan.gov.in/sarathiservice/stateSelection.do',
            'snippet': 'Apply for Learning License online through Sarathi portal'
        },
        'driving license': {
            'title': 'Driving License - Sarathi Parivahan',
            'url': 'https://sarathi.parivahan.gov.in/sarathiservice/stateSelection.do',
            'snippet': 'Apply for Driving License online'
        },
        'pension': {
            'title': 'Pension Schemes - Chhattisgarh',
            'url': 'https://socialsecurity.cg.nic.in/',
            'snippet': 'Social Security Pension Schemes for Chhattisgarh'
        },
        'ration card': {
            'title': 'Ration Card - Public Distribution',
            'url': 'https://khadya.cg.nic.in/',
            'snippet': 'Apply for Ration Card online'
        },
        'aadhar': {
            'title': 'Aadhar Enrollment - UIDAI',
            'url': 'https://uidai.gov.in/',
            'snippet': 'Enroll for Aadhar card or update details'
        },
        'pan card': {
            'title': 'PAN Card Application - NSDL',
            'url': 'https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html',
            'snippet': 'Apply for new PAN card or reprint'
        },
        'scholarship': {
            'title': 'Scholarship Portal - Chhattisgarh',
            'url': 'https://scholarshipportal.cg.nic.in/',
            'snippet': 'Apply for scholarships online'
        }
    }
    
    # Find matching portal
    for key, portal in portals.items():
        if key in query_lower:
            return [portal]
    
    return []

def scrape_form_details(url):
    """
    Scrape details from a government form page
    Extracts requirements, eligibility criteria, documents needed
    
    Args:
        url: URL of the form page
    
    Returns:
        Dictionary with requirements, documents, eligibility
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract page text
        page_text = soup.get_text()
        
        # Extract requirements using patterns
        requirements = extract_requirements(page_text)
        documents = extract_documents(page_text)
        eligibility = extract_eligibility(page_text)
        fees = extract_fees(page_text)
        
        return {
            'requirements': requirements,
            'documents': documents,
            'eligibility': eligibility,
            'fees': fees
        }
        
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return {
            'requirements': [],
            'documents': [],
            'eligibility': [],
            'fees': None
        }

def extract_requirements(text):
    """Extract requirements from page text"""
    requirements = []
    
    # Look for common patterns
    patterns = [
        r'(?:require|need|must have|should have)s?\s+(.+?)(?:\.|;|\n)',
        r'(?:mandatory|compulsory|essential)\s+(.+?)(?:\.|;|\n)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        requirements.extend([m.strip() for m in matches if len(m.strip()) > 10])
    
    # Remove duplicates and limit
    return list(set(requirements))[:10]

def extract_documents(text):
    """Extract required documents from page text"""
    documents = []
    
    # Common document keywords
    doc_keywords = [
        'aadhar', 'aadhaar', 'pan card', 'passport', 'voter id',
        'driving license', 'birth certificate', 'address proof',
        'income certificate', 'caste certificate', 'photo', 'photograph'
    ]
    
    text_lower = text.lower()
    
    for keyword in doc_keywords:
        if keyword in text_lower:
            # Try to extract the full requirement
            pattern = rf'([^.;]*{keyword}[^.;]*)'
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                documents.append(matches[0].strip().capitalize())
    
    # Remove duplicates
    return list(set(documents))[:8]

def extract_eligibility(text):
    """Extract eligibility criteria"""
    eligibility = []
    
    # Age criteria
    age_patterns = [
        r'age\s+(?:should be|must be|:)?\s*(\d+)\s*(?:years?|yrs?|\+)',
        r'(\d+)\s*(?:years?|yrs?)\s+(?:or above|and above|\+|old)',
        r'(?:minimum|min)\s+age\s*:?\s*(\d+)'
    ]
    
    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            age = match.group(1)
            eligibility.append(f"Age: {age}+ years")
            break
    
    # Income criteria
    income_patterns = [
        r'income\s+(?:below|less than|under)\s*₹?\s*([\d,]+)',
        r'₹\s*([\d,]+)\s+(?:income|annual income)'
    ]
    
    for pattern in income_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            income = match.group(1)
            eligibility.append(f"Income: Below ₹{income}")
            break
    
    return eligibility

def extract_fees(text):
    """Extract application fees"""
    fee_patterns = [
        r'(?:fee|fees|cost|charge)s?\s*:?\s*₹\s*([\d,]+)',
        r'₹\s*([\d,]+)\s+(?:fee|fees|only)'
    ]
    
    for pattern in fee_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"₹{match.group(1)}"
    
    return None

def search_form_by_keywords(keywords):
    """
    Intelligent search based on keywords
    Understands different ways users might ask
    """
    # Map common phrases to search queries
    mappings = {
        'i want': '',
        'how to apply': 'application',
        'how to get': 'apply',
        'i need': 'application',
        'apply for': 'application',
        'll': 'learning license',
        'dl': 'driving license'
    }
    
    query = keywords.lower()
    
    for phrase, replacement in mappings.items():
        query = query.replace(phrase, replacement)
    
    return search_government_forms(query.strip())

if __name__ == '__main__':
    # Test the scraper
    print("Testing web scraper...")
    
    results = search_government_forms("learning license", "india", 3)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   {result['snippet']}")
        
        if i == 1:
            print("\n   Scraping details...")
            details = scrape_form_details(result['url'])
            print(f"   Requirements: {details['requirements'][:3]}")
            print(f"   Documents: {details['documents'][:3]}")
