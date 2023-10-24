import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 500

pygame.mixer.music.load("Simply-Three-Dance-Monkey[128][320].mp3")
pygame.mixer.music.play()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 28)
# background = pygame.image.load("pexels-j-lee-6825703.jpg")
# start_button = pygame.image.load("icons8-start-80 (2).png")
# exit_button = pygame.image.load("icons8-exit-64.png")
# start_rect = start_button.get_rect()
# start_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
# exit_rect = exit_button.get_rect()
# exit_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

colors = {0: (224, 224, 224),
          2: (255, 153, 153),
          4: (255, 255, 102),
          8: (0, 255, 255),
          16: (178, 102, 255),
          32: (255, 178, 102),
          64: (246, 94, 59),
          128: (102, 0, 51),
          256: (64, 64, 64),
          512: (204, 0, 102),
          1024: (0, 0, 204),
          2048: (0, 102, 0),
          "light text": (249, 246, 242),
          "dark text": (119, 110, 101),
          "bg": (255, 255, 255)}


board_values = [[0 for i in range(4)] for j in range(4)]
main_menu = False
win = False
game_over = False
new_number = True
direction = ""
score = 0
file = open("high_score", "r")
init_high = int(file.readline())
file.close()
high_score = init_high
TEXT_COL = (255, 255, 255)


def draw_over():
    pygame.draw.rect(screen, (0, 102, 0), [30, 150, 330, 120], 0, 5)
    game_over_text1 = font.render("Game over!!", True, "white")
    game_over_text2 = font.render("Press Enter to Restart", True, "white")
    screen.blit(game_over_text1, (110, 170))
    screen.blit(game_over_text2, (50, 210))


def draw_win():
    pygame.draw.rect(screen, (0, 102, 0), [30, 150, 330, 120], 0, 5)
    win_text1 = font.render("You Won!!", True, "white")
    win_text2 = font.render("Press Enter to Restart", True, "white")
    screen.blit(win_text1, (110, 170))
    screen.blit(win_text2, (50, 210))


def take_turn(direc, board):
    global score
    global win
    merged = [[False for i in range(4)] for j in range(4)]
    if direc == "UP":
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
                        if board[i - shift - 1][j] == 2048:
                            win = True

    elif direc == "DOWN":
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not \
                            merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
                        if board[3 - i + shift][j] == 2048:
                            win = True

    elif direc == "LEFT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
                    if board[i][j - shift - 1] == 2048:
                        win = True

    elif direc == "RIGHT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
                        if board[i][4 - j + shift] == 2048:
                            win = True
    return board


def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


def draw_board():
    pygame.draw.rect(screen, colors["bg"], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f"Score: {score}", True, "dark green")
    high_score_text = font.render(f"High Score: {high_score}", True, "dark green")
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass


def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors["light text"]
            else:
                value_color = colors["dark text"]
            if value <= 2048:
                color = colors[value]
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

run = True
while run:
    timer.tick(60)
    screen.fill("white")
    draw_board()
    draw_pieces(board_values)
    if new_number:
        board_values, game_over = new_pieces(board_values)
        new_number = False
    if direction != " ":
        board_values = take_turn(direction, board_values)
        direction = " "
        new_number = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open("high_score", "w")
            file.write(f"{high_score}")
            file.close()
            init_high = high_score
    if win:
        draw_win()
        if high_score > init_high:
            file = open("high_score", "w")
            file.write(f"{high_score}")
            file.close()
            init_high = high_score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.mixer.music.stop()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     mouse_pos = pygame.mouse.get_pos()
        #     if start_rect.collidepoint(mouse_pos):
        #         print("...")
        #     if exit_rect.collidepoint(mouse_pos):
        #         pygame.quit()
        #         sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for i in range(4)] for j in range(4)]
                    new_number = True
                    score = 0
                    direction = ""
                    game_over = False
            if win:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for i in range(4)] for j in range(4)]
                    new_number = True
                    score = 0
                    direction = ""
                    win = False
    if score > high_score:
        high_score = score
    # screen.fill("white")
    # screen.blit(start_button, start_rect)
    # screen.blit(exit_button, exit_rect)
    pygame.display.flip()

pygame.quit()
# sys.exit()



try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass