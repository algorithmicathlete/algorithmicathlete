import random
from baseball_simulation.simulation.sim_constants import *
# from ..stats_tracker import StatsTracker, GameState
from .contact_engine import ContactEngine
import time


class GameLogicEngine:
    def __init__(self, *, display_messages=False, stats_tracker, game_state):
        self.display_messages = display_messages
        self.stats = stats_tracker
        self.game = game_state

    def advance_runners(self, bases, walk, team, error=False):
        if walk:
            bases = 1  # prevent weird stuf

        new_runners = [False, False, False]

        for i, runner in enumerate(self.game.runners):
            if walk and runner is False:
                # bases will fill up until this point cause base open, but everything after the open base will be the same
                return new_runners[:i + 1] + self.game.runners[i + 1:]

            if runner:
                if i == 1 and self.game.outs == 0:
                    self.stats.second_no_outs_advance += 1
                if (i + bases + 1) >= 4:
                    if i == 2:
                        self.stats.third_sub_two_outs_score += 1
                    self.game.runs[team] += 1
                    self.stats.total_runs += 1
                    self.stats.runs_batted_in += 1
                else:
                    if not walk and not error:
                        if bases == 1 and i == 1:  # single and man on second
                            self.stats.second_single_opps += 1

                            ADVANCE_FAILURE = 0.0111637
                            if random.random() < ADVANCE_FAILURE:
                                self.stats.out_on_home += 1
                                self.game.outs += 1

                                new_runners[1] = False
                                self.stats.first_single_scores += 1
                                new_runners[2] = runner  # move up trailing runner
                                continue

                            if self.game.outs < 3 and random.random() < runner_advance_dict["2nd single"][self.game.outs]: # runner on 1st may have been thrown out at 3rd ending the inning
                                if new_runners[1] and random.random() < 0.5: # tweak
                                    new_runners[1] = False
                                    self.stats.first_single_scores += 1
                                    new_runners[2] = runner  # move up trailing runner

                                self.stats.second_single_scores += 1
                                self.game.runs[team] += 1
                                self.stats.total_runs += 1
                                self.stats.runs_batted_in += 1
                            else:
                                new_runners[2] = runner

                        elif bases == 1 and i == 0:  # single and man on first
                            self.stats.first_single_opps += 1

                            ADVANCE_FAILURE = 0.0252546
                            if random.random() < ADVANCE_FAILURE:
                                self.stats.out_on_third += 1
                                self.game.outs += 1
                                continue

                            if random.random() < runner_advance_dict["1st single"][self.game.outs] and self.game.runners[1] is False:  # no authority if not lead runner
                                self.stats.first_single_scores += 1
                                new_runners[2] = runner
                            else:
                                new_runners[1] = runner

                        elif bases == 2 and i == 0:  # double and man on first
                            self.stats.first_double_opps += 1

                            ADVANCE_FAILURE = 0.03278
                            if random.random() < ADVANCE_FAILURE:
                                self.stats.out_on_home += 1
                                self.game.outs += 1
                                continue

                            if random.random() < runner_advance_dict["1st double"][self.game.outs]:
                                self.stats.first_double_scores += 1
                                self.game.runs[team] += 1
                                self.stats.total_runs += 1
                                self.stats.runs_batted_in += 1
                            else:
                                new_runners[2] = runner

                        else:
                            new_runners[i + bases] = runner
                    else:
                        new_runners[i + bases] = runner

        return new_runners

    def is_error(self):
        FIELDING_PERCENTAGE = 0.985
        return FIELDING_PERCENTAGE < random.random()

    def process_error(self, batter):
        self.stats.errors += 1
        self.stats.reached_on_error += 1
        self.game.runners = self.advance_runners(1, True, "top" if self.game.top else "bottom", error=True)

        self.game.runners[0] = batter
        self.stats.total_on_base += 1
        self.game.at_bat = False

    def process_sac_fly(self, quality_of_contact, batted_ball_type, hit_location, batter):
        tag_up_possible = self.game.outs <= 2 and hit_location in {7, 8, 9}
        TAG_UP_SUCCESS = 0.97

        if tag_up_possible and self.game.runners[2]:
            if (batted_ball_type, quality_of_contact) in sac_fly_dict:

                sac_fly_prob = sac_fly_dict[(batted_ball_type, quality_of_contact)]
                if random.random() < sac_fly_prob:
                    if random.random() < TAG_UP_SUCCESS:
                        self.game.runners[2] = False
                        self.game.runs["top" if self.game.top else "bottom"] += 1
                        self.stats.runs_batted_in += 1
                        self.stats.total_runs += 1
                        self.stats.third_sub_two_outs_score += 1
                        self.stats.sacrifice_flies += 1
                        self.stats.productive_outs += 1
                    else:
                        self.stats.out_on_home += 1
                        self.stats.putouts += 1
                        self.stats.assists += 1  # thrown out
                        self.game.outs += 1

        if tag_up_possible and self.game.runners[1] and not self.game.runners[2]:
            if (batted_ball_type, quality_of_contact) in sac_fly_dict:
                sac_fly_prob = sac_fly_dict[(batted_ball_type, quality_of_contact)]
                if random.random() < sac_fly_prob * [0.2, 0.4, 0.6][hit_location - 7]:  # LF, then cf then rf
                    if random.random() < TAG_UP_SUCCESS:
                        self.game.runners[1] = False
                        self.game.runners[2] = batter
                        if self.game.outs == 1:
                            self.stats.productive_outs += 1
                    else:
                        self.stats.out_on_third += 1
                        self.stats.putouts += 1
                        self.stats.assists += 1  # thrown out
                        self.game.outs += 1

    def process_field_out(self, hit_location):
        if hit_location != 3:
            self.stats.assists += 1
        if self.game.outs < 3:
            if self.game.outs == 1:
                self.stats.productive_outs += 1

            temp_runs = self.stats.total_runs
            self.advance_runners(1, True, "top" if self.game.top else "bottom")
            if self.game.outs == 2 and self.stats.total_runs > temp_runs:
                self.stats.productive_outs += 1

    def process_force_out(self):
        self.stats.total_on_base += 1
        self.stats.assists += 1
        if self.game.outs == 3:
            self.game.runners[0] = False  # don't skew LOB

    def process_double_play(self):
        self.advance_runners(1, True, "top" if self.game.top else "bottom", error=True)  # maybe dont score the runner tho if 3 outs

        self.game.runners[1] = False
        self.stats.grounded_into_double_plays += 1
        self.game.outs += 1
        self.stats.putouts += 1
        self.stats.assists += 2  # maybe 1
        if self.game.outs < 3:
            self.stats.productive_outs += 1

    def process_fielders_choice(self, batter):
        if self.game.outs == 1:
            self.stats.productive_outs += 1
        elif self.game.outs == 2 and (self.game.runners.count(False) == 0):
            self.stats.productive_outs += 1
        self.advance_runners(1, True, "top" if self.game.top else "bottom", error=True)
        self.game.runners[0] = batter
        self.stats.total_on_base += 1
        self.stats.fielders_choice_everybody_safe += 1
        self.game.outs -= 1

    def process_hit_outcome(self, quality_of_contact, batted_ball_type, hit_location, batter):
        outcome = ContactEngine.calc_hit_outcome(quality_of_contact, batted_ball_type, self.game.handedness, hit_location, self.game.are_runners())

        if outcome == "out": # should be called "chance" not "out"
            if self.is_error():
                self.process_error(batter)
                return

            self.game.outs += 1
            self.stats.putouts += 1

            if self.game.are_runners() and self.game.outs == 1: # if first out of inning, any runner advance
                self.stats.productive_outs_opps += 1
            elif self.game.runners[2] and self.game.outs == 2: # need to drive in run w/ 2nd out
                self.stats.productive_outs_opps += 1

            self.process_sac_fly(quality_of_contact, batted_ball_type, hit_location, batter)

            out_dict = ground_ball_out_dict.get((self.game.outs-1, quality_of_contact))
            if batted_ball_type == "ground_ball" and (1 <= hit_location <= 6) and out_dict:
                if self.game.runners[0]:
                    free_third = self.game.runners[2] and not self.game.runners[1]
                    event = random.choices(list(out_dict), weights=list(out_dict.values()))[0]

                    team = "top" if self.game.top else "bottom"

                    if event == "field_out":
                        self.process_field_out(hit_location)

                    elif event == "force_out":
                        self.process_force_out()

                    elif event == "grounded_into_double_play":
                        self.process_double_play()

                    elif event == "fielders_choice":
                        self.process_fielders_choice(batter)

                    if self.game.outs < 3 and free_third:
                        if random.random() < 0.85:
                            self.game.runners[2] = False
                            self.stats.total_runs += 1
                            self.stats.third_sub_two_outs_score += 1
                            self.stats.productive_outs += 1
                            self.game.runs[team] += 1

                else:
                    if hit_location != 3:
                        self.stats.assists += 1

                    if self.game.outs < 3:
                        if self.game.runners[2]:
                            if random.random() < 0.5:
                                self.game.runners[2] = False
                                self.stats.productive_outs += 1
                                self.game.runs["top" if self.game.top else "bottom"] += 1
                                self.stats.runs_batted_in += 1
                                self.stats.total_runs += 1
                                self.stats.third_sub_two_outs_score += 1
                        if self.game.runners[1] and not self.game.runners[2]:
                            if hit_location in {3, 4} and random.random() < 0.55:
                                if self.game.outs == 1:
                                    self.stats.productive_outs += 1
                                self.game.runners[1] = False
                                self.game.runners[2] = batter

        else:
            self.process_hit(outcome, batter)

        if self.display_messages:
            print(outcome.capitalize().replace("_", " ") + "!")
            time.sleep(2)

        self.game.at_bat = False

    def process_hit(self, hit_type, batter):
        error = False
        if hit_type != "home_run" and 0.96 < random.random():
            error = True
            self.stats.errors += 1

        bases = ["single", "double", "triple", "home_run"].index(hit_type)
        self.game.runners = self.advance_runners(bases + 1 + error, False, "top" if self.game.top else "bottom", error=error)
        if (bases == 2 and error) or (bases == 3):
            if bases == 3:
                self.stats.runs_batted_in += 1
            self.stats.total_runs += 1
            self.game.runs["top" if self.game.top else "bottom"] += 1
        else:
            self.game.runners[bases + error] = batter
            self.stats.total_on_base += 1

        setattr(self.stats, hit_type + "s", getattr(self.stats, hit_type + "s") + 1)  # single/double/triple/home_run+ s
        self.stats.hits += 1

    def track_direction(self, hit_location):
        if hit_location in {1, 6, 4, 8}:
            self.stats.center += 1
        elif (hit_location in {5, 7} and self.game.handedness == "R") or (hit_location in {3, 9} and self.game.handedness == "L"):
            self.stats.pull += 1
        else:
            self.stats.oppo += 1

    def process_hit_into_play(self, pitch, zone, batter):
        quality_of_contact = ContactEngine.calc_quality_of_contact(pitch, zone)
        self.stats.qoc[quality_of_contact] += 1
        batted_ball_type = ContactEngine.calc_batted_ball_type(quality_of_contact)
        self.stats.bb_type[batted_ball_type] += 1
        hit_location = ContactEngine.calc_hit_location(quality_of_contact, batted_ball_type, self.game.handedness)
        self.stats.hit_loc[hit_location] += 1

        self.track_direction(hit_location)

        if hit_location is None:
            DOUBLE_PERCENTAGE = 0.07313250914156365
            if random.random() < DOUBLE_PERCENTAGE:
                self.process_hit("double", batter)

            else:
                self.process_hit("home_run", batter)

                if self.display_messages:
                    print(f"No doubt about it! Home run!")
                    time.sleep(2)

            self.game.at_bat = False

        else:
            hit_location = int(hit_location)
            quality_map = {1: "weak", 2: "topped", 3: "undered", 4: "flared", 5: "solid contact", 6: "barreled"}
            positions = [
                None, "pitcher", "catcher", "1st base", "2nd base", "3rd base",
                "shortstop", "left field", "center field", "right field"
            ]

            if self.display_messages:
                print(f"{quality_map[quality_of_contact]} {batted_ball_type.replace('_', ' ')} hit to {positions[hit_location]}...")
                time.sleep(2)

            self.process_hit_outcome(quality_of_contact, batted_ball_type, hit_location, batter)

    def process_foul_ball(self, is_foul_tip):
        if is_foul_tip:
            self.stats.foul_tips += 1
            self.game.strikes += 1
            if self.game.strikes == 3:
                self.stats.strikeout_dict["foul tip"] += 1

        else:
            self.stats.fouls += 1
            if self.display_messages:
                print("The pitch fouled off.")
                time.sleep(1)
            self.game.strikes = min(self.game.strikes + 1, 2)

    def process_whiff(self):
        if self.display_messages:
            print("Swing and a miss!")
            time.sleep(1)
        self.game.strikes += 1
        if self.game.strikes == 3:
            self.stats.strikeout_dict["swinging"] += 1

    def process_steal(self):
        if (self.game.runners[1] and not self.game.runners[2]) or (self.game.runners[0] and not self.game.runners[1]):
            self.stats.stolen_base_opps += 1

        if self.game.runners[1] and not self.game.runners[2]:
            if self.game.runners[1].will_steal("third"):
                temp = self.game.runners[1]
                self.game.runners[1] = False
                if random.random() < 0.8:
                    self.game.runners[2] = temp
                    self.stats.stolen_bases += 1
                else:
                    self.stats.caught_stealings += 1
                    self.game.outs += 1
                    self.stats.putouts += 1
                    self.stats.assists += 1

                if self.game.runners[0]:
                    self.game.runners[0], self.game.runners[1] = False, self.game.runners[0]
                    self.stats.stolen_bases += 1

        # will steal, delay that hoe like giving a sign!

        elif self.game.runners[0] and not self.game.runners[1]:
            if self.game.runners[0].will_steal("second"):
                temp = self.game.runners[0]
                self.game.runners[0] = False
                if random.random() < 0.79:
                    self.stats.stolen_bases += 1
                    self.game.runners[1] = temp
                else:
                    self.stats.caught_stealings += 1
                    self.game.outs += 1
                    self.stats.putouts += 1
                    self.stats.assists += 1

    def lead_runner_out(self):
        if not self.game.are_runners():
            return
        lead = 0
        for i, runner in enumerate(self.game.runners):
            if runner:
                lead = i
        self.game.runners[lead] = False

    def process_sac_bunt(self, success, batter):
        self.stats.sac_bunt_atts += 1
        if success:
            self.stats.productive_outs += 1
            self.stats.sac_bunts += 1
            self.game.runners = self.advance_runners(1, False, "top" if self.game.top else "bottom", error=True)

        else:
            if [bool(x) for x in self.game.runners]  != [False, True, False]:
                self.advance_runners(1, True, "top" if self.game.top else "bottom")
                self.game.runners[0] = batter
                self.stats.total_on_base += 1
                self.lead_runner_out()

        self.game.outs += 1
        self.stats.putouts += 1
        self.stats.assists += 1
        self.game.at_bat = False

    def process_strikeout(self):
        self.stats.strikeouts += 1
        if self.display_messages:
            print("Strikeout!")
            time.sleep(1)
        self.game.outs += 1
        self.stats.putouts += 1
        self.game.at_bat = False

    def process_walk(self, batter):
        self.stats.walks += 1
        if self.display_messages:
            print("And he walked him.")
            time.sleep(1)
        self.game.runners = self.advance_runners(1, True, "top" if self.game.top else "bottom")
        self.game.runners[0] = batter
        self.stats.total_on_base += 1
        self.game.at_bat = False

    def process_hit_by_pitch(self, batter):
        self.stats.hit_by_pitches += 1
        self.game.at_bat = False
        self.game.runners = self.advance_runners(1, True, "top" if self.game.top else "bottom")
        self.game.runners[0] = batter
        self.stats.total_on_base += 1

    def process_wild_pitch(self):
        if self.game.runners.count(False) != 0:
            self.stats.wild_pitches += 1
            self.game.runners = self.advance_runners(1, self.game.runners[2], "top" if self.game.top else "bottom")

    def process_passed_ball(self, zone):
        PASSED_BALL_PROBABILITY = 0.0036
        if zone == "chase" and random.random() < PASSED_BALL_PROBABILITY and self.game.are_runners():
            if self.game.runners.count(False) != 0:
                self.stats.passed_balls += 1
                self.game.runners = self.advance_runners(1, self.game.runners[2], "top" if self.game.top else "bottom")
