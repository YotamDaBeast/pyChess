import pygame
import os
from .piece import Piece, colors
from .bishop import Bishop
from .rook import Rook

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_queen.png")), (50, 50))

    def check_valid_move(self, whites, blacks, row, col):
        if Bishop.check_valid_move(self, whites, blacks, row, col) or Rook.check_valid_move(self, whites, blacks, row, col):
            return True
        return False

    def set_position(self, row, col, sq):
        super().set_position(row, col, sq)

