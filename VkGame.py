import vk_api

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from PillowGame import PillowGame

from config import *

class VkGame(PillowGame):
	def get_dx(self):
		if self.player.angle % 4 == 0: # Right
			return 1
		elif self.player.angle % 4 == 2: # Left
			return -1

		return 0

	def get_dy(self):
		if self.player.angle % 4 == 1: # Bottom
			return 1
		elif self.player.angle % 4 == 3: # Top
			return -1

		return 0

	def execute_command(self, command):
		if command == "w":
			self.player.move(self.get_dx(), self.get_dy())
		elif command == "s":
			self.player.move(-self.get_dx(), -self.get_dy())
		elif command == "a":
			self.player.rotate(-1)
		elif command == "d":
			self.player.rotate(1)

class VkManager():
	def __init__(self):
		self.vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)

		self.longpoll = VkBotLongPoll(self.vk_session, VK_GROUP_ID, 5)
		self.vk = self.vk_session.get_api()
		self.upload = vk_api.VkUpload(self.vk_session)

		self.players: dict[str, VkGame] = {}

		self.keyboard = VkKeyboard()

		self.keyboard.add_button('w', color=VkKeyboardColor.SECONDARY)

		self.keyboard.add_line()
		self.keyboard.add_button('a', color=VkKeyboardColor.SECONDARY)
		self.keyboard.add_button('d', color=VkKeyboardColor.SECONDARY)

		self.keyboard.add_line()
		self.keyboard.add_button('s', color=VkKeyboardColor.SECONDARY)

		self.keyboard.add_line()
		self.keyboard.add_button('restart', color=VkKeyboardColor.SECONDARY)

	def run(self):
		for event in self.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				player_id = event.obj.from_id

				if not player_id in self.players:
					self.players[player_id] = VkGame()

				if event.obj.text == "q":
					exit()
				elif event.obj.text == "restart":
					self.players[player_id] = VkGame()

				game = self.players[player_id]

				game.execute_command(event.obj.text)
				game.render()

				image_path = f"tmp/{player_id}.jpg"

				game.image.save(image_path)

				photo = self.upload.photo_messages(image_path)[0]

				attachments = f"photo{photo['owner_id']}_{photo['id']}"

				self.vk.messages.send(
					user_id = player_id,
					attachment = attachments,
					random_id = get_random_id(),
					message = "Enter command (w/a/s/d)",
					keyboard = self.keyboard.get_keyboard()
				)

if __name__ == "__main__":
	# Запуск игры
	game = VkManager()
	while True:
		try:
			game.run()
		except Exception as e:
			print(e)
