import pandas as pd


def add_missingness_indicators(dataframe: pd.DataFrame,
                                features: list[str],
                                suffix: str = '_missing') -> pd.DataFrame:
    """
    Add binary missingness indicator columns.
    
    Parameters:
        dataframe (pd.DataFrame): Input dataframe
        features (list of str): Features to create indicators for
        suffix (str): Suffix for indicator column names
        
    Returns:
        df_copy (pd.DataFrame): Dataframe with added indicator columns
    """
    df_copy = dataframe.copy()
    
    for feature in features:
        if feature in df_copy.columns:
            indicator_name = f"{feature}{suffix}"
            df_copy[indicator_name] = df_copy[feature].isnull().astype(int)
    
    return df_copy


def simple_impute_numeric(dataframe: pd.DataFrame,
                            feature: str,
                            strategy: str = 'median') -> pd.DataFrame:
    """
    Impute missing values in numeric feature.
    
    Parameters:
        dataframe (pd.DataFrame): Input dataframe
        feature (str): Feature to impute
        strategy (str): 'mean', 'median', or specific value
        
    Returns:
        df_copy (pd.DataFrame): Dataframe with imputed values
    """
    df_copy = dataframe.copy()
    
    if strategy == 'mean':
        fill_value = df_copy[feature].mean()
    elif strategy == 'median':
        fill_value = df_copy[feature].median()
    else:
        fill_value = strategy
    
    df_copy[feature].fillna(fill_value, inplace=True)
        
    return df_copy
