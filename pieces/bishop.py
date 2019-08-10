import pygame
import os
from .piece import Piece, colors

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.queen = None
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_bishop.png")), (50, 50))

    def check_valid_move(self, whites, blacks, row, col):


        if abs(row - self.current_row) == abs(col - self.current_col):
            
            path = []

            if row - self.current_row > 0:
                # going down
                if col - self.current_col > 0:
                    # going right
                    for r in range(row - self.current_row):
                        path.append((self.current_row + r, self.current_col + r))
                else:
                    # going left
                    for r in range(row - self.current_row):
                        path.append((self.current_row + r, self.current_col - r))
            else:
                # going up
                if col - self.current_col > 0:
                    # going right
                    for r in range(self.current_row - row):
                        path.append((self.current_row - r, self.current_col + r))
                else:
                    # going left
                    for r in range(self.current_row - row):
                        path.append((self.current_row - r, self.current_col - r))

            pieces_in_way = 0

            for path_pos in path:
                path_row, path_col = path_pos

                for p in (whites + blacks):

                    if p is not self and p.current_row == path_row and p.current_col == path_col:
                        pieces_in_way += 1
                    
                    elif p is not self and p.color == self.color and p.current_col == col and p.current_row == row:
                        return False

            if pieces_in_way >= 1:
                return False

            for p in (whites + blacks):
                if p is not self and p.color == self.enemy_color and p.current_col == col and p.current_row == row:
                    self.piece_to_kill = p
                    self.pieces_to_kill = self.get_enemy_pieces(whites, blacks)
                    return True


            return True

        else:
            return False