import os
from  data_processing import get_data
from feature_engineering import create_age_groups

if __name__ == '__main__':
    """
    Run the preprocessing pipeline
    """
    print("Running the preprocessing pipeline")

    # Process data
    df = get_data(raw_file='../data/raw/df_ready.csv', processed_file='../data/processed/df_cleaned.csv')

    print(f"Data processed and saved. Shape: {df.shape}")
    print(f"Processed data saved to: ../data/processed/df_cleaned.csv")