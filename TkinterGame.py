from math import sin, cos, pi
from engine.Game import Game
from engine.Maze import Maze
from engine.Player import Player
from engine.Raycast import Raycast

import config

from tkinter import *

class TkinterGame(Game):
	def __init__(self):
		super().__init__()

		self.map = Maze(config.MAP_WIDTH // 2, config.MAP_HEIGHT // 2).toMap()
		self.player = Player(1, 1, 0, self.map)
		self.raycast = Raycast(self.map)

		self.screen_width = 800
		self.screen_height = 600

		self.root = Tk()
		self.root.title("Raycast")
		self.root.geometry(str(self.screen_width) + "x" + str(self.screen_height))

		self.canvas = Canvas(bg="white", width=self.screen_width, height=self.screen_height)
		self.canvas.pack(anchor=CENTER, expand=1)

		self.root.bind("<Key>", self.key_handler)
		self.root.bind("<Configure>", self.on_resize)

	def on_resize(self, event):
		self.screen_width = event.width
		self.screen_height = event.height

		self.canvas.config(width = event.width, height = event.height)

		self.render()

	def key_handler(self, event):
		print(event.char, event.keysym, event.keycode)

		if event.keycode == 87:
			dx = cos(self.player.angle)
			dy = sin(self.player.angle)
			self.player.move(dx, dy)
		elif event.keycode == 83:
			dx = -cos(self.player.angle)
			dy = -sin(self.player.angle)
			self.player.move(dx, dy)
		elif event.keycode == 65:
			self.player.rotate(-pi/2)
		elif event.keycode == 68:
			self.player.rotate(pi/2)
		elif event.keycode == 81:
			self.root.destroy()
			exit()

		self.render()

	def render(self):
		rays = self.raycast.raycast(self.player.x + 0.5, self.player.y + 0.5, self.player.angle, self.screen_width)

		self.canvas.delete("all")

		for ray_i in range(len(rays)):
			ray = rays[ray_i]

			reverse_distance: float = 1 - ray.distance / config.MAX_DEPTH

			height = self.screen_height / max(ray.distance, 1e-6) * 2

			self.canvas.create_rectangle(
				ray_i,
				(self.screen_height - height) / 2,
				ray_i + 1,
				(self.screen_height + height) / 2,
				outline="#" + '{0:02X}'.format(int(reverse_distance * 255)) + '{0:02X}'.format(int(reverse_distance * 255)) + '{0:02X}'.format(int(reverse_distance * 255))
			)

	def run(self):
		self.render()
		self.root.mainloop()

if __name__ == "__main__":
	# Запуск игры
	game = TkinterGame()
	game.run()
