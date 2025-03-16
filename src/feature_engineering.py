import numpy as np
import pandas as pd

def create_age_groups(df, age_col):
    """
    Create age groups based on age column.
    """
    df = df.copy()

    if age_col in df.columns:
        bins = [0, 30, 40, 50, 60, 70, 80, 120]
        labels = ['Under 30', '31-40', '41-50', '51-60', '61-70', '71-80', 'over 80']
        df['age_group'] = pd.cut(df[age_col], bins=bins, labels=labels)

    return df


def create_wealth_features(df, net_worth_col):
    """
    Create wealth features based on net worth column.
    """

    df = df.copy()

    if net_worth_col in df.columns:
        bins = [0, 1, 2, 5, 10, 50, 1000]
        labels = ['$1B', '$1-2B', '$2-5B', '$5-10B', '$10-50B', '$50B+']
        df['wealth_group'] = pd.cut(df[net_worth_col], bins=bins, labels=labels)

        # Create a log scaled net worth column
        df['log_net_worth'] = np.log1p(df[net_worth_col])
    
    return df


def create_geo_features(df, country_col):
    """
    Create geographical features based on country column.
    """

    df = df.copy()

    if country_col in df.columns:
        north_america = ['United States', 'Canada', 'Mexico']
        europe = ['Germany', 'France', 'United Kingdom', 'Italy', 'Spain', 'Russia', 'Switzerland']
        asia = ['China', 'Japan', 'India', 'South Korea', 'Singapore', 'Hong Kong']

        def get_region(country):
            if country in north_america:
                return 'North America'
            elif country in europe:
                return 'Europe'
            elif country in asia:
                return 'Asia'
            else:
                return 'Other'
            
        df['region'] = df[country_col].apply(get_region)
    
    return df

def create_features(df):
    """
    Create features and apply to the dataframe.
    """

    df = create_age_groups(df, 'age')
    df = create_wealth_features(df, 'net_worth')
    df = create_geo_features(df, 'country')
    return df

def create_advanced_features(df):
    """Create more advanced features for predictive modeling"""
    df = df.copy()
    
    # Create wealth-to-GDP ratio (how wealthy the billionaire is relative to country's economy)
    df['wealth_to_gdp_ratio'] = df['wealth'] / (df['gdp_country'] + 1)  # Add 1 to avoid division by zero
    
    # Create log-transformed features for skewed numeric variables
    df['log_wealth'] = np.log1p(df['wealth'])
    df['log_gdp'] = np.log1p(df['gdp_country'])
    df['log_country_pop'] = np.log1p(df['country_pop'])
    
    # Create wealth per capita feature (billionaire's wealth divided by country population)
    df['wealth_per_capita'] = df['wealth'] / (df['country_pop'] + 1)
    
    # Calculate career length (assuming careers start at age 25)
    df['career_years'] = df['age'] - 25
    df['career_years'] = df['career_years'].apply(lambda x: max(x, 1))  # Avoid negative or zero values
    
    # Calculate wealth per career year
    df['wealth_per_year'] = df['wealth'] / df['career_years']
    
    # Create interaction features
    df['gdp_per_capita'] = df['gdp_country'] / (df['country_pop'] + 1)
    
    # Create binary features
    df['is_male'] = (df['gender'] == 'M').astype(int)
    df['is_tech_industry'] = (df['industry'] == 'Technology').astype(int)
    df['is_finance_industry'] = (df['industry'] == 'Finance & Investments').astype(int)
    
    return df