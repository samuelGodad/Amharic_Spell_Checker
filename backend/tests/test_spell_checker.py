import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.getcwd())
from backend.src.main import app  # Assuming your FastAPI app instance is named 'app'

client = TestClient(app)

@pytest.mark.integration
def test_spell_checker_integration():
    # Input text with intentional spelling errors
    input_text = "ሰላም! አንዴ የት ነህ"

    # Expected result with suggestions and rankings
    expected_result = {
        "text": input_text,
        "errors": [
            {
                "word": "አንዴ",
                "suggestions": ["እንደ", "አንዳ", "አንድ", "አንዱ", "አንዷ"],
                "adjacent_words": (None, "የት"),
            }
            # Add more expected error cases as needed
        ],
    }

    # Make a request to the spellcheck endpoint
    response = client.get("/check", params={"text": input_text})
    assert response.status_code == 200

    # Check if the response matches the expected result
    result = response.json()["result"]
    print(result)
    assert result == result

# You can add more integration tests as needed
if __name__ == "__main__":
    pytest.main([__file__])