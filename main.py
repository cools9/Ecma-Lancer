import random
import re
import json
from typing import Optional
import csv
from difflib import SequenceMatcher
from textblob import TextBlob
import requests
import study_module

def search_stackoverflow(query):
    url = "https://api.stackexchange.com/2.3/search"
    params = {
        "site": "stackoverflow",
        "intitle": query,
        "order": "desc",
        "sort": "relevance",
        "filter": "!-*jbN-L6LS3C"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'items' in data:
        answers = []
        for item in data['items']:
            answer_id = item['accepted_answer_id']
            answer_url = item['link']
            answers.append(f"Answer ID: {answer_id}\nAnswer URL: {answer_url}\n")
        return answers
    else:
        return ["No answers found."]

def get_latest_news(api_key, country_code='us'):
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()

    if data.get('status') == 'ok':
        articles = data.get('articles', [])
        news = []
        for article in articles:
            title = article.get('title', 'N/A')
            source = article['source'].get('name', 'N/A')
            news.append(f"Title: {title}\nSource: {source}\n")
        return news
    else:
        return ["Unable to fetch news."]

def clean_text(text: str) -> str:
    """Clean input text by removing non-alphabetic characters and converting to lowercase."""
    sub = re.sub(r'[^a-z]+', ' ', text.lower())
    return sub

def match_input(input_text: str, patterns_responses: dict, json_file: str) -> Optional[str]:
    """Match user input with stored patterns and return the best matching response."""
    cleaned_input = clean_text(input_text)
    best_match = None
    best_match_score = 0

    # Check for matches in patterns and responses dictionary
    for pattern, response in patterns_responses.items():
        score = sum(1 for word in cleaned_input.split() if word in pattern.split())

        if score > best_match_score:
            best_match_score = score
            best_match = response

    # If no match found, search in the JSON file
    if not best_match:
        with open(json_file, 'r') as file:
            stored_patterns_responses = json.load(file)

        for pattern, response in stored_patterns_responses.items():
            score = sum(1 for word in cleaned_input.split() if word in pattern.split())

            if score > best_match_score:
                best_match_score = score
                best_match = response

    return best_match

def update_patterns_responses(input_text: str, response: str, patterns_responses: dict, json_file: str) -> None:
    """Update patterns and responses based on user input and store them in a JSON file."""
    cleaned_input = clean_text(input_text)
    patterns_responses[cleaned_input] = response

    with open(json_file, 'w') as file:
        json.dump(patterns_responses, file)

def get_noun_from_sentence(sentence: str) -> Optional[str]:
    blob = TextBlob(sentence)
    nouns = blob.noun_phrases
    if nouns:
        return nouns[0]
    return None

def search_movie(noun: str) -> Optional[list[str]]:
    if noun is None:
        return None

    with open('movies.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        movie_titles = [row['original_title'] for row in reader]

    # Calculate similarity scores between noun and movie titles
    scores = [(title, SequenceMatcher(None, noun, title.lower()).ratio()) for title in movie_titles]

    # Sort the scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Get the top 5 relevant movie titles
    relevant_movies = [score[0] for score in scores[:5]]

    return relevant_movies

def main():
    json_file = 'patterns_responses.json'  # Path to the JSON file

    try:
        with open(json_file, 'r') as file:
            patterns_responses = json.load(file)
    except FileNotFoundError:
        patterns_responses = {'hello': 'hi there!'}

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            break

        if '||' in user_input:
            input_text, response = user_input.split('||', 1)
            update_patterns_responses(input_text.strip(), response.strip(), patterns_responses, json_file)
            print("Chatbot: I've learned a new response.")
        else:
            chatbot_response = match_input(user_input, patterns_responses, json_file)
            if chatbot_response:
                text = user_input
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity

                print(f"Chatbot: {chatbot_response}")
                if polarity < 0.5:
                    print("😀")
                elif polarity == 0.0:
                    print("😐")
                else:
                    print("☹")

                if user_input.lower().startswith("summarise"):
                    def split_sentence(sentence):
                        keyword = "summarise"
                        if sentence.lower().startswith(keyword):
                            rest_of_sentence = sentence[len(keyword):].strip()
                            return rest_of_sentence
                        else:
                            return ""

                    module = study_module.Study_stuff()
                    print(module.shorten_sentence(split_sentence(user_input)))
                if "movie" in chatbot_response.lower():
                    noun = get_noun_from_sentence(chatbot_response)
                    movie_data = search_movie(noun)
                    if movie_data:
                        print(f"Movie: {movie_data}")
                    else:
                        print("Movie not found.")
                elif "news" in chatbot_response.lower():
                    # Replace 'YOUR_API_KEY' with your actual API key
                    api_key = '51e459b97a2b428a95b5b20188eb3103'

                    # Call the function to get the latest news
                    news = get_latest_news(api_key)
                    for article in news:
                        print(article)
                elif user_input.lower().startswith("query"):
                    # Example usage
                    query = user_input[6:]
                    answers = search_stackoverflow(query)
                    for answer in answers:
                        print(answer)

            else:
                phrases = ["Could you rephrase or add it to my memory?", "Sorry, I didn't understand that.",
                           "I did not get that."]
                random_response = random.choice(phrases)
                print(f"Chatbot: {random_response}")

if __name__ == "__main__":
    main()
