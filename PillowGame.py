from math import pi, cos, sin
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

        self.image_load = self.texture.load()

        self.draw = ImageDraw.Draw(self.image)
    
    def interpalation(self, x1, fx1, x3, fx3, x2):
        try:
            return x1 + (x2 - fx1) * (x3 - x1) / (fx3 - fx1)
        except ZeroDivisionError:
            return 0

    def render(self):
        rays = self.raycast.raycast(self.player.x + 0.5, self.player.y + 0.5, self.player.angle, self.screen_width)

        for ray_i in range(len(rays)):
            ray = rays[ray_i]

            if ray.distance > 0:
                height = int(self.screen_height / ray.distance * 2)

                text_part = self.texture.crop((
                    64 + int(ray.remainder * 64),
                    0,
                    64 + int(ray.remainder * 64) + 1,
                    64
                )).resize((
                    1,
                    height
                ))

                wall_start = (self.screen_height - height) // 2

                self.image.paste(
                    text_part,
                    (
                        ray_i,
                        wall_start,
                        ray_i + 1,
                        wall_start + height,
                    )
                )

                for screen_y in range(wall_start + height, self.screen_height):
                    floor_distance = self.screen_height * 2 / (screen_y * 2 - self.screen_height) / cos(self.player.angle - ray.angle)

                    floor_position = (
                        self.player.x + 0.5 + abs(cos(ray.angle) * floor_distance),
                        self.player.y + 0.5 + abs(sin(ray.angle) * floor_distance),
                    )

                    floor_x = floor_position[0] - floor_position[0] // 1
                    floor_y = floor_position[1] - floor_position[1] // 1

                    self.draw.point(
                        (ray_i, screen_y),
                        self.image_load[int(floor_x * 64), int(floor_y * 64)][:3]
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