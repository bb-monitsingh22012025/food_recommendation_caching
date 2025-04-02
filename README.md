# food_recommendation_caching
Overview

The Food Recommendation System is a GUI-based application that provides food recommendations based on user queries. It utilizes the Hugging Face API (Mistral-7B-Instruct-v0.1) for generating recommendations and caches responses in an Aerospike database for faster retrieval.

Features

Food Query Input: Users can enter a food-related query to receive a recommendation.

Caching with Aerospike: Previously queried recommendations are stored in an Aerospike database to improve response time.

Integration with Hugging Face API: If a query is not found in the cache, a recommendation is generated using the Mistral-7B model.

GUI with Tkinter: A simple and user-friendly interface built using Tkinter.

Requirements

Dependencies

Ensure you have the following dependencies installed:

pip install aerospike huggingface_hub tkinter

External Services

Hugging Face API Token: Replace HUGGINGFACE_API_TOKEN with your actual Hugging Face API token.

Aerospike Server: Ensure that Aerospike is running locally on 127.0.0.1:3000.

Setup and Usage

Clone the repository:

git clone https://github.com/your-repo/food-recommendation.git
cd food-recommendation

Install required dependencies:

pip install aerospike huggingface_hub tkinter

Start the Aerospike server.

Run the script:

python food_recommendation.py

Enter a food query in the GUI and click "Get Recommendation."

Code Structure

Aerospike Configuration: Handles caching of responses.

Hugging Face API Integration: Fetches recommendations when cache misses occur.

Tkinter GUI: Provides a simple interface for user interaction.

Functionality

check_cache(query): Checks if a query exists in the Aerospike cache.

store_in_cache(query, recommendation): Stores a query-result pair in Aerospike.

get_mistral_recommendation(query): Fetches recommendations using Hugging Face API.

get_food_recommendation(): Main function handling query lookup, API calls, and displaying results.

Notes

Ensure that the Aerospike server is running before executing the script.

The Hugging Face API token should be kept secure and not shared publicly.

For better performance, adjust Aerospike configurations as needed.

License

This project is licensed under the MIT License.

Author

Monit Singh

