import pandas as pd

# Load the dataset
try:
    df = pd.read_excel('OFWA_Coding_Test-main\galamsay_data.xlsx')
    # Display the first few rows of the dataset
    print(df.head())
except FileNotFoundError:
    print("The file galamsay_data.xlsx was not found.")
    exit(1) 