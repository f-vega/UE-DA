import pandas as pd
import numpy as np

def analyse(age_file, total_file):
    # Clean and parse the total births dataset
    total_births_df = pd.read_csv(total_file, sep=';')
    total_births_df.columns = total_births_df.columns.str.strip() 
    total_births_df['Year'] = total_births_df['Year'].astype(int)

    # Clean and reshape the births by age dataset
    births_by_age_df = pd.read_csv(age_file, sep=';')
    births_by_age_df.columns = births_by_age_df.columns.str.strip()

    # Reshape births by age dataset to long format
    births_by_age_long = births_by_age_df.melt(
        id_vars=["Age of the mother"],
        var_name="Year",
        value_name="Births"
    )

    # Clean up the Year column and convert Births to numeric for calculations
    births_by_age_long["Year"] = births_by_age_long["Year"].astype(int)
    births_by_age_long["Births"] = pd.to_numeric(births_by_age_long["Births"], errors="coerce")

    # Merge the datasets on Year
    merged_df = pd.merge(total_births_df, births_by_age_long, on="Year")

    # Display the first few rows of the cleaned, merged dataset
    merged_df.to_csv('../analysis/name.csv', sep=';', index=False)

age_file = '../clean_data/12612-0008.csv'
total_file = '../clean_data/12612-0001.csv'
# analyse(age_file=age_file, total_file=total_file)

births_by_age_df = pd.read_csv(age_file, sep=';')


# Parse the provided dataset
age_columns = births_by_age_df.columns[1:]  # Exclude 'Year' column

# Create a list of ages by extracting the numeric values from age columns
ages = np.array([int(age.split(' ')[0]) for age in age_columns])

# Compute weighted average for each year
average_age_by_year = []
for year in births_by_age_df['Year']:
    rates = births_by_age_df.loc[births_by_age_df['Year'] == year, age_columns].values.flatten()
    weighted_avg_age = np.sum(ages * rates) / np.sum(rates)
    average_age_by_year.append({'Year': year, 'Average_Age': weighted_avg_age})

# Convert to DataFrame
average_age_df = pd.DataFrame(average_age_by_year)

# Display the results
average_age_df.to_csv('../analysis/average_age.csv', sep=';', index=None)