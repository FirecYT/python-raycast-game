from engine.Map import Map

class Player:
	def __init__(self, x: float, y: float, angle: float, map: Map):
		self.x = x
		self.y = y
		self.angle = angle
		self.map = map

	def move(self, dx: float, dy: float):
		new_x = self.x + dx
		new_y = self.y + dy
		if self.map.check_collision(int(new_x), int(new_y)):
			self.x = new_x
			self.y = new_y

	def rotate(self, angle: float):
		self.angle += angle
