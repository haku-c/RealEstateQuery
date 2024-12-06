from bs4 import BeautifulSoup
import requests
import random
import json
from userAgents import userAgentList
from getAddress import get_url
import re


session = requests.Session()


# Set a User-Agent to mimic a browser
headers = {
    "User-Agent": random.choice(userAgentList),
    "Referer": "https://www.zillow.com/",
    "Accept-Language": "en-US,en;q=0.5",
}


def get_details(url, debug=False):
    res = {
        "Price": 0,
        "Rooms": 0,
        "Baths": 0,
        "SqFt": 0,
        "Description": None,
        "Schools": [],
    }
    response = session.get(url, headers=headers)

    # check to see if your response was processed or not
    if response.status_code != 200:
        print(response.status_code)
        return

    response_contents = response.text

    soup = BeautifulSoup(response_contents, "html.parser")

    # parse to find the listed price
    price = soup.find_all("span", {"data-testid": "price"})
    if len(price) == 0:
        price = soup.find_all("span", {"data-testid": "zestimate-text"})
        res["Price"] = price[0].text.split(":")[1].strip()
    else:
        res["Price"] = price[0].text

    if debug:
        print(price[0].text)

    # parse for the number of rooms and square footage
    info = soup.find_all("div", {"data-testid": "bed-bath-sqft-fact-container"})

    if len(info) == 0:
        info = soup.find_all("span", {"data-testid": "bed-bath-item"})

    for i in range(len(info)):
        current_info = re.split(r"([0-9,]+)", info[i].text)
        if debug:
            print(" ".join(current_info))
        if i == 0 and len(current_info) > 2:
            res["Rooms"] = current_info[1]
        elif i == 1 and len(current_info) > 2:
            res["Baths"] = current_info[1]
        elif i == 2 and len(current_info) > 2:
            res["SqFt"] = current_info[1]

    # below logic parses the javascript to load information only accessible on scroll
    json_string = soup.find_all("script", {"id": "__NEXT_DATA__"})[0].string
    test = json.loads(json_string)
    # load the json string
    json_convert = json.loads(
        test["props"]["pageProps"]["componentProps"]["gdpClientCache"]
    )

    first_key = next(iter(json_convert))
    description = json_convert[first_key]["property"]["description"]
    if debug:
        print(description)
    res["Description"] = description

    schools = json_convert[first_key]["property"]["schools"]

    for school in schools:
        if debug:
            print(
                " ".join(
                    [
                        school["name"],
                        f'({school["type"]}, {school["level"]})',
                        "rated",
                        str(school["rating"]),
                        "out of 10 at a distance of",
                        str(school["distance"]),
                        "miles.",
                    ]
                )
            )
        res["Schools"].append(
            {
                "Name": school["name"],
                "Rating": school["rating"],
                "Distance": school["distance"],
                "Level": school["level"],
                "Type": school["type"],
            }
        )
    return res


def query(address, debug=False):
    try:
        url = get_url(address)
        details = get_details(url)
        if debug:
            print(details)

    except:
        print("There was an error processing this request. Check the address inputted.")
        details = None
    return details
