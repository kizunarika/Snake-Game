from data import *

from snake import Snake
from fruit import Fruit
from interface import Game_Over_Interface, Main_Menu_Interface


class Game:
    def __init__(self):
        pygame.init()

        # Initialize screen and time
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER)
        )
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)
        pygame.display.set_caption("Snake Game")

        # Initialize images
        self.images = {
            "grass": {
                "green": pygame.image.load("Graphics/grass/green grass.png").convert_alpha(),
                "dark": pygame.image.load("Graphics/grass/dark green grass.png").convert_alpha()
            },
            "snake": {},
            "skins": {
                "blue": pygame.image.load("Graphics/snake/Blue.png").convert_alpha(),
                "green": pygame.image.load("Graphics/snake/Green.png").convert_alpha()
            },
            "square button": {
                "normal": pygame.image.load("Graphics/square btn/normal.png").convert_alpha(),
                "hover": pygame.image.load("Graphics/square btn/hover.png").convert_alpha(),
                "click": pygame.image.load("Graphics/square btn/click.png").convert_alpha()
            },
            "triangle button": {
                "left": {
                    "normal": pygame.image.load("Graphics/triangle btn/normal.png").convert_alpha(),
                    "hover": pygame.image.load("Graphics/triangle btn/hover.png").convert_alpha(),
                    "click": pygame.image.load("Graphics/triangle btn/click.png").convert_alpha()
                },
                "right": {
                    "normal": pygame.transform.rotate(pygame.image.load("Graphics/triangle btn/normal.png").convert_alpha(), 180),
                    "hover": pygame.transform.rotate(pygame.image.load("Graphics/triangle btn/hover.png").convert_alpha(), 180),
                    "click": pygame.transform.rotate(pygame.image.load("Graphics/triangle btn/click.png").convert_alpha(), 180)
                }
            }
        }

        # Initialize game object
        self.fruit = Fruit()

        # Scores
        self.highest_score = 0
        self.current_score = 0

        # Status
        self.status = {
            "playing": False,
            "game_over": False,
            "main_menu": True,
        }

        # Interface resources
        self.font = pygame.font.Font("MinecraftRegular-Bmg3.otf", 28)

        # Interface objects
        self.game_over_interface = Game_Over_Interface(
            images=self.images["square button"],
            font=self.font,
            reset_callback=self.reset_game,
            back_menu_callback=self.back_menu
        )

        self.main_menu_interface = Main_Menu_Interface(
            images={"square button": self.images["square button"],
                    "triangle button": self.images["triangle button"],
                    "skins": self.images["skins"]},
            skins=["blue", "green"],
            font=self.font,
            start_callback=self.start_game
        )

    def run(self):
        """Main Game Loop"""
        while True:
            self.handle_events()
            self.draw_elements()

            pygame.display.update()
            self.clock.tick(30)

    def handle_events(self):
        """Game event handling"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == self.SCREEN_UPDATE and self.status["playing"]:
                self.update()

            elif self.status["playing"] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction.y != 1:
                    self.snake.direction = vector(0, -1)
                elif event.key == pygame.K_RIGHT and self.snake.direction.x != -1:
                    self.snake.direction = vector(1, 0)
                elif event.key == pygame.K_LEFT and self.snake.direction.x != 1 and self.snake.direction != vector(0, 0):
                    self.snake.direction = vector(-1, 0)
                elif event.key == pygame.K_DOWN and self.snake.direction.y != -1:
                    self.snake.direction = vector(0, 1)

            if self.status["main_menu"]:
                self.main_menu_interface.handle_event(event)
            if self.status["game_over"]:
                self.game_over_interface.handle_event(event)

    def update(self):
        """Game status update"""
        if self.status["playing"]:
            try:
                self.snake.move_snake()
                self.check_collision()
            except ValueError:
                self.game_over()

    def draw_elements(self):
        """Draw the main components of the game"""
        self.draw_grass()
        if not self.status["main_menu"]:
            self.fruit.draw_fruit(self.screen)
            self.snake.draw_snake(self.screen)
            self.draw_score()
        else:
            self.main_menu_interface.draw(self.screen)
        if self.status["game_over"]:
            self.game_over_interface.draw(self.screen, self.highest_score)

    def check_collision(self):
        """Check the collision between snake and fruit"""
        if self.snake.body[0] == self.fruit.pos:
            self.snake.add_block()
            self.fruit.randomize()
            self.current_score += 1

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def game_over(self):
        """Enable end game state"""
        self.highest_score = max(self.highest_score, self.current_score)
        self.current_score = 0

        self.status["playing"] = False
        self.status["game_over"] = True

    def start_game(self, skin: str):
        """Start the game"""
        self.status["main_menu"] = False
        self.status["playing"] = True

        # Load snake skin
        self.load_skin(skin)

        # Initialize game object
        self.snake = Snake(self.images["snake"][skin])

    def reset_game(self):
        """Restart the game"""
        self.snake.reset()
        self.fruit.randomize()
        self.current_score = 0
        self.status["playing"] = True
        self.status["game_over"] = False

    def draw_grass(self):
        """Grass background drawing"""
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                grass_color = "green" if (row + col) % 2 == 0 else "dark"
                grass_rect = pygame.Rect(
                    col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.screen.blit(self.images["grass"][grass_color], grass_rect)

    def draw_score(self):
        """Draw the score"""
        score_text = self.font.render(
            str(self.current_score), True, COLOR["white"])
        apple_rect = self.fruit.apple.get_rect(topleft=(10, 10))
        score_rect = score_text.get_rect(
            midleft=(apple_rect.right + 5, apple_rect.centery + 5))

        self.screen.blit(self.fruit.apple, apple_rect)
        self.screen.blit(score_text, score_rect)

    def back_menu(self):
        """Return to the main menu"""
        self.status["main_menu"] = True
        self.status["game_over"] = False

    def load_skin(self, skin: str):
        """Load the snake skin"""
        if skin not in self.images["snake"]:
            self.images["snake"][skin] = {
                "head": {
                    "up": pygame.image.load(f"Graphics/snake/{skin}SnakeHead.png").convert_alpha(),
                    "down": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeHead.png").convert_alpha(), 180),
                    "left": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeHead.png").convert_alpha(), 90),
                    "right": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeHead.png").convert_alpha(), 270)
                },
                "body": {
                    "vertical": pygame.image.load(f"Graphics/snake/{skin}SnakeBody.png").convert_alpha(),
                    "horizontal": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeBody.png").convert_alpha(), 90),
                    "corner": {
                        "tr": pygame.image.load(f"Graphics/snake/{skin}SnakeCorner.png").convert_alpha(),
                        "tl": pygame.transform.rotate(
                            pygame.image.load(f"Graphics/snake/{skin}SnakeCorner.png").convert_alpha(), 90),
                        "br": pygame.transform.rotate(
                            pygame.image.load(f"Graphics/snake/{skin}SnakeCorner.png").convert_alpha(), 270),
                        "bl": pygame.transform.rotate(
                            pygame.image.load(f"Graphics/snake/{skin}SnakeCorner.png").convert_alpha(), 180),
                    },
                },
                "tail": {
                    "up": pygame.image.load(f"Graphics/snake/{skin}SnakeTail.png").convert_alpha(),
                    "down": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeTail.png").convert_alpha(), 180),
                    "left": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeTail.png").convert_alpha(), 90),
                    "right": pygame.transform.rotate(
                        pygame.image.load(f"Graphics/snake/{skin}SnakeTail.png").convert_alpha(), 270),
                }
            }


if __name__ == "__main__":
    game = Game()
    game.run()
