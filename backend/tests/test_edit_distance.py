import pytest
import sys
import os
sys.path.append(os.getcwd())
from backend.src.edit_distance import levenshtein_distance

def test_levenshtein_distance_same_strings():
    assert levenshtein_distance("ሰላም", "ሰላም") == 0

def test_levenshtein_distance_empty_strings():
    assert levenshtein_distance("", "") == 0

def test_levenshtein_distance_insertion():
    assert levenshtein_distance("ድመት", "ድመትን") == 1

def test_levenshtein_distance_deletion():
    assert levenshtein_distance("ድመት", "ድመ") == 1

def test_levenshtein_distance_substitution():
    assert levenshtein_distance("ድመት", "ድምት") == 1

if __name__ == "__main__":
    pytest.main()
