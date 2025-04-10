import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BEIGE = (245, 222, 179)
HIGHLIGHT = (124, 252, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load chess piece images
def load_images():
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    images = {}
    
    for piece in pieces:
        for color in colors:
            # In a real implementation, you would have actual image files
            # images[f"{color}_{piece}"] = pygame.image.load(f"images/{color}_{piece}.png")
            # For this example, we'll create placeholder surfaces
            img = pygame.Surface((SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            img.fill(WHITE if color == 'white' else BLACK)
            pygame.draw.rect(img, BROWN if color == 'white' else BEIGE, 
                            (5, 5, SQUARE_SIZE - 20, SQUARE_SIZE - 20))
            font = pygame.font.SysFont('Arial', 12)
            text = font.render(piece[0].upper() if color == 'white' else piece[0].lower(), True, 
                              BLACK if color == 'white' else WHITE)
            img.blit(text, (SQUARE_SIZE // 2 - 10, SQUARE_SIZE // 2 - 10))
            images[f"{color}_{piece}"] = img
    
    return images

# Chess board representation
class Board:
    def __init__(self):
        self.board = self.create_starting_board()
        self.selected_piece = None
        self.turn = 'white'
    
    def create_starting_board(self):
        # Create an 8x8 board with pieces in starting positions
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Set up pawns
        for col in range(BOARD_SIZE):
            board[1][col] = {'type': 'pawn', 'color': 'black'}
            board[6][col] = {'type': 'pawn', 'color': 'white'}
        
        # Set up other pieces
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(BOARD_SIZE):
            board[0][col] = {'type': back_row[col], 'color': 'black'}
            board[7][col] = {'type': back_row[col], 'color': 'white'}
        
        return board
    
    def draw(self, screen, images, selected=None):
        # Draw the chess board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Determine square color
                color = BEIGE if (row + col) % 2 == 0 else BROWN
                
                # Draw square
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                               SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected square
                if selected and selected == (row, col):
                    pygame.draw.rect(screen, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                                      SQUARE_SIZE, SQUARE_SIZE), 3)
                
                # Draw piece if there is one
                piece = self.board[row][col]
                if piece:
                    piece_img = images[f"{piece['color']}_{piece['type']}"]
                    screen.blit(piece_img, (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))
    
    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        # If a piece is already selected
        if self.selected_piece:
            # Move the piece if the move is valid
            if self.is_valid_move(self.selected_piece, (row, col)):
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
                self.turn = 'black' if self.turn == 'white' else 'white'
            else:
                # If clicking on another piece of the same color, select that piece instead
                if (self.board[row][col] and self.board[row][col]['color'] == self.turn):
                    self.selected_piece = (row, col)
                else:
                    # Deselect if clicking elsewhere
                    self.selected_piece = None
        else:
            # Select a piece if it's of the current player's color
            if self.board[row][col] and self.board[row][col]['color'] == self.turn:
                self.selected_piece = (row, col)
    
    def is_valid_move(self, start, end):
        # This is a simplified version - in a real chess game, you'd need to check
        # all the rules for each piece type
        start_row, start_col = start
        end_row, end_col = end
        
        # Can't move to a square with your own piece
        if (self.board[end_row][end_col] and 
            self.board[end_row][end_col]['color'] == self.board[start_row][start_col]['color']):
            return False
        
        # For simplicity, let's just allow any move that's not to the same square
        return start != end
    
    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # Move the piece
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None

def main():
    images = load_images()
    board = Board()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    board.handle_click(event.pos)
        
        screen.fill(BLACK)
        board.draw(screen, images, board.selected_piece)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
