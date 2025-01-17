import streamlit as st
import pandas as pd
import numpy as np
import textdistance
from textblob import TextBlob
import re
from collections import Counter

# Load the Swahili dataset
def load_swahili_dataset():
    with open('swahili.txt', 'r') as f:
        file_name_data = f.read().lower()
    words = re.findall(r'\w+', file_name_data)
    return words

# Function to create word frequencies and probabilities
def create_word_freq(words):
    word_freq_dict = Counter(words)
    total = sum(word_freq_dict.values())
    probs = {k: word_freq_dict[k] / total for k in word_freq_dict.keys()}
    return word_freq_dict, probs

# Function to perform autocorrect on multiple words
def swahili_autocorrect(input_text, word_freq_dict, probs):
    words = input_text.lower().split()  # Split input into words by spaces
    output = ""

    for input_word in words:
        input_word = re.sub(r'[^A-Za-z0-9]+', '', input_word)
        
        if input_word in word_freq_dict:
            output += f'"{input_word}" is a correctly spelled Swahili word.\n'
        else:
            similarities = [1 - textdistance.Jaccard(qval=2).distance(v, input_word) for v in word_freq_dict.keys()]
            df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
            df = df.rename(columns={'index': 'Word', 0: 'Prob'})
            df['Similarity'] = similarities
            suggestions = df.sort_values(['Similarity', 'Prob'], ascending=False).head()
            output += f'"{input_word}" is a misspelled Swahili word. Suggestions:\n{suggestions.to_string(index=False)}\n\n'

    return output

# Main Streamlit app
def main():
    st.title("Swahili Spell Checker")

    words = load_swahili_dataset()
    word_freq_dict, probs = create_word_freq(words)

    input_text = st.text_area("Please input Swahili words to be checked ;-)", "")

    if st.button("Check"):
        if input_text:
            result = swahili_autocorrect(input_text, word_freq_dict, probs)
            st.text_area("Result", value=result, height=400)

    if st.button("Clear"):
        st.text_area("Result", value="", height=400)

if __name__ == '__main__':
    main()
