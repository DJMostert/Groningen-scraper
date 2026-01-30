import requests
from bs4 import BeautifulSoup
import os

# Get the secret from GitHub environment
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
TARGET_URL = "https://www.makeitinthenorth.nl/jobs?location=Groningen&level=Entry"

def run_scraper():
    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # This finds job titles (Make it in the North uses <h2> for titles)
    listings = soup.find_all('h2') 

    for item in listings[:5]: # Check the first 5 latest items
        title = item.get_text(strip=True)
        link = TARGET_URL # In a real script, we'd extract the specific href link
        
        message = {"content": f"🚀 **New Job Alert:** {title}\nLink: {link}"}
        requests.post(WEBHOOK_URL, json=message)
        print(f"Sent: {title}")

if __name__ == "__main__":
    run_scraper()
