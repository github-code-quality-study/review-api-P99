import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from urllib.parse import parse_qs, urlparse
import json
import pandas as pd
from datetime import datetime
import uuid
import os
from typing import Callable, Any
from wsgiref.simple_server import make_server

nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)

adj_noun_pairs_count = {}
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

reviews = pd.read_csv('data/reviews.csv').to_dict('records')

class ReviewAnalyzerServer:
    def __init__(self) -> None:
        # This method is a placeholder for future initialization logic
        pass

    def analyze_sentiment(self, review_body):
        sentiment_scores = sia.polarity_scores(review_body)
        return sentiment_scores

    def __call__(self, environ: dict[str, Any], start_response: Callable[..., Any]) -> bytes:
        """
        The environ parameter is a dictionary containing some useful
        HTTP request information such as: REQUEST_METHOD, CONTENT_LENGTH, QUERY_STRING,
        PATH_INFO, CONTENT_TYPE, etc.
        """

        if environ["REQUEST_METHOD"] == "GET":
            # variables declarations
            query_params = parse_qs(environ.get(('QUERY_STRING', ''))
            location = query_params.get('location', [None])[0]
            start_date = query_params.get('start_date', [None])[0]
            end_date = query_params.get('end_date', [None])[0]

            filtered_reviews = reviews

            if location:
                valid_locations = [
                "Albuquerque, New Mexico",
                "Carlsbad, California",
                "Chula Vista, California",
                "Colorado Springs, Colorado",
                "Denver, Colorado",
                "El Cajon, California",
                "El Paso, Texas",
                "Escondido, California",
                "Fresno, California",
                "La Mesa, California",
                "Las Vegas, Nevada",
                "Los Angeles, California",
                "Oceanside, California",
                "Phoenix, Arizona",
                "Sacramento, California",
                "Salt Lake City, Utah",
                "San Diego, California",
                "Tucson, Arizona"
                ]
                if location in valid_locations:
                    filtered_reviews = [review for review in reviews if review['location'] == location]
                else:
                    response_body = json.dumps({"error": "Invalid location"}).encode("utf-8")
                    start_response("400 Bad Request", [
                    ("Content-Type", "application/json"),
                    ("Content-Length", str(len(response_body)))
                    ])
                    return [response_body]


            # Create the response body from the reviews and convert to a JSON byte string
            response_body = json.dumps(reviews, indent=2).encode("utf-8")
            
            # Write your code here
            

            # Set the appropriate response headers
            start_response("200 OK", [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response_body)))
             ])
            
            return [response_body]


        if environ["REQUEST_METHOD"] == "POST":
            # Write your code here
            return

if __name__ == "__main__":
    app = ReviewAnalyzerServer()
    port = os.environ.get('PORT', 8000)
    with make_server("", port, app) as httpd:
        print(f"Listening on port {port}...")
        httpd.serve_forever()