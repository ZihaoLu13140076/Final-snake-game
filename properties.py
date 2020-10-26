import pygame
import random

# Gloabal variables - colors
BG_COLOR = (232, 232, 232)
SCORE_TEXT_COLOR = (255, 255, 255)
TIP_TEXT_COLOR = (255, 255, 255)
TIP_OFF_TEXT_COLOR = (255, 97, 0)
INSTRUCTION_TEXT_COLOR = (255, 97, 0)
SNAKE_COLOR = (255, 97, 0)
SNAKE_HEAD_COLOR = (237, 145, 33)
FOOD_COLOR = (255, 97, 0)

# Gloabal variables - sizes
SCREEN_RECT = pygame.Rect(0, 0, 640, 480)
CELL_SIZE = 20

# user events
FOOD_UPDATE_EVENT = pygame.USEREVENT
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1
TEXT_BLINK_EVENT = pygame.USEREVENT + 2


class Label:
    """
    Label(text) displayed on the screen
    """
    def __init__(self, size=48, font_type=0):
        """
        Label initialization

        :param size: font size of lable
        :param font_type: label type, different type has different color and position on the screen,
        """
        self.font = pygame.font.SysFont('bauhaus 93', size)
        self.font_type = font_type
        self.interval = 500

    def draw(self, window, text):
        """
        Draw the label on window

        :param window: where label displayed on
        :param text: the text content of the label
        :return: None
        """
        if self.font_type == 0:
            color = SCORE_TEXT_COLOR
        elif self.font_type == 1:
            color = TIP_TEXT_COLOR
        elif self.font_type == -1:
            color = TIP_OFF_TEXT_COLOR
        else:
            color = INSTRUCTION_TEXT_COLOR
        text_surface = self.font.render(text, True, color)

        text_rect = text_surface.get_rect()
        window_rect = window.get_rect()
        # 0 for score
        if self.font_type == 0:
            text_rect.y = window_rect.height - text_rect.height - 10
            text_rect.x = 10
        # 1 for tip
        elif self.font_type == 1 or self.font_type == -1:
            text_rect.x = (window_rect.width - text_rect.width) / 2
            text_rect.y = (window_rect.height - text_rect.height) / 2
        # 2 for instruction
        elif self.font_type == 2:
            text_rect.x = (window_rect.width - text_rect.width) / 2
            text_rect.y = (window_rect.height - text_rect.height) / 2 - 100
        window.blit(text_surface, text_rect)

class Food:
    """
    Snake food displayed on the screen
    """
    def __init__(self):
        """
        Food initialization, and random its position
        """
        self.color = FOOD_COLOR
        self.score = random.randint(1, 5)
        self.rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)
        self.random_pos()

    def draw(self, window):
        """
        Display the food on the window
        :param window: where the food is displayed
        :return: None
        """
        if self.rect.w < CELL_SIZE:
            self.rect.inflate_ip(2, 2)
        pygame.draw.ellipse(window, self.color, self.rect)

    def random_pos(self):
        """
        Randomly set the position of food, set a timer of  FOOD_UPDATE_EVENT to update the food position

        :return: None
        """
        col = SCREEN_RECT.w / CELL_SIZE - 1
        row = SCREEN_RECT.h/ CELL_SIZE - 1

        x = random.randint(0, col) * CELL_SIZE
        y = random.randint(0, row) * CELL_SIZE
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        # animation of display the food from small to big
        self.rect.inflate_ip(-CELL_SIZE, -CELL_SIZE)

        pygame.time.set_timer(FOOD_UPDATE_EVENT, 10000)


class Snake:
    """
    Snake displayed on the window.
    It's a list of nodes, each node is a square (has position) on the window.
    """
    def __init__(self):
        """
        Snake initialization as 3 nodes
        """
        self.orientation = pygame.K_RIGHT
        self.time_interval = 300
        self.score = 0
        self.color = SNAKE_COLOR
        self.body_list = []
        self.reset_snake()

    def reset_snake(self):
        """
        Reset the snake as 3 nodes if new game

        :return: None
        """
        self.orientation = pygame.K_RIGHT
        self.score = 0
        self.time_interval = 300
        self.body_list.clear()
        for i in range(3):
            self.add_node()

    def add_node(self):
        """
        Add a node at the front of snake based on snake's orientation, set a timer to update the snake

        :return: None
        """
        if self.body_list:
            head = self.body_list[0].copy()
        else:
            head = pygame.Rect(-CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
            self.body_list = []

        if self.orientation == pygame.K_RIGHT:
            head.x += CELL_SIZE
        elif self.orientation == pygame.K_LEFT:
            head.x -= CELL_SIZE
        elif self.orientation == pygame.K_UP:
            head.y -= CELL_SIZE
        elif self.orientation == pygame.K_DOWN:
            head.y += CELL_SIZE

        self.body_list.insert(0, head)

        pygame.time.set_timer(SNAKE_UPDATE_EVENT, self.time_interval)

    def draw(self, window):
        """
        Display the snake on the window, body is solid and head is hollow
        :param window: where the snake is displayed
        :return: None
        """
        for i, rect in enumerate(self.body_list):
            if i == 0:

                pygame.draw.rect(window, SNAKE_HEAD_COLOR, rect.inflate(-2, -2), False)
            else:
                pygame.draw.rect(window, self.color, rect.inflate(-2, -2), False)

    def update(self):
        """
        Update the snake on the window -- make it move : insert one node at the front, and delete the last node

        :return: True if the snake is still alive after update, else False
        """
        back_up = self.body_list.copy()

        self.add_node()
        self.body_list.pop()

        if self.is_dead():
            self.body_list = back_up
            return False
        return True

    def change_ori(self, to_ori):
        """
        Change the snake orientation based on the key that user pressed

        :param to_ori: the orientation user choosed (key pressed)
        :return: None
        """
        h_ori = (pygame.K_RIGHT, pygame.K_LEFT)
        v_ori = (pygame.K_UP, pygame.K_DOWN)

        if (self.orientation in h_ori and to_ori not in h_ori) or (self.orientation in v_ori and to_ori not in v_ori):
            self.orientation = to_ori

    def eaten(self, food):
        """
        Check the position of the food and the snake head.
        If food in head, food is eaten, snake grows longer (add one node), moves faster (time interval decrease).
        Else food is not eaten

        :param food: Food in the game
        :return: True if food is eaten, else False
        """
        if self.body_list[0].contains(food.rect):
            self.score += food.score

            if self.time_interval > 200:
                self.time_interval -= 40

            self.add_node()
            return True
        return False

    def is_dead(self):
        """
        Check if the snake is dead:
        1. It hits the border of window
        2. It hits its body

        :return: True if it is dead, else False
        """
        head = self.body_list[0]
        if not SCREEN_RECT.contains(head):
            return True
        for body in self.body_list[1:]:
            if head.contains(body):
                return True
        return False
