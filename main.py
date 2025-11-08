from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

app = Flask(__name__)
# CORS(app,origins="https://privofy.netlify.app")
CORS(app)
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Backend active"})

@app.route("/api/GetData", methods=["POST"])
def get_ground():
    """
    Fetches all content from a page, bypassing general web scraping stoping methords
    """
    #POST
    data = request.json
    url= data.get("URL") 

    #GET
    # url = request.args.get("URL")
    try:
        print('1')
        # Set up Chrome options to run "headless" (without a visible window)
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/google-chrome"

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print('3')
        # Open the URL
        driver.get(url)
        
        # Get the final, rendered page source (HTML)
        html = driver.page_source
        
        # Close the browser
        driver.quit()
        print('4')
        # Now, parse the final HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove all script and style elements
        for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            element.decompose()
        
        # Get the text, using a space as a separator
        text = soup.get_text(separator=' ', strip=True)
        print('5')
        lines = (line.strip() for line in text.splitlines())
        clean_lines = (line for line in lines if line)
        clean_text = '\n'.join(clean_lines)
        
        return jsonify({'Text':clean_text})

    except Exception as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

