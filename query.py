from bs4 import BeautifulSoup
import requests
import random
import json
from userAgents import userAgentList
from getAddress import get_url
import re

# url = "https://httpbin.io/user-agent"
# url = "https://www.zillow.com/homedetails/5157-Chena-Hot-Springs-Rd-Fairbanks-AK-99712/74498488_zpid/"

session = requests.Session()


# Set a User-Agent to mimic a browser
headers = {
    "User-Agent": random.choice(userAgentList),
    "Referer": "https://www.zillow.com/",
    "Accept-Language": "en-US,en;q=0.5",
}


def get_details(url):
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
    print(price[0].text)
    res["Price"] = price[0].text

    # parse for the number of rooms and square footage
    info = soup.find_all("div", {"data-testid": "bed-bath-sqft-fact-container"})
    # info = soup.find_all("span", {"data-testid": "bed-bath-item"})

    for i in range(len(info)):
        current_info = re.split(r"([0-9,]+)", info[i].text)
        print(" ".join(current_info))
        if i == 0:
            res["Rooms"] = current_info[1]
        elif i == 1:
            res["Baths"] = current_info[1]
        else:
            res["SqFt"] = current_info[1]

    json_string = soup.find_all("script", {"id": "__NEXT_DATA__"})[0].string
    test = json.loads(json_string)
    # load the json string
    json_convert = json.loads(
        test["props"]["pageProps"]["componentProps"]["gdpClientCache"]
    )

    first_key = next(iter(json_convert))
    description = json_convert[first_key]["property"]["description"]
    print(description)
    res["Description"] = description

    schools = json_convert[first_key]["property"]["schools"]

    for school in schools:
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
    # with open("record2.json", "w", encoding="utf-8") as file:
    #     file.write(test)

    # with open("record.json", "w", encoding="utf-8") as f:
    #     json.dump(json_convert, f)
    return res


def query(address):
    url = get_url(address)
    return get_details(url)
