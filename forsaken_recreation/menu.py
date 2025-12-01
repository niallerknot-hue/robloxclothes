import pygame
import constants

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
            self.gm.change_state(constants.STATE_LOBBY)
        elif self.options[self.selected_index] == "Shop":
            self.gm.change_state(constants.STATE_SHOP)
        elif self.options[self.selected_index] == "Quit":
            pygame.quit()
            import sys
            sys.exit()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(constants.BLACK)

        # Title
        title_surf = self.font.render("FORSAKEN PY", True, constants.RED)
        title_rect = title_surf.get_rect(center=(constants.SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        # Options
        for i, option in enumerate(self.options):
            color = constants.WHITE
            if i == self.selected_index:
                color = constants.YELLOW

            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(constants.SCREEN_WIDTH // 2, 300 + i * 60))
            screen.blit(text_surf, text_rect)
