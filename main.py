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
        self.state    = "MENU"
        self.screen   =  pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock    =  pygame.time.Clock()
        self.game_gui =  game_gui.GameGui(self.screen, BOARD_SIZE, DIMENSION)
        self.game     = None

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
    ############################################################


    def menu_screen(self):

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

        button_undo_move = game_gui.Button(self.screen,
                                               panel_dx_layout[0] + 50,
                                               panel_dx_layout[1] + 2*BUTTON_SIZE[1] + 100,
                                               BUTTON_SIZE,
                                               pygame.Color("gray"),
                                               BUTTON_TEXT_SIZE,
                                               "Undo Move")


        self.game = game_engine.GameEngine()

        self.game_gui.init_board_index()
        self.game_gui.load_images(IMGS_PATH)

        sq_selected = ()
        pieces_selected = []
        #self.game.valid_moves = self.game.get_all_possible_moves()
        #self.game.update_all_possible_moves()

        while self.state == "GAME":
            button_quit_game.draw()
            button_save_game.draw()
            button_load_game.draw()
            button_undo_move.draw()

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    button_quit_game.check(mouse_pos, self.open_menu_action)
                    button_save_game.check(mouse_pos, self.save_game_action)
                    button_load_game.check(mouse_pos, self.load_game_action)

                    board_location = self.game_gui.get_board_location(mouse_pos)
                    if board_location:
                        row, col = board_location
                        if sq_selected != board_location and (self.game.is_valid_piece(row, col) or len(pieces_selected) > 0):
                            sq_selected = board_location
                            pieces_selected.append(sq_selected)
                        else:
                            sq_selected = ()
                            piece_selected = []

                        if len(pieces_selected) == 2:
                            move = game_engine.Move(pieces_selected[0], pieces_selected[1], self.game.board)
                            for check_move in self.game.valid_moves:
                                if move == check_move:
                                    self.game.make_move(move)
                                #else:
                                #    print(move.ID + " - " + check_move.ID)

                            self.state = self.game.check_victory()
                            sq_selected = ()
                            pieces_selected = []


                # KEYBOARD COMMANDS
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.game.undo_move()
                        self.state = self.game.check_victory()
                        sq_selected = ()
                        pieces_selected = []


                    if event.key == pygame.K_UP:
                        self.game.restore_move()
                        self.state = self.game.check_victory()
                        sq_selected = ()
                        pieces_selected = []



            # DRAW BOARD, PATHS AND PIECES
            self.game_gui.draw_board()

            if len(pieces_selected) == 1:
                r, c = pieces_selected[0][0], pieces_selected[0][1]
                right_turn = self.game.is_piece_of_right_turn(r, c)
                move_list, capture_list = self.game.check_single_piece_moves(r, c)
                self.game_gui.draw_highlighted_paths(r, c, right_turn, move_list, capture_list)

            self.game_gui.draw_pieces(self.game.board)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def init_sw(self):
        jnt.create_dir(SAVING_PATH)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_LAYOUT

        pygame.display.set_caption("  Breakthru")
        pygame.init()
        pygame.font.init()


if __name__ == "__main__":

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
