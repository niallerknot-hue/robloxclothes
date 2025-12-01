import pygame
import sys
from game_manager import GameManager
import constants

def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Forsaken Py")
    clock = pygame.time.Clock()

    game_manager = GameManager(screen)

    while True:
        dt = clock.tick(constants.FPS)

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
