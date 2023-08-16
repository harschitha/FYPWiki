# app.py

from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from datetime import date, timedelta

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        related_queries_rising = get_trending_queries(search_term)

        # Save the bar graph as graph.png
        plt.figure(figsize=(10, 6))
        plt.bar(related_queries_rising['query'], related_queries_rising['percentage'])
        plt.xlabel('Searches')
        plt.ylabel('Percentage')
        plt.title(f'Most trending related searches with the term {search_term}')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('static/graph.png')  # Save the graph as graph.png in the static folder
        plt.close()  # Close the figure to release resources

        return render_template('result.html', search_term=search_term, results=related_queries_rising)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)






















































