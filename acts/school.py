import pygame

import config
from running_game_hierarchy import Act, MapScene, House, Room, Entrance, ReturnEntrance, EastEntrance, NorthEntrance, \
    SouthEntrance, WestEntrance, RoomBorder
from sprite import Sprite, Sans, Map, Bear, TestNPC, Hitbox

vec = pygame.math.Vector2


# class Kitchen(Room):
#     def set_up(self):
#         self.default_entrance = "west_room"
#
#         self.objects["bg"] = Map("imgs/Kitchen.png", -33, 36, center=True, scale=False)
#         self.objects["player"] = self.player
#
#         # self.objects["Kbox1"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Kbox1"].hitbox = Hitbox(-32, 50, "imgs/empty_sprite.png", 160, 95, collideable= True)
#
#         # self.objects["Kbox2"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Kbox2"].hitbox = Hitbox(-65, 100, "imgs/empty_sprite.png", 42, 45, collideable= True)
#
#         self.update_entrance("west_room", SouthEntrance(self.player, "west_room"))
#         self.entrances.get("west_room").set_shape(32, 2)
#         self.entrances.get("west_room").set_pos(-80, 116)
#
#         self.npcs["bear"] = Bear(x=0, y=0, center=True)
#
#         # self.update_entrance("secret_1", NorthEntrance(self.player, "west_room"))
#         # self.update_entrance("secret_2", WestEntrance(self.player, "west_room"))
#         # self.update_entrance("secret_3", EastEntrance(self.player, "west_room"))
#
#
# class EastHallway(RoomBorder):
#     def update(self, dt):
#         self.dt = dt
#
#         self.camera.set_method("border")
#         borders_rect = self.objects.get("bg").rect
#         self.camera.mode.set_borders(borders_rect.x,
#                                      borders_rect.y,
#                                      borders_rect.x + borders_rect.w,
#                                      borders_rect.y + borders_rect.h + 50)
#
#         self.checks()
#
#     def set_up(self):
#         self.default_entrance = "entrance_room"
#
#         self.objects["bg"] = Map("imgs/Assets/EastHallwaydecored.png", center=True)
#         self.objects["player"] = self.player
#
#         # self.objects["EHbox1"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["EHbox1"].hitbox = Hitbox(-10, 18, "imgs/empty_sprite.png", 730, 80, collideable= True)
#
#         self.objects["EHbox1"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         self.objects["EHbox1"].hitbox = Hitbox(-10, 72, "imgs/empty_sprite.png", 730, 30, collideable=True)
#
#         self.objects["EHbox2"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         self.objects["EHbox2"].hitbox = Hitbox(-10, -32, "imgs/empty_sprite.png", 730, 30, collideable=True)
#
#         self.objects["EHbox3"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         self.objects["EHbox3"].hitbox = Hitbox(370, -32, "imgs/empty_sprite.png", 30, 730, collideable=True)
#
#         self.update_entrance("entrance_room", WestEntrance(self.player, "entrance_room"))
#         self.entrances.get("entrance_room").set_pos(-158, 0)
#         self.entrances.get("entrance_room").set_shape(2, 48)
#         self.entrances.get("entrance_room").set_pos(self.objects.get("bg").rect.x,
#                                                     self.entrances.get("entrance_room").rect.y)
#
#         # self.update_entrance("secret_1", SouthEntrance(self.player, "entrance_room"))
#
#         self.npcs["sans"] = Sans(x=300, y=-10, center=True)
#
#         basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
#                                                    x=-100, y=0, center=True)
#         chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
#                                                   "A chest you can pick up. Nice thing this.",
#                                                   x=100, y=0, center=True)
#         self.items[basket.dict_name] = basket
#         self.items[chest.dict_name] = chest
#
#
# class WestRoom(Room):
#     def set_up(self):
#         self.default_entrance = "entrance_room"
#         self.objects["bg"] = Map("imgs/Assets/Room_West_Floor.png", center=True)
#         self.objects["player"] = self.player
#
#         # self.objects["Wbox1"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Wbox1"].hitbox = Hitbox(150, 56, "imgs/empty_sprite.png", 72, 60, collideable= True)
#
#         # self.objects["Wbox2"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Wbox2"].hitbox = Hitbox(-93, -80, "imgs/empty_sprite.png", 40, 90, collideable= True)
#
#         # self.objects["Wbox3"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Wbox3"].hitbox = Hitbox(0, 15, "imgs/empty_sprite.png", 280, 170, collideable= True)
#
#         self.update_entrance("entrance_room", EastEntrance(self.player, "entrance_room"))
#         self.entrances.get("entrance_room").set_default_east_lower()
#
#         self.update_entrance("kitchen", NorthEntrance(self.player, "kitchen"))
#         self.entrances.get("kitchen").set_shape(32, 2)
#         self.entrances.get("kitchen").set_pos(-110, -118)
#
#         basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
#                                                    x=-100, y=0, center=True)
#         chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
#                                                   "A chest you can pick up. Nice thing this.",
#                                                   x=100, y=0, center=True)
#         self.npcs["TestNPC"] = TestNPC(x=0, y=0, center=True)
#         self.items[basket.dict_name] = basket
#         self.items[chest.dict_name] = chest
#
#
# class EntranceRoom(Room):
#     def set_up(self):
#         self.default_entrance = "entrance_room"
#
#         self.objects["staircase"] = Sprite("imgs/Staircase_1.png", center=True)
#         self.objects["bg"] = Map("imgs/Room_Entrance.png", center=True)
#         self.objects["player"] = self.player
#         self.objects["rail_1"] = Sprite("imgs/Railing_asset1.png", center=True)
#         self.objects["rail_2"] = Sprite("imgs/Railing_asset2.png", center=True)
#         self.objects["rail_3"] = Sprite("imgs/Railing_asset3.png", center=True)
#
#         # self.objects["Ebox1"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=True)
#         # self.objects["Ebox1"].hitbox = Hitbox(0, 65, "imgs/empty_sprite.png", 244, 75, collideable= True)
#
#         # self.objects["Ebox2"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=True)
#         # self.objects["Ebox2"].hitbox = Hitbox(0, 59, "imgs/empty_sprite.png", 330, 60, collideable= True)
#
#         # self.objects["Ebox3"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Ebox3"].hitbox = Hitbox(-107, -10, "imgs/empty_sprite.png", 30, 95, collideable= True)
#
#         # self.objects["Ebox4"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Ebox4"].hitbox = Hitbox(0, 80, "imgs/empty_sprite.png", 40, 95, collideable= True)
#
#         # self.objects["Ebox5"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Ebox5"].hitbox = Hitbox(95, -15, "imgs/empty_sprite.png", 55, 110, collideable= True)
#
#         # self.objects["Ebox6"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Ebox6"].hitbox = Hitbox(-5, -54, "imgs/empty_sprite.png", 155, 35, collideable= True)
#
#         # self.objects["Ebox7"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
#         # self.objects["Ebox7"].hitbox = Hitbox(-13, -26, "imgs/empty_sprite.png", 137, 75, collideable= True)
#
#         self.update_entrance("entrance_room", ReturnEntrance(self, self.player, enter_from="s", return_side="s"))
#         self.entrances.get("entrance_room").set_default_south()
#
#         self.update_entrance("west_room", WestEntrance(self.player, "west_room"))
#         self.entrances.get("west_room").set_default_west_lower()
#
#         self.update_entrance("east_hallway", EastEntrance(self.player, "east_hallway"))
#         self.entrances.get("east_hallway").set_default_east_lower()
#
#         basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
#                                                    x=-100, y=0, center=True, usable=True)
#         chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
#                                                   "A chest you can pick up. Nice thing this.",
#                                                   x=100, y=0, center=True, usable=True)
#         self.items[basket.dict_name] = basket
#         self.items[chest.dict_name] = chest
#
#
# class TestHouse(House):
#     def set_up(self):
#         self.set_entry_name("entrance_room")
#         self.update_room("entrance_room",
#                          EntranceRoom("entrance_room", self.screen, self.game, self.player, self.camera, self))
#         self.update_room("west_room", WestRoom("west_room", self.screen, self.game, self.player, self.camera, self))
#         self.update_room("east_hallway",
#                          EastHallway("east_hallway", self.screen, self.game, self.player, self.camera, self))
#         self.update_room("kitchen", Kitchen("kitchen", self.screen, self.game, self.player, self.camera, self))
#         self.house_sprite = Sprite("imgs/house_test.png", -4604, 1267, center=True)
#         self.music_path = "audio/home.ogg"
#         # self.play_music()


