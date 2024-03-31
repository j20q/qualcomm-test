# Given a words.txt file containing a newline-delimited list of dictionary
# words, please implement the Anagrams class so that the get_anagrams() method
# returns all anagrams from words.txt for a given word.
#
# Bonus requirements:
#   - Optimize the code for fast retrieval
#   - Write more tests
#   - Thread safe implementation

import unittest
from typing import List, Dict
from collections import defaultdict
import threading


class Anagrams:
    def __init__(self, filename="words.txt"):
        self.lock = threading.Lock()
        self.words = self.__txt_to_list(filename)
        self.anagram_dict = self.__build_anagrams_dict()

    def get_anagrams(self, word: str) -> List[str]:
        with self.lock:
            letters = self.__compute_word_key(word)
            return self.anagram_dict[letters]

    def __compute_word_key(self, word):
        """
        Internal method for computing dictionary key of give `word`.
        E.g. word: Apple -> returns 'aelpp'.
        This is useful because every anagram has the same computed string.
        """
        return "".join(sorted(word.lower()))

    def __build_anagrams_dict(self) -> Dict[str, List[str]]:
        """
        Build dictionary of anagrams for fast retrieval: e.g. {aet: [eat, Tea, ate]}.
        """
        d = defaultdict(list)  # So I can just use d[key].append(list_elem)
        for word in self.words:
            with self.lock:
                # using `.lower()` so that words including capital letters are also considered anagrams
                letters = self.__compute_word_key(word)
                d[letters].append(word)
        return d

    def __txt_to_list(self, filename):
        """
        Convert list of strings ending in `\n` to list of strings
        """
        with open(filename, "r") as file:
            return [line.strip() for line in file]


class TestAnagrams(unittest.TestCase):

    def test_anagrams(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams("eat"), ["ate", "eat", "Tea"])
        self.assertEqual(
            anagrams.get_anagrams("plates"),
            ["palest", "pastel", "petals", "plates", "staple"],
        )

    def test_anagrams_disregard_order(self):
        anagrams = Anagrams()
        self.assertNotEqual(
            anagrams.get_anagrams("listen"),
            ["listen", "silent", "enlist", "inlets", "tinsel"],
        )
        # using `set` to make order of list irrelevant
        self.assertEqual(
            set(anagrams.get_anagrams("listen")),
            set(["listen", "silent", "enlist", "inlets", "tinsel"]),
        )

    def test_anagrams_edge_cases(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams(""), [])
        self.assertEqual(anagrams.get_anagrams("2"), [])
        self.assertEqual(anagrams.get_anagrams("("), [])


if __name__ == "__main__":
    unittest.main()
