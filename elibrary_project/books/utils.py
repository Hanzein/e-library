import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
import string

def analyze_book_text(pdf_path):
    """Extract keywords from PDF using NLP analysis"""
    try:
        # Download required NLTK data if not already present
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Process text and extract keywords
        keywords = extract_keywords(text)
        
        return keywords
    except Exception as e:
        print(f"Error in analyze_book_text: {str(e)}")
        return []

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF file"""
    text = ""
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    
    doc.close()
    return text

def extract_keywords(text, num_keywords=20):
    """Extract keywords from text using TF-IDF"""
    if not text.strip():
        return []
    
    # Clean and preprocess text
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords (English and Indonesian common words)
    stop_words = set(stopwords.words('english'))
    indonesian_stopwords = {'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 
                           'pada', 'adalah', 'akan', 'atau', 'juga', 'dalam', 
                           'dapat', 'tidak', 'ada', 'ini', 'itu', 'sebagai',
                           'oleh', 'saya', 'kami', 'kita', 'mereka', 'dia'}
    stop_words.update(indonesian_stopwords)
    
    # Filter tokens
    filtered_tokens = [token for token in tokens 
                      if token not in stop_words 
                      and len(token) > 2 
                      and token.isalpha()]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Use TF-IDF to find important words
    if len(lemmatized_tokens) == 0:
        return []
    
    # Join tokens back to text for TF-IDF
    processed_text = ' '.join(lemmatized_tokens)
    
    # Apply TF-IDF
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    
    try:
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Get top keywords
        keyword_scores = list(zip(feature_names, tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        keywords = [keyword for keyword, score in keyword_scores[:num_keywords] if score > 0]
        
        return keywords
    except Exception as e:
        # Fallback to simple word frequency if TF-IDF fails
        word_freq = Counter(lemmatized_tokens)
        return [word for word, freq in word_freq.most_common(num_keywords)]