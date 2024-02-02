from random import shuffle, random
from engine.Map import Map

class Ceil:
    def __init__(self):
        self.down = False
        self.right = False
        self.collapse = False

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.content = [Ceil() for x in range(self.width * self.height)]

        self.generate(0, 0)
    
    def get(self, x, y):
        return self.content[x + y * self.width]

    def toMap(self):
        content = self.toArray()

        result_map = Map(self.width * 2 + 1, self.height * 2 + 1)
        result_map.content = ''.join([''.join(res) for res in content])

        return result_map

    def print(self):
        content = self.toArray()

        print('\n'.join([''.join(res) for res in content]))

    def toArray(self):
        content = [['#' for j in range(self.height * 2 + 1)] for i in range(self.width * 2 + 1)]

        for y in range(self.height):
            for x in range(self.width):
                ceil = self.get(x, y)

                content[x * 2 + 1][y * 2 + 1] = ' '

                if ceil.right:
                    content[x * 2 + 2][y * 2 + 1] = ' '

                if ceil.down:
                    content[x * 2 + 1][y * 2 + 2] = ' '

        return content

    def generate(self, x, y):
        current_ceil = self.get(x, y)

        current_ceil.collapse = True

        valids = []

        if x > 0 and not self.get(x - 1, y).collapse:
            valids.append('left')
        if y > 0 and not self.get(x, y - 1).collapse:
            valids.append('up')
        if x < self.width - 1 and not self.get(x + 1, y).collapse:
            valids.append('right')
        if y < self.height - 1 and not self.get(x, y + 1).collapse:
            valids.append('down')

        while len(valids) > 0:
            shuffle(valids)
            next_direction = valids.pop()

            if next_direction == 'left':
                self.get(x - 1, y).right = True
                self.generate(x - 1, y)
            if next_direction == 'up':
                self.get(x, y - 1).down = True
                self.generate(x, y - 1)
            if next_direction == 'right':
                current_ceil.right = True
                self.generate(x + 1, y)
            if next_direction == 'down':
                current_ceil.down = True
                self.generate(x, y + 1)

            valids = []

            if x > 0 and not self.get(x - 1, y).collapse:
                valids.append('left')
            if y > 0 and not self.get(x, y - 1).collapse:
                valids.append('up')
            if x < self.width - 1 and not self.get(x + 1, y).collapse:
                valids.append('right')
            if y < self.height - 1 and not self.get(x, y + 1).collapse:
                valids.append('down')


if __name__ == "__main__":
    maze = Maze(20, 20)

    maze.print()
