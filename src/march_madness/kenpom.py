from __future__ import annotations

import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from march_madness import Bracket

known_good_html_path = Path("data/kenpom/known_good.html")
latest_html_path = Path("data/kenpom/latest.html")
known_good_json_path = Path("data/kenpom/known_good.json")

# URL of the webpage containing the table
url = "https://kenpom.com/"


def download_html_from_url() -> None:
    """Get the HTML content save it to `latest_html_path`."""
    print(f"Downloading HTML from {url}")
    # Set up the WebDriver (e.g., Chrome)
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration
    # options.add_argument('--no-sandbox')   # Bypass OS security model
    # options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get(url)

    # Get the page source
    html = driver.page_source

    # Close the WebDriver
    driver.quit()
    # Save the HTML content to the latest_html_path
    with open(latest_html_path, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML saved to {latest_html_path}")


def parse_html(path: Path) -> dict[str, float] | None:
    """Attempt Parse the HTML content of the file at the path."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            html = file.read()
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="ratings-table")

        name_to_kenpom = {}

        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 0:
                names = cells[1].find("a").text
                kenpom = float(cells[4].text)
                name_to_kenpom[names] = kenpom
                # rows.append([cell.text for cell in cells])
        return name_to_kenpom
    except Exception:
        return None


def update_all_from_website():
    download_html_from_url()
    latest = parse_html(latest_html_path)
    if latest is not None:
        print("New data found and successfully parsed.")
        with open(known_good_json_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(latest, indent=4))
        with open(known_good_html_path, "w", encoding="utf-8") as file:
            file.write(latest_html_path.read_text())
    else:
        print("Unable to get new data for some reason.")
    # known_good = parse_html(known_good_html_path)

    # if latest and known_good:
    #     with open(known_good_json_path, 'w', encoding='utf-8') as file:
    #         file.write(known_good)

    #     if latest != known_good:
    #         print("New data found!")
    #         print(latest)
    #     else:
    #         print("No new data found.")
    # else:
    #     print("Error parsing HTML")


def get_kenpom_data() -> dict[str, float]:
    """Get the kenpom data from the known_good_json_path."""
    with open(known_good_json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def update_bracket_kenpoms(bracket: Bracket):
    kenpom_data = get_kenpom_data()
    for team in bracket.teams:
        # kenpom = kenpom_data.get(team.kenpom_id)
        # print(f"Updating {team.name} to {kenpom=}")
        team.kenpom = kenpom_data[team.kenpom_id]

    # for game in bracket.games:
    #     for team in [game.team1, game.team2]:
    #         if team is not None:
    #             team.kenpom = kenpom_data[team.kenpom_id]

    return bracket


if __name__ == "__main__":
    from rich.pretty import pprint

    update_all_from_website()

    kenpom_data = get_kenpom_data()
    pprint(kenpom_data)


# # Parse the HTML content of the page
# soup = parse_html(latest_html_path)

# # Find the table element with the id 'ratings-table'
# table = soup.find('table', id='ratings-table')

# name_to_kenpom = {}

# if table:
#     # Extract table headers
#     headers = [header.text for header in table.find_all('th')]

#     # Extract table rows
#     rows = []
#     for row in table.find_all('tr'):
#         cells = row.find_all('td')
#         if len(cells) > 0:
#             names = cells[1].text
#             kenpom = float(cells[4].text)
#             name_to_kenpom[names] = kenpom
#             rows.append([cell.text for cell in cells])

#     # Print the headers and rows
#     print(headers)
#     for row in rows:
#         print(row)

#     from rich.pretty import pprint
#     pprint(name_to_kenpom)
# else:
#     print("Table with id 'ratings-table' not found.")
#     # print(soup)
