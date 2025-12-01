import pygame
import sys
import json
import os

# ==========================================
# CONSTANTS
# ==========================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Game States
STATE_MENU = "menu"
STATE_LOBBY = "lobby"
STATE_GAME = "game"
STATE_SHOP = "shop"
STATE_GAMEOVER = "gameover"

# Map
TILE_SIZE = 40

# ==========================================
# LEVEL
# ==========================================
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
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif tile == "K":
                    pass

        # Manually add some keys for now
        self.keys = [
            pygame.Rect(200, 200, 20, 20),
            pygame.Rect(1000, 200, 20, 20),
            pygame.Rect(600, 500, 20, 20)
        ]

    def draw(self, screen):
        # Draw floor
        screen.fill(DARK_GRAY)

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, GRAY, wall)

        # Draw keys
        for key in self.keys:
            pygame.draw.rect(screen, YELLOW, key)

# ==========================================
# PLAYER
# ==========================================
class Player:
    def __init__(self, x, y, player_id):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.player_id = player_id
        self.color = WHITE
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
        self.color = GREEN
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
        self.color = RED
        self.health = 1000 # Invincible basically
        self.speed = 220
        self.cooldown = 0

    def use_ability(self):
        # Dash attack or Sense
        if self.cooldown <= 0:
            # Simple color change to indicate ability
            self.color = PURPLE
            self.cooldown = 30
            print(f"{self.player_id} used Ability!")

    def update(self, dt, walls):
        super().update(dt, walls)
        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.color = RED

# ==========================================
# GAME ENGINE
# ==========================================
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
                    self.gm.change_state(STATE_MENU)

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
            text = font.render(f"{self.winner} Wins!", True, YELLOW)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, rect)

    def draw_ui(self, screen):
        font = pygame.font.SysFont(None, 24)
        p1_hp = font.render(f"P1 HP: {self.p1.health}", True, WHITE)
        p2_hp = font.render(f"P2 HP: {self.p2.health}", True, WHITE)
        screen.blit(p1_hp, (10, 10))
        screen.blit(p2_hp, (SCREEN_WIDTH - 100, 10))

# ==========================================
# MENUS
# ==========================================
class Menu:
    def __init__(self, game_manager):
        self.gm = game_manager
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Play", "Shop", "Quit"]
        self.selected_index = 0

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def select_option(self):
        if self.options[self.selected_index] == "Play":
            self.gm.change_state(STATE_LOBBY)
        elif self.options[self.selected_index] == "Shop":
            self.gm.change_state(STATE_SHOP)
        elif self.options[self.selected_index] == "Quit":
            pygame.quit()
            sys.exit()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        # Title
        title_surf = self.font.render("FORSAKEN PY", True, RED)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        # Options
        for i, option in enumerate(self.options):
            color = WHITE
            if i == self.selected_index:
                color = YELLOW

            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            screen.blit(text_surf, text_rect)

