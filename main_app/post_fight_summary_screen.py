# main_app/post_fight_summary_screen.py

import pygame
from button import Button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD

class PostFightSummaryScreen:
    """
    A screen displayed after a fight, showing rewards and offering next actions.
    """
    def __init__(self, game, asset_manager):
        self.game = game
        self.asset_manager = asset_manager
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((30, 30, 30))

        self.next_battle_button = Button(
            (SCREEN_WIDTH / 2) - 150, SCREEN_HEIGHT / 2 + 50, 300, 70, 
            "Next Battle", action=self.next_battle, asset_manager=asset_manager
        )
        self.back_to_world_button = Button(
            (SCREEN_WIDTH / 2) - 150, SCREEN_HEIGHT / 2 + 150, 300, 70, 
            "Back to World", action=lambda: self.game.change_state('game_world'), asset_manager=asset_manager
        )

    def next_battle(self):
        """Starts a new fight immediately."""
        if self.game.player:
            self.game.screens['fight'].start_new_fight(self.game.player)
            self.game.change_state('fight')

    def handle_events(self, events):
        for event in events:
            self.next_battle_button.handle_event(event)
            self.back_to_world_button.handle_event(event)

    def draw(self, screen):
        """Draws the summary screen."""
        self.background.set_alpha(200)
        screen.blit(self.background, (0, 0))
        
        if self.game.last_fight_rewards:
            monster_name = self.game.last_fight_rewards.get("monster_name", "Unknown Foe")
            xp_gained = self.game.last_fight_rewards.get("xp", 0)
            gold_gained = self.game.last_fight_rewards.get("gold", 0)
            items_gained = self.game.last_fight_rewards.get("items", [])
            rejected_items = self.game.last_fight_rewards.get("rejected_items", [])

            self.game.draw_text("Victory!", 'title', GOLD, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200)

            summary_text = (
                f"You defeated the {monster_name}!\n\n"
                f"You gained {xp_gained} XP.\n"
                f"You found {gold_gained} gold."
            )
            if items_gained:
                summary_text += "\nLoot: " + ", ".join(items_gained)
            if rejected_items:
                summary_text += "\n\nInventory full! Lost: " + ", ".join(rejected_items)

            self.game.draw_text(summary_text, 'large', WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)

        font_medium = self.asset_manager.get_font('medium')
        self.next_battle_button.draw(screen, font_medium)
        self.back_to_world_button.draw(screen, font_medium)