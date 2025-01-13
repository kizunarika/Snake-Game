from data import *


class Button:
    def __init__(self, x, y, font, images: dict, callback: lambda: None, text=None):
        """
        :param x, y: Tọa độ trung tâm của nút
        :param text: Nội dung văn bản trên nút
        :param font: Font để hiển thị văn bản
        :param images: Dict chứa các hình ảnh của nút (normal, hover, clicked)
        :param callback: Hàm sẽ được gọi khi nút được nhấn
        """
        self.rect = images["normal"].get_rect(center=(x, y))
        self.text = text
        self.font = font
        self.images = images
        self.callback = callback
        self.state = "normal"

    def handle_event(self, event: pygame.event.Event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = "click"
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == "click" and self.rect.collidepoint(event.pos):
                self.callback()
            self.state = "normal"

    def update(self):
        """Update the button state"""
        if self.state != "click":
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.state = "hover"
            else:
                self.state = "normal"

    def draw(self, screen: pygame.Surface):
        """Draw the button"""
        image = self.images[self.state]
        screen.blit(image, self.rect)

        # Vẽ văn bản
        if self.text is not None:
            text_surface = self.font.render(self.text, True, COLOR["black"])
            text_rect = text_surface.get_rect(
                center=(self.rect.centerx, self.rect.centery+3))
            screen.blit(text_surface, text_rect)


class Game_Over_Interface:
    def __init__(self, images, font, reset_callback, back_menu_callback):
        """
        :param font: Font chữ
        :param images: Dict chứa hình ảnh của nút
        :param reset_callback: Hàm gọi lại khi nhấn Continue
        :param back_menu_callback: Hàm gọi lại khi nhấn Home
        """
        self.font = font
        self.images = images

        # Initialize buttons
        self.buttons: list[Button] = []
        middle = CELL_NUMBER * CELL_SIZE / 2
        self.buttons.append(Button(
            middle, middle,
            text="Continue",
            font=self.font,
            images=self.images,
            callback=reset_callback
        ))
        self.buttons.append(Button(
            middle, middle + 100,
            text="Exit",
            font=self.font,
            images=self.images,
            callback=lambda: (pygame.quit(), exit())
        ))
        self.buttons.append(Button(
            middle, middle + 50,
            text="Home",
            font=self.font,
            images=self.images,
            callback=back_menu_callback
        ))

    def draw(self, screen, highest_score):
        """Draw the end game interface"""
        # Draw overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.fill(COLOR["black"])
        overlay.set_alpha(ALPHA_VALUE_OVERLAY)
        screen.blit(overlay, (0, 0))

        middle = CELL_NUMBER * CELL_SIZE / 2

        # Draw text
        game_over_text = self.font.render("Game Over!", True, COLOR["white"])
        score_text = self.font.render(
            f"Highest Score: {highest_score}", True, COLOR["white"])
        screen.blit(game_over_text, game_over_text.get_rect(
            center=(middle, middle - 100)))
        screen.blit(score_text, score_text.get_rect(
            center=(middle, middle - 60)))

        # Draw buttons
        for button in self.buttons:
            button.update()
            button.draw(screen)

    def handle_event(self, event):
        """Handle mouse events"""
        for button in self.buttons:
            button.handle_event(event)


class Main_Menu_Interface:
    def __init__(self, images, skins, font, start_callback):
        """
        :param font: Font chữ
        :param start_callback: Hàm gọi lại khi nhấn Start
        :param images: Dict chứa hình ảnh của nút hình vuông {square btn, triangle btn, skins}
        :param skins: List chứa tên các skin của rắn
        """
        self.font = font
        self.start_callback = start_callback
        self.images = images
        self.skins = skins
        self.large_font = pygame.font.Font("MinecraftRegular-Bmg3.otf", 50)

        self.current_skin_index = 0

        # Initialize buttons
        self.buttons: list[Button] = []
        middle = CELL_NUMBER * CELL_SIZE / 2
        # previous button
        self.buttons.append(Button(
            x=middle-150, y=middle-100,
            font=self.font,
            images=self.images["triangle button"]["left"],
            callback=self.prev_skin
        ))
        # next button
        self.buttons.append(Button(
            x=middle + 150, y=middle-100,
            font=self.font,
            images=self.images["triangle button"]["right"],
            callback=self.next_skin
        ))
        # start button
        self.buttons.append(Button(
            x=middle, y=middle + 50,
            text="Start",
            font=self.font,
            images=self.images["square button"],
            callback=self.start_game
        ))
        # exit button
        self.buttons.append(Button(
            x=middle, y=middle + 100,
            text="Exit",
            font=self.font,
            images=self.images["square button"],
            callback=lambda: (pygame.quit(), exit())
        ))

    def prev_skin(self):
        """Move to the previous skin"""
        self.current_skin_index = (
            self.current_skin_index - 1) % len(self.skins)

    def next_skin(self):
        """Move to the next skin"""
        self.current_skin_index = (
            self.current_skin_index + 1) % len(self.skins)

    def start_game(self):
        """Start the game with the selected skin"""
        self.start_callback(self.skins[self.current_skin_index])

    def handle_event(self, event):
        """Handle mouse events"""
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen):
        """Draw the skin selector interface"""
        # Draw overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.fill(COLOR["black"])
        overlay.set_alpha(ALPHA_VALUE_OVERLAY)
        screen.blit(overlay, (0, 0))

        middle = CELL_NUMBER * CELL_SIZE / 2

        # Draw text
        text = self.large_font.render("Snake Game", True, COLOR["white"])
        screen.blit(text, text.get_rect(center=(middle, middle-200)))

        # Show skin
        skin_rect = self.images["skins"][self.skins[self.current_skin_index]].get_rect(
            center=(middle, middle-100))
        screen.blit(
            self.images["skins"][self.skins[self.current_skin_index]], skin_rect)

        # Draw buttons
        for button in self.buttons:
            button.update()
            button.draw(screen)
