

import pandas as pd
import json
from typing import Dict, List

import requests
import bs4
import urllib
from robots import process_robots, check_link_ok


# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000


# Task 1 - Get All Links
def task1(starting_links: List[str], json_filename: str) -> Dict[str, List[str]]:
    # Crawl each url in the starting_link list, and output
    # the links you find to a JSON file, with each starting
    # link as the key and the list of crawled links for the
    # value.
    # Implement Task 1 here
    urls = {}

    for link in starting_links:
        urls[link] = sorted(list(findlinks(link)))

    with open(json_filename, 'w') as f:
        json.dump(urls, f)

    return {}

def findlinks(starting_link, visited=None):
    if visited is None:
        visited = {}
    base_url = 'http://115.146.93.142'
    robot_rules = process_robots(starting_link)
    reqs = requests.get(starting_link)
    pages_visited = 1
    soup = bs4.BeautifulSoup(reqs.text, 'html.parser')
    visited[starting_link] = True
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    # only include links that start with base_url
    filtered_links = [link for link in links if link is not None and (link.startswith('/samplewiki/') or link.startswith('/fullwiki/'))]
    # remove duplicate links and sort the list alphabetically
    filtered_links = sorted(list(set(filtered_links)))
    final_links = []
    for link in filtered_links:
        full_link = base_url+link
        if check_link_ok(robot_rules, full_link):
            final_links.append(full_link)
    # crawl and find more links
    for link in filtered_links:
         full_link = base_url + link
         if full_link not in visited.keys() and check_link_ok(robot_rules, full_link):
             pages_visited += 1
             final_links.extend(findlinks(full_link, visited))
    final_links = set(final_links)
    return final_links






