import pygame
import pygame.freetype

# Window settings
WINDOW_SIZE = (1200, 800)
BOARD_SIZE = 4
CELL_SIZE = 140  
PIECE_SIZE = 120  
MARGIN = 50
PIECE_SELECTION_SIZE = 80  

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_PINK = (255, 230, 230)
DARK_PINK = (255, 200, 200)
LIGHT_BROWN = (210, 180, 140)
LIGHT_BUTTER = (249,229,187)
BLACK_BEAN = (73,27,21)
SUMMER_BERRY = (229,154,202)
TUSCAN_RED = (137, 29, 26)
CREAMY_BISCOTTI = (241, 230, 210)
OLIVEWOOD = (33, 7, 6)

# Initialize Pygame and fonts
pygame.init()
pygame.freetype.init()

# Load fonts
TITLE_FONT = pygame.freetype.Font("assets/font/RozhaOne-Regular.ttf", 48)
PROMPT_FONT = pygame.freetype.Font("assets/font/RozhaOne-Regular.ttf", 24)

# Load background
BACKGROUND_IMG = pygame.image.load('assets/bg/2.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, WINDOW_SIZE)

# Game piece attributes
PASTRY_TYPES = ['Croissant', 'Eclair']
FLAVORS = ['Strawberry', 'Matcha']
COLLECTIONS = ['Traditional', 'Indulging']
TOPPINGS = ['PowderSugar', 'WhippedCream']