import pygame
import os
from constants import WHITE, BLACK, FONT_NAME

class InventoryScreen:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.selected_index = 0
        self.font = pygame.font.SysFont(FONT_NAME, 24)
        self.info_font = pygame.font.SysFont(FONT_NAME, 18)
        self.tooltip_font = pygame.font.SysFont(FONT_NAME, 16)
        self.bg_color = (30, 30, 30)
        self.slot_color = (60, 60, 60)
        self.selected_color = (120, 120, 180)
        self.text_color = WHITE
        self.margin = 40
        self.slot_height = 40
        self.info_box_width = 350
        self.item_icon_size = 32  # New size for item icons
        self.item_icons = self.load_item_icons()
        self.dragged_item = None
        self.dragged_item_pos = (0, 0)

    def load_item_icons(self):
        """Load item icons dynamically based on item type."""
        icons = {}
        icon_path = os.path.join("assets", "item_icons")
        default_icon = pygame.Surface((32, 32))  # Placeholder icon
        default_icon.fill((200, 200, 200))
        for item_type in ["weapon", "armor", "helmet", "shield", "accessory"]:
            try:
                icons[item_type] = pygame.image.load(os.path.join(icon_path, f"{item_type}.png"))
            except FileNotFoundError:
                icons[item_type] = default_icon
        return icons

    def draw_tooltip(self, surface, item, position):
        """Draw a tooltip with item details."""
        tooltip_x, tooltip_y = position
        tooltip_width = 200
        tooltip_height = 100
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        pygame.draw.rect(surface, (50, 50, 50), tooltip_rect)
        pygame.draw.rect(surface, WHITE, tooltip_rect, 2)

        lines = [item.name, f"Type: {item.item_type}", f"Value: {item.gold_value}g"]
        if hasattr(item, "attack_bonus") and item.attack_bonus:
            lines.append(f"Attack: +{item.attack_bonus}")
        if hasattr(item, "defense_bonus") and item.defense_bonus:
            lines.append(f"Defense: +{item.defense_bonus}")
        for i, line in enumerate(lines):
            text = self.tooltip_font.render(line, True, WHITE)
            surface.blit(text, (tooltip_x + 5, tooltip_y + 5 + i * 18))

    def handle_event(self, event):
        # Handle return button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            btn_x = self.margin
            btn_y = self.margin + 420
            btn_w = 180
            btn_h = 40
            if btn_x <= mx <= btn_x + btn_w and btn_y <= my <= btn_y + btn_h:
                self.game.return_to_game_world()
                return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = min(self.selected_index + 1, len(self.player.inventory) - 1)
            elif event.key == pygame.K_UP:
                self.selected_index = max(self.selected_index - 1, 0)
            elif event.key == pygame.K_RETURN:
                self.equip_selected_item()
            elif event.key == pygame.K_ESCAPE:
                self.game.return_to_game_world()
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            idx = (my - self.margin) // self.slot_height
            if 0 <= idx < len(self.player.inventory):
                self.selected_index = idx
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                # Check if click is on equipped items summary
                eq_x = self.margin + 420
                eq_y = self.margin + 220
                eq_height = 180
                eq_width = self.info_box_width
                if eq_x <= mx <= eq_x + eq_width and eq_y <= my <= eq_y + eq_height:
                    # Determine which slot was clicked
                    slot_idx = (my - eq_y - 10) // 22
                    slot_map = ["weapon", "armor", "helmet", "shield", "accessory"]
                    if 1 <= slot_idx <= 5:
                        slot = slot_map[slot_idx - 1]
                        eq_obj = getattr(self.player.equipment, slot, None)
                        if eq_obj:
                            unequipped = self.player.equipment.unequip(slot)
                            if unequipped:
                                self.player.inventory.append(unequipped)
                    return
                # Otherwise, equip item from inventory
                self.equip_selected_item()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            idx = (my - self.margin) // self.slot_height
            if 0 <= idx < len(self.player.inventory):
                self.dragged_item = self.player.inventory[idx]
                self.dragged_item_pos = (mx, my)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragged_item:
                mx, my = event.pos
                # Check if dropped on equipment slots
                eq_x = self.margin + 420
                eq_y = self.margin + 220
                eq_width = self.info_box_width
                eq_height = 180
                if eq_x <= mx <= eq_x + eq_width and eq_y <= my <= eq_y + eq_height:
                    slot_idx = (my - eq_y - 10) // 22
                    slot_map = ["weapon", "armor", "helmet", "shield", "accessory"]
                    if 1 <= slot_idx <= 5:
                        slot = slot_map[slot_idx - 1]
                        unequipped = self.player.equipment.equip(self.dragged_item)
                        if unequipped:
                            self.player.inventory.append(unequipped)
                        self.player.inventory.remove(self.dragged_item)
                self.dragged_item = None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragged_item:
                self.dragged_item_pos = event.pos

    def equip_selected_item(self):
        if self.player.inventory:
            item = self.player.inventory[self.selected_index]
            previous = self.player.equipment.equip(item)
            self.player.inventory.pop(self.selected_index)
            if previous:
                self.player.inventory.append(previous)

    def draw(self, surface):
        surface.fill(self.bg_color)
        # Draw inventory slots
        for i, item in enumerate(self.player.inventory):
            y = self.margin + i * self.slot_height
            rect = pygame.Rect(self.margin, y, 400, self.slot_height)
            color = self.selected_color if i == self.selected_index else self.slot_color
            pygame.draw.rect(surface, color, rect)

            # Draw item icon
            if item.item_type in self.item_icons:
                icon = self.item_icons[item.item_type]
                surface.blit(icon, (self.margin + 10, y + 4))

            # Draw item name
            text = self.font.render(item.name, True, self.text_color)
            surface.blit(text, (self.margin + 50, y + 8))

            # Draw tooltip if hovered
            mx, my = pygame.mouse.get_pos()
            if rect.collidepoint(mx, my):
                self.draw_tooltip(surface, item, (mx + 10, my + 10))

        # Draw info box for selected item
        if self.player.inventory and 0 <= self.selected_index < len(self.player.inventory):
            item = self.player.inventory[self.selected_index]
            info_x = self.margin + 420
            info_y = self.margin
            info_rect = pygame.Rect(info_x, info_y, self.info_box_width, 200)
            pygame.draw.rect(surface, (50, 50, 80), info_rect)
            lines = [item.name, f"Type: {item.item_type}", f"Value: {item.gold_value}g"]
            if hasattr(item, "attack_bonus") and item.attack_bonus:
                lines.append(f"Attack: +{item.attack_bonus}")
            if hasattr(item, "defense_bonus") and item.defense_bonus:
                lines.append(f"Defense: +{item.defense_bonus}")
            lines.append("")
            lines.append(item.description)
            for i, line in enumerate(lines):
                info_text = self.info_font.render(line, True, WHITE)
                surface.blit(info_text, (info_x + 10, info_y + 10 + i * 22))
        elif not self.player.inventory:
            info_x = self.margin + 420
            info_y = self.margin
            info_rect = pygame.Rect(info_x, info_y, self.info_box_width, 60)
            pygame.draw.rect(surface, (50, 50, 80), info_rect)
            info_text = self.info_font.render("Inventory is empty.", True, WHITE)
            surface.blit(info_text, (info_x + 10, info_y + 20))

        # Draw return button
        btn_x = self.margin
        btn_y = self.margin + 420
        btn_w = 180
        btn_h = 40
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(surface, (100, 60, 60), btn_rect)
        btn_text = self.font.render("Return", True, WHITE)
        surface.blit(btn_text, (btn_x + 30, btn_y + 8))

        # Draw equipped items summary
        eq_x = self.margin + 420
        eq_y = self.margin + 220
        eq_rect = pygame.Rect(eq_x, eq_y, self.info_box_width, 180)
        pygame.draw.rect(surface, (40, 60, 40), eq_rect)
        eq_lines = ["Equipped:"]
        eq = self.player.equipment
        eq_lines.append(f"Weapon: {eq.weapon.name if eq.weapon else '-'}")
        eq_lines.append(f"Armor: {eq.armor.name if eq.armor else '-'}")
        eq_lines.append(f"Helmet: {eq.helmet.name if eq.helmet else '-'}")
        eq_lines.append(f"Shield: {eq.shield.name if eq.shield else '-'}")
        eq_lines.append(f"Accessory: {eq.accessory.name if hasattr(eq, 'accessory') and eq.accessory else '-'}")
        for i, line in enumerate(eq_lines):
            eq_text = self.info_font.render(line, True, WHITE)
            surface.blit(eq_text, (eq_x + 10, eq_y + 10 + i * 22))

        # Draw dragged item
        if self.dragged_item:
            if self.dragged_item.item_type in self.item_icons:
                icon = self.item_icons[self.dragged_item.item_type]
                surface.blit(icon, self.dragged_item_pos)
            else:
                pygame.draw.rect(surface, (200, 200, 200), (*self.dragged_item_pos, 32, 32))