class Lobby:
    def __init__(self, game_manager):
        self.gm = game_manager
        self.font = pygame.font.SysFont(None, 36)

        # Available characters
        self.characters = ["Survivor", "Killer"]

        self.p1_selection_idx = 0
        self.p2_selection_idx = 1 # Default to Killer

        self.p1_ready = False
        self.p2_ready = False

    @property
    def p1_selection(self):
        return self.characters[self.p1_selection_idx]

    @property
    def p2_selection(self):
        return self.characters[self.p2_selection_idx]

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # P1 Controls (WASD + Space)
                if not self.p1_ready:
                    if event.key == pygame.K_a:
                        self.p1_selection_idx = (self.p1_selection_idx - 1) % len(self.characters)
                    elif event.key == pygame.K_d:
                        self.p1_selection_idx = (self.p1_selection_idx + 1) % len(self.characters)
                    elif event.key == pygame.K_SPACE:
                        self.p1_ready = True
                elif event.key == pygame.K_SPACE:
                    self.p1_ready = False # Unready

                # P2 Controls (Arrows + Enter)
                if not self.p2_ready:
                    if event.key == pygame.K_LEFT:
                        self.p2_selection_idx = (self.p2_selection_idx - 1) % len(self.characters)
                    elif event.key == pygame.K_RIGHT:
                        self.p2_selection_idx = (self.p2_selection_idx + 1) % len(self.characters)
                    elif event.key == pygame.K_RETURN:
                        self.p2_ready = True
                elif event.key == pygame.K_RETURN:
                    self.p2_ready = False # Unready

                # Back to menu
                if event.key == pygame.K_ESCAPE:
                    self.gm.change_state(STATE_MENU)
                    self.p1_ready = False
                    self.p2_ready = False

        if self.p1_ready and self.p2_ready:
            self.start_game()

    def start_game(self):
        self.gm.change_state(STATE_GAME)
        self.p1_ready = False
        self.p2_ready = False

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(DARK_GRAY)

        # Instructions
        info_text = self.font.render("P1: WASD + Space | P2: Arrows + Enter", True, WHITE)
        screen.blit(info_text, (20, 20))

        # P1 Area
        p1_color = GREEN if self.p1_ready else WHITE
        p1_text = self.font.render(f"P1: {self.p1_selection}", True, p1_color)
        screen.blit(p1_text, (200, 300))

        # P2 Area
        p2_color = RED if self.p2_ready else WHITE
        p2_text = self.font.render(f"P2: {self.p2_selection}", True, p2_color)
        screen.blit(p2_text, (800, 300))

        if self.p1_ready and self.p2_ready:
            start_text = self.font.render("STARTING...", True, YELLOW)
            screen.blit(start_text, (SCREEN_WIDTH//2 - 50, 500))

class Shop:
    def __init__(self, game_manager):
        self.gm = game_manager
        self.font = pygame.font.SysFont(None, 40)
        self.skins = [
            {"name": "default", "cost": 0},
            {"name": "blue_suit", "cost": 50},
            {"name": "red_mask", "cost": 100},
            {"name": "gold_aura", "cost": 500}
        ]
        self.selected_idx = 0
        self.message = ""

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_idx = (self.selected_idx - 1) % len(self.skins)
                    self.message = ""
                elif event.key == pygame.K_DOWN:
                    self.selected_idx = (self.selected_idx + 1) % len(self.skins)
                    self.message = ""
                elif event.key == pygame.K_RETURN:
                    self.buy_or_equip()
                elif event.key == pygame.K_ESCAPE:
                    self.gm.change_state(STATE_MENU)
                    self.message = ""

    def buy_or_equip(self):
        skin_data = self.skins[self.selected_idx]
        skin_name = skin_data["name"]
        cost = skin_data["cost"]

        if skin_name in self.gm.game_data["unlocked_skins"]:
            self.message = f"Equipped {skin_name} (Global)"
            self.message = "Already owned!"
        else:
            if self.gm.game_data["coins"] >= cost:
                self.gm.game_data["coins"] -= cost
                self.gm.game_data["unlocked_skins"].append(skin_name)
                self.gm.save_data()
                self.message = f"Purchased {skin_name}!"
            else:
                self.message = "Not enough coins!"

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        title = self.font.render(f"Shop - Coins: {self.gm.game_data['coins']}", True, YELLOW)
        screen.blit(title, (20, 20))

        for i, skin in enumerate(self.skins):
            name = skin["name"]
            cost = skin["cost"]

            color = WHITE
            if i == self.selected_idx:
                color = GREEN

            status = "Locked"
            if name in self.gm.game_data["unlocked_skins"]:
                status = "Owned"

            text_str = f"{name} - {cost} coins [{status}]"
            text = self.font.render(text_str, True, color)
            screen.blit(text, (100, 100 + i * 50))

        if self.message:
            msg_surf = self.font.render(self.message, True, RED)
            screen.blit(msg_surf, (500, 100))

        help_text = self.font.render("Press Enter to Buy. ESC to return.", True, GRAY)
        screen.blit(help_text, (20, SCREEN_HEIGHT - 50))

# ==========================================
# GAME MANAGER
# ==========================================
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = STATE_MENU

        self.data_file = "save_data.json"

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
        if new_state == STATE_GAME:
            # Initialize new game with selections from lobby
            p1_char = self.lobby.p1_selection
            p2_char = self.lobby.p2_selection
            self.game_engine = GameEngine(self, p1_char, p2_char)

    def handle_input(self, events):
        if self.state == STATE_MENU:
            self.menu.handle_input(events)
        elif self.state == STATE_LOBBY:
            self.lobby.handle_input(events)
        elif self.state == STATE_GAME:
            if self.game_engine:
                self.game_engine.handle_input(events)
        elif self.state == STATE_SHOP:
            self.shop.handle_input(events)

    def update(self, dt):
        if self.state == STATE_MENU:
            self.menu.update(dt)
        elif self.state == STATE_LOBBY:
            self.lobby.update(dt)
        elif self.state == STATE_GAME:
            if self.game_engine:
                self.game_engine.update(dt)
        elif self.state == STATE_SHOP:
            self.shop.update(dt)

    def draw(self, screen):
        screen.fill(BLACK)
        if self.state == STATE_MENU:
            self.menu.draw(screen)
        elif self.state == STATE_LOBBY:
            self.lobby.draw(screen)
        elif self.state == STATE_GAME:
            if self.game_engine:
                self.game_engine.draw(screen)
        elif self.state == STATE_SHOP:
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

# ==========================================
# MAIN
# ==========================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Forsaken Py")
    clock = pygame.time.Clock()

    game_manager = GameManager(screen)

    while True:
        dt = clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_manager.handle_input(events)
        game_manager.update(dt)
        game_manager.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
