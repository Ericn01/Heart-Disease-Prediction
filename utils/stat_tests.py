""" 
Statistical tests 
"""

import pandas as pd 
from scipy.stats import chi2_contingency, kruskal, f_oneway

def test_categorical_independence(dataframe: pd.DataFrame, 
                                    var1: str, 
                                    var2: str) -> dict:
    """
    Perform chi-square test of independence for categorical variables.
    
    Parameters:
    -----------
    dataframe : pd.DataFrame
        Input dataframe
    var1, var2 : str
        Categorical variables to test
        
    Returns:
    --------
    dict : Test results including chi2, p-value, conclusion
    """
    contingency = pd.crosstab(dataframe[var1], dataframe[var2])
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    
    result = {
        'test': 'Chi-square',
        'variable_1': var1,
        'variable_2': var2,
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'significant_001': p_value < 0.001,
        'significant_005': p_value < 0.05,
        'significant_010': p_value < 0.10
    }
    
    return result


def test_numeric_across_groups(dataframe: pd.DataFrame, 
                                numeric_var: str, 
                                group_var: str,
                                test: str = 'kruskal') -> dict:
    """
    Test if numeric variable differs across groups.
    
    Parameters:
    -----------
    dataframe : pd.DataFrame
        Input dataframe
    numeric_var : str
        Numeric variable to test
    group_var : str
        Grouping variable
    test : str
        'kruskal' for Kruskal-Wallis or 'anova' for one-way ANOVA
        
    Returns:
    --------
    dict : Test results
    """
    groups = [group[numeric_var].dropna() 
                for name, group in dataframe.groupby(group_var)]
    
    if test == 'kruskal':
        stat, p_value = kruskal(*groups)
        test_name = 'Kruskal-Wallis H'
    elif test == 'anova':
        stat, p_value = f_oneway(*groups)
        test_name = 'One-way ANOVA F'
    else:
        raise ValueError("test must be 'kruskal' or 'anova'")
    
    result = {
        'test': test_name,
        'numeric_variable': numeric_var,
        'group_variable': group_var,
        'statistic': stat,
        'p_value': p_value,
        'significant_001': p_value < 0.001,
        'significant_005': p_value < 0.05,
        'significant_010': p_value < 0.10
    }
    
    return result


def compare_distributions_across_datasets(dataframes: list[pd.DataFrame],
                                            dataset_names: list[str],
                                            feature: str,
                                            test_type: str = 'auto') -> dict:
    """
    Compare feature distribution across multiple datasets.
    
    Parameters:
    -----------
    dataframes : list of pd.DataFrame
        List of dataframes
    dataset_names : list of str
        Names of datasets
    feature : str
        Feature to compare
    test_type : str
        'auto', 'numeric', or 'categorical'
        
    Returns:
    --------
    dict : Comparison results
    """
    # Combine with dataset labels
    combined_data = []
    for df, name in zip(dataframes, dataset_names):
        temp = df[[feature]].copy()
        temp['Dataset'] = name
        combined_data.append(temp)
    
    df_combined = pd.concat(combined_data, ignore_index=True)
    
    # Determine test type
    if test_type == 'auto':
        if df_combined[feature].dtype in ['object', 'category']:
            test_type = 'categorical'
        else:
            test_type = 'numeric'
    
    # Perform appropriate test
    if test_type == 'categorical':
        result = test_categorical_independence(df_combined, 'Dataset', feature)
    else:
        result = test_numeric_across_groups(df_combined, feature, 'Dataset')
    
    return result