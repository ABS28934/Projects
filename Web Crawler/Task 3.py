

from typing import Dict, List
import pandas as pd
import json
import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


from robots import process_robots, check_link_ok

# Task 3 - Producing a Bag Of Words for All Pages 
def task3(link_dictionary: Dict[str, List[str]], csv_filename: str):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename, and should have no extra
    # numeric index.
    # Implement Task 3 here

    # Empty dataframe to demonstrate output data format.
    dataframe = pd.DataFrame(columns=["link_url", "words", "seed_url"])

    rows = []
    #visit each link and find the words
    for seed_url, links in link_dictionary.items():
        for link_url in links:
            # Call the task2 function to extract words from link_url
            words = task2(link_url)

            # Create a row with the urls and words
            rows.append({"link_url": link_url, "words": " ".join(words), "seed_url": seed_url})

    # Concatenate each row to create the dataframe
    dataframe = pd.concat([dataframe, pd.DataFrame(rows)])

    # Sort dataframe by link_url and then seed_url
    dataframe = dataframe.sort_values(by=["link_url", "seed_url"])

    # Output a csv file without auto-indexing 
    dataframe.to_csv(csv_filename, index = False)

    return dataframe


def task2(link_to_extract: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    
    reqs = requests.get(link_to_extract)
    soup = bs4.BeautifulSoup(reqs.content, 'html.parser')
    
    #Stage 1
    # Step 1 - Use find to access the div element with id: mw-content-text
    mw_content_text = soup.find('div', {'id': 'mw-content-text'})
    
    # Step 2 - Remove all th elements with the class of infobox-label
    for th in mw_content_text.select('.infobox-label'):
        th.decompose()
    
    # Step 3 - Remove all div elements with the class of printfooter
    for div in mw_content_text.select('.printfooter'):
        div.decompose()
    
    # Step 4 - Remove the div element with the id of toc
    toc = mw_content_text.find('div', {'id': 'toc'})
    for div in mw_content_text:
        if toc:
            toc.decompose()
    
    # Step 5 - Remove all table elements with the class of ambox
    for table in mw_content_text.select('table.ambox'):
        table.decompose()
    
    # Step 6 - Remove all div elements with the class of asbox
    for div in mw_content_text.select('.asbox'):
        div.decompose()
    
    # Step 7 - Remove all span elements with the class of mw-editsection
    for span in mw_content_text.select('span.mw-editsection'):
        span.decompose()

    # Step 8 - Extract the text from the page
    text = mw_content_text.get_text(strip=True, separator=' ')

    # Stage 2  
    # Step 1 - Change all characters to their casefolded form
    text = text.lower()
    #Step 1 - Normalize all page text to its NFKD form
    text = unicodedata.normalize('NFKD', text)

# Step 2 - Convert non-alphabetic characters to single-space characters
    text = re.sub(r"[^a-z\s\\]", " ", text)

# Step 3 - Convert spacing characters to single-space characters
    text = re.sub(r"\s+", " ", text)

# Step 4 -  Converted to explicit tokens by splitting at single space characters
    tokens = text.split()

# Step 5 - Remove stop words
    tokens = [token for token in tokens if token not in stopwords.words('english')]

# Step 6 - Remove tokens with length less than 2 characters
    tokens = [token for token in tokens if len(token) >= 2]

# Step 7 - Convert tokens to Porter stemming algorithm stemmed form
    porterStemmer = PorterStemmer()
    tokens = [porterStemmer.stem(token) for token in tokens]

    return tokens
