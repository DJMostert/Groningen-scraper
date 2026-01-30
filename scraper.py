import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')

TARGETS = [
    {
        "name": "FREE STUFF",
        "url": "https://www.gratisaftehalen.nl/nl/groningen",
        "selector": "h2.listing-item__title" # Typical class for this site
    }
]

def run_scraper():
    for target in TARGETS:
        print(f"Checking {target['name']}...")
        # Add a 'User-Agent' so the site doesn't think you're a basic bot
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        response = requests.get(target['url'], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        listings = soup.select(target['selector'])

        for item in listings[:3]: # Ping only top 3 to avoid spamming your Discord
            title = item.get_text(strip=True)
            # Find the link (usually the parent or a child <a> tag)
            link_tag = item.find_parent('a') or item.find('a')
            link = link_tag['href'] if link_tag else target['url']
            
            # Formatting for Discord
            message = {
                "content": f"🎁 **{target['name']} Found!**\n**{title}**\n🔗 {link if link.startswith('http') else target['url'] + link}"
            }
            requests.post(WEBHOOK_URL, json=message)

if __name__ == "__main__":
    run_scraper()
