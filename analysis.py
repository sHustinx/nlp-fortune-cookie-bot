# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:12:59 2022

@author: Saskia Hustinx

- general linguistic analysis, word lenght etc,
- most frequent words/n-grams per category
- sentiment

https://towardsdatascience.com/text-analysis-feature-engineering-with-nlp-502d6ea9225d
"""

import pandas as pd

## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
import wordcloud
## for text processing
import re
import nltk
## for sentiment
from textblob import TextBlob


dtf = pd.read_csv("./data/horoscope_saved.csv")

lst_stopwords = nltk.corpus.stopwords.words("english")

def utils_preprocess_text(text, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
                
    ## back to string from list
    text = " ".join(lst_text)
    return text

dtf["text_clean"] = dtf["horoscope"].apply(lambda x: utils_preprocess_text(x, lst_stopwords))
    
dtf['word_count'] = dtf["horoscope"].apply(lambda x: len(str(x).split(" ")))
dtf['char_count'] = dtf["horoscope"].apply(lambda x: sum(len(word) for word in str(x).split(" ")))
dtf['sentence_count'] = dtf["horoscope"].apply(lambda x: len(str(x).split(".")))
dtf['avg_word_length'] = dtf['char_count'] / dtf['word_count']
dtf['avg_sentence_lenght'] = dtf['word_count'] / dtf['sentence_count']
print(dtf.head())

# sentiment analysis
dtf["sentiment"] = dtf['horoscope'].apply(lambda x: 
                   TextBlob(x).sentiment.polarity)
dtf.head()

x, y = "sentiment", "category"
fig, ax = plt.subplots(nrows=1, ncols=2)
fig.suptitle(x, fontsize=12)
for i in dtf[y].unique():
    sns.distplot(dtf[dtf[y]==i][x], hist=True, kde=False, 
                 bins=10, hist_kws={"alpha":0.8}, 
                 axlabel="histogram", ax=ax[0])
    sns.distplot(dtf[dtf[y]==i][x], hist=False, kde=True, 
                 kde_kws={"shade":True}, axlabel="density",   
                 ax=ax[1])
ax[0].grid(True)
ax[0].legend(dtf[y].unique())
ax[1].grid(True)

plt.savefig("./output/sentiment.svg")
plt.show()

top = 10

y = "birthday"
corpus = dtf[dtf["category"]==y]["text_clean"]
lst_tokens = nltk.tokenize.word_tokenize(corpus.str.cat(sep=" "))
fig, ax = plt.subplots(nrows=1, ncols=2)
fig.suptitle("Most frequent words", fontsize=15)
    
## unigrams
dic_words_freq = nltk.FreqDist(lst_tokens)
dtf_uni = pd.DataFrame(dic_words_freq.most_common(), 
                       columns=["Word","Freq"])
dtf_uni.set_index("Word").iloc[:top,:].sort_values(by="Freq").plot(
                  kind="barh", title="Unigrams", ax=ax[0], 
                  legend=False).grid(axis='x')
ax[0].set(ylabel=None)
    
## bigrams
dic_words_freq = nltk.FreqDist(nltk.ngrams(lst_tokens, 2))
dtf_bi = pd.DataFrame(dic_words_freq.most_common(), 
                      columns=["Word","Freq"])
dtf_bi["Word"] = dtf_bi["Word"].apply(lambda x: " ".join(
                   string for string in x) )
dtf_bi.set_index("Word").iloc[:top,:].sort_values(by="Freq").plot(
                  kind="barh", title="Bigrams", ax=ax[1],
                  legend=False).grid(axis='x')
ax[1].set(ylabel=None)
plt.show()

dic_words_freq = nltk.FreqDist(nltk.ngrams(lst_tokens, 3))
dtf_tri = pd.DataFrame(dic_words_freq.most_common(), 
                      columns=["Word","Freq"])
dtf_tri["Word"] = dtf_tri["Word"].apply(lambda x: " ".join(
                   string for string in x) )
dtf_tri.set_index("Word").iloc[:top,:].sort_values(by="Freq").plot(
                  kind="barh", title="Trigrams", ax=ax[1],
                  legend=False).grid(axis='x')

wc = wordcloud.WordCloud(background_color='white', max_words=100, 
                         max_font_size=40)

wc = wc.generate(str(corpus))
fig = plt.figure(num=1)
plt.axis('off')
plt.imshow(wc, cmap=None)
plt.show()

print(dtf.describe())

categories = ["general", "career", "love", "wellness", "birthday"]
for i in enumerate(categories):
    y = cat
    corpus = dtf["text_clean"]   # split per category: dtf[dtf["category"]==y]["text_clean"]
    lst_tokens = nltk.tokenize.word_tokenize(corpus.str.cat(sep=" "))
    
    dic_words_freq = nltk.FreqDist(nltk.ngrams(lst_tokens, 3))
    dtf_n = pd.DataFrame(dic_words_freq.most_common(), 
                          columns=["Word","Freq"])
    dtf_n["Word"] = dtf_n["Word"].apply(lambda x: " ".join(
                       string for string in x) )
    dtf_n.set_index("Word").iloc[:top,:].sort_values(by="Freq").plot(
                      kind="barh", title="n-grams", ax=ax[1],
                      legend=False).grid(axis='x')
    
    print(cat)
    print(dtf_n.iloc[:top,:])
print()



