from spell_checker import SpellChecker
from flair.models import SequenceTagger
from flair.data import Sentence
import os
from pathlib import Path

# models_path = "models/"
# pos_model_path = models_path + 'am_pos_model.pt'
current_dir = Path(__file__).parent
models_path = os.path.normpath(os.path.join(current_dir.parent, "models"))
pos_model_path = os.path.normpath(os.path.join(models_path, "am_pos_model.pt"))
print("this is the path to the pos model: ", pos_model_path)
print("this is the path to the models: ", models_path)

class SpellCheckerWithPOS(SpellChecker):
    def __init__(self, dictionary_model, ngram_model, pos_model_path=pos_model_path):
        super().__init__(dictionary_model, ngram_model)
        self.pos_model = SequenceTagger.load(
            pos_model_path) if pos_model_path else None

    def _get_pos_tags(self, sentence):
        """
        Get POS tags for a given sentence.
        """
        if self.pos_model:
            flair_sentence = Sentence(sentence)
            self.pos_model.predict(flair_sentence)
            # get pos tags from the flair sentence
            return [token.to_dict()['labels'][0]['value'] for token in flair_sentence]

        else:
            # If POS model is not provided, return None for all POS tags
            return [None] * len(sentence.split())

    def check(self, text):
        result = {
            "text": text,
            "errors": []
        }
        preprocessed_text = self.preprocessor(text)
        sentences = self.tokenizer.sentence_tokenize(preprocessed_text)

        for sentence in sentences:
            words = self.tokenizer.word_tokenize(sentence)
            pos_tags = self._get_pos_tags(sentence)

            for i, (word, pos_tag) in enumerate(zip(words, pos_tags)):
                # Skip checking nouns (NOUN) and pronouns (PRON)
                if pos_tag and pos_tag in {'NOUN', 'PRON'}:
                    continue

                if not self._check_spelling(word):
                    suggestions = self._suggest_corrections(word)
                    start_index = text.find(word)
                    adjacent_words = (None, None)  # Initialize adjacent_words
                    if start_index != -1:
                        adjacent_words = (
                            words[i - 1] if i > 0 else None,
                            words[i + 1] if i < len(words) - 1 else None
                        )
                    
                    result["errors"].append({
                        'word': word,
                        'suggestions': suggestions,
                        'index': [start_index, start_index + len(word)],
                        'adjacent_words': adjacent_words,
                    })

        return result