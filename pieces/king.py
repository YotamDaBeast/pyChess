import pygame
import os
from .piece import Piece, colors

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.checking = False
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_king.png")), (30, 30))

    def move(self, win, x, y, squares, whites, blacks):
        for row_num, row in enumerate(squares):
            for sq_num, sq in enumerate(row):
                if self.click(win, x, y, sq):
                    if self.check_valid_king(whites, blacks, row_num, sq_num, squares):
                        if self.pieces_to_kill and self.piece_to_kill:
                            self.kill()
                        self.set_position(row_num, sq_num, sq)

                        self.check_for_check(whites, blacks, row_num, sq_num, win, squares)

                        return True

        return False
    
    def check_valid_king(self, whites, blacks, row, col, squares):
        if col > self.current_col + 1 or col < self.current_col - 1 or row > self.current_row + 1 or row < self.current_row - 1:
            return False

        for p in (whites + blacks):
            if p is not self and p.current_col == col and p.current_row == row:
                if p.color == self.enemy_color:
                    self.piece_to_kill = p
                    self.pieces_to_kill = self.get_enemy_pieces(whites, blacks)

        prev_row, prev_col, prev_sq = self.current_row, self.current_col, self.current_square
        self.set_position(row, col, squares[row][col])

        for p in self.get_enemy_pieces(whites, blacks):
            prev_kill_piece = p.piece_to_kill
            if p != self.piece_to_kill and p.check_valid_move(whites, blacks, row, col):
                print(str(type(p)) + " can kill you")
                print("You can't move to a check position")
                self.set_position(prev_row, prev_col, prev_sq)
                p.piece_to_kill = prev_kill_piece
                return False

        self.set_position(prev_row, prev_col, prev_sq)

        

        return True

    def set_position(self, row, col, sq):
        return super().set_position(row, col, sq)