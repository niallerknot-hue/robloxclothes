import pygame
try:
    from .settings import *
except ImportError:
    from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, map_width, map_height):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.on_wall = False
        self.wall_dir = 0  # -1 for left wall, 1 for right wall
        self.map_width = map_width
        self.map_height = map_height
        self.inventory_blocks = 10  # Start with some blocks

        # Physics tweak: track intended move direction separate from velocity
        self.acceleration = pygame.math.Vector2(0, 0)

    def update(self, keys, walls):
        # Calculate acceleration based on input
        self.acceleration.x = 0
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -0.5  # Acceleration speed
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = 0.5

        # Apply friction
        self.acceleration.x += self.velocity.x * -0.1

        # Apply acceleration to velocity
        self.velocity.x += self.acceleration.x

        # Cap speed (if necessary, but friction handles it mostly)
        if abs(self.velocity.x) < 0.1:
             self.velocity.x = 0

        # Hard cap for max speed to keep it snappy
        if self.velocity.x > PLAYER_SPEED:
            self.velocity.x = PLAYER_SPEED
        if self.velocity.x < -PLAYER_SPEED:
            self.velocity.x = -PLAYER_SPEED

        # Apply Gravity
        self.velocity.y += GRAVITY

        # Wall slide logic
        self.on_wall = False
        self.wall_dir = 0

        # Move X
        self.rect.x += self.velocity.x
        hits = pygame.sprite.spritecollide(self, walls, False)
        for wall in hits:
            if self.velocity.x > 0:
                self.rect.right = wall.rect.left
                self.on_wall = True
                self.wall_dir = 1
                self.velocity.x = 0
            elif self.velocity.x < 0:
                self.rect.left = wall.rect.right
                self.on_wall = True
                self.wall_dir = -1
                self.velocity.x = 0

        # Keep inside map
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > self.map_width:
            self.rect.right = self.map_width
            self.velocity.x = 0

        # Move Y
        self.rect.y += self.velocity.y
        hits = pygame.sprite.spritecollide(self, walls, False)
        self.on_ground = False
        for wall in hits:
            if self.velocity.y > 0:
                self.rect.bottom = wall.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = wall.rect.bottom
                self.velocity.y = 0

        if self.rect.bottom >= self.map_height:
             self.rect.bottom = self.map_height
             self.velocity.y = 0
             self.on_ground = True

        # Wall Sliding
        if self.on_wall and not self.on_ground and self.velocity.y > 0:
             # Slower slide
             if self.velocity.y > WALL_SLIDE_SPEED:
                 self.velocity.y = WALL_SLIDE_SPEED

    def jump(self):
        if self.on_ground:
            self.velocity.y = PLAYER_JUMP
        elif self.on_wall:
            self.velocity.y = PLAYER_JUMP
            # Jump away from wall
            self.velocity.x = -self.wall_dir * WALL_JUMP_FORCE
            # Debug print
            print(f"Wall jump! Dir: {self.wall_dir}, VelX: {self.velocity.x}")

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GRAY):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Block(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, BROWN)
