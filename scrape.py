from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_auth_credentials():
    """Get and validate authentication credentials"""
    auth = os.getenv("AUTH")
    if not auth:
        raise ValueError("AUTH environment variable not found. Please check your .env file or Streamlit secrets.")
    return auth

def get_chrome_options():
    """Configure Chrome options for scraping"""
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options

def scrape_website(website, max_retries=3, timeout=30):
    """
    Scrape website using Bright Data's Scraping Browser
    
    Args:
        website (str): URL to scrape
        max_retries (int): Maximum number of retry attempts
        timeout (int): Timeout in seconds for page load
    
    Returns:
        str: HTML content of the page
    """
    try:
        auth = get_auth_credentials()
        sbr_webdriver = f'https://{auth}@brd.superproxy.io:9515'
        logger.info(f"Connecting to Scraping Browser for: {website}")
        
    except ValueError as e:
        logger.error(f"Authentication error: {e}")
        raise
    
    for attempt in range(max_retries):
        driver = None
        try:
            logger.info(f"Attempt {attempt + 1}/{max_retries}")
            
            # Create connection
            sbr_connection = ChromiumRemoteConnection(sbr_webdriver, "goog", "chrome")
            options = get_chrome_options()
            
            # Initialize driver with timeout
            driver = Remote(sbr_connection, options=options)
            driver.set_page_load_timeout(timeout)
            driver.implicitly_wait(10)
            
            logger.info("Connected successfully! Navigating to website...")
            driver.get(website)
            
            # Handle captcha
            logger.info("Checking for captcha...")
            try:
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        "cmd": "Captcha.waitForSolve",
                        "params": {"detectTimeout": 10000},
                    },
                )
                logger.info(f"Captcha solve status: {solve_res['value']['status']}")
            except Exception as captcha_error:
                logger.warning(f"Captcha handling failed: {captcha_error}")
                # Continue anyway as captcha might not be present
            
            logger.info("Scraping page content...")
            html = driver.page_source
            
            if html and len(html) > 100:  # Basic validation
                logger.info(f"Successfully scraped {len(html)} characters")
                return html
            else:
                raise Exception("Retrieved HTML content is too short or empty")
                
        except WebDriverException as e:
            logger.error(f"WebDriver error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts. Last error: {e}")
                
        except TimeoutException as e:
            logger.error(f"Timeout error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise Exception(f"Page load timeout after {max_retries} attempts")
                
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise Exception(f"Unexpected error after {max_retries} attempts: {e}")
                
        finally:
            # Ensure driver is closed
            if driver:
                try:
                    driver.quit()
                except:
                    pass

def extract_body_content(html_content):
    """Extract body content from HTML"""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        if body_content:
            return str(body_content)
        return ""
    except Exception as e:
        logger.error(f"Error extracting body content: {e}")
        return ""

def clean_body_content(body_content):
    """Clean and extract text from body content"""
    try:
        soup = BeautifulSoup(body_content, "html.parser")
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        
        # Get text content
        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        
        return cleaned_content
    except Exception as e:
        logger.error(f"Error cleaning body content: {e}")
        return ""

def split_dom_content(dom_content, max_length=6000):
    """Split content into chunks"""
    if not dom_content:
        return []
    
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

# Alternative fallback scraper using requests (for simple pages)
def fallback_scrape(website):
    """Fallback scraper using requests (no JavaScript support)"""
    import requests
    
    try:
        logger.info(f"Attempting fallback scrape for: {website}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(website, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Fallback scrape failed: {e}")
        raise

# Main scraping function with fallback
def scrape_with_fallback(website):
    """Try main scraper first, fallback to requests if needed"""
    try:
        return scrape_website(website)
    except Exception as e:
        logger.warning(f"Main scraper failed: {e}")
        logger.info("Attempting fallback scraper...")
        return fallback_scrape(website)
