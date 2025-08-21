import random
from sim_constants import *


class Player:
    def __init__(self, display_messages, game_state):
        self.display_messages = display_messages
        self.game = game_state

    def will_steal(self, base):
        if base == "third":
            return random.random() < 0.0212
        elif base == "second":
            return random.random() < 0.091184
        return False

class Batter(Player):
    def __init__(self, *, display_messages=False, game_state):
        super().__init__(display_messages, game_state)

    def did_swing(self, pitch, zone):
        if self.game.strikes == 2:
            count = "2 strike"
        elif self.game.balls > self.game.strikes:
            count = "ahead"
        elif self.game.balls == self.game.strikes:
            count = "even"
        else:
            count = "behind"

        if zone in ["shadow ball", "shadow strike"]:
            zone = "shadow"

        return random.random() < swing_dict[(count, pitch, zone)]

    def made_contact(self, pitch, zone):
        if zone in ["shadow ball", "shadow strike"]:
            zone = "shadow"

        if self.game.strikes == 2:
            count = "2 strike"
        elif self.game.balls > self.game.strikes:
            count = "ahead"
        elif self.game.balls == self.game.strikes:
            count = "even"
        else:
            count = "behind"

        two_strike_multiplier = 1.02 if self.game.strikes == 2 else 0.99
        return random.random() < contact_dict[(count, pitch, zone)] * two_strike_multiplier

    def hit_into_play(self, pitch, zone):
        if zone in ["shadow ball", "shadow strike"]:
            zone = "shadow"

        return random.random() < bip_dict[(pitch, zone)]

    def did_bunt(self):
        runners = tuple([bool(x) for x in self.game.runners])
        if (self.game.outs, runners) in sac_bunts_dict:
            if random.random() < sac_bunts_dict[(self.game.outs, runners)]/0.576:
                return True

        return False

    def bunt_success(self):
        return random.random() < 0.576

    def is_foul_tip(self):
        FOUL_TIP_PERCENTAGE = 0.05399587541960831
        return random.random() < FOUL_TIP_PERCENTAGE