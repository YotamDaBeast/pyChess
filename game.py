# pylint: disable=no-member
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pieces.piece import Piece, colors
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook

class Game:

    small_update_text = ""
    rules_check = True
    small_text_color = (0, 0, 0)

    def __init__(self):
        pygame.font.init()
        self.width = 400
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        self.squares = [[0 for x in range(8)] for y in range(8)]
        self.square_width = 50
        self.square_height = 50
        self.white_pieces = [Pawn(0) for x in range(8)] + [Rook(0), Knight(0), Bishop(0), Queen(0), King(0), Bishop(0), Knight(0), Rook(0)]
        self.black_pieces = [Pawn(1) for x in range(8)] + [Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Bishop(1), Knight(1), Rook(1)]
        self.current_player = 0
        self.chosen = None
        self.big_font = pygame.font.SysFont('Comic Sans MS', 30, bold=True)
        self.big_update_text = "Chess Game"
        self.small_font = pygame.font.SysFont('Comic Sans MS', 20, bold=True)
        

    def run(self):
        run = True

        self.create_squares()
        self.setup_board()

        while run:
            pygame.time.Clock().tick(60)

            if Game.rules_check:
                self.big_update_text = colors[self.current_player].capitalize() + "'s Turn"
                if self.check_for_mate():
                    pass
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.check_click() and self.chosen:
                            clk_x, clk_y = pygame.mouse.get_pos()
                            if self.chosen.move(self.win, clk_x, clk_y, self.squares[:], self.white_pieces, self.black_pieces):
                                self.chosen = None

                                if self.current_player == 0:
                                    self.current_player = 1
                                else:
                                    self.current_player = 0
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.check_click()

            self.draw()

    def check_for_mate(self):
        white_king, black_king = False, False

        for white in self.white_pieces:
            if type(white) is King:
                white_king = True
                break
        
        for black in self.black_pieces:
            if type(black) is King:
                black_king = True
                break

        if not white_king:
            self.big_update_text = "WHITE LOST"
            Game.small_update_text = ""
        elif not black_king:
            self.big_update_text = "BLACK LOST"
            Game.small_update_text = ""

        return white_king and black_king


    def draw(self):
        
        self.draw_board()
        self.draw_text()
        self.draw_pieces()

        pygame.display.update()

    def setup_board(self):
        # Setup black pieces
        for num, p in enumerate(self.black_pieces):
            if type(p) is Pawn:
                p.set_position(1, num, self.squares[1][num])
            else:
                p.set_position(0, num-8, self.squares[0][num-8])

        # Setup white pieces
        for num, p in enumerate(self.white_pieces):
            if type(p) is Pawn:
                p.set_position(6, num, self.squares[6][num])
            else:
                p.set_position(7, num-8, self.squares[7][num-8])

    def draw_pieces(self):
        # Draw black pieces
        for p in (self.white_pieces + self.black_pieces):
            p.draw(self.win)

        for p in (self.white_pieces + self.black_pieces):
            if type(p) is Pawn:
                p.draw_promotion(self.win)
        

    def draw_board(self):
        for row_num, row in enumerate(self.squares):
            for square_num, square in enumerate(row):

                if self.chosen and self.chosen.current_row == row_num and self.chosen.current_col == square_num:
                    color = (255, 56, 56)
                
                elif row_num % 2 == 0:
                    if square_num % 2 == 0:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                else:
                    if square_num % 2 == 0:
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)
                
                pygame.draw.rect(self.win, color, square)

    def create_squares(self):
        for row in range(8):
            for col in range(8):
                self.squares[row][col] = pygame.Rect(self.width - self.square_width * (8-col), self.height - self.square_height * (8-row), self.square_width, self.square_height)
    
    def draw_text(self):
        pygame.draw.rect(self.win, (128,128,128), pygame.Rect(0, 0, self.width, 100))
        
        if self.current_player == 0:
            text_color = (255, 255, 255)
        else:
            text_color = (0, 0, 0)

        self.win.blit(self.big_font.render(self.big_update_text, True, text_color), (self.width / 3.75, 10))
        self.win.blit(self.small_font.render(Game.small_update_text, True, Game.small_text_color), (self.width / 3.25, 50))
        


    def check_click(self):
        clk_x, clk_y = pygame.mouse.get_pos()

        if Game.rules_check:
            if self.chosen:
                if self.chosen.click(self.win, clk_x, clk_y, self.chosen.current_square):
                    self.chosen = None
                    return True
            else:
                if self.current_player == 0:
                    # Check white
                    for p in self.white_pieces:
                        if p.click(self.win, clk_x, clk_y, p.current_square):
                            self.chosen = p
                            return True
                else:
                    # Check black
                    for p in self.black_pieces:
                        if p.click(self.win, clk_x, clk_y, p.current_square):
                            self.chosen = p
                            return True
            return False
        else:
            for p in (self.white_pieces + self.black_pieces):
                if type(p) is Pawn:
                    p.click_promotion(clk_x, clk_y, self.white_pieces, self.black_pieces)
                        