import pygame
import random
from ChessBoard import*






class ChessGUI:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    ONE_EIGHTH = SCREEN_HEIGHT//8


    def __init__(self):
        self.size = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.cb = ChessBoard()
        self.white_to_move = True
        self.destx = 0
        self.desty = 0
        self.x = 0
        self.y = 0
        self.last_move = None

        self.is_square_selected = None
        self.promote_to = Piece.QUEEN


    def find_position(self,event):
        square = event.pos

        x = square[0] // self.ONE_EIGHTH
        y = 7 - square[1] // self.ONE_EIGHTH

        return [x, y]


    def blit_square(self, type):
        if type == 1:

            self.screen.blit(self.highlight, (self.x*self.ONE_EIGHTH,
                            self.SCREEN_HEIGHT-self.ONE_EIGHTH-self.y*self.ONE_EIGHTH),
                         (0, 0, self.ONE_EIGHTH, self.ONE_EIGHTH))
        elif type == 2:



            if self.white_to_move:
                i, j = self.cb.find_king(1)
                color = 1

            else:
                i, j = self.cb.find_king(-1)
                color = -1
            self.screen.blit(self.red_check, (i * self.ONE_EIGHTH,
                                              self.SCREEN_HEIGHT - self.ONE_EIGHTH - j* self.ONE_EIGHTH),
                             (0, 0, self.ONE_EIGHTH, self.ONE_EIGHTH))

            self.blit_piece(color*6, i, j)

        elif type == 3:
            self.screen.blit(self.orange, (self.last_move[1][0] * self.ONE_EIGHTH,
                                            self.SCREEN_HEIGHT - self.ONE_EIGHTH -
                                        self.last_move[1][1]* self.ONE_EIGHTH),
                                        (50, 50, self.ONE_EIGHTH, self.ONE_EIGHTH))
            self.screen.blit(self.highlight, (self.last_move[0][0] * self.ONE_EIGHTH,
                                              self.SCREEN_HEIGHT - self.ONE_EIGHTH - self.last_move[0][1] * self.ONE_EIGHTH),
                             (0, 0, self.ONE_EIGHTH, self.ONE_EIGHTH))




    def blit_piece(self, piece, i, j):
        if piece == Piece.PAWN:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 12,
                             self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (420, 0, 80, 80))
        elif piece == -Piece.PAWN:

            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 12,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (420, 84, 80, 80))

        elif piece == Piece.KNIGHT:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 17,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (260, 0, 80, 80))

        elif piece == -Piece.KNIGHT:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 17,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (260, 84, 80, 80))

        elif piece == -Piece.QUEEN:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 14,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (90, 84, 80, 80))
        elif piece == Piece.QUEEN:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 14,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (90, 0, 80, 80))
        elif piece == -Piece.KING:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 7,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (0, 84, 80, 80))
        elif piece == Piece.KING:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 7,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (0, 0, 80, 80))
        elif piece == -Piece.BISHOP:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 12,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (170, 84, 80, 80))
        elif piece == Piece.BISHOP:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 12,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (170, 0, 80, 80))
        elif piece == -Piece.ROOK:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 15,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (340, 84, 80, 80))
        elif piece == Piece.ROOK:
            self.screen.blit(self.pieces, (i * self.ONE_EIGHTH + 15,
                                           self.SCREEN_HEIGHT - j * self.ONE_EIGHTH - 93),
                             (340, 0, 80, 80))


    def draw_board(self):
        self.screen.blit(self.board, (0, 0))

        if self.cb.is_in_check(self.get_side_to_move()):
            self.blit_square(2)

        if self.last_move is not None:
            self.blit_square(3)

        if self.is_square_selected and self.is_square_selected is not None:
            self.blit_square(1)

        for i in range(8):
            for j in range(8):
                draw = self.cb.board[i][j]

                if draw == Piece.PAWN:
                    self.blit_piece(1, i, j)
                elif draw == -Piece.PAWN:
                    self.blit_piece(-1, i, j)
                elif draw == Piece.KNIGHT:
                    self.blit_piece(2, i, j)
                elif draw == -Piece.KNIGHT:
                    self.blit_piece(-2, i, j)
                elif draw == -Piece.QUEEN:
                    self.blit_piece(-5, i, j)
                elif draw == Piece.QUEEN:
                    self.blit_piece(5, i, j)
                elif draw == -Piece.KING:
                    self.blit_piece(-6, i, j)
                elif draw == Piece.KING:
                    self.blit_piece(6, i, j)
                elif draw == -Piece.BISHOP:
                    self.blit_piece(-3, i, j)
                elif draw == Piece.BISHOP:
                    self.blit_piece(3, i, j)
                elif draw == -Piece.ROOK:
                    self.blit_piece(-4, i, j)
                elif draw == Piece.ROOK:
                    self.blit_piece(4, i, j)

    def select_square(self):
        if self.white_to_move and self.cb.board[self.x][self.y] > 0:
            self.is_square_selected = True
            self.draw_board()
        elif not self.white_to_move and self.cb.board[self.x][self.y] < 0:
            self.is_square_selected = True
            self.draw_board()
    def is_same_color(self):

        if self.white_to_move and self.cb.board[self.destx][self.desty] > 0:
            return True
        elif not self.white_to_move and self.cb.board[self.destx][self.desty] < 0:
            return True
        else:
            return False
    def search_dest_in_moves(self, legal_moves, dest):
        matches = []
        for move in legal_moves:
            if dest == move[:2]:
                matches.append(move)
        return matches
    def get_side_to_move(self):
        return 1 if self.white_to_move else -1

    def promotion_loop(self):

        while True:


            if self.white_to_move:

                self.screen.blit(self.promote_pieces, (226, 358), (0, 0, 348, 83))
                color = 1
            else:
                self.screen.blit(self.promote_pieces, (226, 358), (0, 83, 348, 83))
                color = -1


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if 226 < x < 313 and 358 < y < 441:

                        return color*Piece.QUEEN

                    if 313 < x < 400 and 358 < y < 441:

                        return color*Piece.BISHOP

                    if 400 < x < 487 and 358 < y < 441:

                        return color*Piece.KNIGHT

                    if 487 < x < 574 and 358 < y < 441:

                        return color*Piece.ROOK



            self.clock.tick(60)
            pygame.display.flip()







    def main_loop(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:

                if not self.is_square_selected:

                    self.x, self.y = self.find_position(event)
                    if self.cb.board[self.x][self.y] is not None:
                        self.select_square()

                else:

                    self.destx, self.desty = self.find_position(event)
                    destination = [self.destx, self.desty]
                    legal_moves = self.cb.show_moves([self.x, self.y])
                    matched_moves = self.search_dest_in_moves(legal_moves, destination)


                    if len(matched_moves) > 0 and not self.cb.is_result_in_check(
                            [self.x, self.y], destination, self.get_side_to_move()):
                        self.last_move = [[self.x, self.y], [self.destx, self.desty]]



                        if len(matched_moves)> 1:
                            self.promote_to = self.promotion_loop()

                            target_move = destination + [self.promote_to]

                        else:
                            target_move = matched_moves[0]


                        self.cb.apply_move([self.x, self.y], target_move)


                        self.draw_board()

                        self.is_square_selected = False

                        self.white_to_move = not self.white_to_move
                        if self.cb.is_in_check(self.get_side_to_move()):
                            if self.cb.is_checkmate(self.get_side_to_move()):
                                self.screen.blit(self.checkmate, (125, 200))
                                print("GGWP")

                            self.blit_square(2)



                    elif self.cb.board[self.destx][self.desty] is None:
                        self.is_square_selected = False

                        self.draw_board()
                    elif self.is_same_color():
                        self.is_square_selected = True
                        self.x = self.destx
                        self.y = self.desty
                        self.draw_board()
                    else:

                        self.is_square_selected = False

                        self.draw_board()




#input x and y output screen x and screen y
    def main(self):

        pygame.init()

        self.board = pygame.image.load("images\800x800.jpg")
        self.pieces = pygame.image.load("images\Pieces.png")
        self.highlight = pygame.image.load("images\YELLOW.jpg")
        self.red_check = pygame.image.load("images\RED.png")
        self.orange = pygame.image.load("images\ORANGE.png")
        self.checkmate = pygame.image.load("images\CHECKMATE.png")
        self.promote_pieces = pygame.image.load("images\PromotePieces.png")

        self.screen = pygame.display.set_mode(self.size)

        self.cb.make_starting_position()



        #self.cb.make_starting_position()
        self.draw_board()
        self.is_square_selected = False

        pygame.display.set_caption("Pie Chess")

        self.clock = pygame.time.Clock()




        while True:
            self.main_loop()



            self.clock.tick(60)
            pygame.display.flip()



cg = ChessGUI()
cg.main()