import pygame
import sys
import pygame.freetype


import random
import copy

# Initialize Pygame
pygame.init()



# Constants
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

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("La Gourmandine Quarto")

# Load fonts
pygame.freetype.init()
title_font = pygame.freetype.Font("font/RozhaOne-Regular.ttf", 48)
prompt_font = pygame.freetype.Font("font/RozhaOne-Regular.ttf", 24)
button_font = pygame.freetype.Font("font/RozhaOne-Regular.ttf", 32)

# Load images
background_img = pygame.image.load('bg/2.png')
background_img = pygame.transform.scale(background_img, WINDOW_SIZE)
prompt_img = pygame.image.load('bg/1.png')
prompt_img = pygame.transform.scale(prompt_img, WINDOW_SIZE)

# Load pastry images
pastry_images = {}
for pt in ['Croissant', 'Eclair']:
    for f in ['Strawberry', 'Matcha']:
        for c in ['Traditional', 'Indulging']:
            for t in ['PowderSugar', 'WhippedCream']:
                key = f"{pt}_{f}_{c}_{t}"
                pastry_images[key] = pygame.image.load(f"pastry/{key}.png")

class Piece:
    def __init__(self, pastry_type, flavor, collection, topping):
        self.pastry_type = pastry_type
        self.flavor = flavor
        self.collection = collection
        self.topping = topping
        self.image = pastry_images[f"{pastry_type}_{flavor}_{collection}_{topping}"]

    def draw(self, x, y, size):
        scaled_image = pygame.transform.scale(self.image, (size, size))
        screen.blit(scaled_image, (x - size // 2, y - size // 2))

class Board:
    def __init__(self):
        # Initialize 4* 4 board
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def place_piece(self, piece, row, col):
        if self.grid[row][col] is None:
            self.grid[row][col] = piece
            return True
        return False

    def is_full(self):
        # Check if all cells are filled
        return all(all(cell is not None for cell in row) for row in self.grid)

    def check_win(self):
        # Check rows and column
        for i in range(BOARD_SIZE):
            if self.check_line(self.grid[i]) or self.check_line([self.grid[j][i] for j in range(BOARD_SIZE)]):
                return True
        # Check diagonals
        if self.check_line([self.grid[i][i] for i in range(BOARD_SIZE)]) or \
           self.check_line([self.grid[i][BOARD_SIZE-1-i] for i in range(BOARD_SIZE)]):
            return True
        return False
    
    def check_line(self, line):
        if None in line:
            return False
        return any(all(getattr(piece, attr) == getattr(line[0], attr) for piece in line) for attr in ['pastry_type', 'flavor', 'collection', 'topping'])

    def draw(self):
        board_width = BOARD_SIZE * CELL_SIZE
        board_start_x = (WINDOW_SIZE[0] - board_width) // 2 
        board_start_y = (WINDOW_SIZE[1] - board_width) // 2

        # Draw board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = board_start_x + col * CELL_SIZE + CELL_SIZE // 2
                y = board_start_y + row * CELL_SIZE + CELL_SIZE // 2
                color = LIGHT_BUTTER if (row + col) % 2 == 0 else BLACK_BEAN
                pygame.draw.rect(screen, color, (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE))
                if self.grid[row][col]:
                    self.grid[row][col].draw(x, y, PIECE_SIZE)

class QuartoAI:
    def __init__(self, max_depth = 4):
        # Initialize AI with maximum depth for minimax algorithm
        self.max_depth = max_depth

    def choose_piece(self, available_pieces):
        # Randomly select a piece for the opponent
        return random.choice(available_pieces)
    
    def get_best_move(self, board, piece):
        # Initialize best scores as negative infinity and best move as None
        best_score = float('-inf')
        best_move = None

        # Try each possible move on the board
        for row in range(4):
            for col in range(4):
                # Check if the cell is empty
                if board.grid[row][col] is None:
                    # Create a deep copy of the board for simulation
                    board_copy = self._copy_board(board)
                    # Make the move on the copied board
                    board_copy.place_piece(piece, row, col)


                    # Calculate score using minimax
                    score = self._minimax(board_copy, self.max_depth, False)

                    # Update best move if current score is better
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move
    
    def _minimax(self, board, depth, is_maximizing):
        # Base case: check if game is over or maximum depth reached
        if board.check_win():
            return 100 if is_maximizing else -100
        if board.is_full() or depth == 0:
            return self._evaluate_board(board)
        
        if is_maximizing:
            #Maximizing player's turn
            max_eval = float('-inf')
            for row in range(4):
                for col in range(4):
                    if board.grid[row][col] is None:
                        #Try each possible move
                        board_copy = self._copy_board(board)
                        # Simulate a random piece placement (since actual piece isn't known)
                        dummy_piece = self._create_dummy_piece()
                        board_copy.place_piece(dummy_piece, row, col)
                        eval = self._minimax(board_copy, depth- 1, False)
                        max_eval = max(max_eval, eval)
                    

            return max_eval
        else:
            #Minimizing player's turn
            min_eval = float('inf')
            for row in range(4):
                for col in range(4):
                    if board.grid[row][col] is None:
                        #Try each possible move
                        board_copy = self._copy_board(board)
                        # Simulate a random piece placement
                        dummy_piece = self._create_dummy_piece()
                        board_copy.place_piece(dummy_piece, row, col)
                        eval = self._minimax(board_copy, depth- 1, True)
                        min_eval = min(min_eval, eval)
            return min_eval
    
    def _evaluate_board(self, board):
        # Count potential winning lines and return a score
        score = 0

        # Check rows
        for row in board.grid:
            score += self._evaluate_line(row)

        # Check col
        for col in range(4):
            column = [board.grid[row][col] for row in range(4)]
            score += self._evaluate_line(column)

        # Check diagonals
        diag1 = [board.grid[i][i] for i in range(4)]
        diag2 = [board.grid[i][3-i] for i in range(4)]
        score += self._evaluate_line(diag1)
        score += self._evaluate_line(diag2)
        
        return score
    
    def _evaluate_line(self, line):
        # Count matching attributes in a line
        if None in line or any(piece is None for piece in line):
            return 0
            
        score = 0
        attributes = ['pastry_type', 'flavor', 'collection', 'topping']
        
        for attr in attributes:
            if all(getattr(piece, attr) == getattr(line[0], attr) for piece in line):
                score += 1
                
        return score
    
    def _copy_board(self, board):
        # Create a deep copy of the board
        new_board = Board()
        for i in range(4):
            for j in range(4):
                new_board.grid[i][j] = board.grid[i][j]
        return new_board
    
    def _create_dummy_piece(self):
        # Create a dummy piece for simulation purposes
        return Piece(
            random.choice(['Croissant', 'Eclair']),
            random.choice(['Strawberry', 'Matcha']),
            random.choice(['Traditional', 'Indulging']),
            random.choice(['PowderSugar', 'WhippedCream'])
        )

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(max(0, min(255, c + 30)) for c in color)
        self.is_hovered = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, OLIVEWOOD, self.rect, 3, border_radius=10)
        text_surface, _ = button_font.render(self.text, OLIVEWOOD)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False
    
class Game:
    def __init__(self):
        self.reset_game()
        self.game_state = "start_screen"  # New state for start screen
        self.start_button = Button(
            WINDOW_SIZE[0]//2 - 100,
            WINDOW_SIZE[1]//2 - 30,
            200, 60,
            "Start Game",
            LIGHT_BUTTER
        )
        self.restart_button = Button(
            WINDOW_SIZE[0]//2 - 100,
            WINDOW_SIZE[1]//2 + 50,
            200, 60,
            "Play Again",
            LIGHT_BUTTER
        )
    
    def reset_game(self):
        self.board = Board()
        self.available_pieces = [
            Piece(pt, f, c, t)
            for pt in ['Croissant', 'Eclair']
            for f in ['Strawberry', 'Matcha']
            for c in ['Traditional', 'Indulging']
            for t in ['PowderSugar', 'WhippedCream']
        ]
        self.current_player = 1
        self.selected_piece = None
        self.game_state = "select_piece"
        self.ai = QuartoAI()
        self.is_ai_turn = False
        self.result = None

    def draw_start_screen(self):
        screen.blit(prompt_img, (0, 0))
        title_text = "La Gourmandine"
        title_font.render_to(screen, (WINDOW_SIZE[0] // 2 - 180, WINDOW_SIZE[1] // 3), title_text, WHITE)
        prompt_text = "Welcome to the sweetest game of strategy!"
        prompt_font.render_to(screen, (WINDOW_SIZE[0] // 2 - 200, WINDOW_SIZE[1] // 2 - 100), prompt_text, BLACK)
        self.start_button.draw()

    def draw_game_over_screen(self):
        # Draw the game state as usual
        self.draw_game_screen()
        # Add a semi-transparent overlay
        overlay = pygame.Surface(WINDOW_SIZE)
        overlay.fill(WHITE)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        # Draw the result and restart button
        prompt_font.render_to(screen, (WINDOW_SIZE[0] // 2 - 100, WINDOW_SIZE[1] // 2 - 20), self.result, BLACK)
        self.restart_button.draw()

    def handle_ai_turn(self):
        if self.is_ai_turn:
            if self.game_state == "select_piece":
                # AI chooses a piece for the opponent (human player)
                self.selected_piece = self.ai.choose_piece(self.available_pieces)
                self.available_pieces.remove(self.selected_piece)
                self.game_state = "place_piece"
                self.switch_player()  # AI switches to placement mode
            elif self.game_state == "place_piece":
                # AI decides where to place the piece
                row, col = self.ai.get_best_move(self.board, self.selected_piece)
                result = self.place_piece(row, col)
                self.game_state = "select_piece"  # Switch back to piece selection after placing
                self.switch_player()  # Switch back to the human player's turn
                self.is_ai_turn = False
                return result
        return None

    
    def switch_player(self):
        self.current_player = 3 - self.current_player

    def select_piece(self, index):
        if index < len(self.available_pieces):
            self.selected_piece = self.available_pieces[index]
            self.available_pieces.pop(index)
            self.game_state = "place_piece"
            self.switch_player()

    def place_piece(self, row, col):
        if self.board.place_piece(self.selected_piece, row, col):
            if self.board.check_win():
                return f"Player {self.current_player} wins!"
            elif self.board.is_full():
                return "It's a draw!"
            self.selected_piece = None
            self.game_state = "select_piece"
        return None
    
    
    def draw_game_screen(self):
        screen.blit(background_img, (0, 0))
        title_text = "La Gourmandine"
        title_font.render_to(screen, (WINDOW_SIZE[0] // 2 - 180, 20), title_text, TUSCAN_RED)
        self.board.draw()
        self.draw_available_pieces()
        if self.selected_piece:
            self.selected_piece.draw(WINDOW_SIZE[0] - MARGIN - CELL_SIZE // 2, MARGIN + CELL_SIZE // 2, PIECE_SIZE)
        if self.game_state == "select_piece":
            prompt_text = f"Player {self.current_player}, your friend would like a pastry!"
        else:
            prompt_text = f"Player {self.current_player}, where would you want to place the selected pastry?"
        prompt_font.render_to(screen, (WINDOW_SIZE[0] // 2 - 200, WINDOW_SIZE[1] - 720), prompt_text, OLIVEWOOD)

    def draw(self):
        if self.game_state == "start_screen":
            self.draw_start_screen()
        elif self.result:
            self.draw_game_over_screen()
        else:
            self.draw_game_screen()

    def draw_available_pieces(self):
        # Draw available pieces at the bottom
        start_x = WINDOW_SIZE[0] // 2 - (len(self.available_pieces) * PIECE_SELECTION_SIZE) // 2
        start_y = WINDOW_SIZE[1] - MARGIN - PIECE_SELECTION_SIZE
        for i, piece in enumerate(self.available_pieces):
            x = start_x + i * (PIECE_SELECTION_SIZE + 10)
            y = start_y
            if self.game_state == "select_piece":
                pygame.draw.rect(screen, LIGHT_BUTTER, (x - PIECE_SELECTION_SIZE // 2 - 4, y - PIECE_SELECTION_SIZE // 2 - 2, PIECE_SELECTION_SIZE + 4, PIECE_SELECTION_SIZE + 4))
            piece.draw(x, y, PIECE_SELECTION_SIZE)

def main():
    game = Game()
    result = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_state == "start_screen":
                    if game.start_button.handle_event(event):
                        game.game_state = "select_piece"
                elif game.result:
                    if game.restart_button.handle_event(event):
                        game.reset_game()
                elif not game.is_ai_turn:
                    x, y = pygame.mouse.get_pos()
                    if game.game_state == "select_piece":
                        start_x = WINDOW_SIZE[0] // 2 - (len(game.available_pieces) * PIECE_SELECTION_SIZE) // 2
                        start_y = WINDOW_SIZE[1] - MARGIN - PIECE_SELECTION_SIZE
                        for i in range(len(game.available_pieces)):
                            piece_x = start_x + i * (PIECE_SELECTION_SIZE + 10)
                            piece_y = start_y
                            if piece_x - PIECE_SELECTION_SIZE // 2 < x < piece_x + PIECE_SELECTION_SIZE // 2 and \
                            piece_y - PIECE_SELECTION_SIZE // 2 < y < piece_y + PIECE_SELECTION_SIZE // 2:
                                game.select_piece(i)
                                break
                    elif game.game_state == "place_piece":
                        board_width = BOARD_SIZE * CELL_SIZE
                        board_start_x = (WINDOW_SIZE[0] - board_width) // 2
                        board_start_y = (WINDOW_SIZE[1] - board_width) // 2
                        col = (x - board_start_x) // CELL_SIZE
                        row = (y - board_start_y) // CELL_SIZE
                        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                            game.result = game.place_piece(row, col)
                            if not game.result:
                                game.is_ai_turn = True
            elif event.type == pygame.MOUSEMOTION:
                if game.game_state == "start_screen":
                    game.start_button.handle_event(event)
                elif game.result:
                    game.restart_button.handle_event(event)

        # Handle AI turns
        if game.is_ai_turn and not result:
            # AI places the piece chosen by the player and chooses a new piece for the player
            result = game.handle_ai_turn()

        game.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()