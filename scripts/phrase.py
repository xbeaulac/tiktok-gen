import spacy

# Load the spacy model
nlp = spacy.load("en_core_web_sm")


def extract_key_phrases(text):
    # Process the text with spacy
    doc = nlp(text)

    # Extract the top-ranked phrases
    key_phrases = [phrase.text for phrase in doc._.phrases]

    return key_phrases


def extract_key_words(text):
    # Process the text with spacy
    doc = nlp(text)

    # Extract nouns, adjectives, adverbs, and verbs
    return [token.text for token in doc if
            token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "ADV" or token.pos_ == "VERB"]


def extract_clauses(text):
    # Process the text with spacy
    doc = nlp(text)

    # Initialize a list to store clauses
    clauses = []

    # Iterate over the sentences in the document
    for sent in doc.sents:
        # Extracting the root of the sentence
        root = [token for token in sent if token.head == token][0]

        # Function to recursively find the sub-clauses
        def get_clauses(token):
            clause = [t.text for t in token.subtree]
            clauses.append(' '.join(clause))

        # Call the function for each child of the root
        for child in root.children:
            get_clauses(child)

    return clauses


# Example text
text = "When you age to 113 years old you're a teenager again."

key_phrases = extract_clauses(text)

# Output the key phrases
for idx, phrase in enumerate(key_phrases):
    print(f"Key Phrase {idx + 1}: {phrase}")
