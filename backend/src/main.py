import sys
from fastapi import FastAPI, HTTPException, Query
import time
import os
from pathlib import Path

# Use absolute imports
from src.spell_checker import SpellChecker
from src.spell_checker_pos import SpellCheckerWithPOS
from src.dictionary import Dictionary
from src.ngram import NgramModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict
from fastapi.staticfiles import StaticFiles

current_dir = Path(__file__).parent
print("this is the current direcotry for render",current_dir)
dictionary_path = os.path.join(current_dir.parent, "data", "amharic_dictionary_v1.txt")
bigram_model_path = os.path.join(current_dir.parent, "models", "bigram_model.pkl")
trigram_model_path = os.path.join(current_dir.parent, "models", "trigram_model.pkl")
pos = os.path.join(current_dir.parent, "models", "am_pos_model.pt")
t1 = time.time()
dictionary_model = Dictionary(dictionary_path)
ngram_model = NgramModel.load(bigram_model_path)

spell_checker = SpellChecker(dictionary_model, ngram_model)
spell_checker_pos = SpellCheckerWithPOS(dictionary_model, ngram_model, pos)
print(f"Models loaded successfully in {round(time.time() - t1, 3)} seconds")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend static files
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

class ErrorModel(BaseModel):
    word: str
    suggestions: List[str]
    index: List[int]
    adjacent_words: tuple[Optional[str], Optional[str]]
class RangeModel(BaseModel):
    index: int
    length: int
    word: str
    suggestions: List[str]

class SpellChekeRequest(BaseModel):
    text: str
    use_pos: bool = True

class SpellCheckResponse(BaseModel):
    text: str
    errors: List[ErrorModel]
    ranges: List[RangeModel]
    model_config = ConfigDict(arbitrary_types_allowed=True)

class ReplaceWordRequest(BaseModel):
    text: str
    index: int
    replacement: str

class ReplaceWordResponse(BaseModel):
    text: str

@app.post("/api/check-spelling", response_model=SpellCheckResponse)
async def check_spelling(request: SpellChekeRequest):
    try:
        if not request.text or request.text.isspace():
            return SpellCheckResponse(
                text=request.text,
                errors=[],
                ranges=[]
            )
        # Use POS tagger if requested
        checker = spell_checker_pos if request.use_pos else spell_checker
        print(f"Checking text:'{request.text}'")
        result = checker.check(request.text)
        print(f"Checking result:{result}")

        # Format response for React-Quill
        ranges = []
        for error in result["errors"]:
            if "index" not in error:
                print(f"Warning: Missing index for error: {error}")
                continue

            ranges.append({
                "index": error["index"][0],
                "length": error["index"][1] - error["index"][0],
                "word": error["word"],
                "suggestions": error["suggestions"]
            })

        return SpellCheckResponse(
            text=request.text,
            errors=result["errors"],
            ranges=ranges
        )
    except Exception as e:
        print(f"Error in checking spelling: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/replace-word", response_model=ReplaceWordResponse)
async def replace_word(request: ReplaceWordRequest):
    try:
        # Replace word at index with the selected suggestion
        new_text = request.text[:request.index] + request.replacement + request.text[request.index + len(request.text[request.index:].split()[0]):]
        return ReplaceWordResponse(text=new_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check")
async def spellcheck(text: str = Query(..., title="Text to Spellcheck", description="Enter the text you want to spellcheck")):
    try:
        result = spell_checker.check(text)
        return {"success": True, "result": result}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/v1/check")
async def spellchecker(text: str = Query(..., title="Text to Spellcheck", description="Enter the text you want to spellcheck")):
    try:
        result = spell_checker_pos.check(text)
        return {"success": True, "result": result}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)