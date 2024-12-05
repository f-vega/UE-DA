import os, json
import pandas as pd


def get_stats(input_path):
    try:
        df = pd.read_csv(input_path, delimiter=';')

        # These two files have strings for second column
        if '12612-0020.csv' in input_path or '12612-0002.csv' in input_path:
            df = df.iloc[:, 2:]
        else:
            # Don't calculate the first column
            df = df.iloc[:, 1:]
        
        # Compute stats for remaining columns
        statistics = {}
        for col in df.columns:
            try:
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                
                # Skip columns that are entirely non-numeric
                if numeric_col.notna().sum() == 0:
                    print(f"Skipping non-numeric column: {col} {input_path}")
                    continue
                
                # Compute stats
                statistics[col] = {
                    'mean': round(numeric_col.mean().item(), 3),
                    'median': round(numeric_col.median().item(), 3),
                    'std_dev': round(numeric_col.std().item(), 3),
                    'min': round(numeric_col.min().item(), 3),
                    'max': round(numeric_col.max().item(), 3)
                }
            except Exception as e:
                print(f"Error processing column '{col}': {e}")
        
        return statistics

    except Exception as e:
        print('Error in: ', input_path)
        print('Exception: ', e)



input_folder = '../clean_data'
stats = {}

# Get statistics
for file in os.listdir(input_folder):
    file_name = os.path.join(input_folder, file)
    stats[file.split('.')[0]] = get_stats(file_name)


# Export the stats as a json file
stats_json = json.dumps(stats, indent=4)

with open('../stats.json', 'w') as json_file:
    json_file.write(stats_json)

