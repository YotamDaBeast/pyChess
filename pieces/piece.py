import pygame

colors = ["white", "black"]

black_check_message = "Black is in check!"
white_check_message = "White is in check"

class Piece:
    def __init__(self, color):
        self.color = colors[color]
        self.img = None
        self.pieces_to_kill = None
        self.piece_to_kill = None
        self.square_size = 50
        self.enemy_king = None

        if self.color == colors[0]:
            self.enemy_color = colors[1]
        else:
            self.enemy_color = colors[0]

    def draw(self, win):
        win.blit(self.img, (self.current_square.left+10, self.current_square.top + 10))

    def click(self, win, x, y, square):
        return x <= square.right and x >= square.left and y >= square.top and y <= square.bottom

    def move(self, win, x, y, squares, whites, blacks):
        for row_num, row in enumerate(squares):
            for sq_num, sq in enumerate(row):
                if self.click(win, x, y, sq):
                    if self.check_valid_move(whites, blacks, row_num, sq_num):
                        if self.pieces_to_kill and self.piece_to_kill:
                            self.kill()
                        self.set_position(row_num, sq_num, sq)

                        if not self.check_for_check(whites, blacks, row_num, sq_num, win, squares):
                            self.cancel_message()

                        return True

        return False


    def cancel_message(self):
        from game import Game
        if self.color == colors[1] and Game.small_update_text == white_check_message:
            Game.small_update_text = ""
        elif self.color == colors[0] and Game.small_update_text == black_check_message:
            Game.small_update_text = ""
        
    def check_for_check(self, whites, blacks, row, col, win, squares):
        from .king import King
        from .pawn import Pawn

        for p in (whites + blacks):
            if p.color == self.enemy_color and type(p) is King:
                self.enemy_king = p

        if self.color == colors[0]:
            team_pieces = whites
        else:
            team_pieces = blacks

        if self.enemy_king:

            for p in team_pieces:
                prev_piece = p.piece_to_kill
                if type(p) is King:
                    if p.check_valid_king(whites, blacks, self.enemy_king.current_row, self.enemy_king.current_col, squares):
                        self.set_check_message()
                        p.piece_to_kill = prev_piece
                        return True
                else:
                    if p.check_valid_move(whites, blacks, self.enemy_king.current_row, self.enemy_king.current_col):
                        self.set_check_message()
                        p.piece_to_kill = prev_piece
                        return True

        return False

    def check_valid_move(self, whites, blacks, row, col):
        pass

    def set_check_message(self):
        from game import Game

        if self.enemy_color == colors[0]:
            Game.small_update_text = white_check_message
            Game.small_text_color = (255, 255, 255)
        elif self.enemy_color == colors[1]:
            Game.small_update_text = black_check_message
            Game.small_text_color = (0, 0, 0)

    def kill(self):
        self.pieces_to_kill.remove(self.piece_to_kill)
        self.pieces_to_kill = None
        self.piece_to_kill = None

    def set_position(self, row, col, sq):
        self.current_square = sq
        self.current_row = row
        self.current_col = col

    def get_enemy_pieces(self, whites, blacks):
        if self.enemy_color == colors[0]:
            return whites
        else:
            return blacks
