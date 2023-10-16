import asyncio

import requests
from bs4 import BeautifulSoup

python_links = set()
visited_links = set()


async def fetch_page(url):
    print("Visiting: " + url)
    visited_links.add(url)
    response = requests.get(url, timeout=10)
    # find links in page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for link in links:
        if "href" not in link.attrs:
            continue
        # strip off the hash and add back the domain
        link_path = link["href"].split("#")[0]
        if link_path.startswith("/"):
            link_path = "https://playwright.dev" + link_path
        if link_path not in python_links:
            print("Found link to: " + link_path)
            if link_path.startswith("https://playwright.dev/python/docs/") or link_path.startswith(
                "/python/docs/"
            ):
                print("Fetching: " + link_path)
                python_links.add(link_path)
                await fetch_page(link_path)


async def build_urls():
    await fetch_page("https://playwright.dev/python/")
    with open("urls.txt", "w") as f:
        for link in python_links:
            f.write(link + "\n")


asyncio.run(build_urls())
