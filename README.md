To run, install requirements listed in the requirements.txt and run 

```
python solution.py
```
I organized the python solution with repeatability and extendability in mind. 
## Summary
I looked for different types of trends (described in the Graph section) but didn't find any. All articles were majority neutral, which is to be expected for fact based articles with little discernable bias. Most were also negative, which is also to be expected from news in general, but especially in a country with unrest and natural disasters. My manual check leads me to largely agree with the sentiment analysis, with the only semi-positive article being the one about a humanitarian mission. 

## Code
First, all variables are listed in the beginning. Most are self-explanatory, but two variables need explaining:
the text_tag refers to the class of only the text from the articles’ html
the article prefix uses the fact that all article links begin with "/news/2", will not work for articles written before 2000

The first section saves links found on the parent page. The next uses these links to access the articles’ raw html. The one after that preprocesses the article into text only. 

I then use vader from nltk to tokenize the articles into sentences, on which I run the sentiment analysis. I chose to do this to see if any interesting patterns evolved from the structure of each article (e.g. if the beginning may be more positive or negative than the middle of each article). No such patterns were clear. I chose Vader as my tool because it is a popular off-the-shelf model with plenty of documentation. Though it comes trained for analyzing sentiments on social media, I still think it is one of the best options in terms of generating a quick analysis because of both dev and runtime efficiency. Given more time, I would train it on a more relevant corpus (like Reuters).  

## Graph :
I didn’t see any clear patterns over any single article, in that they mostly stayed constant over all the sentences within. I also looked for patterns over time, but no significant trends existed on that front either. In the end, I just graphed all the articles and their sentiment values in a large bar graph.

## JSON :
The links were guaranteed to be unique for each article accessed, so I used those as the main keys. I outputted all of the processed text content and results I got from running the sentiment analysis.I did not include the raw html content because it made the output JSON too large to work with. 

The total operation time was ~ 3 seconds for me. 
