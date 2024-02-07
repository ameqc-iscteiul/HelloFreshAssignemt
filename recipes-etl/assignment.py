import pandas as pd
import json


def main():
    """
    Executes the main steps of Python/Pandas HelloFresh Case Study.

    Steps:
    1. Reads the recipes;
    2. Extracts every recipe that has “Chilies” as one of the ingredients;
    3. Adds a 'difficulty' column based on total preparation time, as described in the README.md file;
    4. Saves the resulting DataFrame to 'results.csv'.
    """
    #1-Create Recipe df
    df = get_df()
    #2-Extract Recipies with Chillies
    matching_recipes = extract_recipes_from_ingredient(df)
    #3-Adds Difficulty column
    result = add_difficulty(matching_recipes)
    #4-Saves resulting df
    result.to_csv('results.csv', index=False)

def get_df():
    """
    Reads data from 'open_recipes_local_data.txt', converts the JSON data into a Pandas DataFrame,
    and returns the resulting DataFrame.

    Returns:
    -------
    pandas.DataFrame
        DataFrame containing the parsed recipes JSON data.
    """
    file_path = 'open_recipes_local_data.txt'
    json_list = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                json_data = json.loads(line)
                json_list.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line.strip()} - {e}")
    return pd.DataFrame(json_list)


def extract_recipes_from_ingredient(df):
    """
    Filters recipes from the given DataFrame based on a specified ingredient keyword.
    Currently keyword is hardcoded to 'Chil', since chillie was the specified ingredient to be extracted.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing recipe data.

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing recipes that include the chillie ingredient.
    """
    keyword = 'Chil'
    mask = df['ingredients'].str.contains(fr'\b{keyword}(?!led)\w*\b', case=False, regex=True)

    matching_recipes = df[mask]
    #matching_recipes = df.loc[mask, ['name']]
    return matching_recipes

def add_difficulty(old_df):
    """
    Adds a 'difficulty' column to the DataFrame based on the total preparation time.

    Parameters:
    -----------
    old_df : pandas.DataFrame
        DataFrame containing recipe data.

    Returns:
    --------
    pandas.DataFrame
        Updated DataFrame with an additional 'difficulty' column.
    """
    df = old_df.copy()
    #Create totalTime containing the sum of prep and cook Times
    df['totalTime'] = df.apply(lambda row: get_time(row['prepTime']) + get_time(row['cookTime']), axis=1)
    #Create difficulty column depending on the totalTime value
    df['difficulty'] = df['totalTime'].apply(determine_difficulty)
    #rem aux col
    df = df.drop('totalTime', axis=1)
    return df
    
def get_time(prep_time):
    """
    Extracts preparation time in minutes from the provided format.
    Example: From "PT1H30M" to 90 minutes

    Parameters:
    -----------
    prep_time : str
        The preparation time string in the format (e.g., "PT2H30M" for 2 hours and 30 minutes).

    Returns:
    --------
    int
        Total preparation time in minutes.
    """
    if 'PT' not in prep_time:
        return 0
    hours, minutes = 0, 0
    time_str = prep_time.replace('PT', '')
    if 'H' in time_str:
        hours = int(time_str.split('H')[0])
        time_str = time_str.split('H')[1]

    if 'M' in time_str:
        minutes = int(time_str.split('M')[0])
    total_minutes = hours * 60 + minutes
    return total_minutes

def determine_difficulty(total_time):
    """
    Determines the difficulty level of a recipe based on the total preparation time.

    Parameters:
    -----------
    total_time : int
        Total preparation time in minutes.

    Returns:
    --------
    str
        Difficulty level ('Hard', 'Medium', 'Easy', or 'Unknown').
   """
    if total_time > 60:
        return 'Hard'
    elif 30 <= total_time <= 60:
        return 'Medium'
    elif 0 < total_time < 30:
        return 'Easy'
    else:
        return 'Unknown'


if __name__ == '__main__':
    main()