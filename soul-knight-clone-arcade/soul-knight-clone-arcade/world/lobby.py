import arcade
import config
# IMPORTANT: use full path world.tiles
from world.tiles import Wall, Floor
from entities.interactables import Portal, SkinChanger, WeaponShopItem
from weapons.pistol import Pistol


class Lobby:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.interactable_list = arcade.SpriteList()
        self.decor_list = arcade.SpriteList()  # For furniture

    def setup(self):
        # --- GENERATE FLOOR (WITH RUG) ---
        temp_wall = Wall(0, 0)
        grid = int(temp_wall.width)

        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2

        for x in range(0, config.SCREEN_WIDTH, grid):
            for y in range(0, config.SCREEN_HEIGHT, grid):
                # Create floor
                floor = Floor(x, y)

                # Make a "rug" in the center
                if abs(x - center_x) < 200 and abs(y - center_y) < 150:
                    floor.color = (100, 100, 150)  # Light blue rug
                else:
                    floor.color = (40, 50, 60)  # Dark main floor

                self.floor_list.append(floor)

                # Walls on edges
                if x == 0 or x >= config.SCREEN_WIDTH - grid or y == 0 or y >= config.SCREEN_HEIGHT - grid:
                    self.wall_list.append(Wall(x, y))

        # --- INTERACTABLES ---

        # 1. Wardrobe (Left)
        self.wardrobe = SkinChanger(200, center_y)
        self.interactable_list.append(self.wardrobe)

        # Add "cupboards" around wardrobe for decoration
        for i in range(-1, 2, 2):
            decor = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
            decor.center_x = 200
            decor.center_y = center_y + i * 60
            self.wall_list.append(decor)

            # 2. Shop (Right)
        shop_item = WeaponShopItem(config.SCREEN_WIDTH - 200, center_y,
                                   Pistol, 5, ":resources:images/space_shooter/laserBlue01.png")
        self.interactable_list.append(shop_item)

        # "Table" under the weapon
        table = arcade.Sprite(":resources:images/tiles/boxCrate_single.png", 0.5)
        table.center_x = config.SCREEN_WIDTH - 200
        table.center_y = center_y
        self.decor_list.append(table)

        # 3. Portal (Top)
        self.portal = Portal(center_x, config.SCREEN_HEIGHT - 120)
        self.interactable_list.append(self.portal)

        # 4. TV/Sofa (Bottom) - FIXED RESOURCE PATH
        # Changed bridgeLogs.png to boxCrate_double.png because bridgeLogs was removed in Arcade 3.0
        sofa = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.8)
        sofa.center_x = center_x
        sofa.center_y = 150
        # Color it slightly to look different
        sofa.color = (150, 100, 100)
        self.wall_list.append(sofa)