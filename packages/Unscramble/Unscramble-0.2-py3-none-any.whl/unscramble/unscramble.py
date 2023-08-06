from itertools import permutations
from tqdm import tqdm
from collections import defaultdict
import os
# from tqdm import tqdm_notebook as tqdm


class Unscramble:
    """Class to create multiple dictionary words of different length
    from a given english word.
    """

    def __init__(self, word):
        """Initialize the class instance.
        Convert the word to lower case.
        """
        self.word = word.lower()

    def _load_dictionary(self):
        """Loads the dictionary from ``data/words_alpha.txt`` folder 

        Parameters
        ----------
        None


        Returns
        -------
        A list of words which contains the actual english dictionary words.

        """
        path = os.path.abspath(os.path.dirname(__file__))
        fileName = os.path.join(path, 'data/words_alpha.txt')
        dictionary = [line.rstrip("\n") for line in open(fileName)]
        
        return dictionary

    def _get_word_lengths(self, upto):
        """ Returns the word length

        Parameters
        ----------
        upto : int
            Specify minimum length of the created word

        Return
        ------
        word_lengths : list(int) 
            List of allowed word length

        """
        orig_word_len = len(self.word)
        word_lengths = list(reversed(range(orig_word_len + 1)))
        word_lengths = word_lengths[:-upto]

        return word_lengths

    def _create_permutations(self, upto=4, exact_length=None):
        """Create all possible permutations for the given word.

        Parameters
        ----------
        upto : int
            Specify minimum length of the created word
        exact_length : int
            Specify the exact length of unscrambled word to look for.

        Return
        ------
        possible_words : list(str)
            list of all possible word variations for given word

        """
        self._all_permutations = []

        # Returns a list of int which specify word lengths
        self.word_lengths = self._get_word_lengths(upto)

        if exact_length is not None:
            self.word_lengths = [exact_length]

        for length in tqdm(self.word_lengths, desc="Generating possible words"):
            possible_words = permutations(self.word, length)
            possible_words = map(lambda x: "".join(x), list(possible_words))
            possible_words = list(possible_words)
            self._all_permutations.append(possible_words)

        possible_words = [
            word for word_list in self._all_permutations for word in word_list
        ]
        possible_words = list(set(possible_words))

        return possible_words

    def _total_permutations(self, possible_words):
        """Computes the length of possible permutations

        Parameters
        ----------
        possible_words : list(str)
            List of all possible permutations

        Return
        ------
        length : int
            # of possible permutation

        """
        return len(possible_words)

    def _get_defaultdict(self, actual_words):
        """Creates a structured ``defaultdict`` (from the ``collections`` 
        pacakge) for the unscrambled list of dictionary words.

        This creates a dictionary out of a list where ``key`` specifies 
        the length of the word and ``value`` is list of words of ``key`` length.

        Parameters
        ----------
        actual_words : list(str)
            List of unscrambled dictionary words

        Returns
        -------
        dictionary_words : defultdict(list)
            Dictionary where key represent # of characters in word and
            value is the list of words.

        """
        dict_words = defaultdict(list)
        for word in actual_words:
            dict_words[len(word)].append(word)

        return dict_words

    def _print_dict(self, actual_words):
        """Print dictionary in a user friendly format

        Parameters
        ----------
        actual_words : defaultdict(list)
            Dict of unscrambled words

        Returns
        -------
        NA
            Prints the dict 

        """
        for no_of_char, word_list in sorted(actual_words.items(), reverse=True):
            print("\n---------------------------------------\n")
            print(no_of_char, " letter words: \n")
            print(word_list)

        print("\n---------------------------------------\n")

    def find_words(self, upto=4, exact_length=None):
        """Find other dictionary words out of a given word.
        
        Internally calls following methods:

            - Loads dictionary
            - Create all possible permutations 
            - Lookup in dictionary
            - Convert to dictionary
            - Prints the output

        Parameters
        ----------
        upto : int
            Specify minimum length of the created word
        exact_length : int
            Specify the exact length of unscrambled word to look for.

        Return
        ------
        unscrambled_words : defaultdict(list)
            Dict of words of different lengths

        """
        dictionary = self._load_dictionary()
        possible_words = self._create_permutations(upto, exact_length)
        actual_words = [
            word
            for word in tqdm(possible_words, desc="Dictionary Lookup")
            if word in dictionary
        ]

        actual_words = self._get_defaultdict(actual_words)
        self._print_dict(actual_words)

        return actual_words
