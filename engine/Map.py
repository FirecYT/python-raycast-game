class Map:
    def __init__(self):
        self.content = ''

        self.content += '#########################'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#..#..#..#.....#..#..#..#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#..#....................#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#..#..#..#.....#..#..#..#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#..#..#..#..#..#..#..#..#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#..#....................#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#..#....................#'
        self.content += '#.......................#'
        self.content += '#.......................#'
        self.content += '#########################'

        self.height = 25
        self.width = 25

    def check_collision(self, x: int, y: int):
        if self.content[x + y * self.width] == "#":
            return False
        return True
