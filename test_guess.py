#!/usr/bin/python
import unittest
from guess import NumberGuess

class GuessTest(unittest.TestCase):
    def test_correct_first_try(self):
        ng = NumberGuess(min=1, max=1, answer=1)
        self.assertTrue(ng.guess(1))
        self.assertTrue(ng.answered)
        self.assertEquals(ng.tries, 1)

    def test_correct_second_try(self):
        ng = NumberGuess(min=1, max=1, answer=1)
        self.assertFalse(ng.guess(10))
        self.assertFalse(ng.answered)
        self.assertTrue(ng.guess(1))
        self.assertTrue(ng.answered)
        self.assertEquals(ng.tries, 2)

    def test_guess(self):
        guesses = 100
        ng = NumberGuess(min=1, max=1, answer=guesses+1)
        for x in range(guesses):
            self.assertFalse(ng.guess(x))
            self.assertEquals(ng.tries, x+2)

    def test_hint(self):
        answer = 3
        ng = NumberGuess(min=1, max=1, answer=answer)
        self.assertEquals(ng.hint(answer-1), NumberGuess.HINT_HIGHER)
        self.assertEquals(ng.hint(answer+1), NumberGuess.HINT_LOWER)
        self.assertEquals(ng.hint(answer), NumberGuess.HINT_CORRECT)

    def test_generate_answer(self):
        ng = NumberGuess(min=1, max=2)
        self.assertIn(ng.answer, [1, 2])
        
if __name__ == '__main__':
    unittest.main()
