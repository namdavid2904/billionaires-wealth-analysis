import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')

def save_figure(fig, file_name, dpi=300):
    """
    Save figure to reports directory
    """

    figures_dir = Path('reports/figures')
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig_path = figures_dir / file_name
    fig.savefig(fig_path, bbox_inches='tight', dpi=dpi)

    print(f"Figure saved to {fig_path}")

def plot_wealth_distribution(df, net_worth_col='net_worth', save=True):
    """
    Plot distribution of wealth
    """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Regular distribution
    sns.histplot(data=df, x=net_worth_col, kde=True, ax=ax1)
    ax1.set_title("Distribution of net worth")
    ax1.set_xlabel("Net worth (Billion $)")
    ax1.set_ylabel("Count")

    # Log distribution
    sns.histplot(data=df, x=f'log_net_worth' if 'log_net_worth' in df.columns 
                 else np.log1p(df[net_worth_col]), kde=True, ax=ax2)
    ax2.set_title("Log distribution of net worth")
    ax2.set_xlabel("Log Net worth")
    ax2.set_ylabel("Count")

    plt.tight_layout()

    if save:
        save_figure(fig, 'wealth_distribution.png')

    return fig

def plot_wealth_by_industry(df, industry_col='industry', net_worth_col='net_worth', top_n=10, save=True):
    """
    Plot wealth distribution by industry
    """

    # Average net worth by industry
    industry_wealth = df.groupby(industry_col)[net_worth_col].agg(['mean', 'count']).sort_values(by='mean', ascending=False)
    
    # Filter top n industries
    industry_wealth = industry_wealth[industry_wealth['count'] >= 5].head(top_n)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = sns.barplot(x=industry_wealth.index, y='mean', data=industry_wealth.reset_index(), ax=ax)

    # Add label count on top of bars
    for i, p in enumerate(bars.patches):
        count = industry_wealth.iloc[i]['count']
        bars.annotate(f'n={count}', 
                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', size=10)

    ax.set_title("Average net worth by industry", fontsize=16)
    ax.set_xlabel("Industry", fontsize=14)
    ax.set_ylabel("Average net worth (Billion $)", fontsize=14)
    plt.xticks(rotation=-45, ha='right')
    plt.tight_layout()

    if save:
        save_figure(fig, 'average_wealth_by_industry.png')
    
    return fig

def plot_geo_distribution(df, country_col='country', region_col='region', net_worth_col='net_worth', save=True):
    """
    Plot geographical distribution of billionaires
    """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Plot by region
    if region_col in df.columns:
        region_counts = df[region_col].value_counts()
        region_wealth = df.groupby(region_col)[net_worth_col].sum().sort_values(ascending=False)

        sns.barplot(x=region_counts.index, y=region_counts.values, ax=ax1)
        ax1.set_title("Number of billionaires by region", fontsize=14)
        ax1.set_xlabel("Region", fontsize=12)
        ax1.set_ylabel("Count", fontsize=12)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        sns.barplot(x=region_wealth.index, y=region_wealth.values, ax=ax2)
        ax2.set_title("Total wealth by region (Billion $)", fontsize=14)
        ax2.set_xlabel("Region", fontsize=12)
        ax2.set_ylabel("Total Net Worth", fontsize=12)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Plot by country (if region column is not available)
    else:
        top_countries = df[country_col].value_counts().head(10)
        country_wealth = df.groupby(country_col)[net_worth_col].sum().sort_values(ascending=False).head(10)
    
        sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax1)
        ax1.set_title("Total Wealth by Region (Billion $)", fontsize=14)
        ax1.set_xlabel("Country", fontsize=12)
        ax1.set_ylabel("Count", fontsize=12)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        sns.barplot(x=country_wealth.index, y=country_wealth.values, ax=ax2)
        ax2.set_title("Top 10 Countries by Total Wealth", fontsize=14)
        ax2.set_xlabel("Country", fontsize=12)
        ax2.set_ylabel("Total Net Worth", fontsize=12)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()

    if save:
        save_figure(fig, 'geo_distribution.png')
    
    return fig