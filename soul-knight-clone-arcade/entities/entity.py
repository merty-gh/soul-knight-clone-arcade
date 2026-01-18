import arcade

class Entity(arcade.Sprite):
    # Базовый класс для всех живых существ в игре.
    def __init__(self, filename, scale, start_x, start_y):
        super().__init__(filename, scale)
        self.center_x = start_x
        self.center_y = start_y

    def update(self, delta_time: float = 1/60):
        super().update()