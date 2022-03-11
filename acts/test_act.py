import pygame

import config
from running_game_hierarchy import Act, MapScene, House, Room, Entrance, ReturnEntrance, EastEntrance, NorthEntrance, \
    SouthEntrance, WestEntrance, RoomBorder
from sprite import Sprite, Sans, Map, Bear, TestNPC


class Kitchen(Room):
    def set_up(self):
        self.default_entrance = "west_room"

        self.objects["bg"] = Map("imgs/Kitchen.png", -33, 36, center=True, scale=False)
        self.objects["player"] = self.player

        self.update_entrance("west_room", SouthEntrance(self.player, "west_room"))
        self.entrances.get("west_room").set_shape(32, 2)
        self.entrances.get("west_room").set_pos(-80, 116)

        self.npcs["bear"] = Bear(x=0, y=0, center=True)

        # self.update_entrance("secret_1", NorthEntrance(self.player, "west_room"))
        # self.update_entrance("secret_2", WestEntrance(self.player, "west_room"))
        # self.update_entrance("secret_3", EastEntrance(self.player, "west_room"))


class EastHallway(RoomBorder):
    def update(self, dt):
        self.dt = dt

        self.camera.set_method("border")
        borders_rect = self.objects.get("bg").rect
        self.camera.mode.set_borders(borders_rect.x,
                                     borders_rect.y,
                                     borders_rect.x + borders_rect.w,
                                     borders_rect.y + borders_rect.h + 50)

        self.check_for_entrance_collisions()
        self.check_for_npc_collisions()
        self.check_for_item_collisions()

    def set_up(self):
        self.default_entrance = "entrance_room"

        self.objects["bg"] = Map("imgs/Assets/EastHallwaydecored.png", center=True)
        self.objects["player"] = self.player

        self.update_entrance("entrance_room", WestEntrance(self.player, "entrance_room"))
        self.entrances.get("entrance_room").set_default_west_center_lower()
        self.entrances.get("entrance_room").set_pos(self.objects.get("bg").rect.x,
                                                    self.entrances.get("entrance_room").rect.y)

        # self.update_entrance("secret_1", SouthEntrance(self.player, "entrance_room"))

        self.npcs["sans"] = Sans(x=300, y=-10, center=True)

        basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
                                                   x=-100, y=0, center=True)
        chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
                                                  "A chest you can pick up. Nice thing this.",
                                                  x=100, y=0, center=True)
        self.items[basket.dict_name] = basket
        self.items[chest.dict_name] = chest


class WestRoom(Room):
    def set_up(self):
        self.default_entrance = "entrance_room"
        self.objects["bg"] = Map("imgs/Assets/Room_West_Floor.png", center=True)
        self.objects["player"] = self.player

        self.update_entrance("entrance_room", EastEntrance(self.player, "entrance_room"))
        self.entrances.get("entrance_room").set_default_east_lower()

        self.update_entrance("kitchen", NorthEntrance(self.player, "kitchen"))
        self.entrances.get("kitchen").set_shape(32, 2)
        self.entrances.get("kitchen").set_pos(-110, -118)

        basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
                                                   x=-100, y=0, center=True)
        chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
                                                  "A chest you can pick up. Nice thing this.",
                                                  x=100, y=0, center=True)
        self.npcs["TestNPC"] = TestNPC(x=0, y=0, center=True)
        self.items[basket.dict_name] = basket
        self.items[chest.dict_name] = chest


class EntranceRoom(Room):
    def set_up(self):

        self.default_entrance = "entrance_room"

        self.objects["staircase"] = Sprite("imgs/Staircase_1.png", center=True)
        self.objects["bg"] = Map("imgs/Room_Entrance.png", center=True)
        self.objects["player"] = self.player
        self.objects["rail_1"] = Sprite("imgs/Railing_asset1.png", center=True)
        self.objects["rail_2"] = Sprite("imgs/Railing_asset2.png", center=True)
        self.objects["rail_3"] = Sprite("imgs/Railing_asset3.png", center=True)

        #self.hitboxes["box1"] = Hitbox( surface =self.screen, x = 0, y = 0, height = 100, width = 100)

        self.update_entrance("entrance_room", ReturnEntrance(self, self.player, enter_from="s", return_side="s"))
        self.entrances.get("entrance_room").set_default_south()

        self.update_entrance("west_room", WestEntrance(self.player, "west_room"))
        self.entrances.get("west_room").set_default_west_lower()

        self.update_entrance("east_hallway", EastEntrance(self.player, "east_hallway"))
        self.entrances.get("east_hallway").set_default_east_lower()

        basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
                                                   x=-100, y=0, center=True, usable=True)
        chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
                                                  "A chest you can pick up. Nice thing this.",
                                                  x=100, y=0, center=True, usable=True)
        self.items[basket.dict_name] = basket
        self.items[chest.dict_name] = chest


class TestHouse(House):
    def set_up(self):
        self.set_entry_name("entrance_room")
        self.update_room("entrance_room", EntranceRoom("entrance_room", self.screen, self.game, self.player, self.camera, self))
        self.update_room("west_room", WestRoom("west_room", self.screen, self.game, self.player, self.camera, self))
        self.update_room("east_hallway", EastHallway("east_hallway", self.screen, self.game, self.player, self.camera, self))
        self.update_room("kitchen", Kitchen("kitchen", self.screen, self.game, self.player, self.camera, self))
        self.house_sprite = Sprite("imgs/house_test.png", -4604, 1267, center=True)
        self.music_path = "audio/home.ogg"
        # self.play_music()


class TestScene1(MapScene):
    def set_up(self):
        self.map = Map("imgs/ruins.png", center=True)
        # self.map = Sprite("imgs/zelda_map_test.png", center=True)
        self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))
        self.player.rect.x, self.player.rect.y = -4620, 1450
        self.music_path = "audio/ruins.ogg"
        # pygame.mixer.music.load(self.music_path)
        self.enter()

        self.objects["test_hitbox"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=True)

        self.npcs["sans"] = Sans(x=-4600, y=900, center=True)

        potion = self.player.inventory.create_item("imgs/potion_2.png", "Potion", "A potion which restores 7HP.",
                                                   x=-4520, y=1380, center=True, usable=True,
                                                   heal=7, type="HealPotion")
        potion_2 = self.player.inventory.create_item("imgs/potion_2.png", "Potion", "A potion which restores 2HP.",
                                                     x=-4680, y=1380, center=True, usable=True,
                                                     heal=2, type="HealPotion")
        self.items[potion.dict_name] = potion
        self.items[potion_2.dict_name] = potion_2

        amount = 10
        step = 20
        start_at_y = 1350
        for i, y in enumerate(range(start_at_y, start_at_y - step * amount, -step)):
            basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
                                                       x=-4680, y=y, center=True)
            chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
                                                      "A chest you can pick up. Nice thing this.",
                                                      x=-4520, y=y, center=True)
            self.items[basket.dict_name] = basket
            self.items[chest.dict_name] = chest


# class TestScene2(MapScene):
#     def set_up(self):
#         self.map = Sprite("imgs/zelda_map_test.png", center=True)
#         self.cur_indoors_area = "house 1"
#         self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))
#         self.indoors_areas.get(self.cur_indoors_area).enter_house()


class TestAct(Act):
    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", TestScene1(self.screen, self.game, self.player, self.camera, self))
        # self.update_scene("scene 2", TestScene2(self.screen, self.game, self.player, self.camera, self))
