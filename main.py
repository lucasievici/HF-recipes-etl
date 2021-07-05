# Hello Fresh challenge
# Solution by Luca Mircea
"""
This script loads a dataset of recipes
Fetches those that have 'chilies' while accounting for errors like misspelling, singular, etc.
Then it adds a difficulty level column based on some of their properties

The submission must include docstrings, a README.md file, a requirements.txt, and the csv produced

This script was written in Python 3.8.10
"""

import pandas as pd
import json
import os
import re

# functions


def difficulty(x):
    """
    function to assign difficulty based on total cooking and prep time
    :param x: cooking time in minutes
    :return: difficulty category 'easy' (1-29 min), 'medium' (30-60 min), 'hard' (61+), 'unknown' for 0
    """
    if x == 0:
        return "Unknown"
    if 0 < x < 30:
        return 'Easy'
    if 30 <= x <= 60:
        return 'Medium'
    if x > 60:
        return 'Hard'


"""
Step 1: get the data ready
I'll create a nice path that can work on any system
Then we'll get the json data and make it into a nice dataframe
"""
cd = os.getcwd()
fp = os.path.join(cd, 'recipes.json')
data = [json.loads(line) for line in open(fp, 'r')]

recipes = pd.json_normalize(data)

"""
The data is now ready. Let's get recipes with chilies
To make sure we catch everything, we'll stem the word first

The Lancaster Stemmer proposes 'chi' as them stem.
However, this will also capture 'chips' or 'chives' or other such ingredients
I think 'chil' might be better - it also gets 'chilled', but this is easy to remove

1) We replace ',' and the \n character with space in the recipe dataset to make sure 
we catch everything that starts with "chil" - otherwise we could have stuff like
"\nchilies" that regex might miss. We also turn everything into upper case

2) We make a dataframe with entries that have ' chil' in the ingredients list to reduce the search

3) We only keep entries that have 'chil' but don't end in D, to exclude 'chilled'
"""
recipes.ingredients = recipes.ingredients.str.replace('\n|,', ' ').str.upper()  # remove new line and comma characters

chili_recipes = recipes[recipes.ingredients.str.contains(' CHIL')].reset_index(drop=True)

r = re.compile('CHIL.*[^D]$')  # words that start with "chil" but don't end in d

chili_recipes = chili_recipes[
    chili_recipes.ingredients.str.split(' ').apply(lambda x: any(r.match(y) for y in x))].reset_index(drop=True)

"""
We have the recipes that have chilies in them
I've also included misspellings, derivatives, etc, 
but I've removed entries that only contain 'chilled' as a match

Now it's time to get the total preparation time and assign a difficulty level based on it
"""

chili_recipes['tot_time_min'] = \
    (chili_recipes.prepTime.apply(lambda x:  # get Min from prepTime
                                  re.findall(r"(\d+)M", x)).explode().fillna(0).astype(int) +
     chili_recipes.prepTime.apply(lambda x:  # get H from prepTime
                                  re.findall(r"(\d+)H", x)).explode().fillna(0).astype(int) * 60 +
     chili_recipes.cookTime.apply(lambda x:  # get Min from cookTime
                                  re.findall(r"(\d+)M", x)).explode().fillna(0).astype(int) +
     chili_recipes.cookTime.apply(lambda x:  # get H from cookTime
                                  re.findall(r"(\d+)H", x)).explode().fillna(0).astype(int) * 60
     )

chili_recipes['difficulty'] = chili_recipes.tot_time_min.apply(lambda x: difficulty(x))
chili_recipes = chili_recipes.drop(columns=['tot_time_min'])

chili_recipes.to_csv('chili_recipes_difficulty.csv')
