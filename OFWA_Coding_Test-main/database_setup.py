import sqlite3
import pandas as pd
import json
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('galamsay_analysis.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS galamsay_data')
cursor.execute('DROP TABLE IF EXISTS analysis_results')

# Create a table for storing the raw data
cursor.execute('''
CREATE TABLE IF NOT EXISTS galamsay_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    region TEXT,
    number_of_sites INTEGER,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

# Create a table for storing the analysis results
cursor.execute('''
CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_sites INTEGER,
    region_with_most_sites TEXT,
    average_sites_per_region TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

# Load the dataset
try:
    df = pd.read_excel('OFWA_Coding_Test-main\galamsay_data.xlsx')
    # Rename the 'Unnamed: 0' column to 'City'
    df = df.rename(columns={'Unnamed: 0': 'City'})
    # Convert 'Number_of_Galamsay_Sites' to numeric, coercing errors to NaN
    df['Number_of_Galamsay_Sites'] = pd.to_numeric(df['Number_of_Galamsay_Sites'], errors='coerce')
    # Fill NaN values with 0 to ensure calculations can proceed
    df['Number_of_Galamsay_Sites'] = df['Number_of_Galamsay_Sites'].fillna(0)
    # Convert to integer
    df['Number_of_Galamsay_Sites'] = df['Number_of_Galamsay_Sites'].astype(int)
    # Drop rows with NaN values in 'Region'
    df.dropna(subset=['Region'], inplace=True)
    # Check if DataFrame is empty after cleaning
    if df.empty:
        print("No valid data available after cleaning.")
        exit(1)
except FileNotFoundError:
    print("The file galamsay_data.xlsx was not found.")
    exit(1)

# Store raw data
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO galamsay_data (city, region, number_of_sites, timestamp)
    VALUES (?, ?, ?, ?)
    ''', (row['City'], row['Region'], row['Number_of_Galamsay_Sites'], current_time))

# Perform analysis
total_sites = df['Number_of_Galamsay_Sites'].sum()
region_with_most_sites = df.groupby('Region')['Number_of_Galamsay_Sites'].sum().idxmax()
average_sites_per_region = df.groupby('Region')['Number_of_Galamsay_Sites'].mean().to_json()

# Convert average_sites_per_region to string if it's bytes
if isinstance(average_sites_per_region, bytes):
    average_sites_per_region = average_sites_per_region.decode('utf-8')

# Insert analysis results into the database
cursor.execute('''
INSERT INTO analysis_results (total_sites, region_with_most_sites, average_sites_per_region, timestamp)
VALUES (?, ?, ?, ?)
''', (total_sites, region_with_most_sites, average_sites_per_region, current_time))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data and analysis results have been stored in the database.") 