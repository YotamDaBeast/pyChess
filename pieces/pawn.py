import pygame
import os
from .piece import Piece, colors

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        
        self.making_promotion = False
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets/pieces/" + self.color, self.color + "_pawn.png")), (50, 50))

    def check_valid_move(self, whites, blacks, row, col):

        for p in (whites + blacks):
            if p is not self:
                if self.current_col == col and p.current_col == self.current_col and row == p.current_row:
                    return False

                if p.color == self.enemy_color and p.current_row == row and p.current_col == col and (p.current_col == self.current_col + 1 or p.current_col == self.current_col - 1):
                    if self.color == colors[0]:
                        # color is white
                        if p.current_row == self.current_row - 1:
                            self.piece_to_kill = p
                            self.pieces_to_kill = blacks
                            return True
                    else:
                        # color is black
                        if p.current_row == self.current_row + 1:
                            self.piece_to_kill = p
                            self.pieces_to_kill = whites
                            return True

        for p in (whites + blacks):
            if col == self.current_col:
                if self.color == colors[0]:
                    if self.current_row == 6:
                        if self.current_row - row == 2:
                            if p.current_row == self.current_row - 1 and p.current_col == col:
                                return False
                            return True
                    if self.current_row - row == 1:
                        return True
                    else:
                        return False

                else:
                    if self.current_row == 1:
                        if row - self.current_row == 2:
                            if p.current_row == self.current_row + 1 and p.current_col == col:
                                return False
                            return True
                    if row - self.current_row == 1:
                        return True
                    else:
                        return False
            else:
                return False
            

        return True

    def set_position(self, row, col, sq):
        super().set_position(row, col, sq)
        if self.color == colors[0] and row == 0:
            # color is white
            self.making_promotion = True
            self.create_promotion_screen()
        elif self.color == colors[1] and row == 7:
            # color is black
            self.making_promotion = True
            self.create_promotion_screen()
        

    def draw(self, win):
        super().draw(win)

    def click_promotion(self, x, y, whites, blacks):
        from game import Game

        if self.making_promotion:
            for rect_num, rect in enumerate(self.rects):
                if x <= rect.right and x >= rect.left and y >= rect.top and y <= rect.bottom:
                    self.possible_selections[rect_num].set_position(self.current_row, self.current_col, self.current_square)
                    self.making_promotion = False
                    Game.rules_check = True
                    
                    if self.color == colors[0]:
                        # color is white
                        whites.append(self.possible_selections[rect_num])
                        whites.remove(self)
                    else:
                        # color is black
                        blacks.append(self.possible_selections[rect_num])
                        blacks.remove(self)
                    
                    return

    def create_promotion_screen(self):
        from .queen import Queen
        from .rook import Rook
        from .bishop import Bishop
        from .knight import Knight

        self.wide_rect = pygame.Rect(75, 225, 270, 160)

        self.current_color_index = colors.index(self.color)

        self.possible_selections = [Queen(self.current_color_index), Rook(self.current_color_index), Bishop(self.current_color_index), Knight(self.current_color_index)]
        self.rects = []

        for rect_num in range(len(self.possible_selections)):
            self.rects.append(pygame.Rect(self.wide_rect.left + (50*rect_num) + 10*(rect_num+1) + 10, self.wide_rect.top + self.wide_rect.height*0.5, 50, 50))

        self.font = pygame.font.SysFont('Comic Sans MS', 25, bold = True)


    def draw_promotion(self, win):
        if self.making_promotion:
            from game import Game
            Game.rules_check = False

            pygame.draw.rect(win, (255, 0, 0), self.wide_rect)

            for r_num, r in enumerate(self.rects):
                pygame.draw.rect(win, (255, 255, 255), r)
                win.blit(self.possible_selections[r_num].img, (r.left, r.top))

            win.blit(self.font.render("Choose a promotion", True, (255, 255, 255)), (self.wide_rect.left + 20, self.wide_rect.top + 15))


