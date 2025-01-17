from fastapi import FastAPI, HTTPException, Query
import time

from backend.src.spell_checker import SpellChecker
from backend.src.spell_checker_pos import SpellCheckerWithPOS
from backend.src.dictionary import Dictionary
from backend.src.ngram import NgramModel

dictionary_path = "data/amharic_dictionary_v1.txt"
bigram_model_path = "models/bigram_model.pkl"
trigram_model_path = "models/trigram_model.pkl"
pos = "models/am_pos_model.pt"

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