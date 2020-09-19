import pygame
import game_engine
from pygame.locals import KEYDOWN, K_DOWN, K_UP, K_LEFT, K_RIGHT

IMGS_PATH = "images"

BOARD_WIDTH = BOARD_HEIGHT = 660
DIMENSION = 11

SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(IMGS_PATH + "/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("blue"))
    game = game_engine.GameState()
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []

    while running:

        for event in pygame.event.get():

            # MOUSE COMMANDS
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()

                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = game_engine.Move(playerClicks[0], playerClicks[1], game.board)
                    game.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

            # KEYBOARD COMMANDS
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game.undoMove()
                    sqSelected = ()
                    playerClicks = []
                if event.key == pygame.K_UP:
                    game.restoreMove()
                    sqSelected = ()
                    playerClicks = []


        drawGameState(screen, game.board)
        #if row != -1 and col != -1:
        #    highlightSquare(screen, col, row)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def highlightSquare(screen, pos_x, pos_y):
    pygame.draw.rect(screen, pygame.Color("green"), pygame.Rect(pos_x * SQ_SIZE,  pos_y* SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawGameState(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    #for r in range(DIMENSION):
    #    for c in range(DIMENSION):
    #        color = colors[((r+c)%2)]
    #        pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    screen.fill(pygame.Color("blue"))
    for d in range(DIMENSION):
        # rows
        pygame.draw.line(screen, pygame.Color("gray"), (0, d*SQ_SIZE), (BOARD_WIDTH, d*SQ_SIZE), 1)
        # cols
        pygame.draw.line(screen, pygame.Color("gray"), (d * SQ_SIZE, 0), (d * SQ_SIZE, BOARD_HEIGHT), 1)
        if (3 <= d <= 8):
            # inner rows
            pygame.draw.line(screen, pygame.Color("white"), (3 * SQ_SIZE-1, d * SQ_SIZE), (8 * SQ_SIZE+1, d * SQ_SIZE), 3)
            # inner cols
            pygame.draw.line(screen, pygame.Color("white"), (d * SQ_SIZE, 3 * SQ_SIZE-1), (d * SQ_SIZE, 8 * SQ_SIZE+1), 3)






def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
