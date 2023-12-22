

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import defaultdict


# Task 4 - Plotting the Most Common Words 
def task4(bow: pd.DataFrame, output_plot_filename: str) -> Dict[str, List[str]]:
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.
    # Implement Task 4 here

    # create a dictionary
    most_pop_words = defaultdict(list)
    most_pop_words_df = pd.DataFrame(columns=[ "seed_url", "word", "total occurrences"]) 
    rows = []

    # create a list of words corresponding to a seed_url
    seed_words = defaultdict(list)
    for index, row in bow.iterrows():
        seed_words[row['seed_url']].extend((row['words']).split())
   
    #find the 10 most popular words 
    for seed_url, words in seed_words.items():
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        most_pop = sorted(word_count.items(), key = lambda x: x[1], reverse=True)[:10]
        top10 = []
        for tup in most_pop:
            top10.append(tup[0])
            rows.append({"seed_url": seed_url, "word": tup[0] , "total occurrences": tup[1]})
        most_pop_words[seed_url] = top10

    # create a dataframe and based on that create a bar chart
    most_pop_words_df = pd.concat([most_pop_words_df, pd.DataFrame(rows)])
    figure, ax = plt.subplots(figsize=(10, 8))
    groups = most_pop_words_df.groupby('seed_url')
    color = ['darkblue','grey']
    for i, (name, group) in enumerate(groups):
        ax.barh(group['word'], group['total occurrences'], label=name, alpha=0.8, color = color[i])
    ax.legend()
    ax.set_xlabel('Total Occurrences', fontsize=20)
    ax.set_ylabel('Word', fontsize=20)
    plt.title('Top 10 Most Common Words From a Seed Url', fontsize = 20)
    plt.savefig(output_plot_filename)
    
    return most_pop_words
