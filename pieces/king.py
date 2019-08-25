import pygame
import os
from .piece import Piece, colors

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.checking = False
        #self.message_thread = 
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

    def set_position(self, row, col, sq):
        return super().set_position(row, col, sq)