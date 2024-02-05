from math import pi, sin, cos
from os import get_terminal_size

from random import random

camera = [12.5, 12.5, random() * pi * 2]

size = get_terminal_size()
screenWidth = size.columns
screenHeight = size.lines

mapHeight = 25
mapWidth = 25

map = ''.join(['#' if random() < 0.05 else ' ' for x in range(mapWidth * mapHeight)])

FOV = pi / 3
depth = 25

scale = 25

def cameraAngle():
	return (camera[2] * 90)/180*pi

def raycast():
	result = []

	camera_position = {
		'left': camera[0] - camera[0] // 1,
		'top': camera[1] - camera[1] // 1,
		'right': 1 - (camera[0] - camera[0] // 1),
		'bottom': 1 - (camera[1] - camera[1] // 1),
	}

	for x in range(screenWidth):
		angle = (cameraAngle() - FOV / 2) + (x / screenWidth) * FOV

		rayX = cos(angle)
		rayY = sin(angle)

		vd, hd = 0, 0

		for dep in range(depth):
			if rayX > 0:
				vd = camera_position['right'] / rayX + 1 / rayX * dep
			elif rayX < 0:
				vd = camera_position['left'] / -rayX + 1 / -rayX * dep

			x, y = vd * rayX + camera[0], vd * rayY + camera[1]
			fixed_x, fixed_y = (x - 1e-6 if rayX < 0 else x + 1e-6) // 1, y // 1

			if fixed_x < 0 or fixed_x >= mapWidth or fixed_y < 0 or fixed_y >= mapHeight:
				vd = depth * 2
				break

			if map[int(fixed_y * mapWidth + fixed_x)] == "#":
				break

		for dep in range(depth):
			if rayY > 0:
				hd = camera_position['bottom'] / rayY + 1 / rayY * dep
			elif rayY < 0:
				hd = camera_position['top'] / -rayY + 1 / -rayY * dep

			x, y = hd * rayX + camera[0], hd * rayY + camera[1]
			fixed_x, fixed_y = x // 1, (y - 1e-6 if rayY < 0 else y + 1e-6) // 1

			if fixed_x < 0 or fixed_x >= mapWidth or fixed_y < 0 or fixed_y >= mapHeight:
				hd = depth * 2
				break

			if map[int(fixed_y * mapWidth + fixed_x)] == "#":
				break

		result.append((min(vd, hd) * cos(cameraAngle() - angle), vd < hd))

	return result

colors = '░▒▓█'

if __name__ == '__main__':
	result = raycast()

	for x in range(len(result)):
		dd = 1 - result[x][0] / depth

		height = int(dd * screenHeight)
		color = colors[int(dd*len(colors))] # if result[x][1] else ' '

		result[x] = ' ' * int((screenHeight - height) / 2 + 1) + color * height + ' ' * int((screenHeight - height) / 2)

	screen = [' ' for x in range(screenHeight * screenWidth)]

	for y in range(screenHeight):
		for x in range(screenWidth):
			screen[x + y * screenWidth] = result[x][y]

	print('\033[0;0H' + ''.join(screen), end='')
