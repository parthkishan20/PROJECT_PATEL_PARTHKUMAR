
# Search Engine Project - README

**Author**: Parthkumar Patel  
**CWID**: 20029693  
**Course**: CS-600 Advanced Algorithms  

---

##  What This Project Does

This project is a basic **search engine** built using Python.  
It looks through a group of `.html` web pages and finds which ones match your search words.

Here’s what it can do:

✅ Reads the content of each page  
✅ Ignores common words like "the", "and", "of"  
✅ Remembers which words appear in which files  (Recent Searches)

✅ Lets you search from a webpage  
✅ Shows results ranked by how many times the word appears  
✅ Highlights the matched words  
✅ Shows a preview (snippet) for each result  
✅ Saves every search and result to `output.txt`

---

## 📁 What’s Inside This Project Folder

```
SearchEngineProject/
├── app.py             # Main Flask web app
├── crawler.py         # Script to download sample HTML pages
├── search_engine.py   # Command-line version of the search engine
├── stopwords.txt      # List of common words to ignore in searches
├── output.txt         # File where search results are saved
├── input_pages/       # Folder of HTML files used for search
├── static/
│   ├── style.css      # Styles for the search page and dark mode
│   └── toggle.js      # Dark mode toggle script
└── templates/
    └── index.html     # Webpage design for search interface
```

---

## ▶️ How to Run This Project

### OPTION 1: Web Version 

1. Make sure you have Python installed.
2. Install the required libraries:
   ```bash
   pip install flask beautifulsoup4
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open this link in your browser:  
   `http://localhost:5000`

5. Type a search word, like `wikipedia`, and hit Search.

You’ll see:
- Matching pages
- Number of matches
- A short preview (snippet)
- Highlighted terms
- Recent searches
- Results saved in `output.txt`

---

### OPTION 2: Command-Line Version

1. Open a terminal or command prompt.
2. Run:
   ```bash
   python search_engine.py
   ```
3. Type your search queries.
4. Type `exit` to quit.
5. Results are printed on screen and saved to `output.txt`.

---

## 🧠 How It Works (Simple Terms)

### 📌 Inverted Index (like a dictionary)
The program creates a dictionary that looks like this:
```
{
  "search": { "page1.html": 2, "page3.html": 1 },
  "python": { "page2.html": 1 }
}
```
This tells the program:
- Which word appears in which files
- How many times it appears

### 📌 Stop Words
It uses a file called `stopwords.txt` to skip boring/common words and articles, prepositions, and pronouns like:
- the, a, is, and, of, etc.

### 📌 Ranking
If a word appears more times in a page, that page gets a higher score.

---

## ✨ Features Included

- ✅ Clean and simple web UI
- ✅ Dark mode 
- ✅ Highlights the searched word
- ✅ Snippet/preview from matching page
- ✅ Recent search history (up to 5 items)
- ✅ Search results saved to `output.txt`
- ✅ Works with both web and CLI

---

## 🧪 Tests & Edge Cases

We made sure the app works for:
- Queries with only stop words → shows “no matches”
- Queries with words not found → “no matches”
- Multi-word searches like: `search engine demo`
- HTML pages that don’t have `<title>` or `<meta>` tags
- Words at the very beginning or end of pages

---

## 🧰 Tools and Libraries Used

- Python 3
- Flask (for the web app)
- BeautifulSoup (to read HTML files)


---

Thank You!

---
