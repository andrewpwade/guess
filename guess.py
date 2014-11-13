#!/usr/bin/env python
import anydbm
import dbm
import os
import os
import random
import sys

SCORE_FILE = 'scores' # created witb '.db' suffix

class NumberGuess(object):
    HINT_HIGHER = 'higher'
    HINT_LOWER = 'lower'
    HINT_CORRECT = 'correct'

    def __init__(self, min, max, answer=None):
        assert max >= min
        self.min = min
        self.max = max
        if answer is None:
            self.answer = random.randint(min, max)
        else:
            self.answer = answer
        self.tries = 1
        self.answered = False
        
    def guess(self, n):
        if int(n) == self.answer:
            self.answered = True
            return True
        else:
            self.tries += 1
            return False

    def hint(self, n):
        n = int(n)
        if n > self.answer:
            return self.HINT_LOWER
        elif n < self.answer:
            return self.HINT_HIGHER
        elif n == self.answer:
            return self.HINT_CORRECT

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

def fatal(msg):
    sys.stderr.write('FATAL: {}\n'.format(msg))
    sys.stderr.flush()
    os._exit(1)

def error(msg):
    print('ERROR: {}'.format(msg))
    sys.stdout.flush()

def get_scores():
    out = []
    db = None
    try:
        db = anydbm.open(SCORE_FILE, 'c')
        out = [[name, int(db[name])] for name in db.keys()]
    except (anydbm.error, dbm.error) as err:
        fatal("Failed to open/create database: {}".format(err))
    finally:
        if db:
            db.close()
        return out
    
def print_scoreboard(scores):
    # FIXME: sort
    print('----------')
    for name, score in scores:
        print('{0:>10}{1:>10}'.format(name, score))
    print('----------')

def save_score(name, score):
    name = name.lower()
    score = str(score)
    if not name:
        raise ValueError('name can not be empty')
    if not score:
        raise ValueError('score can not be empty')
    if score < 1:
        raise ValueError('score can not be < 1')

    db = anydbm.open(SCORE_FILE, 'c')
    # only save higher or first scores
    if (name in db and int(score) < int(db[name])) or name not in db:
        db[name] = score
    db.close()

def main_loop(game):
    """
    Play the guessing game. Loops until the correct answer is given.

    Returns the number of tries taken.
    """
    print('\n** Answer is between {} and {} **\n'.format(game.min, game.max))
    while True:
        guess = raw_input('Enter guess #{}: '.format(game.tries))
        try:
            guess = int(guess)
        except ValueError:
            error('Invalid input. Try again')
            continue
        if game.guess(guess):
            print('\nCorrect! Score: {}.'.format(game.tries))
            break
        else:
            print('{}...'.format(game.hint(guess).capitalize()))

def record_win(score):
    name = raw_input('\nWhat is your name?: ')
    if name:
        save_score(name, score)
    else:
        error('** No name provided, can not save score!')
    
def main():
    if len(sys.argv) < 3:
        fatal("two arguments required")
    _min = int(sys.argv[1])
    _max = int(sys.argv[2])
    if _max <= _min:
        fatal("max must be greater than min")
    game = NumberGuess(_min, _max)
    try:
        scores = get_scores()
        if scores:
            print_scoreboard(scores)
        fatal("finished")
        main_loop(game)
        if game.answered:
            record_win(game.tries)
        print_scoreboard(get_scores())            
    except (KeyboardInterrupt, EOFError):
        if not game.answered:
            print('\n****** Answer was: {}'.format(game.answer))
        print('\nExiting.')

if __name__ == '__main__':
    main()
