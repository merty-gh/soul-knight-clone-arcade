import arcade
import random


class Particle(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        # Создаем маленький круг
        self.texture = arcade.make_soft_circle_texture(10, color)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-3, 3)
        self.change_y = random.uniform(-3, 3)
        self.alpha = 255
        self.fade_rate = 10

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.alpha -= self.fade_rate

        if self.alpha <= 0:
            self.remove_from_sprite_lists()


class ParticleSystem:
    def __init__(self):
        self.particle_list = arcade.SpriteList()

    def add_hit_effect(self, x, y, color):
        for _ in range(8):
            particle = Particle(x, y, color)
            self.particle_list.append(particle)

    def update(self):
        self.particle_list.update()

    def draw(self):
        self.particle_list.draw()