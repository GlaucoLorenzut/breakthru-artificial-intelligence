import pygame

class GameGui():

    def __init__(self, screen, board_size, dimension):
        self.screen = screen
        self.board_size = board_size
        self.dimension = dimension
        self.square_size = board_size // dimension
        self.board_layout = self.square_size
        self.images = {}


    def init_board_index(self):
        index_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10}
        text_size = 30

        for abc, ind in index_map.items():

            self.text_rect(
                ind + 1,
                text_size,
                (0, self.board_layout + (10 - ind) * self.square_size),
                (self.square_size, self.square_size),
            )

            self.text_rect(
                ind + 1,
                text_size,
                (self.board_layout + self.board_size, self.board_layout + (10 - ind) * self.square_size),
                (self.square_size, self.square_size),
            )

            self.text_rect(
                abc,
                text_size,
                (self.board_layout + ind * self.square_size, 0),
                (self.square_size, self.square_size),
            )

            self.text_rect(
                abc,
                text_size,
                (self.board_layout + ind * self.square_size, self.board_layout + self.board_size),
                (self.square_size, self.square_size),
            )


    def text_rect(self, text, text_size, position, size, text_color=pygame.Color("white"), color=None):
        if color:
            pygame.draw.rect(self.screen, color, pygame.Rect(position[0], position[1], size[0], size[1]))

        font = pygame.font.Font("freesansbold.ttf", text_size)
        label = font.render(str(text), True, text_color)
        layout_X = int(position[0] + 0.5 * (size[0] - label.get_rect().width))
        layout_Y = int(position[1] + 0.5 * (size[1] - label.get_rect().height))
        self.screen.blit(label, (layout_X, layout_Y))


    def load_images(self, path):
        pieces = {2:"sS", 1:"gS", 3:"gF"}
        for piece, name_file in pieces.items():
            self.images[piece] = pygame.transform.scale(pygame.image.load(path + "/" + name_file + ".png"), (self.square_size, self.square_size))


    def get_board_location(self, screen_position):
        position = (screen_position[0] - self.board_layout, screen_position[1] - self.board_layout)

        if 0 <= position[0] < self.board_size and 0 <= position[1] < self.board_size:
            return (position[1] // self.square_size, position[0] // self.square_size)
        return None


    def draw_board(self):
        pygame.draw.rect(self.screen, pygame.Color("white"), (self.board_layout - 1, self.board_layout - 1, self.board_size + 3, self.board_size + 3), 0)
        pygame.draw.rect(self.screen, pygame.Color("blue"), pygame.Rect(self.board_layout, self.board_layout, self.board_size, self.board_size))

        lower_inner_board = self.board_layout + 3 * self.square_size - 1
        upper_inner_board = self.board_layout + 8 * self.square_size + 1

        for d in range(self.dimension+1):
            line_step = self.board_layout + d * self.square_size
            # rows
            pygame.draw.line(self.screen, pygame.Color("white"), (self.board_layout, line_step), (self.board_layout + self.board_size, line_step), 1)
            # cols
            pygame.draw.line(self.screen, pygame.Color("white"), (line_step, self.board_layout), (line_step, self.board_layout + self.board_size), 1)

            if (3 <= d <= 8):
                # inner rows
                pygame.draw.line(self.screen, pygame.Color("white"), (lower_inner_board, line_step), (upper_inner_board, line_step), 3)
                # inner cols
                pygame.draw.line(self.screen, pygame.Color("white"), (line_step, lower_inner_board), (line_step, upper_inner_board), 3)


    def draw_pieces(self, board):
        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = board[r][c]
                if piece != 0:
                    self.screen.blit(self.images[piece], pygame.Rect(self.board_layout + c*self.square_size, self.board_layout + r*self.square_size, self.square_size, self.square_size))


    def draw_highlighted_paths(self, r, c, right_turn, move_list, capture_list):
        if right_turn and not (len(move_list)==0 and len(capture_list)==0):
            self.highlight_square(r, c, pygame.Color(50, 170, 80))
            for move in move_list:
                end_r, end_c = move.get_end_pos()
                self.highlight_square(end_r, end_c, pygame.Color(50, 170, 80))
            for move in capture_list:
                end_r, end_c = move.get_end_pos()
                self.highlight_square(end_r, end_c, pygame.Color(210, 170, 80))
        else:
            self.highlight_square(r, c, pygame.Color(170, 50, 80))


    def highlight_square(self, row, col, color):
        pygame.draw.rect(self.screen,
                         color,
                         pygame.Rect(self.board_layout + col * self.square_size + 1,
                                                         self.board_layout + row * self.square_size + 1,
                                                         self.square_size - 1,
                                                         self.square_size - 1)
                         )

    def draw_last_move_path(self, start_sqr, end_sqr):
        start_pos = (self.board_layout + start_sqr[1] * self.square_size + 0.5*self.square_size, self.board_layout + start_sqr[0] * self.square_size + 0.5*self.square_size)
        end_pos   = (self.board_layout + end_sqr[1] * self.square_size+ 0.5*self.square_size, self.board_layout + end_sqr[0] * self.square_size + 0.5*self.square_size)
        pygame.draw.line(self.screen, pygame.Color(55, 255, 55),
                        start_pos,
                        end_pos,
                         3
            )

    def draw_game_result(self, result):
        color = pygame.Color("blue")
        text_color = pygame.Color("yellow")
        text = "B R E A K T H R U"

        if result == "GOLD_WIN":
            text = "GOLD PLAYER WINS"
            text_color = pygame.Color("red")
            color = pygame.Color("yellow")
        elif result == "SILVER_WIN":
            text = "SILVER PLAYER WINS"
            text_color = pygame.Color("red")
            color = pygame.Color("gray")
        elif result == "DRAW":
            text = "SILVER PLAYER WINS"
            text_color = pygame.Color("red")
            color = pygame.Color("black")

        pygame.draw.rect(self.screen, pygame.Color("white"), (self.board_layout - 1, self.board_layout - 1, self.board_size + 3, self.board_size + 3), 0)
        self.text_rect(
            text,
            50,
            (self.board_layout+1, self.board_layout+1),
            (self.board_size-1, self.board_size-1),
            text_color,
            color
        )



class Button():

    def __init__(self, screen, x, y, size, color, text_size, text='', outline_color=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.text_size = text_size
        self.text = text
        self.outline_color = outline_color
        self.enabled = True


    def draw(self, enabled=True):
        self.enabled = enabled

        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        color = self.color if self.enabled else (92,83,83)
        pygame.draw.rect(self.screen, color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            color_text = (0, 0, 0) if self.enabled else (50, 50, 50)
            font = pygame.font.SysFont("freesansbold.ttf", self.text_size)
            text = font.render(self.text, 1, color_text)
            self.screen.blit(
                text,
                (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2))
            )


    def check(self, pos, action=None):
        if not self.enabled:
            return False

        if self.x + self.width > pos[0] > self.x and self.y + self.height > pos[1] > self.y:
            pygame.draw.rect(self.screen, pygame.Color("white"), (self.x, self.y, self.width, self.height))
            if action != None:
                return action()
            return True
        return False



class Turner():

    def __init__(self, screen, x, y, size, color, outline_color=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.legenda_size = 28
        self.text_size = 30
        self.outline_color = outline_color


    def draw(self, is_gold_turn, time):
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        # LEGENDA
        font = pygame.font.SysFont("freesansbold.ttf", self.legenda_size)
        legenda = "TURN                         AI TIME"
        text = font.render(legenda, 1, pygame.Color("white"))
        self.screen.blit(
            text,
            (self.x + 12, self.y - 36)
        )

        # TURN
        font = pygame.font.SysFont("freesansbold.ttf", self.text_size)

        turn_text = "GOLD" if is_gold_turn else "SILVER"
        turn_color = pygame.Color("yellow") if is_gold_turn else pygame.Color("gray")
        turn_text = font.render(turn_text, 1, turn_color)
        self.screen.blit(
            turn_text,
            (self.x + 12, self.y + 0.5*(self.height - turn_text.get_height())+1)
        )

        # DIVIDORY
        layout_x = self.x + 99
        pygame.draw.line(self.screen, pygame.Color("white"), (layout_x, self.y),
                         (layout_x, self.y + self.height), 3)

        # TIME
        font = pygame.font.SysFont("freesansbold.ttf", self.text_size)
        time_text = self.get_text_time(time)#"99h : 59m : 59s"
        time_text = font.render(time_text, 1, pygame.Color("white"))
        self.screen.blit(
            time_text,
            (self.x + self.width - time_text.get_width() - 12, self.y + 0.5*(self.height - time_text.get_height())+1)
        )


    def get_text_time(self, time):
        if time != None:

            time = time // 1000
            hours = time // 3600
            hours_text = str(hours) if hours >= 10 else "0" + str(hours)

            minutes = (time % 3600) // 60
            minutes_text = str(minutes) if minutes >= 10 else "0" + str(minutes)

            seconds = time % 60
            seconds_text = str(seconds) if seconds >= 10 else "0" + str(seconds)

            text = ""
            if time >= 3600:
                text += hours_text + "h : "
            if time >= 60:
                text += minutes_text + "m : "

            text += seconds_text + "s"

            return text
        return ""



class Logger():

    def __init__(self, screen, x, y, size, color, outline_color=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.text_list = []
        self.text_size = 28
        self.list_size = 12
        self.text_layout = (x + 10, y + 12)
        self.outline_color = outline_color


    def print_move(self, id, is_gold_turn, type="move"):
        if id:
            while len(self.text_list) >= self.list_size:
                self.text_list.pop(0)

            log_text = "GOLD    " if is_gold_turn else "SILVER  "
            if type == "move":
                log_text += "move    [ " + id + " ]"
            elif type == "undo":
                log_text += "undo    [ " + id + " ]"
            elif type == "restore":
                log_text += "restore [ " + id + " ]"
            elif type == "skip":
                log_text += "move    [ " + id + " ]"
            self.text_list.append(log_text)
            print(log_text)


    def print_message(self, message):
        if message:
            while len(self.text_list) >= self.list_size:
                self.text_list.pop(0)

            self.text_list.append(message)


    def clean_logger(self):
        self.text_list = []


    def draw(self):
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        for i, text in enumerate(self.text_list):
            font = pygame.font.SysFont("freesansbold.ttf", self.text_size)
            text = font.render(text, 1, pygame.Color("white"))
            self.screen.blit(
                text,
                (self.text_layout[0], self.text_layout[1] + i*(20+8))
            )
