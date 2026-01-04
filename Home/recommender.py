from .models import Product
from collections import Counter
import math

# ---------- STOPWORDS ----------
STOPWORDS = {"this", "is", "a", "an", "the", "for", "and", "or", "of", "like", "with", "to", "on"}

# ---------- TOKENIZATION & CLEANING ----------
def normalize_token(token):
    token = token.lower().strip(",.!?()-")
    # simple stemming for plurals
    if token.endswith("s") and len(token) > 3:
        token = token[:-1]
    return token

def tokenize(text):
    tokens = []
    for w in text.replace("-", " ").split():
        w = normalize_token(w)
        if w and w not in STOPWORDS:
            tokens.append(w)
    return tokens

# ---------- BUILD DOCS & VOCAB ----------
def build_docs_and_vocab():
    products = Product.objects.all()
    docs = []
    product_list = []

    for p in products:
        category_display = dict(Product._meta.get_field('category').choices).get(p.category, p.category)
        text = f"{p.Name} {category_display} {p.Description or ''}"
        tokens = tokenize(text)
        docs.append(tokens)
        product_list.append(p)

    vocab = sorted(set(word for doc in docs for word in doc))
    return docs, vocab, product_list

# ---------- TF-IDF HELPERS ----------
def term_frequency(doc, vocab):
    counts = Counter(doc)
    total = len(doc)
    return {word: counts.get(word, 0) / total for word in vocab}

def inverse_document_frequency(docs, vocab):
    idf = {}
    N = len(docs)
    for word in vocab:
        doc_count = sum(1 for doc in docs if word in doc)
        idf[word] = math.log((N + 1) / (doc_count + 1)) + 1
    return idf

def tfidf_vector(doc, vocab, idf):
    tf = term_frequency(doc, vocab)
    return [tf[word] * idf[word] for word in vocab]

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot / (mag1 * mag2)

# ---------- RECOMMEND FUNCTION ----------
def recommend_products(query, top_n=5, min_score=0.1):
    docs, vocab, products = build_docs_and_vocab()
    idf = inverse_document_frequency(docs, vocab)
    tfidf_docs = [tfidf_vector(doc, vocab, idf) for doc in docs]

    q_tokens = tokenize(query)
    q_vec = tfidf_vector(q_tokens, vocab, idf)

    scores = []
    for i, product_vec in enumerate(tfidf_docs):
        # base similarity
        score = cosine_similarity(q_vec, product_vec)

        # category string
        product_category = dict(Product._meta.get_field('category').choices).get(
            products[i].category, products[i].category
        ).lower()

        # tokenize name + category + description
        product_tokens = tokenize(products[i].Name + " " + product_category + " " + (products[i].Description or ""))

        # BOOST exact token matches
        match_count = sum(1 for token in q_tokens if token in product_tokens)
        score += 0.8 * match_count

        # BOOST if query contains category keyword
        for token in q_tokens:
            if token in product_category:
                score += 0.35

        # Only include products with at least one token match or category match
        if match_count > 0 or any(token in product_category for token in q_tokens):
            scores.append((i, score, product_category))

    # if nothing matches, return empty
    if not scores:
        return []

    # sort scores
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # top category boost
    top_category = scores[0][2]
    boosted = []
    for idx, score, category in scores:
        if category == top_category:
            score += 0.15
        boosted.append((idx, score))

    boosted = sorted(boosted, key=lambda x: x[1], reverse=True)

    return [products[idx] for idx, _ in boosted[:top_n]]
