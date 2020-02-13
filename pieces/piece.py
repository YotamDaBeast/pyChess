import pygame
import time
import game
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
        self.current_square = None

        if self.color == colors[0]:
            self.enemy_color = colors[1]
        else:
            self.enemy_color = colors[0]

    def draw(self, win):
        win.blit(self.img, (self.current_square.left, self.current_square.top))

    def click(self, win, x, y, square):
        return x <= square.right and x >= square.left and y >= square.top and y <= square.bottom

    def move(self, win, x, y, squares, whites, blacks):
        from pieces.pawn import Pawn
        from pieces.rook import Rook
        from pieces.king import King
        import game

        white_lost, black_lost = self.check_for_mate(whites, blacks)
        white_has, black_has = self.has_steps(whites, blacks, squares)
        if not white_has or not white_lost:
            self.set_big_message("WHITE LOST")
            game.small_update_text = ""
        elif not black_has or not black_lost:
            self.set_big_message("BLACK LOST")
            game.small_update_text = ""

        if not white_has or not black_has or not white_lost or not black_lost:
            return (False, True)
            

        for row_num, row in enumerate(squares):
            for sq_num, sq in enumerate(row):
                if self.click(win, x, y, sq):
                    prev_row, prev_col, prev_sq = self.current_row, self.current_col, self.current_square

                    self.handle_check_messages(whites, blacks)

                    can_castle = self.check_castling(whites, blacks, row_num, sq_num)

                    if self.check_valid_move(whites, blacks, row_num, sq_num) or can_castle:
                        self.set_position(row_num, sq_num, sq)
                        if self.check_for_check(whites, blacks):
                            threading.Thread(target=self.set_temp_message, args=("You can't move to a check position",)).start()
                            self.set_position(prev_row, prev_col, prev_sq)
                            return (False, False)
                        
                        self.set_position(prev_row, prev_col, prev_sq)

                        if self.pieces_to_kill and self.piece_to_kill:
                            self.kill()
                        self.set_position(row_num, sq_num, sq)
                        self.handle_check_messages(whites, blacks)

                        if can_castle:
                            for p in (whites + blacks):
                                if type(p) is Rook and p.color == self.color:
                                    if sq_num == 6 and p.current_col == 7:
                                        prev_row, prev_col, prev_sq = p.current_row, p.current_col, p.current_square
                                        p.set_position(p.current_row, sq_num - 1, squares[p.current_row][sq_num - 1])
                                        if self.check_for_check(whites, blacks):
                                            threading.Thread(target=self.set_temp_message, args=("You can't move to a check position",)).start()
                                            p.set_position(prev_row, prev_col, prev_sq)
                                            return (False, False)
                                        break
                                    elif sq_num == 2 and p.current_col == 0:
                                        prev_row, prev_col, prev_sq = p.current_row, p.current_col, p.current_square
                                        p.set_position(p.current_row, sq_num + 1, squares[p.current_row][sq_num + 1])
                                        if self.check_for_check(whites, blacks):
                                            threading.Thread(target=self.set_temp_message, args=("You can't move to a check position",)).start()
                                            p.set_position(prev_row, prev_col, prev_sq)
                                            return (False, False)
                                        break

                        if type(self) is Pawn:
                            if self.color == colors[0] and row_num == 0:
                                # color is white
                                game.rules_check = False
                                self.making_promotion = True
                                self.create_promotion_screen()
                            elif self.color == colors[1] and row_num == 7:
                                # color is black
                                game.rules_check = False
                                self.making_promotion = True
                                self.create_promotion_screen()

                        elif type(self) is Rook or type(self) is King:
                            self.has_moved = True
                        return (True, False)

        return (False, False)

    def check_castling(self, whites, blacks, row, col):
        # defined only in King class
        return False

    def create_promotion_screen(self):
        # defined only in Pawn class
        pass

    def check_for_mate(self, whites, blacks):
        from pieces.king import King
        white_king, black_king = False, False

        for white in whites:
            if type(white) is King:
                white_king = True
                break
        
        for black in blacks:
            if type(black) is King:
                black_king = True
                break


        return (white_king, black_king)

    def handle_check_messages(self, whites, blacks):

        for p in (whites + blacks):
            if p.check_for_check(whites, blacks):
                if p.color == colors[0]:
                    game.small_update_text = white_check_message
                else:
                    game.small_update_text = black_check_message
                return

        game.small_update_text = ""

    def cancel_message(self):
        if self.color == colors[1] and game.small_update_text == white_check_message:
            game.small_update_text = ""
        elif self.color == colors[0] and game.small_update_text == black_check_message:
            game.small_update_text = ""
        
    def check_for_check(self, whites, blacks):
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
                if p is not self.piece_to_kill and p.check_valid_move(whites, blacks, king.current_row, king.current_col):
                    p.piece_to_kill = prev_piece
                    return True

        return False

    def check_valid_move(self, whites, blacks, row, col):
        pass

    def kill(self):
        self.pieces_to_kill.remove(self.piece_to_kill)
        self.pieces_to_kill = None
        self.piece_to_kill = None

    def set_position(self, row, col, sq):
        self.current_square = sq
        self.current_row = row
        self.current_col = col

    def has_steps(self, whites, blacks, squares):

        white_has, black_has = False, False

        for p in (whites + blacks):
            for row_num, row in enumerate(squares):
                for square_num in range(len(row)):
                    prev_piece = p.piece_to_kill
                    if p.check_valid_move(whites, blacks, row_num, square_num):
                        prev_row, prev_col = p.current_row, p.current_col

                        p.set_position(row_num, square_num, squares[row_num][square_num])
                        if not p.check_for_check(whites, blacks):
                            if p.color == colors[0]:
                                white_has = True
                            else:
                                black_has = True

                        p.piece_to_kill = prev_piece
                        p.set_position(prev_row, prev_col, squares[prev_row][prev_col])


        return (white_has, black_has)

    def set_temp_message(self, message):

        prev_message = game.small_update_text

        game.small_update_text = message
        time.sleep(2)
        game.small_update_text = prev_message

    def set_big_message(self, message):
        game.big_update_text = message

    def get_enemy_pieces(self, whites, blacks):
        if self.enemy_color == colors[0]:
            return whites
        else:
            return blacks
