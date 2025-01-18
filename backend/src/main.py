from fastapi import FastAPI, HTTPException, Query
import time
import os
from pathlib import Path
from spell_checker import SpellChecker
from spell_checker_pos import SpellCheckerWithPOS
from dictionary import Dictionary
from ngram import NgramModel

current_dir = Path(__file__).parent
dictionary_path = os.path.join(current_dir.parent, "data", "amharic_dictionary_v1.txt")
bigram_model_path = os.path.join(current_dir.parent, "models", "bigram_model.pkl")
trigram_model_path = os.path.join(current_dir.parent, "models", "trigram_model.pkl")
pos = os.path.join(current_dir.parent, "models", "am_pos_model.pt")
print("this is the path to the dictionary: ", dictionary_path)
print("this is the path to the bigram model: ", bigram_model_path)
print("this is the path to the trigram model: ", trigram_model_path)
print("this is the path to the pos model: ", pos)
# dictionary_path = "data/amharic_dictionary_v1.txt"
# bigram_model_path = "models/bigram_model.pkl"
# trigram_model_path = "models/trigram_model.pkl"
# pos = "models/am_pos_model.pt"

print("Loading models...")
t1 = time.time()
dictionary_model = Dictionary(dictionary_path)
ngram_model = NgramModel.load(bigram_model_path)

spell_checker = SpellChecker(dictionary_model, ngram_model)
spell_checker_pos = SpellCheckerWithPOS(dictionary_model, ngram_model, pos)
print(f"Models loaded successfully in {round(time.time() - t1, 3)} seconds")

app = FastAPI()

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
    uvicorn.run(app, host="127.0.0.1", port=4000)