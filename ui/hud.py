import arcade
import config


class HUD:
    def __init__(self):
        # Спрайты UI
        self.ui_sprites = arcade.SpriteList()
        self.weapon_icon = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", scale=0.8)
        self.weapon_icon.center_x = config.SCREEN_WIDTH - 50
        self.weapon_icon.center_y = 50
        self.ui_sprites.append(self.weapon_icon)

        # --- Текстовые объекты ---
        self.hp_text = arcade.Text(
            text="100/100",
            x=25,
            y=config.SCREEN_HEIGHT - 36,
            color=arcade.color.WHITE,
            font_size=12,
            bold=True
        )

        self.score_text = arcade.Text(
            text="Score: 0",
            x=config.SCREEN_WIDTH - 150,
            y=config.SCREEN_HEIGHT - 40,
            color=arcade.color.WHITE,
            font_size=config.UI_FONT_SIZE,
            bold=True
        )

        self.weapon_name_text = arcade.Text(
            text="Pistol",
            x=config.SCREEN_WIDTH - 90,
            y=25,
            color=arcade.color.WHITE,
            font_size=10
        )

    def draw(self, player):
        # 1. Полоски
        bg_left = 20
        bg_right = 20 + config.UI_BAR_WIDTH
        bar_center_y = config.SCREEN_HEIGHT - 30
        bg_top = bar_center_y + config.UI_BAR_HEIGHT / 2
        bg_bottom = bar_center_y - config.UI_BAR_HEIGHT / 2

        arcade.draw_lrbt_rectangle_filled(bg_left, bg_right, bg_bottom, bg_top, config.UI_BG_COLOR)

        health_percent = player.hp / player.max_hp
        if health_percent < 0: health_percent = 0
        current_bar_width = config.UI_BAR_WIDTH * health_percent

        if current_bar_width > 0:
            arcade.draw_lrbt_rectangle_filled(bg_left, bg_left + current_bar_width, bg_bottom, bg_top,
                                              config.UI_HEALTH_COLOR)

        # 2. Текст
        self.hp_text.value = f"{int(player.hp)}/{player.max_hp}"
        self.hp_text.draw()

        self.score_text.value = f"Score: {player.score}"
        self.score_text.draw()

        # 3. Иконки
        self.ui_sprites.draw()
        self.weapon_name_text.draw()