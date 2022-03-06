import pygame

from sprite import Sprite

vec = pygame.math.Vector2


class Inventory:
    def __init__(self, max_len=16):
        self.items = dict()
        self.max_len = max_len
        self.id = 0

        self.types = {
            "Item": Item,
            "Usable": Usable,
            "Equipable": Equipable,
            "HealPotion": HealPotion,
        }

    def create_item(self, main_image_path, display_name="Unknown",
                    desc="Item without a description", x=0, y=0, center=False, scale=False,
                    render_collision_box=False, margin=vec(30, 15), step=30,
                    usable=False, equipable=False, type="Item", heal=0):
        self.id += 1
        dict_name = f"{display_name} {self.id}"
        item = self.types[type](main_image_path, display_name, dict_name, self.id, desc,
                    x, y, center, scale, render_collision_box,
                    margin, step, usable, equipable)

        if heal > 0:
            item.heal = heal

        return item

    def check_if_can_add(self):
        return len(self.items) + 1 <= self.max_len

    def add_item(self, item):
        if self.check_if_can_add():
            self.items[item.dict_name] = item

    def remove_item(self, item_name):
        self.items.pop(item_name)

    def render_inventory(self, surface, start_at):
        for i, item in enumerate(self.items.values()):
            item.render_item_in_box(surface, start_at, i)


class Item(Sprite):
    def __init__(self, main_image_path, display_name="Unknown", dict_name="Unknown 0", id=0,
                 desc="Item without a description", x=0, y=0, center=False, scale=False,
                 render_collision_box=False, margin=vec(30, 15), step=30,
                 usable=False, equipable=False):
        super().__init__(main_image_path, x, y, center, scale, render_collision_box)

        self.margin = margin
        self.step = step

        self.display_name = display_name
        self.dict_name = dict_name
        self.id = id
        self.desc = desc

        self.font = pygame.font.Font("fonts/DeterminationMono.ttf", self.step)

        self.name_text = self.font.render(self.display_name, False, (255, 255, 255))
        self.desc_text = self.font.render(self.desc, False, (255, 255, 255))

        self.usable = usable
        self.equipable = equipable

    def render_item_in_box(self, surface, start_at, i=0):
        surface.blit(self.name_text, (start_at.x + self.margin.x, start_at.y + self.margin.y + self.step * i))

    def use(self, player):
        pass


class Usable(Item):
    def __init__(self, main_image_path, display_name="Unknown", dict_name="Unknown 0", id=0,
                 desc="Item without a description", x=0, y=0, center=False, scale=False,
                 render_collision_box=False, margin=vec(30, 15), step=30,
                 usable=True, equipable=False):
        super().__init__(main_image_path, display_name=display_name, dict_name=dict_name, id=id,
                         desc=desc, x=x, y=y, center=center, scale=scale,
                         render_collision_box=render_collision_box, margin=margin, step=step,
                         usable=usable, equipable=equipable)


class HealPotion(Usable):
    def __init__(self, main_image_path, display_name="Unknown", dict_name="Unknown 0", id=0,
                 desc="Item without a description", x=0, y=0, center=False, scale=False,
                 render_collision_box=False, margin=vec(30, 15), step=30,
                 usable=True, equipable=False, heal=5):
        super().__init__(main_image_path, display_name=display_name, dict_name=dict_name, id=id,
                         desc=desc, x=x, y=y, center=center, scale=scale,
                         render_collision_box=render_collision_box, margin=margin, step=step,
                         usable=usable, equipable=equipable)
        self.heal = heal

    def use(self, player):
        if player.hp + self.heal > player.max_hp:
            player.hp = player.max_hp
        else:
            player.hp += self.heal


class Equipable(Item):
    def __init__(self, main_image_path, display_name="Unknown", dict_name="Unknown 0", id=0,
                 desc="Item without a description", x=0, y=0, center=False, scale=False,
                 render_collision_box=False, margin=vec(30, 15), step=30,
                 usable=False, equipable=True):
        super().__init__(main_image_path, display_name=display_name, dict_name=dict_name, id=id,
                         desc=desc, x=x, y=y, center=center, scale=scale,
                         render_collision_box=render_collision_box, margin=margin, step=step,
                         usable=usable, equipable=equipable)
