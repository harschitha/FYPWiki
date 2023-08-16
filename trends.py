# trends.py

import sys
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from datetime import date, timedelta

def get_trending_queries(search_term):
    pytrend = TrendReq()

    # Set the timeframe to the last 7 days and location to United States
    start_date = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')

    pytrend.build_payload(kw_list=[search_term], timeframe=f'{start_date} {end_date}', geo='US')
    related_queries = pytrend.related_queries()
    related_queries_rising = related_queries[search_term]['rising']

    # Filter out non-web search data and select relevant columns
    related_queries_rising = related_queries_rising[['query', 'value']]
    related_queries_rising['percentage'] = (related_queries_rising['value'] / related_queries_rising['value'].sum() * 100).round(2)
    related_queries_rising.drop('value', axis=1, inplace=True)

    return related_queries_rising

def main():
    # Check if the search term is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Please provide the search term as a command-line argument.")
        print("Usage: python trends.py <search_term>")
        sys.exit(1)

    # Get the search term from the command-line argument
    search_term = sys.argv[1]

    # Fetch trending queries
    related_queries_rising = get_trending_queries(search_term)

    # Print the DataFrame
    print(related_queries_rising)

    # Create a bar graph based on the queries
    plt.figure(figsize=(10, 6))
    plt.bar(related_queries_rising['query'], related_queries_rising['percentage'])
    plt.xlabel('Searches')
    plt.ylabel('Percentage')
    plt.title(f'Most trending related searches with the term {search_term}')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()