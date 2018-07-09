from .exceptions import *
import random

class GuessAttempt(object):

    def is_hit(self):
        return True if self.hit else False

    def is_miss(self):
        return True if self.miss else False
    
    def __init__(self, char, miss=None, hit=None):
        self.char = char
        self.miss = miss
        self.hit = hit
        
        if(self.miss and self.hit):
            raise InvalidGuessAttempt('your guess cannot both miss and hit')


class GuessWord(object):
        
    def perform_attempt(self, char):
        if len(char) != 1:
            raise InvalidGuessedLetterException('guessed letter needs to be a single character')
        else:
            masked_list = list(self.masked)
        
        char = char.lower()
        
        if char in self.answer.lower():
            for index, eachchar in enumerate(self.answer.lower()):
                if eachchar == char:
                    masked_list[index] = eachchar
            self.masked = ''.join(masked_list)
            attempt = GuessAttempt(char, hit=True)
        else:
            attempt = GuessAttempt(char, miss=True)
        
        return attempt

    def __init__(self, word_to_guess):
        self.answer = word_to_guess
        self.masked = len(self.answer) * '*'
        
        if not self.answer:
            raise InvalidWordException('word is empty')


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException('list is empty')
        else:
            return random.choice(list_of_words)
    
    def guess(self, char):
        if self.is_finished():
            raise GameFinishedException('Game finished!')
        
        if char.lower() in self.previous_guesses:
            raise InvalidGuessedLetterException('this letter was already used')
        else:
            self.previous_guesses.append(char.lower())

        attempt = self.word.perform_attempt(char)
        
        if attempt.is_miss():
            self.remaining_misses -= 1

        if self.is_lost():
            raise GameLostException('You lost.')
        if self.is_won():
            raise GameWonException('You won!!')
        
        return attempt
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
    
    def is_lost(self):
        return self.remaining_misses < 1
    
    def is_won(self):
        return self.word.masked == self.word.answer

    def __init__(self, list_of_words=None, number_of_guesses=5):
        if list_of_words:
            selected_word = self.select_random_word(list_of_words)
        else:
            selected_word = self.select_random_word(self.WORD_LIST)

        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(selected_word)
