#!/usr/bin/python2.7
from argparse import ArgumentParser
from datetime import datetime, timedelta
from itertools import cycle
from random import randrange, seed
            

class Player(object):
    def __init__(self):
        self.score = 0
        
    ## Prompts the player for whether to continue rolling.
    def should_continue(self, turn_score, total_score):
        print "Your turn total is", turn_score
        print "Your total score is", total_score
        response = raw_input("Enter 'r' to continue rolling or 'h' to hold: ")
        if response not in ["r", "h"]:
            print "Invalid response."
            return should_continue()
        else:
            return response == "r"
    
class ComputerPlayer(Player):
    def __init__(self):
        super(ComputerPlayer, self).__init__()
        
    def should_continue(self, turn_score, total_score):
        return turn_score < min(25, 100 - total_score)
        
class PlayerFactory(object):
    choices = {"human": Player, "computer": ComputerPlayer}

    @classmethod
    def get_player(cls, type):
        if type in cls.choices:
            return cls.choices[type]()
        else:
            raise ValueError("`type` was not valid.")
        
    @classmethod    
    def get_choices(cls):
        return cls.choices.keys()
            


class Die(object):
    def __init__(self, num_sides):
        self.num_sides = num_sides
        
    def roll(self):
        result = randrange(1, self.num_sides + 1)
        print "You rolled a", result
        return result
        
class Game(object):
    def __init__(self, player_types, num_sides=6):
        self.players = [PlayerFactory.get_player(type) for type in player_types]
        self.die = Die(num_sides)
        self.iterator = cycle(enumerate(self.players))
        
    def play_turn(self):
        index, player = next(self.iterator)
        print "Is is now the turn for player", index
        turn_score = 0
        dice_roll = self.die.roll();
        while dice_roll != 1:
            turn_score += dice_roll
            if not player.should_continue(turn_score, player.score):
                break
            dice_roll = self.die.roll()
        if dice_roll != 1:
            player.score += turn_score
        if player.score >= 100:
            print "The winner was player", index
            return True
        print "Player", index, "ended their turn with a score of", player.score
        return False

class GameProxy(object):
    def __init__(self, player_types, is_timed=False, num_sides=6):
        self.game = Game(player_types, num_sides)
        self.end = datetime.now() + timedelta(minutes=1)

    def play_game(self):
        while datetime.now() < self.end:
            if self.game.play_turn():
                return
        print "Game time limit exceeded."

if __name__ == "__main__":
    # Manually set the seed to have consistent games.
    seed(0)

    # Parse the arguments.
    choices = PlayerFactory.get_choices()
    parser = ArgumentParser()
    parser.add_argument("--player1", choices=choices, required=True)
    parser.add_argument("--player2", choices=choices, required=True)
    parser.add_argument("--timed", action="store_false")
    args = parser.parse_args()
    
    # Play the games via the proxy.
    GameProxy([args.player1, args.player2], args.timed).play_game()
