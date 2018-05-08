import pygame
import sys
from pygame.locals import *
from random import choice
pygame.init()

# Colors:

RGB = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
CMY = [(0, 255, 255), (255, 0, 255), (255, 255, 0)]
BWG = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]


# Global Variables:

fpsclock = pygame.time.Clock()

(screen_width, screen_height) = (640, 480)
screen_centerx = (screen_width/2)
screen_centery = (screen_height/2)

screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
pygame.display.set_caption("Rock, Paper, Scissors")


# Functions & Classes:

def quit_game():
    """Quits the game."""
    print("Exited successfully.")
    pygame.quit()
    sys.exit()


def text_objects(text, font):
    textsurf = font.render(text, True, BWG[0])
    return textsurf, textsurf.get_rect()


def message_display(text, font="arial", size=28, centering=True, x=0, y=0):
    font_and_size = pygame.font.SysFont(font, size)
    textsurf, textrect = text_objects(text, font_and_size)
    if centering:
        textrect.center = (screen_centerx + x, screen_centery + y)
    else:
        textrect = (x, y)
    screen.blit(textsurf, textrect)


def button(msg, x, y, w, h, inactivecolor, activecolor, action=None, centering=True):
    # x and y coordinates start at center
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if centering:
        x = (screen_centerx-(w/2)) + x
        y = (screen_centery-(h/2)) + y
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, activecolor, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactivecolor, (x, y, w, h))
    font_and_size = pygame.font.SysFont("arial", 24)
    textsurf, textrect = text_objects(msg, font_and_size)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textsurf, textrect)


player_choice = ""


def chose_r():
    global player_choice
    player_choice = "Rock"
    global starting
    starting = False


def chose_p():
    global player_choice
    player_choice = "Paper"
    global starting
    starting = False


def chose_s():
    global player_choice
    player_choice = "Scissors"
    global starting
    starting = False


def printchoice():
    print(player_choice)


def whichwinner(a, b):
    message_display(a + " beats " + b.lower() + "!")


def accept():
    global reset
    reset = True


def resetstats():
    global wincount, losecount
    wincount, losecount = 0, 0


# Game initialization global variables:

AI_choice = ""

starting = True
reset = False

winlose = [["P", "R"], ["S", "P"], ["R", "S"]]

wincount = 0
losecount = 0
won = False
lost = False
notscored = True

# --- Game loop ---

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()

    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[K_LALT] or keys_pressed[K_RALT]) and keys_pressed[K_F4]:
        quit_game()

    # - Screen-clearing code:

    screen.fill(BWG[1])

    # - Game logic and drawing code:

    if starting:  # Starting condition. Lets the player choose their option.
        message_display("Rock, paper, or scissors:")
        button("Rock", -150, 150, 100, 40, RGB[0], RGB[1], chose_r)
        button("Paper", 0, 150, 100, 40, RGB[0], RGB[1], chose_p)
        button("Scissors", 150, 150, 100, 40, RGB[0], RGB[1], chose_s)
    else:  # Actions after the player makes their choice.
        if not AI_choice:
            AI_choice = choice(["Rock", "Paper", "Scissors"])
        message_display(("Player chose %s" % player_choice), y=-64)
        message_display(("AI chose %s" % AI_choice), y=-32)
        if AI_choice == player_choice:
            message_display("Tie!")
        elif AI_choice != player_choice:
            if [AI_choice[0], player_choice[0]] in winlose:
                whichwinner(AI_choice, player_choice)
                message_display("Player loses.", y=32)
                lost = True
                if lost and notscored:
                    losecount += 1
                    notscored = False
            else:
                whichwinner(player_choice, AI_choice)
                message_display("Player wins!", y=32)
                won = True
                if won and notscored:
                    wincount += 1
                    notscored = False
        button("Accept", 0, 110, 150, 40, CMY[1], CMY[0], accept)
        if reset:
            AI_choice = ""
            starting = True
            notscored = True
            won = False
            lost = False
            reset = False

    message_display("Wins: %i" % wincount, centering=False, x=4)
    message_display("Loses: %i" % losecount, centering=False, x=4, y=32)
    button("Reset stats", screen_width - 140, 0, 140, 40, RGB[0], RGB[1], resetstats, centering=False)

    # - Display updating and clock ticking code:

    pygame.display.update()
    fpsclock.tick(60)