class SchoolScene(MapScene):
    def set_up(self):
        self.map = Map("imgs/School/floor_1.png", center=True)
        # self.map = Sprite("imgs/zelda_map_test.png", center=True)
        # self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))
        self.player.rect.x, self.player.rect.y = -1980, -90
        self.player_last_pos = vec(-1980, -90)

        self.music_path = "audio/ruins.ogg"
        # pygame.mixer.music.load(self.music_path)
        self.enter()

        self.objects["bg"] = Sprite("imgs/School/floor_1_bg_smaller.png", -440, 157, center=True)
        self.objects["floor"] = Sprite("imgs/School/floor_1_smaller.png", center=True)

        self.objects["flower_1"] = Sprite("imgs/Assets/pottedplant4.png", -1910, -124, center=True)
        self.objects["bucket"] = Sprite("imgs/Assets/bucket_purple.png", -1894, -134, center=True)
        self.objects["flower_2"] = Sprite("imgs/Assets/redflower.png", -1906, -40, center=True)
        self.objects["door_principal"] = Sprite("imgs/Assets/door2.png", -1856, -162, center=True)

        self.objects["door_administrator"] = Sprite("imgs/Assets/door2.png", -1856, -20, center=True)
        self.objects["door_administrator"].image.set_alpha(150)

        # self.objects["Rbox1"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=True)
        # self.objects["Rbox1"].hitbox = Hitbox(-4605, 1467, "imgs/empty_sprite.png", 41, 42, collideable= True)

        # self.objects["Rbox2"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=False)
        # self.objects["Rbox2"].hitbox = Hitbox(-4605, 1437, "imgs/empty_sprite.png", 47, 61, collideable= True)

        # self.objects["Rbox3"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=True)
        # self.objects["Rbox3"].hitbox = Hitbox(-4605, 1276, "imgs/empty_sprite.png", 201, 302, collideable= True)

        # self.objects["Rbox4"] = Sprite("imgs/empty_sprite.png", -4620, 1500, center=True)
        # self.objects["Rbox4"].hitbox = Hitbox(-4605, 1166, "imgs/empty_sprite.png", 242, 82, collideable= True)

        # self.npcs["sans"] = Sans(x=-4600, y=900, center=True)
        #
        # potion = self.player.inventory.create_item("imgs/potion_2.png", "Potion", "A potion which restores 7HP.",
        #                                            x=-4520, y=1380, center=True, usable=True,
        #                                            heal=7, type="HealPotion")
        # potion_2 = self.player.inventory.create_item("imgs/potion_2.png", "Potion", "A potion which restores 2HP.",
        #                                              x=-4680, y=1380, center=True, usable=True,
        #                                              heal=2, type="HealPotion")
        # self.items[potion.dict_name] = potion
        # self.items[potion_2.dict_name] = potion_2
        #
        # amount = 10
        # step = 20
        # start_at_y = 1350
        # for i, y in enumerate(range(start_at_y, start_at_y - step * amount, -step)):
        #     basket = self.player.inventory.create_item("imgs/basket.png", "Basket", "A basket you can pick up.",
        #                                                x=-4680, y=y, center=True)
        #     chest = self.player.inventory.create_item("imgs/chest2.png", "Chest",
        #                                               "A chest you can pick up. Nice thing this.",
        #                                               x=-4520, y=y, center=True)
        #     self.items[basket.dict_name] = basket
        #     self.items[chest.dict_name] = chest


# class TestScene2(MapScene):
#     def set_up(self):
#         self.map = Sprite("imgs/zelda_map_test.png", center=True)
#         self.cur_indoors_area = "house 1"
#         self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))
#         self.indoors_areas.get(self.cur_indoors_area).enter_house()


class SchoolAct(Act):
    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", SchoolScene(self.screen, self.game, self.player, self.camera, self))
        # self.update_scene("scene 2", TestScene2(self.screen, self.game, self.player, self.camera, self))