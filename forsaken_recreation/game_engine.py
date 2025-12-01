import pygame
import constants
from player import Survivor, Killer
from level import Level

class GameEngine:
    def __init__(self, game_manager, p1_char, p2_char):
        self.gm = game_manager

        # Initialize Level
        self.level = Level()

        # Initialize Players
        # Spawn points (simplified)
        self.p1 = self.create_player(p1_char, 100, 100, "p1")
        self.p2 = self.create_player(p2_char, 1100, 600, "p2")

        self.game_over = False
        self.winner = None

    def create_player(self, char_type, x, y, player_id):
        if char_type == "Survivor":
            return Survivor(x, y, player_id)
        elif char_type == "Killer":
            return Killer(x, y, player_id)
        return Survivor(x, y, player_id) # Default

    def handle_input(self, events):
        keys = pygame.key.get_pressed()
        self.p1.handle_input(keys)
        self.p2.handle_input(keys)

        for event in events:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gm.change_state(constants.STATE_MENU)

    def update(self, dt):
        if self.game_over:
            return

        self.p1.update(dt, self.level.walls)
        self.p2.update(dt, self.level.walls)

        self.check_collisions()
        self.check_win_conditions()

    def check_collisions(self):
        # Check interactions
        # Example: Killer catches Survivor
        if isinstance(self.p1, Killer) and isinstance(self.p2, Survivor):
            if self.p1.rect.colliderect(self.p2.rect):
                self.p2.take_damage(1)
        elif isinstance(self.p2, Killer) and isinstance(self.p1, Survivor):
            if self.p2.rect.colliderect(self.p1.rect):
                self.p1.take_damage(1)

        # Check Key Collection (Survivor only)
        survivor = None
        if isinstance(self.p1, Survivor):
            survivor = self.p1
        elif isinstance(self.p2, Survivor):
            survivor = self.p2

        if survivor:
            for key in self.level.keys[:]:
                if survivor.rect.colliderect(key):
                    self.level.keys.remove(key)
                    # Play sound?
                    print("Key collected!")

    def check_win_conditions(self):
        if self.p1.health <= 0:
            self.game_over = True
            self.winner = "Player 2"
            self.award_currency()
        elif self.p2.health <= 0:
            self.game_over = True
            self.winner = "Player 1"
            self.award_currency()

        # Check if survivor collected all keys
        if not self.level.keys:
            # Survivor wins
            self.game_over = True
            if isinstance(self.p1, Survivor):
                self.winner = "Player 1"
            else:
                self.winner = "Player 2"
            self.award_currency()

    def award_currency(self):
        # Award 50 coins to everyone for playing, maybe more for winner?
        # For simplicity, just add 50 coins.
        self.gm.game_data["coins"] += 50
        self.gm.save_data()

    def draw(self, screen):
        self.level.draw(screen)
        self.p1.draw(screen)
        self.p2.draw(screen)

        # UI
        self.draw_ui(screen)

        if self.game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render(f"{self.winner} Wins!", True, constants.YELLOW)
            rect = text.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2))
            screen.blit(text, rect)

    def draw_ui(self, screen):
        font = pygame.font.SysFont(None, 24)
        p1_hp = font.render(f"P1 HP: {self.p1.health}", True, constants.WHITE)
        p2_hp = font.render(f"P2 HP: {self.p2.health}", True, constants.WHITE)
        screen.blit(p1_hp, (10, 10))
        screen.blit(p2_hp, (constants.SCREEN_WIDTH - 100, 10))
