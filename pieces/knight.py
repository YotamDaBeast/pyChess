import pygame
import os
from .piece import Piece, colors

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_knight.png")), (30, 30))

    def check_valid_move(self, whites, blacks, row, col):
        valid_moves = [(self.current_row + 2, self.current_col + 1), (self.current_row + 2, self.current_col - 1), (self.current_row + 1, self.current_col + 2)
        , (self.current_row + 1, self.current_col - 2), (self.current_row - 2, self.current_col + 1), (self.current_row - 2, self.current_col - 1)
        , (self.current_row - 1, self.current_col + 2), (self.current_row - 1, self.current_col - 2)]

        if ((row, col)) not in valid_moves:
            return False
        
        for p in (whites + blacks):
            if p is not self and p.current_col == col and p.current_row == row:
                if p.color != self.enemy_color:
                    return False
                
                self.piece_to_kill = p

                self.pieces_to_kill = self.get_enemy_pieces(whites, blacks)

        return True