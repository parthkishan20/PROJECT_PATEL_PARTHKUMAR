
# ================================================
# search_engine.py
# Author: PARTHKUMAR PATEL
# Description:
# This is a command-line version of a search engine.
# It builds an inverted index from HTML files, accepts user queries, and ranks results based on word frequency.
# ================================================

import os  # Used for file/directory handling
import re  # Used for text cleaning (regular expressions)
from bs4 import BeautifulSoup  # Used to extract text from HTML files

# === Function: load_stopwords ===
# Reads stopwords from a file and stores them in a set
def load_stopwords(filepath="stopwords.txt"):
    with open(filepath, 'r') as f:
        return set(word.strip().lower() for word in f.readlines())

# === Function: tokenize ===
# Cleans text and removes punctuation and stopwords
def tokenize(text, stopwords):
    text = re.sub(r'[^\w\s]', '', text.lower())  # Lowercase and remove punctuation
    words = text.split()
    return [word for word in words if word not in stopwords and word.isalpha()]  # Keep only alphabetic words

# === Function: build_inverted_index ===
# Reads each HTML file and builds an inverted index
# Format: {word: {filename: frequency}}
def build_inverted_index(folder, stopwords):
    index = {}

    for filename in os.listdir(folder):  # Loop through all files in the folder
        if filename.endswith(".html"):  # Process only HTML files
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')  # Parse HTML content
                text = soup.get_text()  # Extract visible text
                words = tokenize(text, stopwords)  # Clean and tokenize

                # Count the frequency of each word in this file
                for word in words:
                    if word not in index:
                        index[word] = {}
                    if filename not in index[word]:
                        index[word][filename] = 0
                    index[word][filename] += 1  # Increase frequency

    return index  # Return the full inverted index

# === Function: search_query ===
# Looks up the query in the inverted index and returns matching files ranked by word frequency
def search_query(index, query, stopwords):
    results = {}  # Dictionary to store file scores
    terms = tokenize(query, stopwords)  # Clean and tokenize user input

    for term in terms:
        if term in index:
            for file, freq in index[term].items():
                results[file] = results.get(file, 0) + freq  # Sum frequencies if multiple terms match

    # Return results sorted by frequency (highest first)
    return sorted(results.items(), key=lambda x: x[1], reverse=True)

# === Main Function: Runs the CLI search engine ===
def main():
    stopwords = load_stopwords()  # Load stop words
    index = build_inverted_index("input_pages", stopwords)  # Build index from HTML files

    print("📚 Simple Search Engine Ready! Type your query (or 'exit' to quit):")
    logs = []  # Store logs to write to file later

    while True:
        query = input("\nQuery: ").strip()  # Ask user for input
        if query.lower() == 'exit':
            break

        matches = search_query(index, query, stopwords)  # Get matching files
        log_entry = f"Query: {query}\n"

        if matches:
            log_entry += "Results:\n"
            for file, score in matches:
                log_entry += f"  {file} (score: {score})\n"
                print(f"{file} (score: {score})")  # Print to console
        else:
            log_entry += "No matches found.\n"
            print("No matches found.")

        logs.append(log_entry)  # Save the result

    # Save everything to output.txt
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("=== Search Engine Query Log ===\n\n")
        f.write("\n".join(logs))

    print("\n📁 All results saved to output.txt ✅")

# === Entry Point: Run the program ===
if __name__ == "__main__":
    main()
