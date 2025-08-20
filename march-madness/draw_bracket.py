from PIL import Image, ImageDraw, ImageFont
from utils import team_seeds
import numpy as np


def bracket_creator():
    seeds = {}
    visited = set()

    for seed in range(1, 17):
        filtered = [x for x in team_seeds[seed].items() if x[0] not in visited]
        items = [x[0] for x in filtered]
        weights = np.array([x[1] for x in filtered], dtype=float)

        probs = weights / weights.sum()
        choices = list(np.random.choice(items, size=4, replace=False, p=probs))

        for choice in choices:
            visited.add(choice)

        seeds[seed] = {
            region: choices[i]
            for i, region in enumerate(["South", "West", "East", "Midwest"])
        }

    return seeds


class BracketDrawer:
    def __init__(self, regions, winner_left, winner_right, champion):
        self.im = Image.open("bracket.png")

        self.font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        self.font_path_narrow = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"

        try:
            self.font = ImageFont.truetype(self.font_path, 32)
        except OSError:
            self.font_path = input("Please input a valid font path: ")
            self.font_path_narrow = input("Please input a valid font path for small text: ")
            self.font = ImageFont.truetype(self.font_path, 32)

        self.draw = ImageDraw.Draw(self.im)
        self.regions = regions
        self.winner_left = winner_left
        self.winner_right = winner_right
        self.champion = champion

        self.bracket_teams = bracket_creator()

    def fit_text(self, draw, text):
        font_size = 32
        font = self.font

        while draw.textlength(text, font=font) > 210 and font_size > 5:
            font_size -= 1
            font = ImageFont.truetype(self.font_path if font_size > 28 else self.font_path_narrow, font_size)

        return font

    @staticmethod
    def fill_color(x):
        return "white" if type(x) == int else  (30, 144, 255)

    def get_team(self, seed, region):
        text = self.bracket_teams[int(seed)][region]
        if region in ["South", "West"]:
            return f"({seed}) {text}"
        else:
            return f"{text} ({seed})"

    def draw_region_round(self, section, teams, r, top=True, right=False):
        x = 130 if not right else 2700
        y = 30 if top else 1130

        region = ["South", "West", "East", "Midwest"]

        y_step = 60 * 2**r # round starts at 0
        for i in range(2**(4-r)):
            x_coord = x - 20 + 230 * r if not right else x - 60 - 230 * r

            font = self.fit_text(self.draw, self.get_team(teams[i], region[section]))

            self.draw.text(
                (x_coord, y_step/2 + y + y_step*i),
                self.get_team(teams[i], region[section]),
                font=font, fill=self.fill_color(teams[i])
            )

    def draw_region(self, section, teams):
        for r in range(5):
            self.draw_region_round(section, teams[r], r, top=(section % 2 == 0), right=(section >= 2))

    def draw_winner_left(self):
        seed, region = self.winner_left['seed'], self.winner_left['region']

        text = self.get_team(seed, region)
        text_width = self.draw.textlength(text, font=self.font)

        self.draw.text((1210 - text_width / 2, 1085), text, font=self.font, fill=self.fill_color(self.winner_left['seed']))

    def draw_winner_right(self):
        seed, region = self.winner_right['seed'], self.winner_right['region']

        text = self.get_team(seed, region)
        text_width = self.draw.textlength(text, font=self.font)

        self.draw.text(
            (1740 - text_width / 2, 1085), text, font=self.font,
            fill=self.fill_color(self.winner_right['seed'])
        )


    def draw_champion(self):
        seed, region = self.champion['seed'], self.champion['region']
        text = self.get_team(seed, region)
        text_width = self.draw.textlength(text, font=self.font)

        self.draw.text(
            (1475 - text_width / 2, 1340), text, font=self.font,
            fill=self.fill_color(self.champion['seed'])
        )

    def draw_final_four(self):
        self.draw_winner_left()
        self.draw_winner_right()
        self.draw_champion()

    def draw_bracket(self):
        for i in range(4):
            self.draw_region(i, self.regions[i])

        self.draw_final_four()

        return self.im
