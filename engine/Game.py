from abc import ABC, abstractmethod
from engine.Map import Map
from engine.Player import Player
from engine.Raycast import Raycast

from tkinter import *

class Game(ABC):
    @abstractmethod
    def __init__(self):
        self.map = Map(25, 25)
        self.player = Player(12, 12, 0, self.map)
        self.raycast = Raycast(self.map)

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def run(self):
        pass
