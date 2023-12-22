
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Union, List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer


# Task 5 - Dimensionality Reduction
def task5(bow_df: pd.DataFrame, tokens_plot_filename: str, distribution_plot_filename: str) -> Dict[str, Union[List[str], List[float]]]:
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.
    # Implement Task 5 here

    # Produce a bag of words representation of words across all pages 
    corpus = list(bow_df['words'])
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform(corpus)

    # Normalization 
    transformer = Normalizer(norm='max')
    bow_normalized = transformer.fit_transform(bow)
   
    # PCA using 2 components 
    pca = PCA(n_components=2, random_state=535)
    bow_pca = pca.fit_transform(bow_normalized.toarray())
    
    # Get the feature names from the vectorizer
    feature_names = vectorizer.get_feature_names_out()
    
    # create a sorted list of indices of the pca components in reverse
    sorted_indices_0 = np.argsort(pca.components_[0])[::-1]
    sorted_indices_1 = np.argsort(pca.components_[1])[::-1]

    #  create a list of the top 10 most positively and negatively weighted tokens for each component
    top10_positive_0 = [feature_names[i] for i in sorted_indices_0[:10]]
    top10_negative_0 = [feature_names[i] for i in sorted_indices_0[-10:]]
    top10_positive_1 = [feature_names[i] for i in sorted_indices_1[:10]]
    top10_negative_1 = [feature_names[i] for i in sorted_indices_1[-10:]]

    # create a list of the weights corresponding to the top 10 most positive and negative tokens
    positive_weights_0 = [pca.components_[0][vectorizer.vocabulary_[token]] for token in top10_positive_0]
    negative_weights_0 = [pca.components_[0][vectorizer.vocabulary_[token]] for token in top10_negative_0]
    positive_weights_1 = [pca.components_[1][vectorizer.vocabulary_[token]] for token in top10_positive_1]
    negative_weights_1 = [pca.components_[1][vectorizer.vocabulary_[token]] for token in top10_negative_1]

    # create a dictionary where the PCA component ID corresponds to the weights and words of the top 10 most positive and negative PCA values
    result_dict = {
    '0': {
        'positive': top10_positive_0,
        'negative': top10_negative_0,
        'positive_weights': positive_weights_0,
        'negative_weights': negative_weights_0
    },
    '1': {
        'positive': top10_positive_1,
        'negative': top10_negative_1,
        'positive_weights': positive_weights_1,
        'negative_weights': negative_weights_1
    }
}
   # Plot the top 10 most positively weighted tokens and their weights and 10 most negatively weighted tokens and their weights for each component
    figure, axs = plt.subplots(2, figsize=(10, 7), gridspec_kw={'hspace': 0.3})
    plt.suptitle('Top 10 Most Weighted Tokens', fontsize=16)
    for i, component in enumerate(['0', '1']):
        axs[i].barh(y=result_dict[component]['positive'], width=result_dict[component]['positive_weights'], color='purple', alpha=0.8, label='Positive')
        axs[i].barh(y=result_dict[component]['negative'], width=result_dict[component]['negative_weights'], 
        color='lightblue', alpha=0.8, label='Negative')
        axs[i].set_title(f'Component {component}', fontsize=14)
        axs[i].set_xlabel('Weight', fontsize=14)
        axs[i].set_ylabel('Token', fontsize=14)
        axs[i].tick_params(axis='y', labelsize=7)
        axs[i].legend()
    plt.savefig(tokens_plot_filename)
    
   

    # Plot where articles from each seed_url fall on the 2-component axes
    plt.figure(figsize=(10, 8))

    for seed_url in bow_df['seed_url'].unique():
        urls = bow_df[bow_df['seed_url']==seed_url]
        bow_pca_urls = bow_pca[bow_df['seed_url']==seed_url]
        plt.scatter(bow_pca_urls[:, 0], bow_pca_urls[:, 1], label=seed_url)

    plt.title('Location of URLs on a 2-Component Axes', fontsize=14)
    plt.xlabel('1st Principle Component', fontsize=14)
    plt.ylabel('2nd Principle Component', fontsize=14)
    plt.legend()

    plt.savefig(distribution_plot_filename)

    return result_dict




