import os
import pygame
import game_engine


IMGS_PATH = "images"
WINDOW_LAYOUT = (80, 80)
WINDOW_WIDTH = WINDOW_HEIGHT = 720
BOARD_WIDTH = BOARD_HEIGHT = 660
DIMENSION = 11

SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_LAYOUT
    #pygame.display.set_caption("asd")
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(pygame.Color("black"))

    def write_index(text, size, pos_X, pos_Y):
        font = pygame.font.Font(None, size)  # pygame.font.SysFont('Times New Roman', 36)
        label = font.render(str(text), True, pygame.Color("white"))
        layout_X = 0.5*(SQ_SIZE - label.get_rect().width)
        layout_Y = 0.5*(SQ_SIZE - label.get_rect().height) + 3
        screen.blit(label, (pos_X + layout_X, pos_Y + layout_Y))
        #print(str(text) + " - " + str(label.get_rect().height) + " - " + str(pos_Y + layout_X))

    index_map = {0: "K", 1: "J", 2: "I", 3: "H", 4: "G", 5: "F", 6: "E", 7: "D", 8: "C", 9: "B", 10: "A"}
    for ind, abc in index_map.items():
        write_index(abc, 44, BOARD_WIDTH, ind*SQ_SIZE)
        write_index(ind+1, 44, ind * SQ_SIZE, BOARD_HEIGHT)

    clock = pygame.time.Clock()

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

                if 0 <= location[0] < BOARD_WIDTH and 0 <= location[1] < BOARD_HEIGHT:
                    row = location[1] // SQ_SIZE
                    col = location[0] // SQ_SIZE

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


def loadImages():
    pieces = ["bR", "wR", "wK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(IMGS_PATH + "/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def highlightSquare(screen, row, col):
    pygame.draw.rect(screen, pygame.Color(50, 170, 80), pygame.Rect(col * SQ_SIZE+1,  row* SQ_SIZE+1, SQ_SIZE-1, SQ_SIZE-1))


def drawBoard(screen):
    pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT))
    for d in range(DIMENSION +1):
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
