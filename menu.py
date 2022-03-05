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

        inv_rect = pygame.image.load("imgs/Assets/inventory_box.png").get_rect()
        inv_rect.x, inv_rect.y = screen_size.x // 2 - inv_rect.w // 2, screen_size.y // 2 - inv_rect.h // 2

        margin = 10

        menu_rect = pygame.image.load("imgs/Assets/menu_empty.png").get_rect()
        menu_rect.x, menu_rect.y = inv_rect.x - menu_rect.w - margin, inv_rect.y + inv_rect.h - menu_rect.h

        info_rect = pygame.image.load("imgs/Assets/info_box.png").get_rect()
        info_rect.x, info_rect.y = inv_rect.x + inv_rect.w + margin, inv_rect.y + inv_rect.h - info_rect.h

        # Menu Box
        menu_margin = vec(25, 90)
        menu_step = 25
        self.menu_box = MenuBox("imgs/Assets/menu_empty.png",
                                [MenuItem("Items", menu_margin, menu_step), MenuItem("Exit", menu_margin, menu_step)],
                                self.player,
                                x=menu_rect.x,
                                y=menu_rect.y,
                                margin=menu_margin,
                                step=menu_step)

        # Inventory box
        self.inventory_box = InventoryBox("imgs/Assets/inventory_box.png",
                                          self.player.inventory.items.values(),
                                          self.player,
                                          x=inv_rect.x,
                                          y=inv_rect.y,
                                          margin=vec(30, 16),
                                          step=29,
                                          parent=self.menu_box)

        # Info box
        self.info_box = InfoBox("imgs/Assets/info_box.png",
                                [MenuItem("Items", menu_margin, menu_step), MenuItem("Exit", menu_margin, menu_step)],
                                self.player,
                                x=info_rect.x,
                                y=info_rect.y,
                                margin=menu_margin,
                                step=menu_step,
                                parent=self.inventory_box)

        # Set the selected box
        self.selected_box = self.menu_box

        self.set_up()

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
        }

    def render(self):
        self.menu_box.render(self.screen)
        self.inventory_box.render(self.screen)
        self.info_box.render(self.screen)

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
                        self.selected_box = self.inventory_box
                        self.selected_box.show = True
                        self.selected_box.parent.show_cursor = False
                        if len(self.selected_box.options) > 0:
                            self.selected_box.show_cursor = True

                    elif self.selected_box.get_selected_item().display_name == "Exit":
                        self.menu_box.reset_box()
                        self.inventory_box.reset_box()
                        self.info_box.reset_box()
                        self.selected_box = self.menu_box

                        self.game.change_state(GameState.RUNNING)

                elif self.selected_box == self.inventory_box:
                    if len(self.selected_box.options) > 0:
                        self.selected_box = self.info_box
                        self.selected_box.show_cursor = True
                        self.selected_box.show = True

            elif event.key == pygame.K_LEFT:
                if self.selected_box != self.menu_box:
                    self.selected_box.show_cursor = False
                    self.selected_box.parent.show_cursor = True
                    self.game.game_states.get(GameState.RUNNING).render(None)
                    self.selected_box.reset_box()
                    self.selected_box = self.selected_box.parent
                    self.render()

        elif event.type == pygame.KEYUP:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # if self.selected_box == self.inventory_box:
                    #     self.show_items = False
                    #     self.menu_box.show_cursor = True
                    #     self.selected_box = self.menu_box
                    # else:
                    #     self.game.change_state(GameState.ENDED)

                    self.game.change_state(GameState.ENDED)

                self.test_dct.get(event.key, lambda x, y: None)(self.og_screen_size, self.screen_scaling_factor)

            self.update_cursor(event)


class ChoosingBox:
    def __init__(self, bg_path, options, x=0.0, y=0.0, margin=vec(0, 0), step=30):
        super().__init__()

        self.options = options

        self.step = self.calc_right_step(step)
        self.margin = margin

        self.bg = DialogBox(bg_path)
        self.bg.rect.x = x
        self.bg.rect.y = y

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
    def __init__(self, bg_path, options, player, x=0, y=0, margin=vec(0, 0), step=30):
        super().__init__(bg_path, options, x, y, margin, step)

        self.player = player
        self.font = pygame.font.Font("fonts/DeterminationMono.ttf", self.step // 2)

    def render_text(self, surface):
        player_name = self.font.render(self.player.name, False, (255, 255, 255))
        player_lvl = self.font.render(f"LVL:{self.player.lvl}", False, (255, 255, 255))
        player_hp_stats = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", False, (255, 255, 255))

        surface.blit(player_name, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2))
        surface.blit(player_lvl, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2 * 2))
        surface.blit(player_hp_stats, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2 * 3))

    def render(self, surface):
        self.bg.render(surface)

        self.render_text(surface)

        if self.show_cursor:
            self.cursor.render(surface)
        for i, item in enumerate(self.options):
            item.render_item_in_box(surface, vec(self.bg.rect.x, self.bg.rect.y), i)


