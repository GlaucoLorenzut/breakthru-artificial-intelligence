import os
import pygame
import game_engine
import game_GUI


IMGS_PATH = "images"
WINDOW_LAYOUT = (550, 80)
WINDOW_WIDTH = 980
WINDOW_HEIGHT = 720
BOARD_WIDTH = BOARD_HEIGHT = 660
DIMENSION = 11
MAX_FPS = 15


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_LAYOUT

    #pygame.display.set_caption("asd")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(pygame.Color("black"))


    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    gui = game_GUI.GameGUI(screen, BOARD_WIDTH, BOARD_HEIGHT, DIMENSION)
    game = game_engine.GameState()

    gui.init_board_index()

    validMoves = game.getAllPossibleMoves()

    moveMade = False
    gui.load_images(IMGS_PATH)
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
        for event in pygame.event.get():
            # MOUSE COMMANDS
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = gui.get_board_location(pygame.mouse.get_pos())

                if location:
                    row, col = location
                    if sqSelected != location and (game.isValidPiece(row, col) or len(playerClicks) > 0):
                        sqSelected = location
                        playerClicks.append(sqSelected)
                    else:
                        sqSelected = ()
                        playerClicks = []

                    if len(playerClicks) == 2:
                        move = game_engine.Move(playerClicks[0], playerClicks[1], game.board)
                        for check_move in validMoves:
                            if move == check_move:
                                game.makeMove(move)
                            else:
                                print(move.ID + " - " + check_move.ID)

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
            status = game.checkVictory()
            if status != "":
                print(status)
                running = False
            else:
                validMoves = game.getAllPossibleMoves()
                moveMade = False

        gui.draw_board()

        if len(playerClicks) > 0:
            if game.isYourTurn(playerClicks[0][0], playerClicks[0][1]):
                gui.highlightSquare(playerClicks[0][0], playerClicks[0][1], pygame.Color(50, 170, 80))
            else:
                gui.highlightSquare(playerClicks[0][0], playerClicks[0][1], pygame.Color(170, 50, 80))

        gui.draw_pieces(game.board)

        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
