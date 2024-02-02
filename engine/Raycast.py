from engine.Map import Map
import config
import math

class Ray:
    def __init__(self, distance: int, vertical: bool, angle: float, remainder: float) -> None:
        self.distance = distance
        self.vertical = vertical
        self.remainder = remainder
        self.angle = angle

class Raycast:
    def __init__(self, map: Map):
        self.map = map
    
    def raycast(self, camera_x: float, camera_y: float, camera_angle: float, screen_width: int) -> list[Ray]:
        result = []

        camera_position = {
            'left': camera_x - camera_x // 1,
            'top': camera_y - camera_y // 1,
            'right': 1 - (camera_x - camera_x // 1),
            'bottom': 1 - (camera_y - camera_y // 1),
        }

        for ray_x in range(screen_width):
            angle = (camera_angle - config.FOV / 2) + (ray_x / screen_width) * config.FOV

            ray_cos = math.cos(angle)
            ray_sin = math.sin(angle)

            vd, hd = 0, 0

            for dep in range(config.MAX_DEPTH):
                if ray_cos > 0:
                    vd = camera_position['right'] / ray_cos + 1 / ray_cos * dep
                elif ray_cos < 0:
                    vd = camera_position['left'] / -ray_cos + 1 / -ray_cos * dep

                x, y = vd * ray_cos + camera_x, vd * ray_sin + camera_y
                fixed_x, fixed_y = (x - 1e-6 if ray_cos < 0 else x + 1e-6) // 1, y // 1

                if fixed_x < 0 or fixed_x >= self.map.width or fixed_y < 0 or fixed_y >= self.map.height:
                    vd = config.MAX_DEPTH
                    break

                if not self.map.check_collision(int(fixed_x), int(fixed_y)):
                    break

            for dep in range(config.MAX_DEPTH):
                if ray_sin > 0:
                    hd = camera_position['bottom'] / ray_sin + 1 / ray_sin * dep
                elif ray_sin < 0:
                    hd = camera_position['top'] / -ray_sin + 1 / -ray_sin * dep

                x, y = hd * ray_cos + camera_x, hd * ray_sin + camera_y
                fixed_x, fixed_y = x // 1, (y - 1e-6 if ray_sin < 0 else y + 1e-6) // 1

                if fixed_x < 0 or fixed_x >= self.map.width or fixed_y < 0 or fixed_y >= self.map.height:
                    hd = config.MAX_DEPTH
                    break

                if not self.map.check_collision(int(fixed_x), int(fixed_y)):
                    break

            distance = min(vd, hd)
            vertical = vd < hd

            remainder = (distance * ray_sin + camera_y) if vertical else (distance * ray_cos + camera_x)

            result.append(Ray(
                distance * math.cos(camera_angle - angle),
                vertical,
                angle,
                remainder - remainder // 1
            ))

        return result
