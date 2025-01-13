from data import *


class Snake:
    def __init__(self, images):
        # Snake state
        self.body = [vector(5, 10), vector(4, 10), vector(3, 10)]
        self.direction = vector(0, 0)
        self.new_block = False

        self.images = images
        self.head = self.images["head"]["up"]
        self.tail = self.images["tail"]["down"]

    def draw_snake(self, screen: pygame.Surface):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            elif index != 0:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                self.draw_body_part(screen, block_rect,
                                    previous_block, next_block)

        x_pos = int(self.body[0].x * CELL_SIZE)
        y_pos = int(self.body[0].y * CELL_SIZE)
        block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        screen.blit(self.head, block_rect)

    def draw_body_part(self, screen: pygame.Surface, rect, previous_block, next_block):
        if previous_block.x == next_block.x:
            screen.blit(self.images["body"]["vertical"], rect)
        elif previous_block.y == next_block.y:
            screen.blit(self.images["body"]["horizontal"], rect)
        else:
            corners = self.images["body"]["corner"]
            if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                screen.blit(corners["br"], rect)
            elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                screen.blit(corners["tl"], rect)
            elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                screen.blit(corners["bl"], rect)
            elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                screen.blit(corners["tr"], rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == vector(1, 0):
            self.head = self.images["head"]["left"]
        elif head_relation == vector(-1, 0):
            self.head = self.images["head"]["right"]
        elif head_relation == vector(0, 1):
            self.head = self.images["head"]["up"]
        elif head_relation == vector(0, -1):
            self.head = self.images["head"]["down"]

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == vector(1, 0):
            self.tail = self.images["tail"]["left"]
        elif tail_relation == vector(-1, 0):
            self.tail = self.images["tail"]["right"]
        elif tail_relation == vector(0, 1):
            self.tail = self.images["tail"]["up"]
        elif tail_relation == vector(0, -1):
            self.tail = self.images["tail"]["down"]

    def move_snake(self):
        next_pos = self.body[0] + self.direction
        # Check fail
        if self.direction != vector(0, 0) and self.check_fail(next_pos):
            raise ValueError("Game over")

        # Add block
        if self.new_block:
            self.body.insert(0, next_pos)
            self.new_block = False

        # Move snake
        elif self.direction != vector(0, 0):
            self.body.pop()
            self.body.insert(0, next_pos)

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [vector(5, 10), vector(4, 10), vector(3, 10)]
        self.direction = vector(0, 0)

    def check_fail(self, position: vector) -> bool:
        if not (0 <= position.x < CELL_NUMBER and 0 <= position.y < CELL_NUMBER):
            return True
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
        return False
