# HF-recipes-etl
Solution for the Hello Fresh technical challenge by Luca Mircea

This file is an ETL that produces the difficulty level for recipes containing a certain ingredient.

A function is defined that takes as an input a number x and returns the categories 'Unknown' for x = 0, 'Easy', for x < 30, 'Medium' for 30 <= x <= 60, and 'Hard' for x > 60.

The script then reads the json file provided and converts it into a dataframe. One of the columns in this dataframe is the ingredients list, given as a continuous string.

Then it processes the column with the ingredient lists by replacing "\n" and "," with blank space ' ' in each row, to make sure that the beginnings of words are easily found. The ingredients list is also converted to uppercase letters to make sure no instance is missed due to case mismatches.

Then, a shorter dataframe is created by selecting only the rows that contain the string ' CHIL' in the ingredients list string. These are going to be words that start with CHIL, and they include all the derivatives of "chilies", the target word, but also the word "chilled".

The next step subsets the dataframe by splitting all ingredient lists into individual words or characters (it splits at a blank space ' ') and selecting only the rows that contain minimum one word which starts with "CHIL" but doesn't end in "D", to make sure that the rows which only contain "CHILLED"s are left out.

Then, the total time required is calculated by parsing the minutes and hours from the prepTime and cookTime columns, which are then added up after multiplying the hours by 60 to convert them into minutes. The final value is given in minutes.

Then, the function defined in the beginning is applied to the column with the total time required in order to produce the difficulty level in an additional column.

Finally, the column with the total time required is dropped (as it is no longer needed) and a CSV file with the output is created.
