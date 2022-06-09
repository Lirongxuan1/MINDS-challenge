#!/usr/bin/env python
# coding: utf-8


import plotly.express as px
import pandas as pd
import time
from datetime import datetime 
import requests
import json
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
nltk.download('punkt')
nltk.download('vader_lexicon')
start = time.time()


root_url = "https://www.aljazeera.com/"
parent_page = "where/mozambique/"
json_output = "articles.json"
text_class = "wysiwyg wysiwyg--all-content css-1ck9wyi"
# Prefix for links from Mozambique page
article_prefix = "/news/2"
# Get contents from root page
resp = requests.get(root_url + parent_page)
soup = BeautifulSoup(resp.text, 'html.parser')


# Get links from the parent page
links = []
for link in soup.find_all('a'):
    if link.get('href').startswith(article_prefix):
        links.append(link.get('href'))
# Sorting list to get most most recent
links = list(set(links))
links.sort(reverse=True)
links = links[:10]


# Fetch all raw articles
articles = []
for link in tqdm(links, desc = "Fetching raw articles"):
    resp = requests.get(root_url + link)
    article_soup = BeautifulSoup(resp.text, 'html.parser')
    articles.append(article_soup)


# Preprocess so only text is in article_texts
article_texts = []
for article_soup in tqdm(articles, desc = "Preprocessing articles"):
    # Use tag to find text only
    text = article_soup.find("div", {"class": text_class})
    # Get text from html tags, remove newline characters
    article_texts.append(text.get_text().replace('\n',' '))


article_sentence_sentiments = []
for art in tqdm(article_texts, desc = "Calculating sentiments"):
    sentiments = {'compound' : [], 'neg' : [], 'neu' : [],'pos' : []}
    sentences = sent_tokenize(art)
    for sent in sentences:
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sent)
        sentiments['compound'].append(ss['compound'])
        sentiments['neg'].append(ss['neg'])
        sentiments['neu'].append(ss['neu'])
        sentiments['pos'].append(ss['pos'])
    article_sentence_sentiments.append(sentiments)



article_average_sentiments = []
for sents in article_sentence_sentiments:
    art_sent = {}
    art_sent['compound'] = sum(sents['compound']) / len(sents['compound'])
    art_sent['neg'] = sum(sents['neg']) / len(sents['neg'])
    art_sent['neu'] = sum(sents['neu']) / len(sents['neu'])
    art_sent['pos'] = sum(sents['pos']) / len(sents['pos'])
    article_average_sentiments.append(art_sent)


average_sentiments_df = pd.DataFrame.from_dict(article_average_sentiments)
# Format the titles of articles
titles = [link.split('/')[len(link.split('/')) - 1] for link in links]
titles = [title.replace('-',' ').title() for title in titles]
# Add the dates of article publication
datestr = ["/".join(link.split('/')[2:-1]) for link in links]
dates = [datetime.strptime(date, "%Y/%m/%d") for date in datestr]
average_sentiments_df["titles"] = titles 
average_sentiments_df["dates"] = dates


# Export to JSON
# All indexes are in order
articles_json = {}
for ind in tqdm(range(10), desc = "Saving everything to JSON"):
    articles_json[links[ind]] = {}
    articles_json[links[ind]]["title"] = titles[ind]
    # Saving as datestr because datetime is not serializable
    articles_json[links[ind]]["date"] = datestr[ind]
    articles_json[links[ind]]["neg"] = article_average_sentiments[ind]["neg"]
    articles_json[links[ind]]["neu"] = article_average_sentiments[ind]["neu"]
    articles_json[links[ind]]["pos"] = article_average_sentiments[ind]["pos"]
    articles_json[links[ind]]["processed-content"] = article_texts[ind]
    


json_string = json.dumps(articles_json)
with open(json_output, 'w') as outfile:
    outfile.write(json_string)


# Generate Plotly
fig = px.bar(average_sentiments_df, x = "titles", y=["pos", "neu", "neg"],
              title = "Sentiment Change in Mozambique News Over Time", 
             barmode = "group", width=2000, height=1000 )
fig.update_layout(xaxis_title='Article Name', yaxis_title='Sentiment')
fig.show()
end = time.time()
print("Time Elapsed " +str(end - start))