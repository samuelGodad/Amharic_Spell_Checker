import streamlit as st
import time

from backend.src.spell_checker import SpellChecker
from backend.src.spell_checker_pos import SpellCheckerWithPOS
from backend.src.dictionary import Dictionary
from backend.src.ngram import NgramModel

def load_models():
    dictionary_path = "data/amharic_dictionary_v1.txt"
    bigram_model_path = "models/bigram_model.pkl"
    trigram_model_path = "models/trigram_model.pkl"
    pos = "models/am_pos_model.pt"

    st.write("Loading models...")
    t1 = time.time()
    dictionary_model = Dictionary(dictionary_path)
    ngram_model = NgramModel.load(bigram_model_path)

    spell_checker = SpellChecker(dictionary_model, ngram_model)
    spell_checker_pos = SpellCheckerWithPOS(dictionary_model, ngram_model, pos)
    st.write(f"Models loaded successfully in {round(time.time() - t1, 3)} seconds")

    return spell_checker, spell_checker_pos

# Load models only once and store them in session_state
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = True
    spell_checker, spell_checker_pos = load_models()
    st.session_state.spell_checker = spell_checker
    st.session_state.spell_checker_pos = spell_checker_pos
else:
    spell_checker = st.session_state.spell_checker
    spell_checker_pos = st.session_state.spell_checker_pos

def main():
    st.title("Amharic Spell Checker")

    option = st.selectbox("Select Spell Checker Type", ["Basic Spell Checker", "Advanced Spell Checker"])

    text = st.text_area("Enter the text you want to spellcheck")

    if st.button("Check Spelling"):
        if option == "Basic Spell Checker":
            result = spell_checker.check(text)
        else:
            result = spell_checker_pos.check(text)

        st.write("Spellchecking Result:")
        st.write(result)

if __name__ == "__main__":
    main()
