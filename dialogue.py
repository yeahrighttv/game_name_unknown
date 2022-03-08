import textboxify

from game_state import GameState
from program_states import AbstractState
from sprite import NPC

vec = pygame.math.Vector2


class Dialogue(AbstractState):
    def __init__(self, screen, game, dialogue_text, main_fight_sprite_path):
        super().__init__(screen, game)

        self.dialogue_text = dialogue_text

        screen_size = self.og_screen_size * self.screen_scaling_factor
