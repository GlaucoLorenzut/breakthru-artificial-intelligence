import pygame
import game_engine
#from pygame.locals import KEYDOWN, K_DOWN, K_UP, K_LEFT, K_RIGHT

IMGS_PATH = "images"
BOARD_WIDTH = BOARD_HEIGHT = 660
DIMENSION = 11

SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "wR", "wK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(IMGS_PATH + "/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("blue"))
    game = game_engine.GameState()
    validMoves = game.getValidMoves()
    moveMade = False
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

                #print(str(sqSelected != (row, col))+"-"+str(game.isValidPiece(row, col))+"-"+str(len(playerClicks) > 0))
                if sqSelected != (row, col) and (game.isValidPiece(row, col) or len(playerClicks) > 0):
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                else:
                    sqSelected = ()
                    playerClicks = []

                if len(playerClicks) == 2:
                    move = game_engine.Move(playerClicks[0], playerClicks[1], game.board)
                    if move in validMoves:
                        game.makeMove(move)
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True

            # KEYBOARD COMMANDS
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True

                if event.key == pygame.K_UP:
                    game.restoreMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True

        if moveMade:
            validMoves = game.getValidMoves()
            moveMade = False

        drawBoard(screen)

        if len(playerClicks) > 0:
            highlightSquare(screen, playerClicks[0][0], playerClicks[0][1])

        drawPieces(screen, game.board)

        clock.tick(MAX_FPS)
        pygame.display.flip()

def highlightSquare(screen, row, col):
    pygame.draw.rect(screen, pygame.Color(50, 170, 80), pygame.Rect(col * SQ_SIZE+1,  row* SQ_SIZE+1, SQ_SIZE-1, SQ_SIZE-1))


def drawBoard(screen):
    screen.fill(pygame.Color("blue"))
    for d in range(DIMENSION):
        # rows
        pygame.draw.line(screen, pygame.Color("white"), (0, d*SQ_SIZE), (BOARD_WIDTH, d*SQ_SIZE), 1)
        # cols
        pygame.draw.line(screen, pygame.Color("white"), (d * SQ_SIZE, 0), (d * SQ_SIZE, BOARD_HEIGHT), 1)
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
