from math import pi
from engine.Game import Game
from PIL import Image, ImageDraw

import config

class PillowGame(Game):
    def __init__(self, data = None):
        super().__init__()

        if data:
            self.player.x = data['player_x']
            self.player.y = data['player_y']
            self.player.angle = data['player_angle']

        self.screen_width = 1920
        self.screen_height = 1080

        self.texture = Image.open('walltext.png')

        self.image = Image.new(
            'RGBA',
            (self.screen_width, self.screen_height),
            (0, 0, 0, 255)
        )

        self.draw = ImageDraw.Draw(self.image)

    def render(self):
        rays = self.raycast.raycast(self.player.x + 0.5, self.player.y + 0.5, self.player.angle, self.screen_width)

        for ray_i in range(len(rays)):
            ray = rays[ray_i]

            if ray.distance > 0:
                height = int(self.screen_height / ray.distance * 2)
                reverse_distance: float = 1 - ray.distance / config.MAX_DEPTH

                text_part = self.texture.crop((
                    64 + int(ray.remainder * 64),
                    0,
                    64 + int(ray.remainder * 64) + 1,
                    64
                )).resize((
                    1,
                    height
                ))

                self.image.paste(
                    text_part,
                    (
                        ray_i,
                        (self.screen_height - height) // 2,
                        ray_i + 1,
                        (self.screen_height + height) // 2,
                    )
                )

    def run(self):
        self.render()
        self.image.show()

if __name__ == "__main__":
    # Запуск игры
    game = PillowGame({
        "player_x": 12,
        "player_y": 1,
        "player_angle": -pi/2*3,
    })
    game.run()