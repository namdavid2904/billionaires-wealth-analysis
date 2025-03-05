import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """"
    Load billionaire data set from file path
    """
    return pd.read_csv(file_path)

def clean_data(df):
    """
    Clean billionaire data set:
    - Handle missing values
    - Remove duplicates
    - Fix data types
    """

    # Create a copy of the data frame
    df_cleaned = df.copy()

    # Handle missing values
    numeric_columns = df_cleaned.select_dtypes(include=['number']).columns
    for col in numeric_columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())

    # Fill missing values in categorical columns
    categorical_columns = df_cleaned.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])

    # Remove duplicates
    df_cleaned = df_cleaned.drop_duplicates()

    # Convert date columns
    if 'year' in df_cleaned.columns:
        df_cleaned['year'] = pd.to_numeric(df_cleaned['year'], errors='coerce')
    
    return df_cleaned

def save_data(df, file_path):
    """
    Save processed data frame to file path
    """

    # create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)

def get_data():
    """
    Load, clean and return data frame
    """

    data = load_data()
    data_cleaned = clean_data(data)
    save_data(data_cleaned)
    return data_cleaned