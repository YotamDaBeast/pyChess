import pygame
import os
from .piece import Piece, colors

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.has_moved = False

        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_king.png")), (50, 50))
    
    def check_valid_move(self, whites, blacks, row, col):

        if col > self.current_col + 1 or col < self.current_col - 1 or row > self.current_row + 1 or row < self.current_row - 1:
            return False

        for p in (whites + blacks):
            if p is not self and p.current_col == col and p.current_row == row:
                if p.color == self.enemy_color:
                    self.piece_to_kill = p
                    self.pieces_to_kill = self.get_enemy_pieces(whites, blacks)
                else:
                    return False
        

        return True

    def check_castling(self, whites, blacks, row, col):
        from pieces.rook import Rook

        if (col == self.current_col - 2 or col == self.current_col + 2) and row == self.current_row:

            if self.color == colors[0]:
                # color is white
                group_pieces = whites
            else:
                # color is black
                group_pieces = blacks

            if not self.has_moved:
                # check if rook has moved
                for p in group_pieces:
                    if type(p) is Rook:
                        if col == 2 and p.current_col == 0:
                            group_rook = p
                        elif col == 6 and p.current_col == 7:
                            group_rook = p


                if group_rook and not group_rook.has_moved:
                    for p in (whites + blacks):
                        if p is not self and p is not group_rook:
                            if col == 2:
                                if p.current_row == row and p.current_col > group_rook.current_col and p.current_col < self.current_col:
                                    return False
                            elif col == 7:
                                if p.current_row == row and p.current_col < group_rook.current_col and p.current_col > self.current_col:
                                    return False

                    return True

                            

        return False