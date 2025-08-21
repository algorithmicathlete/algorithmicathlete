import random
import time
from sim_constants import *


class Pitcher:
    def __init__(self, *, display_messages=False, game_state):
        self.display_messages = display_messages
        self.game = game_state

    def choose_pitch(self):
        pitch_dict = pitch_type_dict[(self.game.balls, self.game.strikes, self.game.outs, self.game.are_runners())]
        return random.choices(list(pitch_dict), weights=list(pitch_dict.values()))[0]

    def choose_pitch_location(self, pitch):
        pitch_dict = pitch_zone_dict[(self.game.balls, self.game.strikes, self.game.outs, self.game.are_runners(), pitch)]
        return random.choices(list(pitch_dict), weights=list(pitch_dict.values()))[0]

    def do_pitch_prep(self):
        pitch = self.choose_pitch()
        zone = self.choose_pitch_location(pitch)

        if self.display_messages:
            print()
            print(f"{self.game.balls}-{self.game.strikes} count, {self.game.say_runners()}, and here's the pitch")
            time.sleep(2)

            print(f"{pitch} pitch in the {zone} zone...")
            time.sleep(2)

        return pitch, zone

    def hit_batter_with_pitch(self, zone):
        return random.random() < hbp_dict.get(zone, -1)

    def did_wild_pitch(self, zone):
        WILD_PITCH_PROBABILITY = 0.0474
        return zone == "waste" and random.random() < WILD_PITCH_PROBABILITY and self.game.are_runners()
