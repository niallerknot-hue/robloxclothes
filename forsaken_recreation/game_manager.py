import pygame
import constants
import json
import os
from menu import Menu
from lobby import Lobby
from game_engine import GameEngine
from shop import Shop

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = constants.STATE_MENU

        self.data_file = "forsaken_recreation/save_data.json"

        # Shared data
        self.game_data = {
            "coins": 0,
            "unlocked_skins": ["default"],
            "current_skins": {"p1": "default", "p2": "default"}
        }
        self.load_data()

        self.menu = Menu(self)
        self.lobby = Lobby(self)
        self.game_engine = None # Will be created when starting game
        self.shop = Shop(self)

    def change_state(self, new_state):
        self.state = new_state
        if new_state == constants.STATE_GAME:
            # Initialize new game with selections from lobby
            p1_char = self.lobby.p1_selection
            p2_char = self.lobby.p2_selection
            self.game_engine = GameEngine(self, p1_char, p2_char)

    def handle_input(self, events):
        if self.state == constants.STATE_MENU:
            self.menu.handle_input(events)
        elif self.state == constants.STATE_LOBBY:
            self.lobby.handle_input(events)
        elif self.state == constants.STATE_GAME:
            if self.game_engine:
                self.game_engine.handle_input(events)
        elif self.state == constants.STATE_SHOP:
            self.shop.handle_input(events)

    def update(self, dt):
        if self.state == constants.STATE_MENU:
            self.menu.update(dt)
        elif self.state == constants.STATE_LOBBY:
            self.lobby.update(dt)
        elif self.state == constants.STATE_GAME:
            if self.game_engine:
                self.game_engine.update(dt)
        elif self.state == constants.STATE_SHOP:
            self.shop.update(dt)

    def draw(self, screen):
        screen.fill(constants.BLACK)
        if self.state == constants.STATE_MENU:
            self.menu.draw(screen)
        elif self.state == constants.STATE_LOBBY:
            self.lobby.draw(screen)
        elif self.state == constants.STATE_GAME:
            if self.game_engine:
                self.game_engine.draw(screen)
        elif self.state == constants.STATE_SHOP:
            self.shop.draw(screen)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Merge loaded data with defaults (in case of missing keys)
                    for key, value in data.items():
                        self.game_data[key] = value
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.game_data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
