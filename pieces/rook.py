import pygame
import os
from .piece import Piece, colors

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.queen = None
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_rook.png")), (30, 30))

    def check_valid_move(self, whites, blacks, row, col):

        if row == self.current_row or col == self.current_col:
            for p in (whites + blacks):
                if p is not self:
                    if row == self.current_row and p.current_row == row:
                        # moving horizontally
                        if col < self.current_col:
                            if p.current_col > col and p.current_col <= self.current_col:
                                return False
                        elif col > self.current_col:
                            if p.current_col < col and p.current_col >= self.current_col:
                                return False
    
                    elif col == self.current_col and p.current_col == col:
                        # moving vertically
                        if row < self.current_row:
                            if p.current_row > row and p.current_row <= self.current_row:
                                return False
                        elif row > self.current_row:
                            if p.current_row < row and p.current_row >= self.current_row:
                                return False

            for p in (whites + blacks):
                if p is not self and p.color == self.enemy_color:
                    if p.current_col == col and p.current_row == row:
                        print("yes for " + str(type(p)))
                        self.piece_to_kill = p
                        self.pieces_to_kill = self.get_enemy_pieces(whites, blacks)
                        return True
                elif p is not self and p.current_row == row and p.current_col == col:
                    return False


        else:
            return False

        return True