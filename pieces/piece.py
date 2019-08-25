import pygame
import time
import threading

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
        win.blit(self.img, (self.current_square.left, self.current_square.top))

    def click(self, win, x, y, square):
        return x <= square.right and x >= square.left and y >= square.top and y <= square.bottom

    def move(self, win, x, y, squares, whites, blacks):
        for row_num, row in enumerate(squares):
            for sq_num, sq in enumerate(row):
                if self.click(win, x, y, sq):
                    prev_row, prev_col, prev_sq = self.current_row, self.current_col, self.current_square
                    self.set_position(row_num, sq_num, sq)

                    print(str(self.check_for_check(whites, blacks, row_num, sq_num, win, squares)))
                    
                    if self.check_for_check(whites, blacks, row_num, sq_num, win, squares):
                        threading.Thread(target=self.set_temp_message, args=("You can't move to a check position",)).start()
                        self.set_position(prev_row, prev_col, prev_sq)
                        return False

                    self.set_position(prev_row, prev_col, prev_sq)

                    if self.check_valid_move(whites, blacks, row_num, sq_num):
                        if self.pieces_to_kill and self.piece_to_kill:
                            self.kill()
                        self.set_position(row_num, sq_num, sq)

                        if self.check_for_check(whites, blacks, row_num, sq_num, win, squares):
                            self.set_check_message()
                        else:
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

        if self.color == colors[0]:
            team_pieces = whites
        else:
            team_pieces = blacks

        for p in team_pieces:
            if type(p) is King:
                king = p

        if king:

            for p in self.get_enemy_pieces(whites, blacks):
                prev_piece = p.piece_to_kill
                if p.check_valid_move(whites, blacks, king.current_row, king.current_col):
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

    def set_temp_message(self, message):
        from game import Game

        prev_message = Game.small_update_text

        Game.small_update_text = message
        time.sleep(2)
        Game.small_update_text = prev_message

    def get_enemy_pieces(self, whites, blacks):
        if self.enemy_color == colors[0]:
            return whites
        else:
            return blacks
