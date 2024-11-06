import random
import copy
from runner import Board, Piece


class QuartoAI:
    def __init__(self, max_depth = 3):
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
                if board[row][col] is None:
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
                    if board[row][col] is None:
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
                    if board[row][col] is None:
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