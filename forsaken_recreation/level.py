import pygame
import constants

class Level:
    def __init__(self):
        self.map_data = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W..............................W",
            "W..WWWW......WWWWWW............W",
            "W..W...........W...............W",
            "W..W...........W...............W",
            "W..WWWW........WWWW.....WWWW...W",
            "W..............................W",
            "W......WWWWWWWW................W",
            "W..............................W",
            "W..............................W",
            "W...WWWW................WWWW...W",
            "W...W...................W......W",
            "W...W...................W......W",
            "W...WWWW................WWWW...W",
            "W..............................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        self.walls = []
        self.keys = []
        self.create_map()

    def create_map(self):
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile in enumerate(row):
                if tile == "W":
                    x = col_idx * constants.TILE_SIZE
                    y = row_idx * constants.TILE_SIZE
                    self.walls.append(pygame.Rect(x, y, constants.TILE_SIZE, constants.TILE_SIZE))
                elif tile == "K": # Key placeholder, I'll add "K" to map_data manually or just randomly place them
                    pass

        # Manually add some keys for now
        self.keys = [
            pygame.Rect(200, 200, 20, 20),
            pygame.Rect(1000, 200, 20, 20),
            pygame.Rect(600, 500, 20, 20)
        ]

    def draw(self, screen):
        # Draw floor
        screen.fill(constants.DARK_GRAY)

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, constants.GRAY, wall)

        # Draw keys
        for key in self.keys:
            pygame.draw.rect(screen, constants.YELLOW, key)
