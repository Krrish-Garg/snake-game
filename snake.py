import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

gameWindow = pygame.display.set_mode((800, 600))

bgimg = pygame.image.load("snakebg.jpg")
bgimg = pygame.transform.scale(bgimg, (800, 600)).convert_alpha()

pygame.display.set_caption("Snake game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((200, 240, 250))
        text_screen("Welcome to Snake Game", black, 190, 210)
        text_screen("Press Space bar to Play", black, 205, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    wc_sound.play(loops=-1)
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Creating game loop
def gameloop():

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 95
    snake_y = 55
    velocity_x = 0
    snk_list = []
    snk_length = 1
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(100, 700)
    food_y = random.randint(100, 500)
    velocity_y = 0
    snake_size = 10
    fps = 30
    score = 0

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(white)
            text_screen("Game Over! Press Enter to continue", red, 65, 250)
            wc_sound.stop()  # Stop the music when game over

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -5
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -5
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = 5
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(100, 700)
                food_y = random.randint(100, 500)
                snk_length += 3
                beep_sound.play()
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  High Score: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                gameover_sound.play()

            if snake_x < 0 or snake_x > 800 or snake_y < 0 or snake_y > 600:
                game_over = True
                gameover_sound.play()

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

# Load sounds
wc_sound = pygame.mixer.Sound('wc.mp3')
beep_sound = pygame.mixer.Sound('beep.mp3')
gameover_sound = pygame.mixer.Sound('gameover.mp3')
welcome()
