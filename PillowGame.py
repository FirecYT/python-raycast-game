from math import pi, cos, sin
from engine.Game import Game
from engine.Maze import Maze
from engine.Player import Player
from engine.Raycast import Raycast
from PIL import Image, ImageDraw

import config

MAP_SCALE = 32

class PillowGame(Game):
	def __init__(self, data = None):
		super().__init__()

		self.map = Maze(config.MAP_WIDTH // 2, config.MAP_HEIGHT // 2).toMap()
		self.player = Player(1, 1, 0, self.map)
		self.raycast = Raycast(self.map)

		if data:
			self.player.x = data['player_x']
			self.player.y = data['player_y']
			self.player.angle = data['player_angle']

		self.screen_width = 1920
		self.screen_height = 1080

		self.texture = Image.open('walltext.png')

		self.image = Image.new(
			'RGB',
			(self.screen_width, self.screen_height),
			(0, 0, 0)
		)

		self.image_load = self.texture.load()

		self.draw = ImageDraw.Draw(self.image)

	def player_angle(self):
		return self.player.angle * pi / 2

	def render(self):
		rays = self.raycast.raycast(self.player.x + 0.5, self.player.y + 0.5, self.player_angle(), self.screen_width)

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

				if wall_start > 0:
					self.draw.rectangle(
						(
							ray_i,
							0,
							ray_i + 1,
							wall_start,
						),
						fill=(0,0,0)
					)

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
					floor_distance = self.screen_height * 2 / (screen_y * 2 - self.screen_height) / cos(self.player_angle() - ray.angle)

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

				for y in range(self.map.height):
					for x in range(self.map.width):
						self.draw.rectangle(
							(
								x * MAP_SCALE,
								y * MAP_SCALE,
								x * MAP_SCALE + MAP_SCALE,
								y * MAP_SCALE + MAP_SCALE,
							),
							fill = (255, 255, 255) if self.map.check_collision(x, y) else (64, 64, 64),
							outline = (0, 0, 0)
						)

				self.draw.rectangle(
					(
						self.player.x * MAP_SCALE + MAP_SCALE / 4,
						self.player.y * MAP_SCALE + MAP_SCALE / 4,
						self.player.x * MAP_SCALE + MAP_SCALE / 2,
						self.player.y * MAP_SCALE + MAP_SCALE / 2,
					),
					(255, 0, 0)
				)

	def run(self):
		self.render()
		self.image.show()

if __name__ == "__main__":
	# Запуск игры
	game = PillowGame({
		"player_x": 12,
		"player_y": 1,
		"player_angle": 0,
	})
	game.run()
