class StatsTracker:
    def __init__(self):
        self.contacts = 0
        self.fouls = 0
        self.foul_tips = 0
        self.swings = 0
        self.whiffs = 0
        self.balls_hit_into_play = 0
        self.total_pitches = 0
        self.called_strikes = 0
        self.strikeout_dict = {"swinging": 0, "called": 0, "foul tip": 0}
        self.count_dict = {'0-0': 0, '0-1': 0, '1-1': 0, '1-2': 0, '1-0': 0, '2-2': 0, '0-2': 0, '2-1': 0, '3-2': 0, '2-0': 0, '3-1': 0, '3-0': 0}

        self.pitches = {"fastball": 0, "breaking": 0, "offspeed": 0}
        self.zones = {"heart": 0, "shadow": 0, "chase": 0, "waste": 0}

        self.qoc = {x: 0 for x in range(1, 7)}
        self.bb_type = {"fly_ball": 0, "popup": 0, "ground_ball": 0, "line_drive": 0}
        self.hit_loc = {x: 0 for x in range(1, 10)}
        self.hit_loc[None] = 0

        self.pull = 0
        self.center = 0
        self.oppo = 0

        self.extra_innings = 0

        self.plate_appearances = 0
        self.total_innings = 0
        self.total_runs = 0
        self.hits = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.home_runs = 0
        self.runs_batted_in = 0
        self.stolen_base_opps = 0
        self.stolen_bases = 0
        self.caught_stealings = 0
        self.walks = 0
        self.strikeouts = 0
        self.sacrifice_flies = 0
        self.hit_by_pitches = 0
        self.wild_pitches = 0
        self.passed_balls = 0
        self.grounded_into_double_plays_opps = 0
        self.grounded_into_double_plays = 0
        self.total_on_base = 0
        self.left_on_base = 0

        # retard


        # fielding
        self.putouts = 0
        self.assists = 0
        self.errors = 0
        self.reached_on_error = 0
        self.fielders_choice_everybody_safe = 0

        # sit. hitting stats
        self.sac_bunt_atts = 0
        self.sac_bunts = 0
        self.productive_outs_opps = 0
        self.productive_outs = 0
        self.third_sub_two_outs = 0
        self.third_sub_two_outs_score = 0
        self.second_no_outs = 0
        self.second_no_outs_advance = 0
        self.total_baserunners = 0

        # baserunning stats
        self.out_on_first = 0
        self.out_on_second = 0
        self.out_on_third = 0
        self.out_on_home = 0
        self.first_single_opps = 0
        self.first_single_scores = 0
        self.first_double_opps = 0
        self.first_double_scores = 0
        self.second_single_opps = 0
        self.second_single_scores = 0

        self.random_counter = 0
        self.random_counter_2 = 0
        self.random_counter_3 = 0

    @property
    def at_bats(self):
        return self.plate_appearances - self.walks - self.sacrifice_flies - self.hit_by_pitches - self.sac_bunts

    @property
    def babip(self):
        return (self.hits - self.home_runs)/(self.at_bats - self.home_runs - self.strikeouts + self.sacrifice_flies)

    @property
    def batting_average(self):
        return round(self.hits / self.at_bats, 3) if self.at_bats > 0 else 0.0

    @property
    def batting_average_str(self):
        return f"{self.batting_average:.3f}"

    @property
    def on_base_percentage(self):
        return round((self.hits + self.walks + self.hit_by_pitches) / self.plate_appearances, 3) if self.plate_appearances > 0 else 0.0

    @property
    def on_base_percentage_str(self):
        return f"{self.on_base_percentage:.3f}"

    @property
    def slugging_percentage(self):
        return round((self.singles + self.doubles * 2 + self.triples * 3 + self.home_runs * 4)/self.at_bats, 3) if self.plate_appearances > 0 else 0.0

    def stat_to_str(self, stat):
        return f"{stat:.3f}"

    def results(self):
        print(f"Total Pitches: {self.total_pitches}")
        print(f"Swings (%): {self.swings} ({round(self.swings/self.total_pitches, 3)})")
        print(f"Contacts (%): {self.contacts} ({round(self.contacts/self.swings, 3)})") # around 76.8%
        print(f"Whiffs (%): {self.whiffs} {round(self.whiffs/self.swings, 3)}") # around 23.2%
        print(f"SwStr%: {round(self.whiffs / self.total_pitches, 4)*100}") # around 11
        print(f"Fouls (%): {self.fouls} ({round(self.fouls/self.total_pitches, 3)})") # 18 percentish
        print(f"Foul Tips (%): {self.foul_tips} ({round(self.foul_tips/self.total_pitches,3)})")
        print(f"BABIP: {self.stat_to_str(self.babip)} {self.hits/self.balls_hit_into_play}")
        print(f"ISO: {self.stat_to_str(self.slugging_percentage-self.batting_average)}")
        print(f"Hit Into Play%: {round(self.balls_hit_into_play/self.total_pitches, 3)*100}") # 17.5
        print(f"Called Strike%: {round(self.called_strikes/self.total_pitches,3)*100}") # 16.2
        print(self.pitches) # {'fastball': 387287, 'breaking': 211627, 'offspeed': 92505}
        print(self.zones) # {'heart': 166367, 'chase': 165373, 'shadow strike': 151359, 'shadow ball': 133594, 'waste': 74726}
        print(self.qoc) # {1.0: 5394, 2.0: 37556, 3.0: 31670, 4.0: 29450, 5.0: 7609, 6.0: 9506}
        print(self.hit_loc) # {1.0: 4341, 2.0: 41742, 3.0: 9041, 4.0: 13831, 5.0: 12984, 6.0: 14983, 7.0: 18758, 8.0: 21339, 9.0: 19416}
        print()
        print(f"2B%: {round(self.doubles/self.plate_appearances, 3)*100}")
        print(f"HR%: {round(self.home_runs/self.plate_appearances, 4)*100}")
        print(f"K%: {round(self.strikeouts / self.plate_appearances, 3)*100}")
        print(f"BB%: {round(self.walks / self.plate_appearances, 3)*100}")
        print(self.strikeout_dict)
        print(self.count_dict)
        # {'0-0': 178231, '0-1': 90947, '1-1': 69936, '1-2': 68641, '1-0': 66450, '2-2': 58085, '0-2': 47749, '2-1': 35582, '3-2': 35073, '2-0': 22028, '3-1': 14595, '3-0': 6687, '4-2': 1}
        print()
        print(f"LD%: {round(self.bb_type['line_drive'] / self.balls_hit_into_play, 3) * 100}")
        print(f"GB%: {round(self.bb_type['ground_ball'] / self.balls_hit_into_play, 3) * 100}")
        print(f"FB%: {round(self.bb_type['fly_ball'] / self.balls_hit_into_play, 3) * 100}")
        print()
        print(f"RS%: {round((self.total_runs-self.home_runs)/(self.hits-self.home_runs+self.walks+self.hit_by_pitches), 3)*100}")
        print(f"XBT%: {round((self.first_single_scores+self.first_double_scores+self.second_single_scores)/(self.first_single_opps+self.first_double_opps+self.second_single_opps), 3)*100}")
        print()
        print(f"Extra Inning Games: {self.extra_innings}")
        print(f"IP: {self.total_innings}")
        print(f"PA: {self.plate_appearances}")
        print(f"AB: {self.at_bats}")
        print(f"R: {self.total_runs}")
        print(f"H: {self.hits}")
        print(f"2B: {self.doubles}")
        print(f"3B: {self.triples}")
        print(f"HR: {self.home_runs}")
        print(f"RBI: {self.runs_batted_in}")
        print(f"SBO: {self.stolen_base_opps}")
        print(f"SB: {self.stolen_bases}")
        print(f"CS: {self.caught_stealings}")
        print(f"SB%: {round(self.stolen_bases/(self.stolen_bases+self.caught_stealings), 3)*100}")
        print(f"BB: {self.walks}")
        print(f"SO: {self.strikeouts}")
        print(f"SF: {self.sacrifice_flies}")
        print(f"HBP: {self.hit_by_pitches}")
        print(f"GIDP Opp: {self.grounded_into_double_plays_opps}")
        print(f"GIDP: {self.grounded_into_double_plays}")
        print(f"GIDP%: {round(self.grounded_into_double_plays/self.grounded_into_double_plays_opps, 3)*100}")
        print(f"WP: {self.wild_pitches}")
        print(f"PB: {self.passed_balls}")
        print(f"TOB: {self.total_on_base}")
        print(f"LOB: {self.left_on_base}")
        print(f"LOB%: {round((self.hits+self.walks+self.hit_by_pitches-self.total_runs)/(self.hits+self.walks+self.hit_by_pitches-(1.4*self.home_runs)), 3)*100}")
        print()
        print(f"PO: {self.putouts}")
        print(f"A: {self.assists}")
        print(f"E: {self.errors}")
        print(f"ROE: {self.reached_on_error}")
        print(f"FLD%: {round((self.putouts + self.assists) / (self.putouts + self.assists + self.errors), 3)}")
        print(f"Fielder's Choice (everyone safe): {self.fielders_choice_everybody_safe}")
        print()
        print(f"BA: {self.batting_average_str}")
        print(f"OBP: {self.on_base_percentage_str}")
        print(f"SLG: {self.stat_to_str(self.slugging_percentage)}")
        print()
        print(f"WHIP: {round((self.walks+self.hits)/(self.total_innings), 2)}")
        print(f"H/9: {round((9 * self.hits) / (self.total_innings ), 1)}")
        print(f"HR/9: {round((9 * self.home_runs) / (self.total_innings ), 1)}")
        print(f"BB/9: {round((9 * self.walks) / (self.total_innings), 1)}")
        print(f"K/9: {round((9 * self.strikeouts) / (self.total_innings), 1)}")
        print(f"SO/W: {round((self.strikeouts) / (self.walks), 2)}")
        print()
        print(f"SH Att: {self.sac_bunt_atts}")
        print(f"SH: {self.sac_bunts}")
        print(f"SH %: {round(self.sac_bunts/self.sac_bunt_atts, 3)*100}")
        print(f"Prd Out Opps: {self.productive_outs_opps}")
        print(f"Prd Out: {self.productive_outs}")
        print(f"<2, 3B: {self.third_sub_two_outs}")
        print(f"0, 2B: {self.second_no_outs}")
        print(f"BR: {self.total_baserunners}")
        print()
        print(f"OOB1: {self.out_on_first}")
        print(f"OOB2: {self.out_on_second}")
        print(f"OOB3: {self.out_on_third}")
        print(f"OOBHm: {self.out_on_home}")
        print(f"1stS: {self.first_single_opps}")
        print(f"1stS2: {self.first_single_opps-self.first_single_scores}")
        print(f"1stS3: {self.first_single_scores}")
        print(f"1stD: {self.first_double_opps}")
        print(f"1stD3: {self.first_double_opps-self.first_double_scores}")
        print(f"1stDH: {self.first_double_scores}")
        print(f"2ndS: {self.second_single_opps}")
        print(f"2ndSH: {self.second_single_scores}")
        print()
        print(f"random counter (debugging): {self.random_counter}")
        print(f"random counter 2 (debugging): {self.random_counter_2}")
        print(f"random counter 3 (debugging): {self.random_counter_3}")

class GameState:
    def __init__(self):
        self.inning = 1
        self.top = True
        self.runners = [False, False, False]  # 1st 2nd 3rd
        self.runs = {"top": 0, "bottom": 0}
        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.at_bat = False
        self.handedness = None

    def are_runners(self):
        return any(runner for runner in self.runners)

    def say_runners(self):
        s = []
        for i, runner in enumerate(self.runners):
            if runner:
                s.append(["1st", "2nd", "3rd"][i])

        if not s:
            return "bases empty"
        else:
            return "runners on " + ", ".join(s)
