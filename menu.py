import pygame

import config
from game_state import GameState
from player import Inventory
from program_states import AbstractState
from sprite import DialogBox, Item

vec = pygame.math.Vector2


class Menu(AbstractState):
    def __init__(self, screen, game, player):
        super().__init__(screen, game)

        self.player = player

        screen_size = self.og_screen_size * self.screen_scaling_factor

        # Inventory box
        self.inventory_box = ChoosingBox("imgs/inventory_box.png",
                                         self.player.inventory.items.values(),
                                         screen_size=screen_size,
                                         margin=vec(30, 30),
                                         step=30,
                                         custom_pos=True,
                                         center=True)

        # Menu Box
        menu_margin = vec(25, 90)
        menu_step = 25
        self.menu_box = MenuBox("imgs/Assets/menu_empty.png",
                                [MenuItem("Items", menu_margin, menu_step), MenuItem("Exit", menu_margin, menu_step)],
                                self.player,
                                screen_size=screen_size,
                                margin=menu_margin,
                                offset=vec(self.inventory_box.bg.rect.x - 10,
                                           self.inventory_box.bg.rect.y + self.inventory_box.bg.rect.h),
                                custom_pos=True,
                                center=False,
                                step=menu_step)

        # Set the selected box
        self.selected_box = self.menu_box

        # Variables for the cursor
        self.show_items = False

        self.set_up()

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
        }

    def render(self):
        # self.screen.blit(self.menu, self.menu_rect)
        # self.screen.blit(self.cursor, self.cursor_rect)
        self.menu_box.render(self.screen)

        if self.show_items:
            self.inventory_box.render(self.screen)
            self.player.inventory.render_inventory(self.screen, vec(self.inventory_box.bg.rect.x, self.inventory_box.bg.rect.y))

        pygame.transform.scale(self.screen, self.og_screen_size * self.screen_scaling_factor)

    def update(self, dt):
        self.render()
        self.handle_events()

    def update_cursor(self, event):
        # This updates the cursor
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_box.update_index(1)
            elif event.key == pygame.K_UP:
                self.selected_box.update_index(-1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT:
                if self.selected_box == self.menu_box:
                    if self.selected_box.get_selected_item().display_name == "Items":
                        self.show_items = True
                        self.selected_box = self.inventory_box
                        self.menu_box.show_cursor = False
                        if len(self.inventory_box.options) > 0:
                            self.inventory_box.show_cursor = True

                    elif self.selected_box.get_selected_item().display_name == "Exit":
                        self.show_items = False

                        self.menu_box.reset_box()
                        self.inventory_box.reset_box()
                        self.selected_box = self.menu_box

                        self.game.change_state(GameState.RUNNING)

                elif self.selected_box == self.inventory_box:
                    pass

            elif event.key == pygame.K_LEFT:
                if self.selected_box == self.inventory_box:
                    self.show_items = False
                    self.menu_box.show_cursor = True
                    self.selected_box = self.menu_box

        elif event.type == pygame.KEYUP:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.selected_box == self.inventory_box:
                        self.show_items = False
                        self.menu_box.show_cursor = True
                        self.selected_box = self.menu_box
                    else:
                        self.game.change_state(GameState.ENDED)

                self.test_dct.get(event.key, lambda x, y: None)(self.og_screen_size, self.screen_scaling_factor)

            self.update_cursor(event)


class ChoosingBox:
    def __init__(self, bg_path, options, x=0, y=0, screen_size=vec(0, 0), margin=vec(0, 0), offset=vec(0, 0),
                 custom_pos=False, center=False, step=30):
        super().__init__()

        self.options = options

        self.step = self.calc_right_step(step)
        self.margin = margin

        self.bg = DialogBox(bg_path)
        self.bg.rect.x = x
        self.bg.rect.y = y

        if custom_pos:
            center_factor = 0.5 if center else 0
            bg_factor = 0.5 if center else 1
            self.bg.rect.x = screen_size.x * center_factor - self.bg.rect.w * bg_factor + offset.x
            self.bg.rect.y = screen_size.y * center_factor - self.bg.rect.h * bg_factor + offset.y

        self.cursor = DialogBox('imgs/Assets/cursor.png')
        self.cursor.rect.x = self.bg.rect.x + margin.x - self.step // 2 - self.cursor.rect.w // 2
        self.cursor.rect.y = self.bg.rect.y + margin.y + self.step // 2 - self.cursor.rect.h // 2
        self.cursor_pos_og = vec(self.cursor.rect.x, self.cursor.rect.y)
        self.show_cursor = len(self.options) > 0
        self.index = 0

    def reset_box(self):
        self.index = 0
        self.cursor.rect.x, self.cursor.rect.y = self.cursor_pos_og.xy

    def update_index(self, update_value):
        if len(self.options) > 0:
            self.index = (self.index + update_value) % len(self.options)
            self.cursor.rect.y = self.cursor_pos_og.y + self.index * self.step

    def get_selected_item(self):
        return self.options[self.index]

    def render(self, surface):
        self.bg.render(surface)

        if self.show_cursor:
            self.cursor.render(surface)
        for i, item in enumerate(self.options):
            item.render_item_in_box(surface, vec(self.bg.rect.x, self.bg.rect.y), i)

    def calc_right_step(self, step):
        font = pygame.font.Font("fonts/DeterminationMono.ttf", step)
        text = font.render("", False, (255, 255, 255))
        step = text.get_rect().h
        return step


class MenuBox(ChoosingBox):
    def __init__(self, bg_path, options, player, x=0, y=0, screen_size=vec(0, 0), margin=vec(0, 0), offset=vec(0, 0),
                 custom_pos=False, center=False, step=30):
        super().__init__(bg_path, options, x, y, screen_size, margin, offset, custom_pos, center, step)

        self.player = player
        self.font = pygame.font.Font("fonts/DeterminationMono.ttf", self.step // 2)

    def render(self, surface):
        self.bg.render(surface)

        player_name = self.font.render(self.player.name, False, (255, 255, 255))
        player_lvl = self.font.render(f"LVL:{self.player.lvl}", False, (255, 255, 255))
        player_hp_stats = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", False, (255, 255, 255))

        surface.blit(player_name, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2))
        surface.blit(player_lvl, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2 * 2))
        surface.blit(player_hp_stats, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2 * 3))

        if self.show_cursor:
            self.cursor.render(surface)
        for i, item in enumerate(self.options):
            item.render_item_in_box(surface, vec(self.bg.rect.x, self.bg.rect.y), i)


class MenuItem:
    def __init__(self, display_name="Unknown", margin=vec(30, 30), step=30):
        self.margin = margin
        self.step = step

        self.display_name = display_name
        self.font = pygame.font.Font("fonts/DeterminationMono.ttf", self.step)
        self.text = self.font.render(self.display_name, False, (255, 255, 255))

    def render_item_in_box(self, surface, start_at, i=0):
        surface.blit(self.text, (start_at.x + self.margin.x, start_at.y + self.margin.y + self.step * i))
