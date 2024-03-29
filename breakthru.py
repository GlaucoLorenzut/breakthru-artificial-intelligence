
import pygame
import game_engine
import game_gui
import os
import utils.janitor as saving_lib
from pathlib import Path
import sys

saving_lib.exe_installer()

import yaml

class Breakthru():

    def __init__(self, window_size, board_length):
        self.window_size = window_size
        self.board_length = board_length
        self.row_dimension = 11 # 11x11

        self.images_path = Path("images")
        self.saves_path = Path("saves")

        self.state    = "MENU"
        
        self.screen   = pygame.display.set_mode(self.window_size)
        self.clock    = pygame.time.Clock()
        self.game_gui = game_gui.GameGui(self.screen, self.board_length, self.row_dimension)
        self.game     = None
        self.sq_selected = ()
        self.pieces_selected = []

        self.button_vs_gold_AI   = None
        self.button_vs_silver_AI = None
        self.button_multi_player = None
        self.button_save_game    = None
        self.button_load_game    = None
        self.button_undo_move    = None
        self.button_restore_move = None
        self.button_skip_round   = None
        self.button_quit_game    = None

        self.multi_player = True
        self.AI_turn = None
        self.game_pause = False

        self.init_sw()

    ###################### BUTTON ACTIONS ######################
    def quit_action(self):
        pygame.quit()
        sys.exit()


    def init_multiplayer_game_action(self):
        self.state = "GAME"
        self.multi_player = True
        self.game = game_engine.GameEngine()
        

    def init_singleplayer_game_action(self, opponent, ai="THE_ALPHABETA_GUY"):
        self.state = "GAME"
        self.multi_player = False
        self.game = game_engine.GameEngine(ai)
        self.AI_turn = opponent # G against golden AI


    def open_menu_action(self):
        self.state = "MENU"


    def save_game_action(self):
        saving_lib.pickle_save(self.game, self.saves_path / "save.pickle")
        self.logger.print_message("[game saved]")


    def load_game_action(self):
        load_game = saving_lib.pickle_load(self.saves_path / "save.pickle")
        if load_game:
            self.game = load_game
            self.logger.print_message("[game loaded]")
        else:
            self.logger.print_message("[no games found]")


    def undo_move_action(self):
        move_id = self.game.undo_move()
        gold_turn = self.game.is_gold_turn()
        self.logger.print_move(move_id, gold_turn, "undo")
        self.sq_selected = ()
        self.pieces_selected = []
        if not self.multi_player and move_id:
            self.game_pause = True
            self.logger.print_message("[press P to continue]")


    def restore_move_action(self):
        gold_turn = self.game.is_gold_turn()

        move_id = self.game.restore_move()
        self.logger.print_move(move_id, gold_turn, "restore")
        self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []
        if not self.multi_player and move_id:
            self.game_pause = True
            self.logger.print_message("[press P to continue]")


    def skip_move_action(self):
        gold_turn = self.game.is_gold_turn()
        move_id = self.game.skip_move()
        self.logger.print_move(move_id, gold_turn, "skip")
        self.state = self.game.check_victory()
        self.sq_selected = ()
        self.pieces_selected = []
    ############################################################


    def init_sw(self):
        saving_lib.create_dir(self.saves_path)
        pygame.display.set_caption("  Breakthru")
        pygame.init()
        pygame.font.init()

        m_btn_size = config['menu_button']['size']
        m_btn_color = config['menu_button']['color']
        m_btn_txt_size = config['menu_button']['text_size']

        g_btn_size = config['game_button']['size']
        g_btn_color = config['game_button']['color']
        g_btn_txt_size = config['game_button']['text_size']

        turner_size          = config['turner']['size']
        turner_color         = config['turner']['color']
        turner_color_outline = config['turner']['color_outline']

        logger_size          = config['logger']['size']
        logger_color         = config['logger']['color']
        logger_color_outline = config['logger']['color_outline']

        ######### INIT MENU ELEMENTS #############
        A = self.game_gui.board_size + self.game_gui.board_layout
        menu_layout_dx = (A + 0.5*(self.window_size[0] - A) - 0.5*m_btn_size[0], 0.5*self.window_size[1])

        self.button_vs_gold_AI = game_gui.Button(self.screen,
                                               menu_layout_dx[0],
                                               menu_layout_dx[1] - 0.5*m_btn_size[1] - m_btn_size[1] - 70,
                                               m_btn_size,
                                               m_btn_color,
                                               m_btn_txt_size,
                                               "vs Gold AI")

        self.button_vs_silver_AI = game_gui.Button(self.screen,
                                               menu_layout_dx[0],
                                               menu_layout_dx[1] - 0.5*m_btn_size[1],
                                               m_btn_size,
                                               m_btn_color,
                                               m_btn_txt_size,
                                               "vs Silver AI")

        self.button_multi_player = game_gui.Button(self.screen,
                                               menu_layout_dx[0],
                                               menu_layout_dx[1] - 0.5*m_btn_size[1] + m_btn_size[1] + 70,
                                               m_btn_size,
                                               m_btn_color,
                                               m_btn_txt_size,
                                               "Multi Player")

        ######## INIT GAME ELEMENTS ###############
        A = self.game_gui.board_size + 2*self.game_gui.board_layout
        game_layout_dx = (0.5*A + 0.5*self.window_size[0], self.game_gui.board_layout+ 1)


        self.turner = game_gui.Turner(self.screen,
                                 game_layout_dx[0] - 0.5*turner_size[0],
                                 game_layout_dx[1],
                                 turner_size,
                                 turner_color,
                                 turner_color_outline,
                                 )

        self.logger = game_gui.Logger(self.screen,
                                 game_layout_dx[0] - 0.5*logger_size[0],
                                 self.window_size[1] - game_layout_dx[1] - logger_size[1] + 9,
                                 logger_size,
                                 logger_color,
                                 logger_color_outline,
                                 )

        button_layout_sx_dx = (-(g_btn_size[0] + 10), 10)
        button_layout_vertical = turner_size[1]

        self.button_save_game = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[0],
                                               game_layout_dx[1] + button_layout_vertical + 20,
                                               g_btn_size,
                                               g_btn_color,
                                               g_btn_txt_size,
                                               "Save Game")

        self.button_load_game = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[1],
                                               game_layout_dx[1] + button_layout_vertical + 20,
                                               g_btn_size,
                                               g_btn_color,
                                               g_btn_txt_size,
                                               "Load Game")

        self.button_undo_move = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[0],
                                               game_layout_dx[1] + button_layout_vertical + g_btn_size[1] + 40,
                                               g_btn_size,
                                               g_btn_color,
                                               g_btn_txt_size,
                                               "Undo Move")

        self.button_restore_move = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[1],
                                               game_layout_dx[1] + button_layout_vertical + g_btn_size[1] + 40,
                                               g_btn_size,
                                               g_btn_color,
                                               g_btn_txt_size,
                                               "Restore Move")

        self.button_skip_round = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[0],
                                               game_layout_dx[1] + button_layout_vertical + 2*g_btn_size[1] + 60,
                                               g_btn_size,
                                               g_btn_color,
                                               g_btn_txt_size,
                                               "Skip First Play")

        self.button_quit_game = game_gui.Button(self.screen,
                                               game_layout_dx[0] + button_layout_sx_dx[1],
                                               game_layout_dx[1] + button_layout_vertical + 2*g_btn_size[1] + 60,
                                               g_btn_size,
                                               g_btn_color,
                                               g_btn_txt_size,
                                               "Quit Game")


    def draw_menu_elements(self):
        self.button_vs_gold_AI.draw()
        self.button_vs_silver_AI.draw()
        self.button_multi_player.draw()


    def draw_game_elements(self):
        self.turner.draw(self.game.is_gold_turn(), self.game.ai_timer)
        self.logger.draw()

        self.button_quit_game.draw()
        self.button_save_game.draw()
        self.button_load_game.draw()
        self.button_undo_move.draw()
        self.button_restore_move.draw()
        self.button_skip_round.draw(self.game.is_first_move and (self.multi_player or self.AI_turn=='S'))


    def menu_screen(self):
        while bkt.state != "GAME":
            for event in pygame.event.get():
                # MOUSE COMMANDS
                if event.type == pygame.QUIT:
                    self.quit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.button_vs_gold_AI.check(mouse_pos, lambda: self.init_singleplayer_game_action("G"))
                    self.button_vs_silver_AI.check(mouse_pos, lambda: self.init_singleplayer_game_action("S"))
                    self.button_multi_player.check(mouse_pos, self.init_multiplayer_game_action)

            self.draw_menu_elements()
            self.game_gui.draw_game_result(self.state)

            self.clock.tick(config['max_fps'])
            pygame.display.update()


    def game_screen(self):
        self.game_gui.init_board_index()
        self.game_gui.load_images(self.images_path)

        self.sq_selected = ()
        self.pieces_selected = []
        self.logger.clean_logger()

        while self.state == "GAME":
            #self.draw_game_elements()

            if not self.multi_player and self.is_AI_turn() and not self.game_pause:
                move_ai, score = self.game.ai_choose_move()

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
                # KEYBOARD COMMANDS
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game_pause = False

            # DRAW BOARD, PATHS AND PIECES
            self.game_gui.draw_board()

            if len(self.pieces_selected) == 1:
                r, c = self.pieces_selected[0][0], self.pieces_selected[0][1]
                right_turn = self.game.is_piece_of_right_turn(r, c)
                move_list, capture_list = self.game.check_single_piece_moves(r, c)
                self.game_gui.draw_highlighted_paths(r, c, right_turn, move_list, capture_list)

            if len(self.game.game_log)> 0:
                last_move = self.game.game_log[-1]
                if last_move.ID != "skip":
                    self.game_gui.draw_last_move_path(self.game.game_log[-1].start, self.game.game_log[-1].end)

            self.game_gui.draw_pieces(self.game.board)
            self.draw_game_elements()
            self.clock.tick(config['max_fps'])
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


    def is_AI_turn(self):
        if not self.AI_turn:
            return False
        if (self.game.is_gold_turn() and self.AI_turn == "G") or (not self.game.is_gold_turn() and self.AI_turn == "S"):
            return True
        return False


if __name__ == "__main__":
    with open('config\\config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # set the gui position on the screen
    win_pos_x, win_pos_y = config['window']['position']
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_pos_x, win_pos_y)

    bkt = Breakthru(
        window_size=config['window']['size'], 
        board_length=config['board']['length']
        )
    
    while True:
        bkt.screen.fill(pygame.Color("black"))

        if bkt.state != "GAME": # bkt.state == "MENU" | "GOLD_WIN" | "SILVER_WIN" | "DRAW":
            bkt.menu_screen()
        elif bkt.state == "GAME":
            bkt.game_screen()
