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
WINDOW_LAYOUT_X, WINDOW_LAYOUT_Y = 250, 80
WINDOW_WIDTH, WINDOW_HEIGHT = 1050, 720
BOARD_SIZE = 616

MENU_BUTTON_SIZE = (200, 60)
MENU_BUTTON_TEXT_SIZE = 30
MENU_BUTTON_COLOR = pygame.Color("gray")

GAME_BUTTON_SIZE = (130, 40)
GAME_BUTTON_TEXT_SIZE = 23
GAME_BUTTON_COLOR = pygame.Color("gray")

TURNER_SIZE = (275, 50)
TURNER_COLOR = pygame.Color("blue")
TURNER_COLOR_OUTLINE = pygame.Color("white")


LOGGER_SIZE = (275, 350)
LOGGER_COLOR = pygame.Color("blue")
LOGGER_COLOR_OUTLINE = pygame.Color("white")


class Breakthru():

    def __init__(self):
        self.state    = "GAME"
        self.screen   =  pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock    =  pygame.time.Clock()
        self.game_gui =  game_gui.GameGui(self.screen, BOARD_SIZE, DIMENSION)
        self.game     = None
        self.sq_selected = ()
        self.pieces_selected = []
        self.timer = 0

    ###################### BUTTON ACTIONS ######################
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

    def undo_move_action(self):
        self.game.undo_move()
        #self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []

    def restore_move_action(self):
        self.game.restore_move()
        self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []
    ############################################################


    def menu_screen(self):
        A = self.game_gui.board_size + self.game_gui.board_layout
        panel_dx_layout = (A + 0.5*(WINDOW_WIDTH - A) - 0.5*MENU_BUTTON_SIZE[0], 0.5*WINDOW_HEIGHT)


        button_vs_gold_AI = game_gui.Button(self.screen,
                                               panel_dx_layout[0],
                                               panel_dx_layout[1] - 0.5*MENU_BUTTON_SIZE[1] - MENU_BUTTON_SIZE[1] - 70,
                                               MENU_BUTTON_SIZE,
                                               MENU_BUTTON_COLOR,
                                               MENU_BUTTON_TEXT_SIZE,
                                               "vs Gold AI")

        button_vs_silver_AI = game_gui.Button(self.screen,
                                               panel_dx_layout[0],
                                               panel_dx_layout[1] - 0.5*MENU_BUTTON_SIZE[1],
                                               MENU_BUTTON_SIZE,
                                               MENU_BUTTON_COLOR,
                                               MENU_BUTTON_TEXT_SIZE,
                                               "vs Silver AI")

        button_multi_player = game_gui.Button(self.screen,
                                               panel_dx_layout[0],
                                               panel_dx_layout[1] - 0.5*MENU_BUTTON_SIZE[1] + MENU_BUTTON_SIZE[1] + 70,
                                               MENU_BUTTON_SIZE,
                                               MENU_BUTTON_COLOR,
                                               MENU_BUTTON_TEXT_SIZE,
                                               "Multi Player")


        while bkt.state == "MENU" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            button_vs_gold_AI.draw()
            button_vs_silver_AI.draw()
            button_multi_player.draw()

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    button_vs_gold_AI.check(mouse_pos, self.init_game_action)
                    button_vs_silver_AI.check(mouse_pos, self.init_game_action)
                    button_multi_player.check(mouse_pos, self.init_game_action)

            self.game_gui.draw_game_result(self.state)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def game_screen(self):
        A = self.game_gui.board_size + 2*self.game_gui.board_layout
        panel_dx_layout = (0.5*A + 0.5*WINDOW_WIDTH, self.game_gui.board_layout)


        turner = game_gui.Turner(self.screen,
                                 panel_dx_layout[0] - 0.5*TURNER_SIZE[0],
                                 panel_dx_layout[1],
                                 TURNER_SIZE,
                                 TURNER_COLOR,
                                 TURNER_COLOR_OUTLINE,
                                 )

        logger = game_gui.Logger(self.screen,
                                 panel_dx_layout[0] - 0.5*LOGGER_SIZE[0],
                                 WINDOW_HEIGHT - panel_dx_layout[1] - LOGGER_SIZE[1],
                                 LOGGER_SIZE,
                                 LOGGER_COLOR,
                                 LOGGER_COLOR_OUTLINE,
                                 )

        button_layout_sx_dx = (-(GAME_BUTTON_SIZE[0] + 10), 10)
        button_layout_vertical = TURNER_SIZE[1]

        button_save_game = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + button_layout_sx_dx[0],
                                               panel_dx_layout[1] + button_layout_vertical + 20,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Save Game")

        button_load_game = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + button_layout_sx_dx[1],
                                               panel_dx_layout[1] + button_layout_vertical + 20,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Load Game")

        button_undo_move = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + button_layout_sx_dx[0],
                                               panel_dx_layout[1] + button_layout_vertical + GAME_BUTTON_SIZE[1] + 40,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Undo Move")

        button_restore_move = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + button_layout_sx_dx[1],
                                               panel_dx_layout[1] + button_layout_vertical + GAME_BUTTON_SIZE[1] + 40,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Restore Move")

        button_quit_game = game_gui.Button(self.screen,
                                               panel_dx_layout[0] - 0.5*GAME_BUTTON_SIZE[0],
                                               panel_dx_layout[1] + button_layout_vertical + 2*GAME_BUTTON_SIZE[1] + 60,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Quit Game")


        self.game = game_engine.GameEngine()

        self.game_gui.init_board_index()
        self.game_gui.load_images(IMGS_PATH)

        self.sq_selected = ()
        self.pieces_selected = []
        self.timer = 0
        #self.game.valid_moves = self.game.get_all_possible_moves()
        #self.game.update_all_possible_moves()

        while self.state == "GAME":
            turner.draw()
            logger.draw()
            button_quit_game.draw()
            button_save_game.draw()
            button_load_game.draw()
            button_undo_move.draw()
            button_restore_move.draw()

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    button_quit_game.check(mouse_pos, self.open_menu_action)
                    button_save_game.check(mouse_pos, self.save_game_action)
                    button_load_game.check(mouse_pos, self.load_game_action)
                    button_undo_move.check(mouse_pos, self.undo_move_action)
                    button_restore_move.check(mouse_pos, self.restore_move_action)

                    self.make_the_move(mouse_pos)

            # DRAW BOARD, PATHS AND PIECES
            self.game_gui.draw_board()

            if len(self.pieces_selected) == 1:
                r, c = self.pieces_selected[0][0], self.pieces_selected[0][1]
                right_turn = self.game.is_piece_of_right_turn(r, c)
                move_list, capture_list = self.game.check_single_piece_moves(r, c)
                self.game_gui.draw_highlighted_paths(r, c, right_turn, move_list, capture_list)

            self.game_gui.draw_pieces(self.game.board)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def init_sw(self):
        jnt.create_dir(SAVING_PATH)

        pygame.display.set_caption("  Breakthru")
        pygame.init()
        pygame.font.init()

    def make_the_move(self, mouse_pos):
        start_clock = pygame.time.get_ticks()
        board_location = self.game_gui.get_board_location(mouse_pos)
        if board_location:
            row, col = board_location
            if self.sq_selected != board_location and (self.game.is_valid_piece(row, col) or len(self.pieces_selected) > 0):
                self.sq_selected = board_location
                self.pieces_selected.append(self.sq_selected)
            else:
                self.sq_selected = ()
                self.piece_selected = []

            if len(self.pieces_selected) == 2:
                move = game_engine.Move(self.pieces_selected[0], self.pieces_selected[1], self.game.board)
                if move in self.game.valid_moves:
                    self.game.make_move(move)

                self.state = self.game.check_victory()
                self.sq_selected = ()
                self.pieces_selected = []
        end_clock = pygame.time.get_ticks()
        self.timer += end_clock - start_clock
        print(self.timer)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_LAYOUT_X, WINDOW_LAYOUT_Y)
    bkt = Breakthru()
    bkt.init_sw()

    while True:
        bkt.screen.fill(pygame.Color("black"))

        if bkt.state == "MENU" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            bkt.menu_screen()
        elif bkt.state == "GAME":
            bkt.game_screen()
        else:
            print("[ERROR]: state is ( " + bkt.state + " )")
            bkt.quit_action()
