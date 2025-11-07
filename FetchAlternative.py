from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import sys
import time

def get_visible_text(url):
    """
    Fetches a webpage using a real browser (headless Chrome)
    to render JavaScript, then extracts all visible text.
    Removes content from <script>, <style>, <head>, <title>, and <meta> tags.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        str: A string containing the cleaned, visible text,
             or None if an error occurred.
    """
    try:
        # Set up Chrome options to run "headless" (without a visible window)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("window-size=1920x1080")
        
        # Automatically install and set up the correct Chrome driver
        service = Service(ChromeDriverManager().install())
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Open the URL
        driver.get(url)
        
        # *** Wait for the JavaScript to load the content ***
        # We'll wait 5 seconds. For more complex pages, this might need to be longer
        # or use a more advanced "explicit wait".
        #time.sleep(5) 
        
        # Get the final, rendered page source (HTML)
        html = driver.page_source
        
        # Close the browser
        driver.quit()
        
        # Now, parse the final HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove all script and style elements
        for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            element.decompose()
        
        # Get the text, using a space as a separator
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace:
        # 1. Split text into lines
        # 2. Strip whitespace from each line
        # 3. Filter out any blank lines
        # 4. Join the lines back together with a single newline
        lines = (line.strip() for line in text.splitlines())
        clean_lines = (line for line in lines if line)
        clean_text = '\n'.join(clean_lines)
        
        return clean_text

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    
    return None

if __name__ == "__main__":
    # The URL that needs JavaScript
    target_url = ""
    
    print(f"Fetching visible text from: {target_url}\n")
    
    visible_text = get_visible_text(target_url)
    
    if visible_text:
        print("--- Start of Extracted Text ---")
        print(visible_text)
        print("--- End of Extracted Text ---")
    else:
        print("Failed to retrieve text.")

