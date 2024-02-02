from math import sin, cos, pi
from os import get_terminal_size

import config

class ConsoleGame:
    def __init__(self):
        super().__init__()
        
        size = get_terminal_size()
        self.screen_width = size.columns
        self.screen_height = size.lines

        self.colors = '░▒▓█'

    def render(self):
        rays = self.raycast.raycast(self.player.x + 0.5, self.player.y + 0.5, self.player.angle, self.screen_width)
        screen_lines = []

        for ray in rays:
            reverse_distance: float = 1 - ray.distance / config.MAX_DEPTH

            height = int(self.screen_height / max(ray.distance, 1e-6))

            color_index = int(reverse_distance * len(self.colors))

            if color_index == len(self.colors): color_index -= 1
            color = self.colors[color_index] # if ray.vertical else ' '

            # sky
            line = ' ' * int((self.screen_height - height) / 2 + 1) 
            # walls
            line += color * height
            # floor
            line += ' ' * int((self.screen_height - height) / 2)

            screen_lines.append(line)

        screen = [' ' for x in range(self.screen_height * self.screen_width)]

        for y in range(self.screen_height):
            for x in range(self.screen_width):
                screen[x + y * self.screen_width] = screen_lines[x][y]

        for y in range(self.map.height):
            for x in range(self.map.width):
                screen[x + y * self.screen_width] = '.' if self.map.check_collision(x, y) else '#'

        screen[int(self.player.x + self.player.y * self.screen_width)] = 'p'

        print('\033[0;0H' + ''.join(screen), end='')

    def run(self):
        while True:
            self.render()

            command = input("Enter command (w/a/s/d): ")
            if command == "w":
                dx = cos(self.player.angle)
                dy = sin(self.player.angle)
                self.player.move(dx, dy)
            elif command == "s":
                dx = -cos(self.player.angle)
                dy = -sin(self.player.angle)
                self.player.move(dx, dy)
            elif command == "a":
                self.player.rotate(-pi/2)
            elif command == "d":
                self.player.rotate(pi/2)
            elif command == "i":
                item = input("Enter item to add to inventory: ")
                self.player.add_to_inventory(item)
            elif command == "q":
                exit()

if __name__ == "__main__":
    # Запуск игры
    game = ConsoleGame()
    game.run()