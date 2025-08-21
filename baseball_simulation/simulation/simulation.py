import random
import time
from batter import Batter
from pitcher import Pitcher
from stats_tracker import StatsTracker, GameState
from umpire import Umpire
from engines.game_logic_engine import GameLogicEngine


class Game:
    def __init__(self, *, display_messages=False, stats_tracker: StatsTracker):
        self.display_messages = display_messages
        self.stats = stats_tracker
        self.game = GameState()
        self.engine = GameLogicEngine(display_messages=display_messages, stats_tracker=stats_tracker, game_state=self.game)

    def new_at_bat(self):
        self.game.at_bat = True
        self.game.handedness = "L" if random.random() < 0.4 else "R"
        self.game.strikes = 0
        self.game.balls = 0

        if self.game.runners[0] and self.game.outs < 2:
            self.stats.grounded_into_double_plays_opps += 1

        if self.game.outs < 2 and self.game.runners[2]:
            self.stats.third_sub_two_outs += 1

        if self.game.outs == 0 and self.game.runners[1]:
            self.stats.second_no_outs += 1

        self.stats.total_baserunners += 3 - self.game.runners.count(False)

        self.stats.plate_appearances += 1
        if self.display_messages:
            print(f"{'Righty' if self.game.handedness == 'R' else 'Lefty'} up to bat.")
            time.sleep(2)

    def end_half_inning(self):
        self.stats.left_on_base += 3 - self.game.runners.count(False)

        self.game.outs = 0
        self.game.runners = [False, False, False]
        if (not self.game.top and self.game.inning == 9) or self.game.inning >= 10: # just bottom of 9th / soon to be top 10th or 10th or later, extra runner
            self.game.runners = [False, Batter(display_messages=False, game_state=self.game), False]
            self.stats.second_no_outs -= 1

        self.stats.total_innings += 1
        if self.game.top:
            if self.display_messages:
                print("\n")
                print(f"Bottom of inning {self.game.inning}, the score is {self.game.runs}")
                time.sleep(2)
            self.game.top = False
        else:
            if self.display_messages:
                print("\n")
                print(f"Start of inning number {self.game.inning}, score {self.game.runs}")
                time.sleep(2)
            self.game.top = True
            self.game.inning += 1

    def run(self):
        if self.display_messages:
            print("Start of the game")

        pitcher = Pitcher(display_messages=False, game_state=self.game)
        batter = Batter(display_messages=False, game_state=self.game)
        umpire = Umpire(display_messages=False, game_state=self.game)

        have_to_equalize = False
        while (self.game.inning <= 9) or (self.game.runs["top"] == self.game.runs["bottom"]) or (self.game.runs["top"] > self.game.runs["bottom"] and have_to_equalize):
            if not self.game.at_bat:
                batter = Batter(display_messages=False, game_state=self.game)  # batter factory????

                self.engine.process_steal()

                if batter.did_bunt():
                    self.engine.process_sac_bunt(batter.bunt_success(), batter)

                if self.game.outs >= 3:
                    self.end_half_inning()

                self.new_at_bat()

            self.stats.count_dict[f"{self.game.balls}-{self.game.strikes}"] += 1

            pitch, zone = pitcher.do_pitch_prep()
            self.stats.total_pitches += 1
            self.stats.pitches[pitch] += 1
            self.stats.zones["shadow" if zone in ["shadow ball", "shadow strike"] else zone] += 1

            if pitcher.hit_batter_with_pitch(zone):
                self.engine.process_hit_by_pitch(batter)
                continue

            if pitcher.did_wild_pitch(zone):
                self.engine.process_wild_pitch()
            self.engine.process_passed_ball(zone)

            if batter.did_swing(pitch, zone):
                self.stats.swings += 1
                if batter.made_contact(pitch, zone):
                    self.stats.contacts += 1
                    if batter.hit_into_play(pitch, zone):
                        self.stats.balls_hit_into_play += 1
                        self.engine.process_hit_into_play(pitch, zone, batter)
                    else:
                        self.engine.process_foul_ball(batter.is_foul_tip())
                else:
                    self.stats.whiffs += 1
                    self.engine.process_whiff()

            else:
                umpire.call_pitch(zone)

            if self.game.strikes == 3:
                self.engine.process_strikeout()
            elif self.game.balls == 4:
                self.engine.process_walk(batter)

            if self.game.outs >= 3:
                self.end_half_inning()
                if self.game.inning == 10 and self.game.top and self.game.runs["top"] == self.game.runs["bottom"]:
                    self.stats.extra_innings += 1

                if self.game.inning >= 9:
                    if not self.game.top:
                        if self.game.runs["bottom"] > self.game.runs["top"]:
                            break
                        elif self.game.runs["bottom"] < self.game.runs["top"]:
                            have_to_equalize = True
                    else:
                        if have_to_equalize and self.game.runs["top"] > self.game.runs["bottom"]:
                            break
                        have_to_equalize = False

class Simulation:
    def __init__(self, *, display_messages=False, stats_tracker: StatsTracker):
        self.display_messages = display_messages
        self.stats = stats_tracker

    def run(self):
        for i in range(2430):
            game = Game(display_messages=self.display_messages, stats_tracker=self.stats)
            game.run()


sim = Simulation(display_messages=False, stats_tracker=StatsTracker())
sim.run()
sim.stats.results()
