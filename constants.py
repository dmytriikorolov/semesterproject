import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'

def load_background():

    bg = pygame.image.load("img/table.jpg").convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return bg


def load_card(scale_width=70, scale_height=100):
    """
    Loads every card from 'img/cards/<rank><suit>.png'.
    Example: 'img/cards/AC.png'
    """
    card_images = {}
    for suit in SUITS:
        for rank in RANKS:
            filename = f"img/cards/{rank}{suit}.png"
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (scale_width, scale_height))
            card_images[(rank, suit)] = image
    return card_images
