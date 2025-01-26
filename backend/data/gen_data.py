import random
from enum import Enum

class HoheBetType(Enum):
    SIMPLE = 1
    COMPOUND = 2

class Hohe:
    regular_compound_bets = [tuple(range(0x1208, 0x1210)),
                     tuple(range(0x1210, 0x1218)), 
                     tuple(range(0x1218, 0x1220)), 
                     tuple(range(0x1220, 0x1228)), 
                     tuple(range(0x1228, 0x1230)), 
                     tuple(range(0x1230, 0x1238)), 
                     tuple(range(0x1238, 0x1240)), 
                     tuple(range(0x1260, 0x1268)),
                     tuple(range(0x1268, 0x1270)),
                     tuple(range(0x1270, 0x1278)),
                     tuple(range(0x1278, 0x1280)),
                     tuple(range(0x1290, 0x1298)),
                     tuple(range(0x1298, 0x12a0)),
                     tuple(range(0x12d8, 0x12e0)),
                     tuple(range(0x12e0, 0x12e8)),
                     tuple(range(0x12f0, 0x12f8)),
                     tuple(range(0x1300, 0x1308)),
                     tuple(range(0x1320, 0x1328)),
                     tuple(range(0x1328, 0x1330)),
                     tuple(range(0x1330, 0x1338)),
                     tuple(range(0x1338, 0x1340)),
                     tuple(range(0x1348, 0x1350)),
                     tuple(range(0x1350, 0x1358))]
    irregular_compound_bets = [tuple(list(range(0x1240,0x1247))+[0x124b]),
                      tuple(list(range(0x1280,0x1287))+[0x128b]),
                      tuple(list(range(0x12a8,0x12af))+[0x12b3]),
                      tuple(list(range(0x12b8,0x12bf))+[0x12c3]),
                      tuple(list(range(0x1308,0x130f))+[0x1313]),
                      tuple(range(0x12a0,0x12a8))]
    simple_bets = [tuple(range(0x1200, 0x1207)),
                     tuple(range(0x12c8, 0x12cf)), 
                     tuple(range(0x12d0, 0x12d7)),
                     tuple(range(0x12e8, 0x12ef)),
                     tuple(range(0x1340, 0x1347))]
    compound_bets = irregular_compound_bets + regular_compound_bets
    categories = [simple_bets, compound_bets]
    bet_category = {}
    def populate_categories():
        for bet in Hohe.simple_bets:
            Hohe.bet_category[bet[0]] = (HoheBetType.SIMPLE, bet)
        for bet in Hohe.compound_bets:
            Hohe.bet_category[bet[0]] = (HoheBetType.COMPOUND, bet)
    def __init__(self):
        if len(Hohe.bet_category) == 0:
            Hohe.populate_categories()
    def get_rand_from_hohe_bet(self, char):
        hohe_bet = ord(self.geez_bet(char))
        if hohe_bet not in Hohe.bet_category:
            # print(f"problematic {hohe_bet} {chr(hohe_bet)}")
            return chr(hohe_bet)
        if Hohe.bet_category[hohe_bet][0] == HoheBetType.SIMPLE:
            return chr(random.choice(Hohe.bet_category[hohe_bet][1]))
        if Hohe.bet_category[hohe_bet][0] == HoheBetType.COMPOUND:
            return chr(random.choices(Hohe.bet_category[hohe_bet][1], weights=[0.14]*7+[0.02], k=1)[0])
    
    def geez_bet(self, char):
        code_point = ord(char)
        if code_point in [*list(range(0x1240, 0x1260)), *list(range(0x1280, 0x1290))]:
            return chr(code_point - code_point%16)
        if code_point in [*list(range(0x12b0, 0x12b8)), *list(range(0x12c0, 0x12c8)), *list(range(0x1310, 0x1318))]:
            return chr((code_point - code_point%8)-8)
        if code_point in range(0x1200, 0x1358):
            return chr(code_point - code_point%8)
        return char
    
    def get_rand_hohe_bet(self, char, percentage_self_hohe=0.8):
        hohe_bet = ord(self.geez_bet(char))
        picked_bet = random.choice(list(Hohe.bet_category.keys()))
        return chr(random.choices([hohe_bet, picked_bet], weights=[percentage_self_hohe, 1-percentage_self_hohe], k=1)[0])

class WordDistort:
    def __init__(self):
        self.hohe = Hohe()
    def distort(self, word, num=None):
        new_word = list(word)
        indices = [i+1 for i in range(len(word))]
        weights=[2**(-i) for i in indices]
        indices_to_change = random.sample(range(len(word)), k=random.choices(indices,weights=weights)[0])
        for i in indices_to_change:
            # hohe_bet = ord(self.hohe.geez_bet(word[i]))
            # if hohe_bet not in Hohe.bet_category:
            #     print(f"problematic {num=} {hohe_bet} {chr(hohe_bet)}")
            new_word[i] = self.hohe.get_rand_from_hohe_bet(self.hohe.get_rand_hohe_bet(word[i]))
        return "".join(new_word)


def combine(destination_file, correctly_spelled, wrongly_spelled):
    """Function to combine a file with correctly spelled words and 
    a file with incorrectly spelled words and put the combination in another file."""
    
    with open(destination_file, 'w', encoding='utf-8') as dest_file:
        with open(correctly_spelled, 'r', encoding='utf-8') as correct_file:
            with open(wrongly_spelled, 'r', encoding='utf-8') as wrong_file:
                files = [correct_file, wrong_file]
                while files:
                    file = random.choice(files)
                    line = file.readline()
                    if not line:
                        files.remove(file)
                        continue
                    line = line.strip('\n')
                    dest_file.write(line+'\n')

def generate_wrongly_spelled_words(*, dictionary, new_file):
    """ Function to generate words with incorrect spelling."""

    word_distort = WordDistort()
    wrongly_spelled_words = []
    with open(dictionary, 'r', encoding='utf-8') as src_file:
        with open(new_file, "w", encoding="utf-8") as dest_file:
            num = 0
            while text:=src_file.readline().strip('\n'):
                num += 1
                wrongly_spelled_word = word_distort.distort(text, num)
                dest_file.write(wrongly_spelled_word+"\n")


# generate_wrongly_spelled_words(dictionary="amharic_dictionary.txt", new_file="amharic_incorrect_spelling.txt")

combine("amharic_correct_and_incorrect_data.txt", "amharic_dictionary.txt", "amharic_incorrect_spelling.txt")
