import pytest
import sys
import os
sys.path.append(os.getcwd())
from backend.src.normalizer import AmharicNormalizer

@pytest.fixture
def normalizer():
    return AmharicNormalizer()

def test_normalize_same_string(normalizer):
    assert normalizer.normalize("") == ""
    
def test_normalize_same_string(normalizer):
    assert normalizer.normalize("ሰላም") == "ሰላም"

def test_normalize_replacements(normalizer):
    assert normalizer.normalize("ኣንድ ነህ") == "አንድ ነህ"

def test_normalize_whitespace(normalizer):
    assert normalizer.normalize("ጩዋታ") == "ጯታ"

def test_normalize_combined_rules(normalizer):
    assert normalizer.normalize("ፉዋ ያለ ቀን ይሁንላቹ") == "ፏ ያለ ቀን ይሁንላቹ"

def test_normalize_combined_rules(normalizer):
    assert normalizer.normalize("ሰላም! ኣንዴ የት ነህ") == "ሰላም! አንዴ የት ነህ"

if __name__  == "__main__":
    pytest.main([__file__])