"""
CVD Project Utilities: Data Loading Module
==========================================

Since this is a fairly large project, I'm creating a file to define helper functions with the analysis process to help with code modularity and clealiness.
The goal with these functions is to be simple and readable, hence no fancy list comprehensions or any other syntatic magic here.

This module was created for the loading process of the datasets to keep everything consistent between the different notebooks.
"""

import pandas as pd
import numpy as np

def convert_question_mark_to_nan (dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Instead of using NaN or null values to denote empty entries, the UCI Heart Disease datasets use a question mark (?) character. This can cause issues if not converted; as a result this function handles that. 
    
    Parameters:
        dataframe (pd.Dataframe): The input dataframe 
            
    Returns:
        dataframe (pd.DataFrame) : Dataframe with "?" characters replaced with NaN values 
    """
    modified_df = dataframe.replace("?", np.nan)
    return modified_df


def create_file_path (filename : str, 
                        directory: str = "data", 
                        file_prefix: str = "processed") -> str:
    """
    Create a standardized file path.
    
    Parameters:
        filename (str): Name of the file (e.g., 'cleveland.data')
        directory (str): Directory containing the file
        file_prefix (str): Prefix to add before filename
    
    Returns:
        file_path (str): Complete file path
    """
    file_path = f"./{directory}/{file_prefix}.{filename}"
    return file_path

def load_datasets(filepaths : list[str], 
                    seperator : str = ",") -> list[pd.DataFrame]:
    """
    Load multiple datasets from file paths.
    
    Parameters:
        filepaths (list of str): List of file paths to load
        separator (str): Column separator (default: comma)
        
    Returns:
        dataframes (list of pd.DataFrame) : Loaded dataframes
    """

    dataframes = []
    for filepath in filepaths:
        df = pd.read_csv(filepath, sep=seperator) 
        dataframes.append(df)
    if len(dataframes) == 0:
        print("No dataframe was loaded. Check the file paths.")
    return dataframes

def add_dataset_identifier (dataframes: list[pd.DataFrame], 
                            dataset_names: list[str],
                            column_name: str = "Dataset") -> list[pd.DataFrame]:
    """
    Add dataset identifier column to each dataframe.
    
    Parameters:
        dataframes (list of pd.DataFrame): List of dataframes
        dataset_names (list of str): Names to assign to each dataset
        column_name (str): Name of the identifier column
            
    Returns:
        list of pd.DataFrame : Dataframes with identifier column
    """

    if len(dataframes) != len(dataset_names):
        raise ValueError("Number of dataframes must match number of dataset names")
    
    modified_dfs = []
    for df, name in zip(dataframes, dataset_names):
        df_copy = df.copy()
        df_copy[column_name] = name
        modified_dfs.append(df_copy)
    return modified_dfs


def modify_column_names(dataframe: pd.DataFrame, 
                        col_names: list[str], 
                        inplace: bool = False) -> pd.DataFrame:
    """
    Assign new column names to a dataframe.
    
    Parameters:
        dataframe (pd.DataFrame): DataFrame to modify
        col_names (list of str): New column names
        inplace (bool): If True, modify original dataframe
        
    Returns:
        df_copy (pd.DataFrame): DataFrame with new column names
    """
    if dataframe.shape[1] != len(col_names):
        raise ValueError(
            f"Column count mismatch: DataFrame has {dataframe.shape[1]} columns, "
            f"but {len(col_names)} names provided."
        )
    
    if inplace:
        dataframe.columns = col_names
        return dataframe
    else:
        df_copy = dataframe.copy()
        df_copy.columns = col_names
        return df_copy


def combine_datasets(dataframes: list[pd.DataFrame], 
                        reset_index: bool = True) -> pd.DataFrame:
    """
    Concatenate multiple dataframes into one.
    
    Parameters:
        dataframes (list of pd.DataFrame): Dataframes to combine
        reset_index (bool): Whether to reset index after concatenation
        
    Returns:
        combined (pd.DataFrame): Combined dataframe
    """
    combined = pd.concat(dataframes, 
                            ignore_index=reset_index)
    return combined

def apply_domain_cleaning(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Plausible ranges (screening thresholds; adjust if clinical context suggests otherwise)
    range_checks = {
        'Age': (0, 120),
        'Rest BP': (80, 250),
        'Chol': (50, 700),
        'Max HR': (60, 220),
        'Oldpeak': (0, 10),
    }
    df_copy = dataframe.copy()

    for col, (min_val, max_val) in range_checks.items():
        out_of_range = ((df_copy[col] < min_val) | (df_copy[col] > max_val) & df_copy[col].notnull())
    return df_copy 


def modify_datataset(dataframe: pd.DataFrame, column_names):
    """
    Docstring for modify_datataset
    
    Parameters:
        dataframe: Description
        :type dataframe: pd.DataFrame
    Returns:
        :param column_names: Description
    """
    df_copy = dataframe.copy()
    df_modified = modify_column_names(df_copy, column_names)
    df_modified = convert_question_mark_to_nan(df_modified)
    df_modified = apply_domain_cleaning(df_modified)
    return df_modified

def prepare_cvd_datasets(files: list[str], 
                        dataset_names: list[str],
                        column_names: list[str],
                        directory: str = "data",
                        file_prefix: str = "processed") -> tuple[list[pd.DataFrame], pd.DataFrame]:
    """
    Complete workflow to load and prepare CVD datasets.
    
    Parameters:
        files (list of str): File names
        dataset_names (list of str): Names for each dataset
        column_names (list of str): Column names to assign
        directory (str): Data directory
        file_prefix (str): File prefix

    Returns:
        datasets (tuple): list of individual dataframes, combined dataframe
    """
    # Create file paths
    filepaths = [create_file_path(f, directory, file_prefix) for f in files]
    
    # Load datasets
    dfs = load_datasets(filepaths)
    
    # Assign column names, Replace "?" values with NaN and convert impossible values to NaN
    dfs = [modify_datataset(df, column_names) for df in dfs]
    
    # Combine
    df_combined = combine_datasets(dfs)
    
    return dfs, df_combined
