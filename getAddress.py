import requests
from bs4 import BeautifulSoup
import re
import urllib
import random
from userAgents import userAgentList

session = requests.Session()


def get_url(address):
    # Format the address to be suitable for URL
    address = urllib.parse.quote(address)  # Replace spaces with '+' for URL encoding

    # Construct the Zillow search URL with the address
    url = f"https://www.zillow.com/homes/{address}_rb/"

    # Set user-agent to mimic a real browser request
    headers = {
        "User-Agent": random.choice(userAgentList),
        "Referer": "https://www.zillow.com/",
        "Accept-Language": "en-US,en;q=0.5",
    }

    # Send a GET request to the Zillow search page
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Use regex to find the ZPID in the page source
    zpid_match = re.search(r'"zpid":"(\d+)"', str(soup))
    zpid = zpid_match.group(1)
    final_url = f"https://www.zillow.com/homes/{address}_rb/{zpid}_zpid"
    print(final_url)
    return final_url


# Example usage
# address = "374 Parkland Dr, Fairbanks, AK 99712"
# url = get_url(address)
# print(url)
