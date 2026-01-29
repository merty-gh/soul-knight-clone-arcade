from enemies.base_enemy import BaseEnemy

class MeleeEnemy(BaseEnemy):
    def __init__(self, x, y, player_ref):
        # Используем спрайт зомби
        super().__init__(":resources:images/animated_characters/zombie/zombie_idle.png",
                         x, y, player_ref)