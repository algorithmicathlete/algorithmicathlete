import time


class Umpire:
    def __init__(self, *, display_messages=False, game_state):
        self.display_messages = display_messages
        self.game = game_state

    def call_pitch(self, zone):
        if zone in ["heart", "shadow strike"]:
            self.game.strikes += 1
            if self.display_messages:
                print("Called strike!")
                time.sleep(1)
        else:
            self.game.balls += 1
            if self.display_messages:
                print(f"Ball {self.game.balls}.")
                time.sleep(1)