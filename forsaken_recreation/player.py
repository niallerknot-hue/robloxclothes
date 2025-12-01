import pygame
import constants

class Player:
    def __init__(self, x, y, player_id):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.player_id = player_id
        self.color = constants.WHITE
        self.speed = 300
        self.health = 100
        self.max_health = 100
        self.velocity = pygame.math.Vector2(0, 0)

    def handle_input(self, keys):
        self.velocity.x = 0
        self.velocity.y = 0

        if self.player_id == "p1":
            if keys[pygame.K_w]: self.velocity.y = -1
            if keys[pygame.K_s]: self.velocity.y = 1
            if keys[pygame.K_a]: self.velocity.x = -1
            if keys[pygame.K_d]: self.velocity.x = 1
            # Ability
            if keys[pygame.K_q]: self.use_ability()

        elif self.player_id == "p2":
            if keys[pygame.K_UP]: self.velocity.y = -1
            if keys[pygame.K_DOWN]: self.velocity.y = 1
            if keys[pygame.K_LEFT]: self.velocity.x = -1
            if keys[pygame.K_RIGHT]: self.velocity.x = 1
            # Ability
            if keys[pygame.K_RSHIFT]: self.use_ability()

        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

    def update(self, dt, walls):
        # Move X
        self.rect.x += self.velocity.x * (dt / 1000)
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity.x > 0:
                    self.rect.right = wall.left
                if self.velocity.x < 0:
                    self.rect.left = wall.right

        # Move Y
        self.rect.y += self.velocity.y * (dt / 1000)
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity.y > 0:
                    self.rect.bottom = wall.top
                if self.velocity.y < 0:
                    self.rect.top = wall.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def use_ability(self):
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

class Survivor(Player):
    def __init__(self, x, y, player_id):
        super().__init__(x, y, player_id)
        self.color = constants.GREEN
        self.health = 3
        self.speed = 200 # Slower than killer generally
        self.cooldown = 0

    def use_ability(self):
        # Sprint burst
        if self.cooldown <= 0:
            self.speed = 400
            self.cooldown = 60 # frames? need proper timer
            print(f"{self.player_id} used Sprint!")

    def update(self, dt, walls):
        super().update(dt, walls)
        if self.speed > 200:
            self.speed -= 5 # Decay speed boost

        if self.cooldown > 0:
            self.cooldown -= 1

class Killer(Player):
    def __init__(self, x, y, player_id):
        super().__init__(x, y, player_id)
        self.color = constants.RED
        self.health = 1000 # Invincible basically
        self.speed = 220
        self.cooldown = 0

    def use_ability(self):
        # Dash attack or Sense
        if self.cooldown <= 0:
            # Simple color change to indicate ability
            self.color = constants.PURPLE
            self.cooldown = 30
            print(f"{self.player_id} used Ability!")

    def update(self, dt, walls):
        super().update(dt, walls)
        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.color = constants.RED
