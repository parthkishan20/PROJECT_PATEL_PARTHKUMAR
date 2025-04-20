
# ================================
# app.py
# Author: PARTHKUMAR PATEL
# Description:
# This is a Flask-based Search Engine.
# It builds an inverted index from HTML files and supports search queries through a web interface.
# ================================

# Import required libraries
from flask import Flask, render_template, request, session, url_for, send_from_directory  # Flask components
from flask_cors import CORS  # Allows cross-origin access (not strictly needed here but useful)
from bs4 import BeautifulSoup  # For reading HTML content
from datetime import timedelta  # To set session timeout
import os  # File operations
import re  # Regular expressions for text cleaning

# Creating the Flask app
app = Flask(__name__)

# Set a secret key (required for session management)
app.secret_key = "top_secret_key"  # In production, use a secure, random key

# Set session timeout to 5 minutes
app.permanent_session_lifetime = timedelta(minutes=5)

# Enable CORS (Cross-Origin Resource Sharing) for all routes
CORS(app)

# =============================
# Function: load_stopwords
# Purpose: Reads stopwords from file and returns them as a set
# =============================
def load_stopwords(filepath="stopwords.txt"):
    with open(filepath, 'r') as f:
        return set(word.strip().lower() for word in f.readlines())

# =============================
# Function: tokenize
# Purpose: Cleans text, removes punctuation and stopwords, splits into words
# =============================
def tokenize(text, stopwords):
    text = re.sub(r'[^\w\s]', '', text.lower())  # Lowercase and remove punctuation
    words = text.split()  # Split into words
    return [word for word in words if word not in stopwords and word.isalpha()]  # Filter out stopwords and non-words

# =============================
# Function: highlight_text
# Purpose: Adds <span> tags around search terms to highlight them in HTML
# =============================
def highlight_text(text, terms):
    for term in terms:
        # Case-insensitive match and wrap matches in a span with 'highlight' class
        pattern = re.compile(rf'\b({re.escape(term)})\b', re.IGNORECASE)
        text = pattern.sub(r'<span class="highlight">\1</span>', text)
    return text

# =============================
# Function: build_inverted_index
# Purpose: Creates the inverted index and extracts metadata like title and description
# =============================
def build_inverted_index(folder, stopwords):
    index = {}  # Main inverted index
    metadata = {}  # Store file title and description

    for filename in os.listdir(folder):  # Loop through all files
        if filename.endswith(".html"):  # Only process .html files
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                text = soup.get_text()  # Get raw text from HTML
                words = tokenize(text, stopwords)  # Clean and tokenize

                # Extract metadata from title and meta description
                title = soup.title.string.strip() if soup.title else filename
                description_tag = soup.find("meta", attrs={"name": "description"})
                description = description_tag['content'].strip() if description_tag and description_tag.get('content') else ""

                metadata[filename] = {
                    "title": title,
                    "description": description
                }

                # Build the inverted index
                for word in words:
                    if word not in index:
                        index[word] = {}
                    if filename not in index[word]:
                        index[word][filename] = 0
                    index[word][filename] += 1  # Count frequency

    return index, metadata

# =============================
# Function: search_query
# Purpose: Searches query terms in index and returns ranked results
# =============================
def search_query(index, query, stopwords, metadata):
    results = {}  # Store scores
    snippets = {}  # Store preview text for each result
    terms = tokenize(query, stopwords)  # Clean and split query

    for term in terms:
        if term in index:
            for file, freq in index[term].items():
                results[file] = results.get(file, 0) + freq  # Add score

                # Create snippet (only once per file)
                if file not in snippets:
                    with open(os.path.join("input_pages", file), 'r', encoding='utf-8') as f:
                        text = BeautifulSoup(f, 'html.parser').get_text()
                        words = tokenize(text, stopwords)
                        for i, word in enumerate(words):
                            if word == term:
                                start = max(i - 5, 0)
                                end = min(i + 5, len(words))
                                snippet = " ".join(words[start:end]) + "..."
                                snippets[file] = highlight_text(snippet, terms)
                                break

    # Sort results by score (high to low)
    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return [
        (highlight_text(metadata[file]["title"], terms), score, snippets.get(file, ""), file)
        for file, score in ranked
    ]

# =============================
# Route: /view/<filename>
# Purpose: Serves original HTML pages
# =============================
@app.route("/view/<path:filename>")
def view_page(filename):
    return send_from_directory("input_pages", filename)

# =============================
# Route: /
# Purpose: Main route for search form and results
# =============================
@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    query = ""
    recent = session.get("recent_searches", [])  # Get previous queries

    if request.method == "POST":
        query = request.form["query"].strip()  # Get the query text
        stopwords = load_stopwords()
        index, metadata = build_inverted_index("input_pages", stopwords)
        results = search_query(index, query, stopwords, metadata)

        # Log results to output.txt
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(f"Query: {query}\n")
            if results:
                f.write("Results:\n")
                for title, score, _, actual_file in results:
                    f.write(f"  {actual_file} (score: {score}) - Title: {title}\n")
            else:
                f.write("No matches found.\n")
            f.write("\n")

        # Save query to session history
        if query and query not in recent:
            recent.insert(0, query)
        if len(recent) > 5:
            recent = recent[:5]
        session["recent_searches"] = recent

    return render_template("index.html", results=results, query=query, recent=recent)

# =============================
# Start the Flask app
# =============================
if __name__ == "__main__":
    app.run(debug=True)
