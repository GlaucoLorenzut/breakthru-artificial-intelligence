import os
import pygame
import game_engine
import game_gui
import janitor as jnt
from pathlib import Path


IMGS_PATH = "images"
SAVING_PATH = "saves"
DIMENSION = 11
MAX_FPS = 15
WINDOW_LAYOUT = (500, 80)
WINDOW_WIDTH = 1040
WINDOW_HEIGHT = 720
BOARD_SIZE = 616
BUTTON_SIZE = (200, 50)
BUTTON_TEXT_SIZE = 24


class Breakthru():

    def __init__(self):
        self.state = "MENU"
        self.screen = None
        self.clock = None
        self.game_gui = None
        self.game = None

    def quit_action(self):
        pygame.quit()
        quit()

    def init_game_action(self):
        self.state = "GAME"

    def open_menu_action(self):
        self.state = "MENU"

    def save_game_action(self):
        jnt.pickle_save(self.game, Path(SAVING_PATH) / "save.pickle")

    def load_game_action(self):
        self.game = jnt.pickle_load(Path(SAVING_PATH) / "save.pickle")


    def init_game(self):
        jnt.create_dir(SAVING_PATH)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_LAYOUT
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("  Breakthru")
        self.clock = pygame.time.Clock()
        self.screen.fill(pygame.Color("black"))
        self.game_gui = game_gui.GameGUI(self.screen, BOARD_SIZE, DIMENSION)



        pygame.init()
        pygame.font.init()


    def menu_screen(self):
        self.screen.fill(pygame.Color("black"))

        panel_dx_layout = (self.game_gui.board_size + 2 * self.game_gui.board_layout, self.game_gui.board_layout)

        button_single_player = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + 50,
                                               panel_dx_layout[1],
                                               BUTTON_SIZE,
                                               pygame.Color("gray"),
                                               BUTTON_TEXT_SIZE,
                                               "Single Player")

        button_multi_player = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + 50,
                                               panel_dx_layout[1] + BUTTON_SIZE[1] + 50,
                                               BUTTON_SIZE,
                                               pygame.Color("gray"),
                                               BUTTON_TEXT_SIZE,
                                               "Multi Player")


        while bkt.state == "MENU" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            button_single_player.draw()
            button_multi_player.draw()

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    button_single_player.check(mouse_pos, self.init_game_action)
                    button_multi_player.check(mouse_pos, self.init_game_action)

            self.game_gui.draw_game_result(self.state)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def game_screen(self):
        self.screen.fill(pygame.Color("black"))

        self.game = game_engine.GameState()

        self.game_gui.init_board_index()

        validMoves = self.game.getAllPossibleMoves()

        moveMade = False
        self.game_gui.load_images(IMGS_PATH)
        sqSelected = ()
        playerClicks = []

        panel_dx_layout = (self.game_gui.board_size + 2 * self.game_gui.board_layout, self.game_gui.board_layout)

        button_quit_game = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + 50,
                                               panel_dx_layout[1],
                                               BUTTON_SIZE,
                                               pygame.Color("gray"),
                                               BUTTON_TEXT_SIZE,
                                               "Quit Game")

        button_save_game = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + 50,
                                               panel_dx_layout[1] + BUTTON_SIZE[1] + 50,
                                               BUTTON_SIZE,
                                               pygame.Color("gray"),
                                               BUTTON_TEXT_SIZE,
                                               "Save Game")

        button_load_game = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + 50,
                                               panel_dx_layout[1] + 2*BUTTON_SIZE[1] + 100,
                                               BUTTON_SIZE,
                                               pygame.Color("gray"),
                                               BUTTON_TEXT_SIZE,
                                               "Load Game")


        while self.state == "GAME":
            button_quit_game.draw()
            button_save_game.draw()
            button_load_game.draw()

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    location = self.game_gui.get_board_location(mouse_pos)

                    button_quit_game.check(mouse_pos, self.open_menu_action)
                    button_save_game.check(mouse_pos, self.save_game_action)
                    button_load_game.check(mouse_pos, self.load_game_action)

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
                self.state = self.game.checkVictory()
                if self.state == "GAME":
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


if __name__ == "__main__":
    bkt = Breakthru()
    bkt.init_game()

    while True:
        if bkt.state == "MENU" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            bkt.menu_screen()
        elif bkt.state == "GAME":
            bkt.game_screen()
        else:
            bkt.screen.fill(pygame.Color("black"))
            print("ERROR")
