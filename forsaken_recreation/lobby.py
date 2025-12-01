import pygame
import constants

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
                    self.gm.change_state(constants.STATE_MENU)
                    self.p1_ready = False
                    self.p2_ready = False

        if self.p1_ready and self.p2_ready:
            self.start_game()

    def start_game(self):
        self.gm.change_state(constants.STATE_GAME)
        self.p1_ready = False
        self.p2_ready = False

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(constants.DARK_GRAY)

        # Instructions
        info_text = self.font.render("P1: WASD + Space | P2: Arrows + Enter", True, constants.WHITE)
        screen.blit(info_text, (20, 20))

        # P1 Area
        p1_color = constants.GREEN if self.p1_ready else constants.WHITE
        p1_text = self.font.render(f"P1: {self.p1_selection}", True, p1_color)
        screen.blit(p1_text, (200, 300))

        # P2 Area
        p2_color = constants.RED if self.p2_ready else constants.WHITE
        p2_text = self.font.render(f"P2: {self.p2_selection}", True, p2_color)
        screen.blit(p2_text, (800, 300))

        if self.p1_ready and self.p2_ready:
            start_text = self.font.render("STARTING...", True, constants.YELLOW)
            screen.blit(start_text, (constants.SCREEN_WIDTH//2 - 50, 500))
