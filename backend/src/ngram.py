from backend.src.tokenizer import AmharicSegmenter
from backend.src.preprocessing import AmharicTextProcessor
from nltk.util import ngrams
from collections import defaultdict
import pickle
import os

preprocessor = AmharicTextProcessor().preprocess

class NgramModel:
    def __init__(self, tokens: list, ngram_size=2):
        self.tokens = tokens
        self.ngram_size = ngram_size
        self.ngram_counts = defaultdict(int)
    
    def train(self):
        for ngram in ngrams(self.tokens, self.ngram_size):
                self.ngram_counts[ngram] += 1
    
    def get_ngram_count(self, ngram):
        return self.ngram_counts[ngram]
    
    def get_ngram_probability(self, ngram):
        ngram_count = self.get_ngram_count(ngram)
        total_count = sum(self.ngram_counts.values())
        return ngram_count / total_count

    def save(self, path):
        if not path.endswith('.pkl'):
            path += 'model.pkl'
        # check: if path does not exist create one
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, path):
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            # Handle the exception according to your application's requirements
            print(f"Error loading model: {e}")
            return None  # Or raise the exception if needed
    
    def get_ngram_probability_with_smoothing(self, ngram):
        """
        ngram: (a, b, c) = (before, word, after)
        """ 
        ngram_count = self.get_ngram_count(ngram)
        total_count = sum(self.ngram_counts.values())
        return (ngram_count + 1) / (total_count + len(self.ngram_counts))