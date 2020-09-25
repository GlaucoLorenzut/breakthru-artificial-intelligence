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

        self.text_rect(
            text,
            50,
            (self.board_layout, self.board_layout),
            (self.board_size + 1, self.board_size + 1),
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

    def draw(self):
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(None, self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(
                text,
                (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2))
            )

    def check(self, pos, action=None):
        if self.x + self.width > pos[0] > self.x and self.y + self.height > pos[1] > self.y:
            pygame.draw.rect(self.screen, pygame.Color("white"), (self.x, self.y, self.width, self.height))
            if action != None:
                return action()
            return True
        return False



def text_button(self, event, text, text_size, pos_x, pos_y, width, height, color, action_color, action=None):

    return

    if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
        pygame.draw.rect(self.screen, action_color, (pos_x, pos_y, width, height))
        if event == pygame.MOUSEBUTTONDOWN and action != None:
            pygame.draw.rect(self.screen, pygame.Color("white"), (pos_x, pos_y, width, height))
            return action()
    else:
        pygame.draw.rect(self.screen, color, (pos_x, pos_y, width, height))

    def text_objects(text, font):
        textSurface = font.render(text, True, pygame.Color("black"))
        return textSurface, textSurface.get_rect()

    smallText = pygame.font.Font("freesansbold.ttf", text_size)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((pos_x + (width / 2)), (pos_y + (height / 2)))
    self.screen.blit(textSurf, textRect)