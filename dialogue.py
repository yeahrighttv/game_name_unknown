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

        portrait = main_fight_sprite_path.get_rect()
        portrait_width = int(portrait.x)
        portrait_height = int(portrait.y)

        self.dialog_box = textboxify.TextBoxFrame(
            text=dialogue_text,
            text_width=(screen_size.x // 2),
            lines=2,
            pos=((screen_size.x // 8), (screen_size // 2)),
            padding=(150, 100),
            font_color=(255, 255, 255),
            font_size=26,
            bg_color=(0, 0, 0),
            border=DEFAULT,
            alpha=255
        )

        dialog_box.set_indicator()

        dialog_box.set_portrait(f"imgs/{main_fight_sprite_path}", (portrait_width, portrait_height))

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
        }
