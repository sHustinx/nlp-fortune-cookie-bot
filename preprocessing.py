# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 15:42:35 2022

- lowercasing input data
- removal of filtered words
- conversion ot single-column csv for training

@author: Saskia Hustinx
"""

import pandas as pd

removal_list = [", aries",", taurus",", gemini",", cancer", ", leo", ", virgo", ", libra", ", scorpio", ", sagittarius", ", capricorn", ", aquarius", ", pisces",
                "aries","taurus","gemini","cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
                ]
    
    
df = pd.read_csv("./data/horoscope_saved.csv", usecols=["horoscope"])

# lowercase and remove filter words
for index, row in df.iterrows():
    row[0] = row[0].lower()
    for word in removal_list:
        row[0] = row[0].replace(word, "")


print(df['horoscope'][0])

df.to_csv('./data/clean-data.csv', index=False)