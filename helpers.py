'''
Since this is a fairly large project, I'm creating a file to define helper functions with the analysis process to help with code modularity and clealiness.
The goal with these functions is to be simple and readable, hence no fancy list comprehensions or any other syntatic magic here.
'''
import pandas as pd

def create_file_path (filename : str, directory: str, file_prefix: str) -> str:
    file_path = f"./{directory}/{file_prefix}.{filename}"
    return file_path

def load_datasets(filepaths_directory : list[str]) -> list[pd.DataFrame]:
    dataframes = []
    for filepath in filepaths_directory:
        df = pd.read_csv(filepath, sep=",") 
        dataframes.append(df)
    if len(dataframes) == 0:
        print("No dataframe was loaded. Check the file paths.")
    return dataframes

def modify_column_names(dataframe: pd.DataFrame, col_names: list[str]) -> pd.DataFrame:
    num_cols = dataframe.shape[1]
    if (num_cols != len(col_names)):
        print("The number of column names passed does not equal the number of columns in the DataFrame.")
        return dataframe 
    
    dataframe.columns = col_names 
    return dataframe