import os
import pygame
import game_engine
import game_gui
import janitor as jnt
from pathlib import Path
import game_ai


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

LOGGER_SIZE = (275, 360)
LOGGER_COLOR = pygame.Color("blue")
LOGGER_COLOR_OUTLINE = pygame.Color("white")

ADVANCED_RULES = True

TEST = [
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]",
   "move  [ a3-d5 ]"
]

class Breakthru():

    def __init__(self):
        self.state    = "MENU"
        self.screen   =  pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock    =  pygame.time.Clock()
        self.game_gui =  game_gui.GameGui(self.screen, BOARD_SIZE, DIMENSION)
        self.game     = None
        self.sq_selected = ()
        self.pieces_selected = []
        #self.isFirstRound = True

        self.button_vs_gold_AI   = None
        self.button_vs_silver_AI = None
        self.button_multi_player = None
        self.button_save_game    = None
        self.button_load_game    = None
        self.button_undo_move    = None
        self.button_restore_move = None
        self.button_skip_round   = None
        self.button_quit_game    = None

        #self.ai = game_ai.AI(None, None)
        self.multi_player = True
        self.AI_turn = None
        #self.timer = 0


    ###################### BUTTON ACTIONS ######################
    def quit_action(self):
        pygame.quit()
        quit()

    def init_multiplayer_game_action(self):
        self.state = "GAME"
        self.game = game_engine.GameEngine()
        self.multi_player = True

    def init_vs_goldAI_game_action(self):
        self.state = "GAME"
        self.multi_player = False
        self.AI_turn = "G"
        self.game = game_engine.GameEngine("THE_RANDOM_GUY")
        #self.game.ai.board = self.game.board
        #self.game.ai.init_ai("THE_RANDOM_GUY")

    def init_vs_silverAI_game_action(self):
        self.state = "GAME"
        self.multi_player = False
        self.AI_turn = "S"
        self.game = game_engine.GameEngine("THE_NOMNOM_GUY")
        #self.game.ai.board = self.game.board
        #self.game.ai.init_ai("THE_NOMNOM_GUY")

    def open_menu_action(self):
        self.state = "MENU"

    def save_game_action(self):
        jnt.pickle_save(self.game, Path(SAVING_PATH) / "save.pickle")

    def load_game_action(self):
        self.game = jnt.pickle_load(Path(SAVING_PATH) / "save.pickle")

    def undo_move_action(self):
        gold_turn = self.game.is_gold_turn()
        move_id = self.game.undo_move()
        self.logger.print_move(move_id, gold_turn, "undo")
        #self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []

    def restore_move_action(self):
        gold_turn = self.game.is_gold_turn()
        move_id = self.game.restore_move()
        self.logger.print_move(move_id, gold_turn, "restore")
        self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []

    def skip_move_action(self):
        gold_turn = self.game.is_gold_turn()
        move_id = self.game.skip_move()
        self.logger.print_move(move_id, gold_turn, "skip")
        self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []
    ############################################################


    def init_sw(self):
        jnt.create_dir(SAVING_PATH)
        pygame.display.set_caption("  Breakthru")
        pygame.init()
        pygame.font.init()

        ######### INIT MENU ELEMENTS #############
        A = self.game_gui.board_size + self.game_gui.board_layout
        menu_layout_dx = (A + 0.5*(WINDOW_WIDTH - A) - 0.5*MENU_BUTTON_SIZE[0], 0.5*WINDOW_HEIGHT)


        self.button_vs_gold_AI = game_gui.Button(self.screen,
                                               menu_layout_dx[0],
                                               menu_layout_dx[1] - 0.5*MENU_BUTTON_SIZE[1] - MENU_BUTTON_SIZE[1] - 70,
                                               MENU_BUTTON_SIZE,
                                               MENU_BUTTON_COLOR,
                                               MENU_BUTTON_TEXT_SIZE,
                                               "vs Gold AI")

        self.button_vs_silver_AI = game_gui.Button(self.screen,
                                               menu_layout_dx[0],
                                               menu_layout_dx[1] - 0.5*MENU_BUTTON_SIZE[1],
                                               MENU_BUTTON_SIZE,
                                               MENU_BUTTON_COLOR,
                                               MENU_BUTTON_TEXT_SIZE,
                                               "vs Silver AI")

        self.button_multi_player = game_gui.Button(self.screen,
                                               menu_layout_dx[0],
                                               menu_layout_dx[1] - 0.5*MENU_BUTTON_SIZE[1] + MENU_BUTTON_SIZE[1] + 70,
                                               MENU_BUTTON_SIZE,
                                               MENU_BUTTON_COLOR,
                                               MENU_BUTTON_TEXT_SIZE,
                                               "Multi Player")

        ######## INIT GAME ELEMENTS ###############
        A = self.game_gui.board_size + 2*self.game_gui.board_layout
        game_layout_dx = (0.5*A + 0.5*WINDOW_WIDTH, self.game_gui.board_layout+ 1)


        self.turner = game_gui.Turner(self.screen,
                                 game_layout_dx[0] - 0.5*TURNER_SIZE[0],
                                 game_layout_dx[1],
                                 TURNER_SIZE,
                                 TURNER_COLOR,
                                 TURNER_COLOR_OUTLINE,
                                 )

        self.logger = game_gui.Logger(self.screen,
                                 game_layout_dx[0] - 0.5*LOGGER_SIZE[0],
                                 WINDOW_HEIGHT - game_layout_dx[1] - LOGGER_SIZE[1] + 9,
                                 LOGGER_SIZE,
                                 LOGGER_COLOR,
                                 LOGGER_COLOR_OUTLINE,
                                 )

        button_layout_sx_dx = (-(GAME_BUTTON_SIZE[0] + 10), 10)
        button_layout_vertical = TURNER_SIZE[1]

        self.button_save_game = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[0],
                                               game_layout_dx[1] + button_layout_vertical + 20,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Save Game")

        self.button_load_game = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[1],
                                               game_layout_dx[1] + button_layout_vertical + 20,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Load Game")

        self.button_undo_move = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[0],
                                               game_layout_dx[1] + button_layout_vertical + GAME_BUTTON_SIZE[1] + 40,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Undo Move")

        self.button_restore_move = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[1],
                                               game_layout_dx[1] + button_layout_vertical + GAME_BUTTON_SIZE[1] + 40,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Restore Move")

        self.button_skip_round = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[0],
                                               game_layout_dx[1] + button_layout_vertical + 2*GAME_BUTTON_SIZE[1] + 60,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Skip First Play")

        self.button_quit_game = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[1],
                                               game_layout_dx[1] + button_layout_vertical + 2*GAME_BUTTON_SIZE[1] + 60,
                                               GAME_BUTTON_SIZE,
                                               GAME_BUTTON_COLOR,
                                               GAME_BUTTON_TEXT_SIZE,
                                               "Quit Game")


    def draw_menu_elements(self):
        self.button_vs_gold_AI.draw()
        self.button_vs_silver_AI.draw()
        self.button_multi_player.draw()

    def draw_game_elements(self):
        self.turner.draw(self.game.is_gold_turn(), self.game.ai.timer)
        self.logger.draw()

        self.button_quit_game.draw()
        self.button_save_game.draw()
        self.button_load_game.draw()
        self.button_undo_move.draw()
        self.button_restore_move.draw()
        self.button_skip_round.draw(self.game.is_first_move)


    def menu_screen(self):
        while bkt.state != "GAME":
            self.draw_menu_elements()

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.button_vs_gold_AI.check(mouse_pos, self.init_vs_goldAI_game_action)
                    self.button_vs_silver_AI.check(mouse_pos, self.init_vs_silverAI_game_action)
                    self.button_multi_player.check(mouse_pos, self.init_multiplayer_game_action)

            self.game_gui.draw_game_result(self.state)

            self.clock.tick(MAX_FPS)
            pygame.display.update()


    def game_screen(self):
        self.game_gui.init_board_index()
        self.game_gui.load_images(IMGS_PATH)

        self.sq_selected = ()
        self.pieces_selected = []
        self.logger.clean_logger()
        #self.timer = 0
        #for test in TEST:
        #    self.logger.print_move(test)
