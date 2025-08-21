from baseball_simulation.simulation.sim_constants  import *
import random


class ContactEngine:
    @staticmethod
    def calc_quality_of_contact(pitch, zone):
        if zone in ["shadow ball", "shadow strike"]:
            zone = "shadow"

        quality_of_contact_dict = launch_speed_dict[(pitch, zone)]
        return random.choices(list(quality_of_contact_dict), weights=list(quality_of_contact_dict.values()))[0]

    @staticmethod
    def calc_batted_ball_type(quality_of_contact):
        batted_ball_dict = batted_ball_type_dict[quality_of_contact]
        return random.choices(list(batted_ball_dict), weights=list(batted_ball_dict.values()))[0]

    @staticmethod
    def calc_hit_location(quality_of_contact, bb_type, handedness):
        hit_dict = hit_location_dict[(quality_of_contact, bb_type, handedness)].copy()

        try:
            return random.choices(list(hit_dict), weights=list(hit_dict.values()))[0]
        except Exception as e:
            print(hit_dict, quality_of_contact, bb_type, handedness)
            raise e

    @staticmethod
    def calc_hit_outcome(quality_of_contact, bb_type, handedness, hit_location, runners_on):
        hit_outcome_dict = event_dict[(quality_of_contact, bb_type, handedness, hit_location)].copy()
        hit_outcome_dict["out"] *= 0.987 if runners_on else 1.012  # modeling like shifts
        return random.choices(list(hit_outcome_dict), weights=list(hit_outcome_dict.values()))[0]