class InventoryBox(ChoosingBox):
    def __init__(self, bg_path, options, player, parent, x=0, y=0, margin=vec(0, 0), step=30):
        super().__init__(bg_path, options, x, y, margin, step)

        self.player = player
        self.parent = parent
        self.font = pygame.font.Font("fonts/DeterminationMono.ttf", self.step)

        self.show = False

    def reset_box(self):
        self.show = False
        self.index = 0
        self.cursor.rect.x, self.cursor.rect.y = self.cursor_pos_og.xy

    def render_text(self, surface):
        player_lvl_and_xp = self.font.render(f"LVL: {self.player.lvl} XP: {self.player.xp}/{self.player.max_xp}",
                                             False,
                                             (255, 255, 255))
        player_hp_stats = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", False, (255, 255, 255))

        surface.blit(player_lvl_and_xp, (self.bg.rect.x + self.margin.x * 0.5,
                                         self.bg.rect.y + self.bg.rect.h - self.step * 2.5))
        surface.blit(player_hp_stats, (self.bg.rect.x + self.margin.x * 0.5,
                                       self.bg.rect.y + self.bg.rect.h - self.step * 1.5))

        # XP rendering
        self.draw_relative_filled_boxes(surface,
                                        self.player.xp,
                                        self.player.max_xp,
                                        color=(0, 0, 200),
                                        start_box_y=self.bg.rect.y + self.bg.rect.h - self.step * 2.5,
                                        start_box_x=self.bg.rect.x + self.margin.x * 0.5 + player_lvl_and_xp.get_rect().w,
                                        end_box_x=self.bg.rect.x + self.bg.rect.w,
                                        margin=vec(10, 2),
                                        inner_box_margin=3)

        # HP rendering
        self.draw_relative_filled_boxes(surface,
                                        self.player.hp,
                                        self.player.max_hp,
                                        color=(200, 0, 0),
                                        start_box_y=self.bg.rect.y + self.bg.rect.h - self.step * 1.5,
                                        start_box_x=self.bg.rect.x + self.margin.x * 0.5 + player_hp_stats.get_rect().w,
                                        end_box_x=self.bg.rect.x + self.bg.rect.w,
                                        margin=vec(10, 2),
                                        inner_box_margin=3)

    def draw_relative_filled_boxes(self, surface, cur, tot, color, start_box_y, start_box_x, end_box_x, margin,
                                   inner_box_margin):
        percentage = cur / tot
        start_box_x += margin.x
        end_box_x -= margin.x
        end_box_w = end_box_x - start_box_x
        outer_box_rect = pygame.Rect(start_box_x,
                                     start_box_y + margin.y,
                                     end_box_w,
                                     self.step - margin.y * 2)
        pygame.draw.rect(surface, (255, 255, 255), outer_box_rect)

        pygame.draw.rect(surface, (0, 0, 0),
                         pygame.Rect(outer_box_rect.x + inner_box_margin,
                                     outer_box_rect.y + inner_box_margin,
                                     (outer_box_rect.w - inner_box_margin * 2),
                                     outer_box_rect.h - inner_box_margin * 2))
        if cur > 0:
            pygame.draw.rect(surface, color,
                             pygame.Rect(outer_box_rect.x + inner_box_margin,
                                         outer_box_rect.y + inner_box_margin,
                                         (outer_box_rect.w - inner_box_margin * 2) * percentage,
                                         outer_box_rect.h - inner_box_margin * 2))

    def render(self, surface):
        if self.show:
            self.bg.render(surface)

            self.render_text(surface)

            if self.show_cursor:
                self.cursor.render(surface)
            for i, item in enumerate(self.options):
                item.render_item_in_box(surface, vec(self.bg.rect.x, self.bg.rect.y), i)


class InfoBox(ChoosingBox):
    def __init__(self, bg_path, options, player, parent, x=0, y=0, margin=vec(0, 0), step=30):
        super().__init__(bg_path, options, x, y, margin, step)

        self.player = player
        self.parent = parent
        self.font = pygame.font.Font("fonts/DeterminationMono.ttf", self.step // 2)

        self.show = False

    def reset_box(self):
        self.show = False
        self.index = 0
        self.cursor.rect.x, self.cursor.rect.y = self.cursor_pos_og.xy

    def render_text(self, surface):
        player_name = self.font.render(self.player.name, False, (255, 255, 255))
        player_lvl = self.font.render(f"LVL:{self.player.lvl}", False, (255, 255, 255))
        player_hp_stats = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", False, (255, 255, 255))

        surface.blit(player_name, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2))
        surface.blit(player_lvl, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2 * 2))
        surface.blit(player_hp_stats, (self.bg.rect.x + self.margin.x * 0.5, self.bg.rect.y + self.step // 2 * 3))

    def render(self, surface):
        if self.show:
            self.bg.render(surface)

            self.render_text(surface)

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
