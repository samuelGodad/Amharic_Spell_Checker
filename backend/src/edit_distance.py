import Levenshtein

def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculate the Damerau-Levenshtein distance between two strings.
    """
    distance = Levenshtein.distance(str1, str2)
    return distance

if __name__ == '__main__':
    print(levenshtein_distance("kitten", "sitting"))
