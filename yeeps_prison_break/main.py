import pygame
import sys
try:
    from .settings import *
    from .sprites import Player, Wall, Block
except ImportError:
    from settings import *
    from sprites import Player, Wall, Block

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Yeeps Prison Break")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 24)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # Simple Map: "P" = Player, "W" = Wall, "." = Empty, "E" = Exit
        # 20x15 grid (800x600 / 40)
        self.map_data = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W..................W",
            "W..................W",
            "W...P..............W",
            "W..................W",
            "W.......WWWW.......W",
            "W..................W",
            "W..................W",
            "WWWW...............W",
            "W..................W",
            "W........WW........W",
            "W..................W",
            "W....WWWW..........W",
            "W..................E",
            "WWWWWWWWWWWWWWWWWWWW",
        ]

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "W":
                    wall = Wall(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                elif tile == "P":
                    self.player = Player(col * TILE_SIZE, row * TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.all_sprites.add(self.player)
                elif tile == "E":
                    self.exit_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    self.place_block(pygame.mouse.get_pos())

    def place_block(self, pos):
        if self.player.inventory_blocks > 0:
            # Snap to grid
            x = (pos[0] // TILE_SIZE) * TILE_SIZE
            y = (pos[1] // TILE_SIZE) * TILE_SIZE

            # Check if occupied
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            # Avoid placing on player or existing walls
            if not self.player.rect.colliderect(rect):
                occupied = False
                for sprite in self.walls:
                    if sprite.rect.colliderect(rect):
                        occupied = True
                        break

                if not occupied:
                    block = Block(x, y)
                    self.walls.add(block)
                    self.all_sprites.add(block)
                    self.player.inventory_blocks -= 1

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.walls)

        # Check Win Condition
        if self.player.rect.colliderect(self.exit_rect):
            print("You Escaped!")
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Draw Exit
        pygame.draw.rect(self.screen, GREEN, self.exit_rect)

        # Draw UI
        text = self.font.render(f"Blocks: {self.player.inventory_blocks}", True, WHITE)
        self.screen.blit(text, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pygame.quit()
    sys.exit()
