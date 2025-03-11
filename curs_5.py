class Letter:
    def __init__(self, letter: str, index: int = None):  
        self.letter = letter
        self.index = index
        self.in_word = False
        self.in_correct_place = False  # Atribut nomi o'zgartirildi
    
    def is_in_word(self) -> bool:
        return self.in_word
    
    def is_in_correct_place(self) -> bool:
        return self.in_correct_place  # Atribut nomi bilan moslashdi
    





import random

class Bot:
    def __init__(self, word_list_file):
        with open(word_list_file, "r") as file:
            self.word_list = [line.strip().upper() for line in file.readlines()]
        self.guesses = []
        self.known_positions = [None] * 5  # Track correct letters in correct positions
        self.misplaced_letters = set()  # Letters in word but wrong position
        self.excluded_letters = set()  # Letters not in word

    def make_guess(self):
        possible_words = []
        for word in self.word_list:
            if self.is_valid_guess(word):
                possible_words.append(word)
        
        if not possible_words:
            guess = random.choice(self.word_list)  # Fallback to a random word
        else:
            guess = random.choice(possible_words)
        
        self.guesses.append(guess)
        return guess

    def is_valid_guess(self, word):
        """Check if a word follows the known feedback rules."""
        for i, letter in enumerate(word):
            if self.known_positions[i] and word[i] != self.known_positions[i]:
                return False  # Word must match known letters in correct positions
            if letter in self.excluded_letters:
                return False  # Word cannot contain excluded letters
        
        # Ensure misplaced letters are in the word somewhere
        if not all(letter in word for letter in self.misplaced_letters):
            return False
        
        return True

    def record_guess_results(self, guess, results):
        for i, letter_info in enumerate(results):
            if letter_info.is_in_correct_place():
                self.known_positions[i] = guess[i]
            elif letter_info.is_in_word():
                self.misplaced_letters.add(guess[i])
            else:
                self.excluded_letters.add(guess[i])
