# HelloFresh-CaseStudy

The file open_recipes_local_data.txt contains a list of recipes in JSON format that was previously obtained from https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json, provided in the Hello Frsh Case Study.

The file assignemnts.py is the script that generates the results.csv by using the data present in open_recipes_local_data.txt.

What does assignment.py do?
It will create a recipe panda data frame based on data from open_recipes_local_data.txt.
Then it will extract from that dataframe, all the recipes that have chillies as an ingredient.
Secondly, it will add a new column to the resulting dataframe, that represents the difficulty of each recipe. If a recipe needs more than 1 hour to be concluded it is classified as Hard, Easy if in less than 30 minutes and Medium if in between. 
The resulting dataset is saved in the results.csv file.

To run the code, create a virtual environment, install there the requirements.txt and finally run the assignments.py file.
This project was developed using Python 3.10.4.
