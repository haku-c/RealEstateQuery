from bs4 import BeautifulSoup
import requests
import random
import json
import urllib.parse

# url = "https://httpbin.io/user-agent"
# url = "https://www.zillow.com/homedetails/5157-Chena-Hot-Springs-Rd-Fairbanks-AK-99712/74498488_zpid/"

session = requests.Session()

# randomizing the user agent to avoid 403 error
userAgents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675787110",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5412.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5361.172 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5388.177 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5397.215 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
]

# Set a User-Agent to mimic a browser
headers = {
    "User-Agent": random.choice(userAgents),
}


def getUrl(address):
    base_url = "https://www.zillow.com/homes/"
    encoded_address = urllib.parse.quote(address)
    search_url = f"{base_url}{encoded_address}_rb/"
    return search_url


def getDetails(url):
    response = session.get(url, headers=headers)

    # check to see if your response was processed or not
    # print(response.status_code)
    # print(response.text)

    response_contents = response.text

    soup = BeautifulSoup(response_contents, "html.parser")

    # parse a description
    # description = soup.find_all("div", {"data-testid": "description"})
    # print(description[0].text)

    # parse to find the listed price
    price = soup.find_all("span", {"data-testid": "zestimate-text"})
    print(price[0].texts.split(" ")[1])

    # parse for the number of rooms and square footage
    # info = soup.find_all("div", {"data-testid": "bed-bath-sqft-fact-container"})
    info = soup.find_all("span", {"data-testid": "bed-bath-item"})

    for i in range(len(info)):
        print(info[i].text)

    json_string = soup.find_all("script", {"id": "__NEXT_DATA__"})[0].string
    test = json.loads(json_string)
    # load the json string
    json_convert = json.loads(
        test["props"]["pageProps"]["componentProps"]["gdpClientCache"]
    )

    first_key = next(iter(json_convert))
    description = json_convert[first_key]["property"]["description"]
    print(description)

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
    # with open("record2.json", "w", encoding="utf-8") as file:
    #     file.write(test)

    with open("record.json", "w", encoding="utf-8") as f:
        json.dump(json_convert, f)
