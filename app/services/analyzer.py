import re
from collections import Counter
from app.models.schemas import SERPItem
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

STOPWORDS = {
    "the", "and", "for", "to", "of", "in", "a", "on", "with", "best", "top",
    "2025", "2024", "how", "what", "why", "when", "where", "can", "will",
    "your", "you", "is", "are", "this", "that", "from", "by", "at", "an"
}


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9\-]+", text.lower())
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return tokens


def extract_keywords(serp_items: list[SERPItem], top_n: int = 15) -> dict:
    counter = Counter()
    bigram_counter = Counter()
    
    for item in serp_items:
        title_tokens = tokenize(item.title)
        snippet_tokens = tokenize(item.snippet)
        
        counter.update(title_tokens)
        counter.update(title_tokens)
        counter.update(snippet_tokens)
        
        for i in range(len(title_tokens) - 1):
            bigram = f"{title_tokens[i]} {title_tokens[i+1]}"
            bigram_counter[bigram] += 2
        
        for i in range(len(snippet_tokens) - 1):
            bigram = f"{snippet_tokens[i]} {snippet_tokens[i+1]}"
            bigram_counter[bigram] += 1
    
    most_common = [k for k, _ in counter.most_common(top_n)]
    most_common_bigrams = [k for k, _ in bigram_counter.most_common(5)]
    
    primary = most_common_bigrams[0] if most_common_bigrams else " ".join(most_common[:2])
    secondary = most_common[:10]
    
    return {
        "primary": primary,
        "secondary": secondary,
        "bigrams": most_common_bigrams
    }


def extract_common_themes(serp_items: list[SERPItem]) -> list[str]:
    all_text = " ".join([item.title + " " + item.snippet for item in serp_items])
    tokens = tokenize(all_text)
    
    counter = Counter(tokens)
    themes = [word for word, count in counter.most_common(20) if count >= 3]
    
    return themes


def calculate_keyword_density(text: str, keywords: list[str]) -> dict[str, float]:
    words = text.lower().split()
    total_words = len(words)
    
    if total_words == 0:
        return {kw: 0.0 for kw in keywords}
    
    densities = {}
    for kw in keywords:
        count = text.lower().count(kw.lower())
        densities[kw] = round((count / total_words) * 100, 2)
    
    return densities

