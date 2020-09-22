import pygame

class GameGUI():
    def __init__(self, screen, board_size, dimension):
        self.screen = screen
        self.board_size = board_size
        self.dimension = dimension
        self.square_size = board_size // dimension
        self.board_layout = self.square_size
        self.images = {}

    def init_board_index(self):
        index_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10}

        for abc, ind in index_map.items():
            #self.write_index(ind + 1, 44, 0, self.board_layout + (10 - ind) * self.square_size)
            self.text_rect(
                ind + 1,
                44,
                (0, self.board_layout + (10 - ind) * self.square_size),
                (self.square_size, self.square_size),
            )
            #self.write_index(ind + 1, 44, self.board_layout + self.board_size, self.board_layout + (10 - ind) * self.square_size)
            self.text_rect(
                ind + 1,
                44,
                (self.board_layout + self.board_size, self.board_layout + (10 - ind) * self.square_size),
                (self.square_size, self.square_size),
            )

            #self.write_index(abc, 44, self.board_layout + ind * self.square_size, 0)
            self.text_rect(
                abc,
                44,
                (self.board_layout + ind * self.square_size, 0),
                (self.square_size, self.square_size),
            )
            #self.write_index(abc, 44, self.board_layout + ind * self.square_size, self.board_layout + self.board_size)
            self.text_rect(
                abc,
                44,
                (self.board_layout + ind * self.square_size, self.board_layout + self.board_size),
                (self.square_size, self.square_size),
            )




    def text_rect(self, text, text_size, position, size, text_color=pygame.Color("white"), color=None):

        if color:
            pygame.draw.rect(self.screen, color, pygame.Rect(position[0], position[1], size[0], size[1]))

        font = pygame.font.Font(None, text_size)
        label = font.render(str(text), True, text_color)
        layout_X = int(position[0] + 0.5 * (size[0] - label.get_rect().width))
        layout_Y = int(position[1] + 0.5 * (size[1] - label.get_rect().height))
        self.screen.blit(label, (layout_X, layout_Y))

    #def write_index(self, text, size, pos_X, pos_Y):
    #    font = pygame.font.Font(None, size)  # pygame.font.SysFont('Times New Roman', 36)
    #    label = font.render(str(text), True, pygame.Color("white"))
    #    layout_X = 0.5 * (self.square_size - label.get_rect().width)
    #    layout_Y = 0.5 * (self.square_size - label.get_rect().height) + 3
    #    self.screen.blit(label, (int(pos_X + layout_X), int(pos_Y + layout_Y)))
    #    # print(str(text) + " - " + str(label.get_rect().height) + " - " + str(pos_Y + layout_X))


    def load_images(self, path):
        pieces = ["sS", "gS", "gF"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load(path + "/" + piece + ".png"), (self.square_size, self.square_size))


    def get_board_location(self, screen_position):
        position = (screen_position[0] - self.board_layout, screen_position[1] - self.board_layout)

        if 0 <= position[0] < self.board_size and 0 <= position[1] < self.board_size:
            return (position[1] // self.square_size, position[0] // self.square_size)
        return None


    def highlight_square(self, row, col, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(self.board_layout + col * self.square_size + 1,  self.board_layout + row * self.square_size + 1, self.square_size-1, self.square_size-1))


    def draw_board(self):
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
                if piece != "--":
                    self.screen.blit(self.images[piece], pygame.Rect(self.board_layout + c*self.square_size, self.board_layout + r*self.square_size, self.square_size, self.square_size))


    def draw_game_result(self, result):
        color = pygame.Color("black")
        text = "DRAW"

        if result == "GOLD_WIN":
            text = "GOLD PLAYER WINS"
            color = pygame.Color("yellow")
        elif result == "SILVER_WIN":
            text = "SILVER PLAYER WINS"
            color = pygame.Color("gray")

        self.text_rect(
            text,
            80,
            (self.board_layout, self.board_layout),
            (self.board_size + 1, self.board_size + 1),
            pygame.Color("red"),
            color
        )
