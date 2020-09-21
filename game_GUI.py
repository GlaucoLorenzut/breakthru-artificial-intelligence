import pygame

class GameGUI():
    def __init__(self, screen, board_width, board_height, dimension):
        self.screen = screen
        self.width = board_width
        self.height = board_height
        self.dimension = dimension
        self.square_size = board_width // dimension
        self.images = {}

    def init_board_index(self):
        index_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10}

        for abc, ind in index_map.items():
            self.write_index(ind + 1, 44, self.width, (10 - ind) * self.square_size)
            self.write_index(abc, 44, ind * self.square_size, self.height)

    def write_index(self, text, size, pos_X, pos_Y):
        font = pygame.font.Font(None, size)  # pygame.font.SysFont('Times New Roman', 36)
        label = font.render(str(text), True, pygame.Color("white"))
        layout_X = 0.5 * (self.square_size - label.get_rect().width)
        layout_Y = 0.5 * (self.square_size - label.get_rect().height) + 3
        self.screen.blit(label, (int(pos_X + layout_X), int(pos_Y + layout_Y)))
        # print(str(text) + " - " + str(label.get_rect().height) + " - " + str(pos_Y + layout_X))


    def load_images(self, path):
        pieces = ["sS", "gS", "gF"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load(path + "/" + piece + ".png"), (self.square_size, self.square_size))


    def get_board_location(self, position):
        if 0 <= position[0] < self.width and 0 <= position[1] < self.height:
            return (position[1] // self.square_size, position[0] // self.square_size)
        return None


    def highlight_square(self, row, col, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(col * self.square_size+1,  row* self.square_size+1, self.square_size-1, self.square_size-1))


    def draw_board(self):
        pygame.draw.rect(self.screen, pygame.Color("blue"), pygame.Rect(0, 0, self.width, self.height))
        for d in range(self.dimension+1):
            # rows
            pygame.draw.line(self.screen, pygame.Color("white"), (0, d*self.square_size), (self.width, d*self.square_size), 1)
            # cols
            pygame.draw.line(self.screen, pygame.Color("white"), (d * self.square_size, 0), (d * self.square_size, self.height), 1)
            if (3 <= d <= 8):
                # inner rows
                pygame.draw.line(self.screen, pygame.Color("white"), (3 * self.square_size-1, d * self.square_size), (8 * self.square_size+1, d * self.square_size), 3)
                # inner cols
                pygame.draw.line(self.screen, pygame.Color("white"), (d * self.square_size, 3 * self.square_size-1), (d * self.square_size, 8 * self.square_size+1), 3)


    def draw_pieces(self, board):
        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = board[r][c]
                if piece != "--":
                    self.screen.blit(self.images[piece], pygame.Rect(c*self.square_size, r*self.square_size, self.square_size, self.square_size))


    def draw_game_result(self, result):
        font = pygame.font.Font(None, 80)

        if result == "GOLD_WIN":
            pygame.draw.rect(self.screen, pygame.Color("yellow"),
                             pygame.Rect(0, 0, self.width,
                                         self.height))
            label = font.render("GOLD PLAYER WINS", True, pygame.Color("black"))
        elif result == "SILVER_WIN":
            pygame.draw.rect(self.screen, pygame.Color("gray"),
                             pygame.Rect(0, 0, self.width,
                                         self.height))
            label = font.render("SILVER PLAYER WINS", True, pygame.Color("black"))
        else: # draw
            pygame.draw.rect(self.screen, pygame.Color("black"),
                             pygame.Rect(0, 0, self.width,
                                         self.height))
            label = font.render("DRAW", True, pygame.Color("white"))

        layout_X = 0.5 * (self.width - label.get_rect().width)
        layout_Y = 0.5 * (self.height - label.get_rect().height)
        self.screen.blit(label, (int(0 + layout_X), int(0 + layout_Y)))