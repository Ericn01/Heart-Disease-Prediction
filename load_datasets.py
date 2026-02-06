from utils.data_loading import prepare_cvd_datasets

# Setting up the constants
FILES = ['cleveland.data', 'hungarian.data', 'switzerland.data', 'va.data']
DIRECTORY = 'data'
DATASET_NAMES = ['Cleveland', 'Hungarian', 'Switzerland', 'VA Long Beach']
COLUMN_NAMES = ["Age", "Sex", "Chest Pain", "Rest BP", "Chol", "FBS", 
                "Rest ECG", "Max HR", "Ex Angina", "Oldpeak", "Slope", 
                "Ca", "Thal", "CVD Class"]

# We'll make the datasets global so that they can be loaded into all notebooks
dfs, df_combined = prepare_cvd_datasets(
    files=FILES, 
    dataset_names=DATASET_NAMES,
    column_names=COLUMN_NAMES, 
    directory=DIRECTORY
)
