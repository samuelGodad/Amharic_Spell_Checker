# Distance Calculation and Dictionary Look Up
from edit_distance import levenshtein_distance
from dictionary import Dictionary

# Text Preprocessing
from preprocessing import AmharicTextProcessor
from tokenizer import AmharicSegmenter

# Context Analyzer
from ngram import NgramModel

class SpellChecker:
    def __init__(self, dictionary_model: Dictionary, ngram_model: NgramModel):
        self.dictionary = dictionary_model
        self.model = ngram_model
        self.tokenizer = AmharicSegmenter()
        self.preprocessor = AmharicTextProcessor().preprocess

    def _suggest_corrections(self, word, num_suggestions=10, threshold=0.6):
        """
        Suggest corrections for the given word based on levenshtein distance.
        """
        suggestions = []

        for candidate in self.dictionary.get_words():
            distance = levenshtein_distance(word, candidate)
            similarity = 1 - distance / max(len(word), len(candidate), 1) # solving division by zero
            if similarity > threshold:
                suggestions.append(candidate)
        
        suggestions = suggestions[:num_suggestions]
        if suggestions[0] == word and len(suggestions) == 1: return []
        if suggestions[-1] == word: suggestions[:-1]
        return suggestions

    def _check_spelling(self, word):
        """
        Check the spelling of the given word.
        """
        return self.dictionary.look(word)

    def check(self, text):
        result = {
            "text": text,
            "errors": []
        }
        preprocessed_text = self.preprocessor(text)
        words = self.tokenizer.word_tokenize(preprocessed_text)
        for i, word in enumerate(words):
            if not self._check_spelling(word):
                suggestions = self._suggest_corrections(word)
                adjacent_words = (
                    words[i-1] if i > 0 else None, words[i+1] if i < len(words) - 1 else None)
                result["errors"].append({
                    'word': word,
                    'suggestions': suggestions,
                    'adjacent_words': adjacent_words,
                })

        return self._rank_suggestions(result)

    def _rank_suggestions(self, dictionary_result):
        result = {
            'text': dictionary_result['text'],
            'errors': []
        }

        for error in dictionary_result["errors"]:
            word = error["word"]
            suggestions = error["suggestions"]
            adjacent_words = error["adjacent_words"]
            ranked_suggestions = self._rank_individual_suggestions(
                word, suggestions, adjacent_words)

            result["errors"].append({
                'word': word,
                'suggestions': ranked_suggestions,
            })

        return result

    def _calculate_relevance_score(self, suggestion, adjacent_words):
        """
        Calculate the relevance score of the given suggestions based on the adjacent words.
        """
        score = 0
        if adjacent_words[0] is not None:  # before provided
            score += self.model.get_ngram_probability((adjacent_words[0],) + (suggestion,))
        elif adjacent_words[1] is not None:  # after provided
            score += self.model.get_ngram_probability((suggestion,) + (adjacent_words[1],))
        else:
            score += self.model.get_ngram_probability((suggestion,))
        return score

    def _rank_individual_suggestions(self, wrong_word, suggestions, adjacent_words):
        """
        Rank the given suggestions for the given wrong word.
        """
        if len(suggestions) <= 1:
            return suggestions

        ranked_suggestions = []
        scores = [self._calculate_relevance_score(
            suggestion, adjacent_words) for suggestion in suggestions]
        
        for i in range(len(suggestions)):
            ranked_suggestions.append((suggestions[i], scores[i]))
        ranked_suggestions = sorted(
            ranked_suggestions, key=lambda x: x[1], reverse=True)

        return [suggestion[0] for suggestion in ranked_suggestions]
