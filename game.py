import pygame
from properties import *
from itertools import cycle


class Game:
    """
    Game class controls the main process of a game
    """
    def __init__(self):
        """
        Game initialization
        window is 640 * 480, can be divided into small squares (20 * 20)
        """
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Snake Game")
        bg_img = pygame.image.load("snake_bg.jpg")
        self.bg_img = pygame.transform.scale(bg_img, (640, 480))

        self.scoreLabel = Label()
        self.tipLabel = Label(32, 1)
        self.tipLabel_off = Label(32, -1)
        self.instructionLabel = Label(28, 2)

        self.food = Food()

        self.snake = Snake()

        # control flag of game status: game_over/game_pause
        self.is_game_over = False
        self.is_pause = False

    def start(self):
        """
        Game start:
        Continuously draw items on the window, detect the user input, update food and snake, check the game status

        :return: None
        """
        clock = pygame.time.Clock()
        # Blink the tip label
        tipLabels = cycle([self.tipLabel, self.tipLabel_off])
        pygame.time.set_timer(TEXT_BLINK_EVENT, self.tipLabel.interval)
        flash_label = self.tipLabel

        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        if self.is_game_over:
                            self.reset()
                        else:
                            self.is_pause = not self.is_pause
                if not self.is_pause and not self.is_game_over:
                    if event.type == FOOD_UPDATE_EVENT:
                        self.food.random_pos()

                    elif event.type == SNAKE_UPDATE_EVENT:
                        self.is_game_over = not self.snake.update()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                            self.snake.change_ori(event.key)
                else:
                    if event.type == TEXT_BLINK_EVENT:
                        flash_label = next(tipLabels)
            self.window.blit(self.bg_img, (0,0))

            self.scoreLabel.draw(self.window, "Score: %d" % self.snake.score)

            self.food.draw(self.window)

            self.snake.draw(self.window)

            if self.is_game_over:
                flash_label.draw(self.window, "GAME OVER, Press SPACE to restart...")
                self.instructionLabel.draw(self.window, "Press UP, DOWN, LEFT, RIGHT to move")
            elif self.is_pause:
                flash_label.draw(self.window, "Game paused, Press SPACE to continue...")
                self.instructionLabel.draw(self.window, "Press UP, DOWN, LEFT, RIGHT to move")
            else:
                if self.snake.eaten(self.food):
                    self.food.random_pos()
            clock.tick(60)

            pygame.display.update()

    def reset(self):
        """
        Reset the game properties if game is over, user can play it again

        :return: None
        """
        self.is_game_over = False
        self.is_pause = False

        self.snake.reset_snake()

        self.food.random_pos()


if __name__ == '__main__':
    pygame.init()

    Game().start()

    pygame.quit()