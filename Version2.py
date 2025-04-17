import pygame
import sys
import chess  # python-chess

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

# Load chess piece images (placeholder)
def load_images():
    piece_names = {
        chess.PAWN: 'pawn',
        chess.ROOK: 'rook',
        chess.KNIGHT: 'knight',
        chess.BISHOP: 'bishop',
        chess.QUEEN: 'queen',
        chess.KING: 'king'
    }

    colors = ['white', 'black']
    images = {}

    for piece_type, piece_name in piece_names.items():
        for color in colors:
            img = pygame.Surface((SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            img.fill(WHITE if color == 'white' else BLACK)
            pygame.draw.rect(img, BROWN if color == 'white' else BEIGE,
                             (5, 5, SQUARE_SIZE - 20, SQUARE_SIZE - 20))
            font = pygame.font.SysFont('Arial', 12)
            text = font.render(piece_name[0].upper() if color == 'white' else piece_name[0].lower(),
                               True, BLACK if color == 'white' else WHITE)
            img.blit(text, (SQUARE_SIZE // 2 - 10, SQUARE_SIZE // 2 - 10))
            images[f"{color}_{piece_type}"] = img

    return images

class Board:
    def __init__(self):
        self.board = chess.Board()
        self.selected_piece = None
        self.turn = 'white'

    def draw(self, screen, images, selected=None):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = BEIGE if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                square = chess.square(col, 7 - row)
                if selected is not None and square == selected:
                    pygame.draw.rect(screen, HIGHLIGHT,
                                     (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

                piece = self.board.piece_at(square)
                if piece:
                    piece_img = images[f"{'white' if piece.color == chess.WHITE else 'black'}_{piece.piece_type}"]
                    screen.blit(piece_img, (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        clicked_square = chess.square(col, 7 - row)

        if self.selected_piece is not None:
            move = chess.Move(self.selected_piece, clicked_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_piece = None
                self.turn = 'black' if self.turn == 'white' else 'white'
            else:
                self.selected_piece = None  # Deselect if move is illegal
        else:
            piece = self.board.piece_at(clicked_square)
            if piece and piece.color == (chess.WHITE if self.turn == 'white' else chess.BLACK):
                self.selected_piece = clicked_square

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
                if event.button == 1:  # Left click
                    board.handle_click(event.pos)

        screen.fill(BLACK)
        board.draw(screen, images, board.selected_piece)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