#
        while self.state == "GAME":
            self.draw_game_elements()

            if not self.multi_player and self.is_AI_turn():
                move_ai = self.game.ai.choose_move(self.game.valid_moves)
                if move_ai:
                    gold_turn = self.game.is_gold_turn()
                    move_id = self.game.make_move(move_ai)
                    self.logger.print_move(move_id, gold_turn)
                    self.state = self.game.check_victory()
                    self.sq_selected = ()
                    self.pieces_selected = []

            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.button_quit_game.check(mouse_pos, self.open_menu_action)
                    self.button_skip_round.check(mouse_pos, self.skip_move_action)
                    self.button_save_game.check(mouse_pos, self.save_game_action)
                    self.button_load_game.check(mouse_pos, self.load_game_action)
                    self.button_undo_move.check(mouse_pos, self.undo_move_action)
                    self.button_restore_move.check(mouse_pos, self.restore_move_action)

                    if self.multi_player or not self.is_AI_turn():
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


    def make_the_move(self, mouse_pos):
        new_location = self.game_gui.get_board_location(mouse_pos)
        if new_location:
            row, col = new_location

            if self.sq_selected != new_location:
                if len(self.pieces_selected) == 0 and self.game.is_valid_piece(row, col):
                    self.sq_selected = new_location
                    self.pieces_selected.append(self.sq_selected)
                elif len(self.pieces_selected) == 1 and not self.game.is_valid_piece(row, col):
                    self.sq_selected = new_location
                    self.pieces_selected.append(self.sq_selected)
                elif len(self.pieces_selected) == 1 and self.game.is_valid_piece(row, col):
                    if self.game.is_piece_of_right_turn(row, col):
                        self.sq_selected = new_location
                        self.pieces_selected = [self.sq_selected]
                    else:
                        self.sq_selected = new_location
                        self.pieces_selected.append(self.sq_selected)

                if len(self.pieces_selected) == 2:
                    move = game_engine.Move(self.pieces_selected[0], self.pieces_selected[1], self.game.board)
                    if move in self.game.valid_moves:
                        gold_turn = self.game.is_gold_turn()
                        move_id = self.game.make_move(move)
                        self.logger.print_move(move_id, gold_turn)
                        self.state = self.game.check_victory()
                        self.sq_selected = ()
                        self.pieces_selected = []
                    else:
                        self.sq_selected = new_location
                        self.pieces_selected = [new_location] if self.game.is_valid_piece(row, col) else []
            else:
                self.sq_selected = ()
                self.piece_selected = []

            #else:
            #    pass
                #self.sq_selected = ()
                #self.piece_selected = []

            #print(self.sq_selected)
            #print(new_location)
            #print(self.pieces_selected)
            #print("\n")


    def is_AI_turn(self):
        if not self.AI_turn:
            return False
        if (self.game.is_gold_turn() and self.AI_turn == "G") or (not self.game.is_gold_turn() and self.AI_turn == "S"):
            return True
        return False


if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_LAYOUT_X, WINDOW_LAYOUT_Y)
    bkt = Breakthru()
    bkt.init_sw()

    while True:
        bkt.screen.fill(pygame.Color("black"))

        if bkt.state != "GAME": #== "MENU" or bkt.state == "GOLD_WIN" or bkt.state == "SILVER_WIN" or bkt.state == "DRAW":
            bkt.menu_screen()
        elif bkt.state == "GAME":
            bkt.game_screen()
        #else:
        #    print("[ERROR]: state is ( " + bkt.state + " )")
        #    bkt.quit_action()