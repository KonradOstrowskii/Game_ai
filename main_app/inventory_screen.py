import pygame

class InventoryScreen:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.asset_manager = game.asset_manager  # Get asset_manager from game
        self.selected_index = 0
        self.font = self.asset_manager.get_font('small')
        self.info_font = self.asset_manager.get_font('small')
        self.tooltip_font = self.asset_manager.get_font('small')
        self.bg_color = (30, 30, 30)
        self.slot_color = (60, 60, 60)
        self.selected_color = (120, 120, 180)
        self.text_color = (255, 255, 255)
        self.margin = 40
        self.slot_height = 40
        self.info_box_width = 350
        self.item_icon_size = 32
        self.dragged_item = None
        self.dragged_item_pos = (0, 0)

    def get_item_icon(self, item_type):
        """Get the appropriate icon for an item type."""
        icon_key = f"{item_type}_icon"
        icon = self.asset_manager.get_image(icon_key)
        if icon:
            return icon
        # Fallback to general icon
        return self.asset_manager.get_image('potion_icon')  # Default fallback

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
                eq_height = 220  # Increased height to include quick slots
                if eq_x <= mx <= eq_x + eq_width and eq_y <= my <= eq_y + eq_height:
                    slot_idx = (my - eq_y - 10) // 22
                    if 1 <= slot_idx <= 5:
                        # Equipment slots
                        slot_map = ["weapon", "armor", "helmet", "shield", "accessory"]
                        slot = slot_map[slot_idx - 1]
                        unequipped = self.player.equipment.equip(self.dragged_item)
                        if unequipped:
                            self.player.inventory.append(unequipped)
                        self.player.inventory.remove(self.dragged_item)
                    elif 7 <= slot_idx <= 10:
                        # Quick slots (after empty line at index 6)
                        quick_slot_idx = slot_idx - 7
                        if self.dragged_item.item_type == "potion":
                            # Swap with existing item in quick slot
                            existing_item = self.player.equipment.quick_slots[quick_slot_idx]
                            self.player.equipment.quick_slots[quick_slot_idx] = self.dragged_item
                            if existing_item:
                                self.player.inventory.append(existing_item)
                            self.player.inventory.remove(self.dragged_item)
                        else:
                            # Non-potion items can't go in quick slots
                            pass
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
        
        # Draw inventory header with capacity
        header_text = f"Inventory ({len(self.player.inventory)}/{self.player.max_inventory_slots})"
        header_font = self.asset_manager.get_font('large') if hasattr(self, 'asset_manager') else self.font
        header_surface = header_font.render(header_text, True, WHITE)
        surface.blit(header_surface, (self.margin, self.margin - 40))
        
        # Draw inventory slots
        for i, item in enumerate(self.player.inventory):
            y = self.margin + i * self.slot_height
            rect = pygame.Rect(self.margin, y, 400, self.slot_height)
            color = self.selected_color if i == self.selected_index else self.slot_color
            pygame.draw.rect(surface, color, rect)

            # Draw item icon
            icon = self.get_item_icon(item.item_type)
            if icon:
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
        eq_rect = pygame.Rect(eq_x, eq_y, self.info_box_width, 220)  # Increased height
        pygame.draw.rect(surface, (40, 60, 40), eq_rect)
        eq_lines = ["Equipped:"]
        eq = self.player.equipment
        eq_lines.append(f"Weapon: {eq.weapon.name if eq.weapon else '-'}")
        eq_lines.append(f"Armor: {eq.armor.name if eq.armor else '-'}")
        eq_lines.append(f"Helmet: {eq.helmet.name if eq.helmet else '-'}")
        eq_lines.append(f"Shield: {eq.shield.name if eq.shield else '-'}")
        eq_lines.append(f"Accessory: {eq.accessory.name if hasattr(eq, 'accessory') and eq.accessory else '-'}")
        eq_lines.append("")  # Empty line
        eq_lines.append("Quick Slots:")
        for i, slot in enumerate(eq.quick_slots):
            eq_lines.append(f"Slot {i+1}: {slot.name if slot else '-'}")
        for i, line in enumerate(eq_lines):
            eq_text = self.info_font.render(line, True, WHITE)
            surface.blit(eq_text, (eq_x + 10, eq_y + 10 + i * 22))

        # Draw dragged item
        if self.dragged_item:
            icon = self.get_item_icon(self.dragged_item.item_type)
            if icon:
                surface.blit(icon, self.dragged_item_pos)
            else:
                pygame.draw.rect(surface, (200, 200, 200), (*self.dragged_item_pos, 32, 32))
