import pandas as pd

# Load the dataset
df = pd.read_excel('OFWA_Coding_Test-main\galamsay_data.xlsx')

# Rename the 'Unnamed: 0' column to 'City'
df = df.rename(columns={'Unnamed: 0': 'City'})

# Convert 'Number_of_Galamsay_Sites' to numeric, coercing errors to NaN
df['Number_of_Galamsay_Sites'] = pd.to_numeric(df['Number_of_Galamsay_Sites'], errors='coerce')

# Fill NaN values with 0 to ensure calculations can proceed
df['Number_of_Galamsay_Sites'] = df['Number_of_Galamsay_Sites'].fillna(0)

# Convert to integer
df['Number_of_Galamsay_Sites'] = df['Number_of_Galamsay_Sites'].astype(int)

# Calculate total number of Galamsay sites across all cities
total_sites = df['Number_of_Galamsay_Sites'].sum()

# Find the region with the highest number of Galamsay sites
region_with_most_sites = df.groupby('Region')['Number_of_Galamsay_Sites'].sum().idxmax()

# Print column names to verify
print("\nColumn names:", df.columns)

# List cities where the Galamsay sites exceed a given threshold
def cities_exceeding_threshold(threshold):
    return df[df['Number_of_Galamsay_Sites'] > threshold]['City'].tolist()

# Calculate average number of Galamsay sites per region
average_sites_per_region = df.groupby('Region')['Number_of_Galamsay_Sites'].mean()

# Print results
print(f"\nTotal number of Galamsay sites: {total_sites}")
print(f"Region with the highest number of Galamsay sites: {region_with_most_sites}")
print("\nAverage number of Galamsay sites per region:")
print(average_sites_per_region)

# Example usage
threshold = 10
print(f"\nCities with more than {threshold} Galamsay sites:")
print(cities_exceeding_threshold(threshold))

