import pandas as pd

def get_csv_file(path: str) -> pd.DataFrame:
    """
    Reads a CSV file from the given path and returns it as a pandas DataFrame.
    
    :param path: The path to the CSV file.
    :return: A pandas DataFrame containing the CSV file data.
    """
    return pd.read_csv(path, encoding='ISO-8859-1', on_bad_lines='skip')

def save_csv_file(dataframe: pd.DataFrame, path: str) -> None:
    """
    Saves the DataFrame to a CSV file at the given path.
    
    :param dataframe: The DataFrame to save.
    :param path: The path where the CSV file will be saved.
    """
    dataframe.to_csv(path, index=False)

def sort_column_by_presence(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Sorts the DataFrame based on the presence of elements in the specified column.
    Rows with elements in the specified column are moved up.
    
    :param dataframe: The DataFrame to sort.
    :param column_name: The name of the column to sort by.
    :return: The sorted DataFrame.
    """
    if column_name in dataframe.columns:
        dataframe['temp_sort'] = dataframe[column_name].notnull()
        dataframe.sort_values(by='temp_sort', ascending=False, inplace=True)
        dataframe.drop(columns=['temp_sort'], inplace=True)
    return dataframe

def delete_empty_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Deletes columns that are completely empty (excluding the header row).
    
    :param dataframe: The DataFrame to process.
    :return: The DataFrame with empty columns removed.
    """
    return dataframe.dropna(axis=1, how='all')

def delete_column(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Deletes a specified column from the DataFrame.
    
    :param dataframe: The DataFrame to process.
    :param column_name: The name of the column to delete.
    :return: The DataFrame with the specified column removed.
    """
    return dataframe.drop(columns=[column_name], errors='ignore')


path = "/Users/brianprzezdziecki/Code/realty_data/152_Corona_10-20Yr_Owned.csv"

file = get_csv_file(path)
file = sort_column_by_presence(file, 'Owner 1 Phone Numbers')
file = delete_empty_columns(file)
columns_to_delete = ["Post Direction", "Unit Type", "Unit Number", "ZIP 4", "Mailing Pre Direction", "Mailing Post Direction", "Mailing Unit Type", "Mailing Unit Number", "Mailing ZIP 4"]
for column in columns_to_delete:
    file = delete_column(file, column)
file = delete_column(file, 'Owner 1 Email')
save_csv_file(file, "/Users/brianprzezdziecki/Code/realty_data/152_Corona_10-20Yr_Owned_clean.csv")

