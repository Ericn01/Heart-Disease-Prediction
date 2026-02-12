def write_md_cell(id, header, content):
    """
    Formats a string for a Jupyter Notebook markdown cell
    with an HTML anchor and a bulleted list.
    """
    # 1. Create the anchor tag using the id 
    anchor = f"<a id='{id.strip()}'></a>"
    
    # 2. Add the header text (using ## for a standard sub-header)
    header_text = f"## {header.strip()}"
    
    # 3. Process the content into a markdown list
    # .splitlines() handles different newline characters automatically
    list_items = ""
    for item in content.splitlines():
        if item.strip():  # Only add if the line isn't empty
            list_items += f"- {item.strip()}\n"
            
    output = f"{anchor}\n{header_text}\n{list_items}"
    return output

def make_toc_item(id:str, header:str, index) -> str:
    return f"{int(index)}. ({header.strip().title()})[#{id.strip()}]\n"

notebook_cells = [""" 
introduction;
Introduction;d

Reference to Notebooks 1 & 2
Objectives
Research questions""",

"""
setup-and-data-loading;
Setup & Data Loading;

Import libraries
Load cleaned dataset from Notebook 2
Verify data quality and completeness
""",
"""
dataset-overview;
Dataset Overview;

Final sample size
Target variable distribution
Summary statistics
""",
"""
univariate-analysis;
Univariate Analysis;

Distribution of each predictor variable
Identify skewness, outliers
Check for transformations needed
Visualizations: histograms, box plots


Identify which variables are consistent vs. population-specific
""",
"""
target-variable-relationships;
Target Variable Relationships;

For each predictor:

Relationship with heart disease severity
Visualization (box plots for categorical, scatter/violin for continuous)
Statistical significance


Rank variables by apparent association strength
""", 
"""
correlation-analysis;
Correlation Analysis;

Correlation matrix (for continuous variables)
Identify multicollinearity issues
Visualization: heatmap
""",
"""
bivariate-relationships;
Bivariate Relationships;

Key predictor pairs
Interaction effects
Conditional relationships
""",
"""
feature-engineering-ideas;
Feature Engineering Ideas;

Potential transformations (log, polynomial, binning)
Interaction terms to create
Domain-knowledge based features
Rationale for each""", 
"""
conclusions-and-modeling-preview;
Conclusions & Modeling Preview;

Top features associated with heart disease
Hypotheses for modeling
Summary of exploratory findings
Expected important features
Transition to modeling phase
"""]

def write_to_stream(formatted_content, file_path, mode='a'):
    """
    Writes the formatted string to a specified file.
    
    Args:
        formatted_content (str): The output from your write_md_cell function.
        file_path (str): The name or path of the .ipynb or .md file.
        mode (str): 'a' for append (default) or 'w' to overwrite.
    """
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(formatted_content + "\n")
        print(f"Successfully wrote to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

filepath="notebook_stream.txt"
toc_string = ""

for index, cell_content in enumerate(notebook_cells):
    id, header, content = cell_content.split(";")
    cell = write_md_cell(id, header, content)
    toc_string += make_toc_item(id, header, index+1)
    write_to_stream(cell, file_path=filepath)

write_to_stream(toc_string, file_path=filepath)