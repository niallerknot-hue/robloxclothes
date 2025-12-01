import pygame
import constants

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
                    self.gm.change_state(constants.STATE_MENU)
                    self.message = ""

    def buy_or_equip(self):
        skin_data = self.skins[self.selected_idx]
        skin_name = skin_data["name"]
        cost = skin_data["cost"]

        if skin_name in self.gm.game_data["unlocked_skins"]:
            self.message = f"Equipped {skin_name} (Global)"
            # For simplicity, equipping sets it as default for p1/p2 or we could have skin selection in lobby
            # Let's just say this sets the 'preferred' skin or similar, or just unlocks it.
            # But the prompt asks for "purchasable skins".
            # I will set it for both P1 and P2 for now as a global override or just show it's owned.
            # In a real game, Lobby would select skins.
            # Let's just confirm it is unlocked.
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
        screen.fill(constants.BLACK)

        title = self.font.render(f"Shop - Coins: {self.gm.game_data['coins']}", True, constants.YELLOW)
        screen.blit(title, (20, 20))

        for i, skin in enumerate(self.skins):
            name = skin["name"]
            cost = skin["cost"]

            color = constants.WHITE
            if i == self.selected_idx:
                color = constants.GREEN

            status = "Locked"
            if name in self.gm.game_data["unlocked_skins"]:
                status = "Owned"

            text_str = f"{name} - {cost} coins [{status}]"
            text = self.font.render(text_str, True, color)
            screen.blit(text, (100, 100 + i * 50))

        if self.message:
            msg_surf = self.font.render(self.message, True, constants.RED)
            screen.blit(msg_surf, (500, 100))

        help_text = self.font.render("Press Enter to Buy. ESC to return.", True, constants.GRAY)
        screen.blit(help_text, (20, constants.SCREEN_HEIGHT - 50))
