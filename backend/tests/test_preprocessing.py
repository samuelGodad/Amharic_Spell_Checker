import pytest
import sys
import os
sys.path.append(os.getcwd())
from backend.src.preprocessing import AmharicTextProcessor

@pytest.fixture
def text_processor():
    return AmharicTextProcessor()

def test_remove_non_amharic(text_processor):
    input_text = "ሰላም ! Hello 123"
    expected_output = "ሰላም"
    assert text_processor.remove_non_amharic(input_text) == expected_output

def test_preprocess(text_processor):
    input_text = "ሰላም! ኣንዴ የት ነህ"
    expected_output = 'ሰላም አንዴ የት ነህ'
    assert text_processor.preprocess(input_text) == expected_output

if __name__  == "__main__":
    pytest.main([__file__])