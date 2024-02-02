class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.content = '' * self.width * self.height

    def check_collision(self, x: int, y: int):
        if self.content[x + y * self.width] == "#":
            return False
        return True
