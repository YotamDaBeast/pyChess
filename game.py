# pylint: disable=no-member
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pieces.piece import Piece, colors, black_check_message
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook

small_update_text = ""
rules_check = True
small_text_color = (0, 0, 0)
big_text_color = (0, 0, 0)

class Game:

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
        pygame.display.set_caption("pyChess")
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load("assets/pieces/black/black_king.png"), (32, 32)))
        

    def run(self):
        run = True

        self.create_squares()
        self.setup_board()

        while run:

            global rules_check

            if rules_check:
                self.big_update_text = colors[self.current_player].capitalize() + "'s Turn"
                if not self.has_steps():
                   rules_check = False
                if not self.check_for_mate():
                    rules_check = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.check_click() and self.chosen:
                            clk_x, clk_y = pygame.mouse.get_pos()
                            if self.chosen.move(self.win, clk_x, clk_y, self.squares[:], self.white_pieces, self.black_pieces):
                                self.chosen = None
                                
                                # if self.current_player == 0:
                                #     self.current_player = 1
                                # else:
                                #     self.current_player = 0
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.check_click()

            self.draw()

    def has_steps(self):

        white_has, black_has = False, False

        for p in (self.white_pieces + self.black_pieces):
            for row_num, row in enumerate(self.squares):
                for square_num in range(len(row)):
                    prev_piece = p.piece_to_kill
                    if p.check_valid_move(self.white_pieces, self.black_pieces, row_num, square_num):
                        prev_row, prev_col = p.current_row, p.current_col

                        p.set_position(row_num, square_num, self.squares[row_num][square_num])
                        if not p.check_for_check(self.white_pieces, self.black_pieces):
                            if p.color == colors[0]:
                                white_has = True
                            else:
                                black_has = True

                        p.piece_to_kill = prev_piece
                        p.set_position(prev_row, prev_col, self.squares[prev_row][prev_col])

        global small_update_text

        if not white_has:
            self.big_update_text = "WHITE LOST"
            small_update_text = ""
        elif not black_has:
            self.big_update_text = "BLACK LOST"
            small_update_text = ""

        return white_has or black_has

        
            
                        
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

        global small_update_text

        if not white_king:
            self.big_update_text = "WHITE LOST"
            small_update_text = ""
        elif not black_king:
            self.big_update_text = "BLACK LOST"
            small_update_text = ""

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
                
                elif (square_num % 2 == 0 and row_num % 2 == 0) or (square_num % 2 != 0 and row_num % 2 != 0):
                    color = (235, 220, 179)
                else:
                    color = (183, 135, 99)
                
                pygame.draw.rect(self.win, color, square)

    def create_squares(self):
        for row in range(8):
            for col in range(8):
                self.squares[row][col] = pygame.Rect(self.width - self.square_width * (8-col), self.height - self.square_height * (8-row), self.square_width, self.square_height)
    
    def draw_text(self):
        global big_text_color

        pygame.draw.rect(self.win, (128,128,128), pygame.Rect(0, 0, self.width, 100))

        if rules_check:
            if self.current_player == 0:
                big_text_color = (255, 255, 255)
            else:
                big_text_color = (0, 0, 0)

        self.win.blit(self.big_font.render(self.big_update_text, True, big_text_color), (self.width / 3.75, 10))

        if len(small_update_text) > len(black_check_message):
            center_text = self.width / 10
        else:
            center_text = self.width / 3.25

        self.win.blit(self.small_font.render(small_update_text, True, small_text_color), (center_text, 50))
        


    def check_click(self):
        clk_x, clk_y = pygame.mouse.get_pos()

        if rules_check:
            if self.chosen:
                if self.chosen.color == colors[0]:
                    pieces = self.white_pieces
                else:
                    pieces = self.black_pieces

                for p in pieces:
                    if p.click(self.win, clk_x, clk_y, p.current_square):
                        self.chosen = p
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