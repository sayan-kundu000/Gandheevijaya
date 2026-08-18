import math
import re
import difflib
from collections import Counter
from typing import List, Set, TypeVar, Any

import numpy as np

T = TypeVar('T')

class SemanticDeduplicator:
    """
    Data Science NLP Engine for Semantic Question Deduplication & Diversity Enforcement.
    Combines Word TF-IDF, Char 3-Gram TF-IDF, Token Fuzzy Alignment, and Sequence Matcher.
    """
    def __init__(self, stop_words: Set[str] = None):
        self.stop_words = stop_words or {
            "a", "an", "the", "and", "or", "but", "if", "then", "else", "when", "at", "from",
            "by", "for", "with", "about", "against", "between", "into", "through", "during",
            "before", "after", "above", "below", "to", "from", "up", "down", "in", "out",
            "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
            "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
            "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can",
            "will", "just", "should", "now", "which", "what", "who", "whom", "this", "that",
            "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "having", "do", "does", "did", "doing", "would", "should",
            "could", "ought", "i", "you", "he", "she", "it", "we", "they", "following", "statement",
            "statements", "correct", "incorrect", "select", "choose", "find", "given"
        }

    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        # Remove code blocks and markdown tags
        text = re.sub(r'```[a-z]*', ' ', text)
        text = re.sub(r'```', ' ', text)
        # Normalize punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        # Collapse whitespace
        return re.sub(r'\s+', ' ', text).strip()

    def get_char_ngrams(self, text: str, n=3) -> List[str]:
        norm = self.normalize_text(text).replace(" ", "")
        if len(norm) < n:
            return [norm] if norm else []
        return [norm[i:i+n] for i in range(len(norm) - n + 1)]

    def get_word_tokens(self, text: str) -> List[str]:
        norm = self.normalize_text(text)
        words = [w for w in norm.split() if w not in self.stop_words and len(w) > 1]
        unigrams = words
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)]
        return unigrams + bigrams

    def compute_tfidf_similarity(self, items1: List[str], items2: List[str]) -> float:
        if not items1 or not items2:
            return 0.0

        vocab = sorted(list(set(items1 + items2)))
        v1 = Counter(items1)
        v2 = Counter(items2)

        vec1 = []
        vec2 = []
        for term in vocab:
            df = (1 if term in v1 else 0) + (1 if term in v2 else 0)
            idf = math.log((2.0 + 1.0) / (df + 1.0)) + 1.0
            tf1 = v1[term] / len(items1)
            tf2 = v2[term] / len(items2)
            vec1.append(tf1 * idf)
            vec2.append(tf2 * idf)

        arr1 = np.array(vec1)
        arr2 = np.array(vec2)

        dot = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

    def compute_token_fuzzy_similarity(self, text1: str, text2: str) -> float:
        words1 = [w for w in self.normalize_text(text1).split() if w not in self.stop_words]
        words2 = [w for w in self.normalize_text(text2).split() if w not in self.stop_words]

        if not words1 or not words2:
            return 0.0

        matches = 0
        for w1 in words1:
            best_match = max((difflib.SequenceMatcher(None, w1, w2).ratio() for w2 in words2), default=0.0)
            if best_match >= 0.80:
                matches += 1

        denom = max(len(words1), len(words2))
        return matches / denom if denom > 0 else 0.0

    def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculates Data Science semantic similarity score between two texts in range [0.0, 1.0].
        Weights: Word TF-IDF (35%), Char 3-Gram TF-IDF (35%), Token Fuzzy Match (30%).
        """
        norm1 = self.normalize_text(text1)
        norm2 = self.normalize_text(text2)
        if not norm1 or not norm2:
            return 0.0
        if norm1 == norm2:
            return 1.0

        word_tokens1 = self.get_word_tokens(text1)
        word_tokens2 = self.get_word_tokens(text2)
        word_tfidf = self.compute_tfidf_similarity(word_tokens1, word_tokens2)

        char_ngrams1 = self.get_char_ngrams(text1, n=3)
        char_ngrams2 = self.get_char_ngrams(text2, n=3)
        char_tfidf = self.compute_tfidf_similarity(char_ngrams1, char_ngrams2)

        token_fuzzy = self.compute_token_fuzzy_similarity(text1, text2)

        composite = (0.35 * word_tfidf) + (0.35 * char_tfidf) + (0.30 * token_fuzzy)
        return round(composite, 4)

    def is_semantically_similar(self, text1: str, text2: str, threshold: float = 0.40) -> bool:
        return self.get_semantic_similarity(text1, text2) >= threshold

    def filter_semantically_diverse_questions(
        self, questions: List[Any], threshold: float = 0.40, text_attr: str = "question_text"
    ) -> List[Any]:
        """
        Filters candidate question objects to ensure NO TWO QUESTIONS in the returned list
        share high semantic similarity (>= threshold).
        """
        selected: List[Any] = []
        for q in questions:
            q_text = getattr(q, text_attr, None) or (q.get(text_attr) if isinstance(q, dict) else str(q))
            is_similar = False
            for chosen in selected:
                chosen_text = getattr(chosen, text_attr, None) or (chosen.get(text_attr) if isinstance(chosen, dict) else str(chosen))
                if self.is_semantically_similar(q_text, chosen_text, threshold=threshold):
                    is_similar = True
                    break
            if not is_similar:
                selected.append(q)
        return selected

default_semantic_deduplicator = SemanticDeduplicator()
