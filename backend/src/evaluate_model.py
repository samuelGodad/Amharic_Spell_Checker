import os
import random
from spell_checker import SpellChecker
from dictionary import Dictionary
from ngram import NgramModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm  # Import tqdm for progress bar

# Initialize the spell checker
current_dir = os.path.dirname(os.path.abspath(__file__))
dictionary_path = os.path.join(current_dir, "../data/amharic_dictionary.txt")
bigram_model_path = os.path.join(current_dir, "../models/bigram_model.pkl")
dictionary_model = Dictionary(dictionary_path)
ngram_model = NgramModel.load(bigram_model_path)
spell_checker = SpellChecker(dictionary_model, ngram_model)

# Load the combined file
combined_file_path = os.path.join(current_dir, "../data/amharic_correct_and_incorrect_data.txt")
with open(combined_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Randomly select one-fourth of the data
sample_size = len(lines) // 4
sampled_lines = random.sample(lines, sample_size)

# Evaluate the spell checker
y_true = []
y_pred = []

# Use tqdm to add a progress bar
for line in tqdm(sampled_lines, desc="Evaluating"):
    word = line.strip()
    result = spell_checker.check(word)
    if not result["errors"]:
        y_pred.append(1)  # Correctly identified
    else:
        y_pred.append(0)  # Incorrectly identified
    y_true.append(1 if word in dictionary_model.get_words() else 0)

# Calculate accuracy
accuracy = accuracy_score(y_true, y_pred)

# Display results
print(f"Sample size: {sample_size}")
print(f"Accuracy: {accuracy:.2f}")
