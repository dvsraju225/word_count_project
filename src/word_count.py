import json
import pandas as pd
from collections import Counter
import re

# Function to preprocess text: lowercase, remove punctuation, and tokenize
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    # Filter words to keep only those with at least 5 letters
    filtered_words = [word for word in words if len(word) >= 5]
    return filtered_words

# Function to count word frequencies
def word_frequencies(words):
    return dict(Counter(words))

# Function to process the JSON data
def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Normalize the nested JSON data
    df = pd.json_normalize(data, sep='_')

    # Apply preprocessing to the `abstract__value` column
    df['abstract_words'] = df['abstract__value'].apply(preprocess_text)

    # Apply word frequency count to the `abstract_words` column
    df['word_freq'] = df['abstract_words'].apply(word_frequencies)

    # Create a new DataFrame for the word frequencies
    word_freq_df = pd.json_normalize(df['word_freq']).fillna(0)

    # Sum the occurrences of each word across all rows to find the top 20 most common words
    top_words = word_freq_df.sum().sort_values(ascending=False).head(20).index

    # Filter the word_freq_df to keep only the top 20 words
    top_word_freq_df = word_freq_df[top_words]

    # Add a unique identifier column
    top_word_freq_df['unique_id'] = range(1, len(df) + 1)

    # Reorder columns to place the unique identifier column at the beginning
    columns = ['unique_id'] + top_word_freq_df.columns[:-1].tolist()
    top_word_freq_df = top_word_freq_df[columns]

    return top_word_freq_df

# Function to save the DataFrame to a CSV file
def save_to_csv(df, output_path):
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Path to the local JSON file
    file_path = r'D:/Big Data/Aviva Task/input_data.json'
    df = process_json(file_path)
    print(df.head())

    # Write the final DataFrame to a CSV file
    output_path = r'D:/Big Data/Aviva Task/output.csv'
    save_to_csv(df, output_path)
