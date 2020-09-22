import os
import pygame
import game_engine
import game_GUI


IMGS_PATH = "images"
WINDOW_LAYOUT = (500, 80)
WINDOW_WIDTH = 1040
WINDOW_HEIGHT = 720
BOARD_SIZE = 616
DIMENSION = 11
MAX_FPS = 15


class Breakthru():

    def __init__(self):
        self.state = "HOME"
        self.screen = None
        self.clock = None
        self.game_gui = None
        self.game = None


    def init_game(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_LAYOUT
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("  Breakthru")
        self.clock = pygame.time.Clock()
        self.screen.fill(pygame.Color("black"))



        pygame.init()
        pygame.font.init()


    def home_screen(self):
        self.screen.fill(pygame.Color("black"))
        self.game_gui = game_GUI.GameGUI(self.screen, BOARD_SIZE, DIMENSION)

        while self.state == "HOME":

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()

            self.game_gui.text_button("Single Player", 250, 400, 200, 45, pygame.Color("gray"), pygame.Color("blue"), self.init_game_action)
            self.game_gui.text_button("Multi Player", 550, 400, 200, 45, pygame.Color("gray"), pygame.Color("blue"), self.quit_action)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def switch_screen(self):
        self.screen.fill(pygame.Color("black"))
        self.game_gui = game_GUI.GameGUI(self.screen, BOARD_SIZE, DIMENSION)

        while bkt.state == "SWITCH" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
            self.game_gui.draw_game_result(self.state)
            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def game_screen(self):
        self.game_gui = game_GUI.GameGUI(self.screen, BOARD_SIZE, DIMENSION)
        self.screen.fill(pygame.Color("black"))

        self.game = game_engine.GameState()

        self.game_gui.init_board_index()

        validMoves = self.game.getAllPossibleMoves()

        moveMade = False
        self.game_gui.load_images(IMGS_PATH)
        sqSelected = ()
        playerClicks = []

        while self.state == "GAME":
            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = self.game_gui.get_board_location(pygame.mouse.get_pos())

                    if location:
                        row, col = location
                        if sqSelected != location and (self.game.isValidPiece(row, col) or len(playerClicks) > 0):
                            sqSelected = location
                            playerClicks.append(sqSelected)
                        else:
                            sqSelected = ()
                            playerClicks = []

                        if len(playerClicks) == 2:
                            move = game_engine.Move(playerClicks[0], playerClicks[1], self.game.board)
                            for check_move in validMoves:
                                if move == check_move:
                                    self.game.makeMove(move)
                                else:
                                    print(move.ID + " - " + check_move.ID)

                            sqSelected = ()
                            playerClicks = []
                            moveMade = True

                # KEYBOARD COMMANDS
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.game.undoMove()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = True

                    if event.key == pygame.K_UP:
                        self.game.restoreMove()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = True

            if moveMade:
                status_of_game = self.game.checkVictory()
                if status_of_game != "":
                    self.state = status_of_game
                else:
                    validMoves = self.game.getAllPossibleMoves()
                    moveMade = False

            self.game_gui.draw_board()

            if len(playerClicks) > 0:
                p_row, p_col = playerClicks[0][0], playerClicks[0][1]
                if self.game.is_correct_turn(p_row, p_col):
                    self.game_gui.highlight_square(p_row, p_col, pygame.Color(50, 170, 80))
                    move_list, capture_list = self.game.check_single_piece_moves(p_row, p_col, validMoves)
                    for move in move_list:
                        self.game_gui.highlight_square(move.endRow, move.endCol, pygame.Color(50, 170, 80))
                    for move in capture_list:
                        self.game_gui.highlight_square(move.endRow, move.endCol, pygame.Color(210, 170, 80))
                else:
                    self.game_gui.highlight_square(p_row, p_col, pygame.Color(170, 50, 80))

            self.game_gui.draw_pieces(self.game.board)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def quit_action(self):
        pygame.quit()
        quit()

    def init_game_action(self):
        self.state = "GAME"

    def switch_game_action(self):
        self.state = "SWITCH"

if __name__ == "__main__":
    bkt = Breakthru()
    bkt.init_game()

    while True:
        if bkt.state == "HOME":
            bkt.home_screen()
        elif bkt.state == "GAME":
            bkt.game_screen()
        elif bkt.state == "SWITCH" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            bkt.switch_screen()
        else:
            bkt.screen.fill(pygame.Color("black"))
            print("ERROR")
