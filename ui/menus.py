import arcade
import config


class MenuRenderer:
    def __init__(self):
        # Заголовки
        self.title_text = arcade.Text(
            text=config.SCREEN_TITLE,
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT - 150,
            color=arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            bold=True
        )

        self.start_text = arcade.Text(
            text="Press [ENTER] to Start",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        self.pause_text = arcade.Text(
            text="PAUSED",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 + 50,
            color=arcade.color.YELLOW,
            font_size=40,
            anchor_x="center",
            bold=True
        )

        self.continue_text = arcade.Text(
            text="Press [P] to Continue",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 - 20,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        self.game_over_text = arcade.Text(
            text="GAME OVER",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 + 50,
            color=arcade.color.RED,
            font_size=50,
            anchor_x="center",
            bold=True
        )

        self.restart_text = arcade.Text(
            text="Press [R] to Restart",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 - 20,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        # текст для финального счета
        self.final_score_text = arcade.Text(
            text="",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 + 10,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        # Тексты для экрана победы
        self.victory_text = arcade.Text(
            text="VICTORY!",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 + 60,
            color=arcade.color.GREEN,
            font_size=50,
            anchor_x="center",
            bold=True
        )
        self.victory_hint_text = arcade.Text(
            text="Press [R] to Restart",
            x=config.SCREEN_WIDTH // 2,
            y=config.SCREEN_HEIGHT // 2 - 10,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

    def draw_main_menu(self):
        """Отрисовка главного меню"""
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 200))
        self.title_text.draw()
        self.start_text.draw()

    def draw_pause_menu(self):
        """Отрисовка паузы"""
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 150))
        self.pause_text.draw()
        self.continue_text.draw()

    def draw_game_over(self, score):
        """Отрисовка экрана проигрыша"""
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 200))
        self.game_over_text.draw()

        # Обновляем текст счета и рисуем его
        self.final_score_text.value = f"Final Score: {score}"
        self.final_score_text.draw()

        self.restart_text.draw()

    def draw_victory(self, score):
        """Отрисовка экрана победы"""
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 200))
        self.victory_text.draw()

        # Показываем финальный счёт
        self.final_score_text.value = f"Final Score: {score}"
        self.final_score_text.draw()

        self.victory_hint_text.draw()