"""
CVD Project Utilities: Data Quality and Validation Module
=========================================================

This module contains several utility functions relating to data quality (assessing missing values, duplicates, etc).
"""

import pandas as pd

def calculate_missingness_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a comprehensive data missingness summary

    Parameters:
        dataframe (pd.DataFrame): Input dataframe
    
    Returns:
        missing summary (pd.DataFrame): Summary of missing values.
    """
    
    missing_counts = dataframe.isnull().sum()
    missing_summary = pd.DataFrame({ 
        'Feature': dataframe.columns, 
        'Missing_Count': missing_counts.values, 
        'Missing_Percent': (missing_counts / len(dataframe) * 100).values
    })

    missing_summary = missing_summary[missing_summary['Missing_Count'] > 0]
    missing_summary = missing_summary.sort_values('Missing_Percent', ascending=False)
    missing_summary = missing_summary.reset_index(drop=True)
    
    return missing_summary

def get_complete_case_percentage(dataframe: pd.DataFrame) -> float:
    """
    Calculate percentage of complete cases (no missing values).
    
    Parameters:
        dataframe (pd.DataFrame): Input dataframe
        
    Returns:
        percent records (float) : Percentage of complete cases
    """
    complete_cases = (~dataframe.isnull().any(axis=1)).sum()
    percentage = (complete_cases / len(dataframe)) * 100
    return percentage


def create_data_quality_report(dataframe: pd.DataFrame, 
                                dataset_name: str = "Dataset") -> dict:
    """
    Generate comprehensive data quality report.
    
    Parameters:
        dataframe (pd.DataFrame): Input dataframe
        dataset_name (str): Name of dataset for reporting
        
    Returns:
        report (dict): Data quality metrics
    """
    report = {
        'Dataset Name': dataset_name,
        'N Observations': len(dataframe),
        'N Features': dataframe.shape[1],
        'N Duplicates': dataframe.duplicated().sum(),
        'Percent Duplicates': (dataframe.duplicated().sum() / len(dataframe) * 100),
        'N Complete Cases': (~dataframe.isnull().any(axis=1)).sum(),
        'Percent Complete Cases': get_complete_case_percentage(dataframe),
        'Total Missing Cells': dataframe.isnull().sum().sum(),
        'Percent Missing Cells': (dataframe.isnull().sum().sum() / dataframe.size * 100),
        'Features With Missing Cells': (dataframe.isnull().sum() > 0).sum()
    }
    
    return report