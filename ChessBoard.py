
class Piece():
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Side():
    WHITE = 1
    BLACK = -1


class ChessBoard:
    def __init__(self):
        self.board = []

        #has_king_move[0] is white, [1] is black
        self.has_king_moved = [False, False]
        #[x][1] refers to queen rook
        self.has_rook_moved = [[False, False], [False, False]]

        #[0] piece [1] = x [2] = y
        self.last_move = [None, None, None]


        for i in range(8):

            file = []

            for i in range(8):

                file.append(None)

            self.board.append(file)

    def make_starting_position(self):


        for i in range (8):
            row = self.board[i]

            row [1] = Piece.PAWN
            row [6] = -Piece.PAWN

        self.board[0][7] = -Piece.ROOK
        self.board[7][7] = -Piece.ROOK
        self.board[7][0] = Piece.ROOK
        self.board[0][0] = Piece.ROOK
        self.board[6][7] = -Piece.KNIGHT
        self.board[1][7] = -Piece.KNIGHT
        self.board[6][0] = Piece.KNIGHT
        self.board[1][0] = Piece.KNIGHT
        self.board[5][7] = -Piece.BISHOP
        self.board[2][7] = -Piece.BISHOP
        self.board[5][0] = Piece.BISHOP
        self.board[2][0] = Piece.BISHOP
        self.board[4][7] = -Piece.KING
        self.board[4][0] = Piece.KING
        self.board[3][7] = -Piece.QUEEN
        self.board[3][0] = Piece.QUEEN


    def print_chessboard(self):

        for j in range(8):

            for i in range (8):
                print(self.board[i][7-j], end=' ')
            print()

    def move_coordinates(self,source,dest):
        # example: source = [2, 5], dest = [4, 5]
        content = self.board[source[0]][source[1]]



        if content == Piece.KING:
            self.has_king_moved[0] = True
        if content == -Piece.KING:
            self.has_king_moved[1] = True
        if content == Piece.ROOK:
            if source[0] == 0 and source[1] == 0:
                self.has_rook_moved[0][1] = True
            else:
                self.has_rook_moved[0][0] = True
        if content == -Piece.ROOK:
            if source[0] == 0 and source[1] == 7:
                self.has_rook_moved[1][1] = True
            else:
                self.has_rook_moved[0][0] = True

        self.board[dest[0]][dest[1]] = content
        self.board[source[0]][source[1]] = None


    def notation_to_coordinates(self, notation):
        rank = "abcdefgh".index(notation[0])
        file = int(notation[1])-1

        return [rank, file]



    def move_algebraic(self, source, dest):
        self.move_coordinates(self.notation_to_coordinates(source),self.notation_to_coordinates(dest))


    def show_moves(self, coordinates):
        legal_moves = []
        x = coordinates[0]
        y = coordinates [1]



        if self.board[x][y] is None:
            return legal_moves
        else:
            square = abs(self.board[x][y])



        if square == Piece.ROOK:
            legal_moves.extend(self.calc_rook_moves(x,y))

        elif square == Piece.BISHOP:
            legal_moves.extend(self.calc_bishop_moves(x,y))

        elif square == Piece.QUEEN:
            legal_moves.extend(self.calc_bishop_moves(x,y))
            legal_moves.extend(self.calc_rook_moves(x, y))

        elif square == Piece.KNIGHT:
            legal_moves.extend(self.calc_knight_moves(x, y))
        elif square == Piece.KING:
            legal_moves.extend(self.calc_king_moves(x, y))
        elif square == Piece.PAWN:
            legal_moves.extend(self.calc_pawn_moves(x, y))
        else:
            pass




        return legal_moves

    def calc_rook_moves (self,x,y):
        legal_moves = self.check_for_blocks(x,y,
                          [(7 - y, (0, 1)),
                          (abs(y), (0, -1)),
                          (7 - x, (1, 0)),
                          (abs(x), (-1, 0))])

        return legal_moves

    def legal_to_kingside_castle(self, side):

        i = 0 if side == 1 else 1
        rank = i*7

        check_squares = [[5,rank],[6,rank],[4,rank]]

        for square in check_squares[:2]:
            if self.board[square[0]][square[1]] is not None:
                return False


        attacked_squares = self.calc_attacked_squares(-side)

        for square in check_squares:
            if square in attacked_squares:

                return False


        return not self.has_rook_moved[i][0] and not self.has_king_moved[i]

    def legal_to_queenside_castle(self, side):

        i = 0 if side == 1 else 1
        rank = i * 7

        check_squares = [[3, rank], [2, rank], [1, rank], [4, rank]]

        for square in check_squares[:3]:
            if self.board[square[0]][square[1]] is not None:
                return False

        attacked_squares = self.calc_attacked_squares(-side)

        for square in check_squares:
            if square in attacked_squares:

                return False


        return not self.has_rook_moved[i][1] and not self.has_king_moved[i]




    def check_for_blocks(self, x, y,specifications):
        source_color = self.find_color(self.board[x][y])
        constraints = []
        legal_moves = []

        # range of the loop, the direction,

        for specification in specifications:
            loop_range, direction = specification

            for i in range(loop_range):


                ix = x + direction[0] * (i+1)
                iy = y + direction[1] * (i+1)

                if self.is_on_board(ix,iy):
                    square = self.board[ix][iy]
                    if square is not None:

                        if self.find_color(square) == source_color:
                            break
                        else:
                            legal_moves.append([ix, iy])
                            break
                    legal_moves.append([ix, iy])

                else:
                    break






        return legal_moves

    def calc_king_moves(self,x,y):
        print("In calc king moves")
        legal_moves = self.check_for_blocks(x,y,
                          [(1, (1, 1)),
                          (1, (-1, -1)),
                          (1, (-1, 1)),
                          (1, (1, -1)),
                          (1, (0, 1)),
                          (1, (0, -1)),
                          (1, (1, 0)),
                          (1, (-1, 0))])
        side = 1 if self.board[x][y] > 0 else -1

        print("SIDE ", side)


        if self.legal_to_kingside_castle(side):
            print("Castle is a legal move")
            #[0] new king pos, [3] new rook pos
            legal_moves.append([x+2, y, 5, y])
        if self.legal_to_queenside_castle(side):
            print("Castle is a legal move")
            #[0] new king pos, [3] new rook pos
            legal_moves.append([x-2, y, 3, y])

        return legal_moves


    def calc_bishop_moves(self,x,y):
        legal_moves = self.check_for_blocks(x,y,
                          [(min(7-x,7-y), (1, 1)),
                          (min(x,y), (-1, -1)),
                          (min(x,7-y), (-1, 1)),
                          (min(7-x,y), (1, -1))])

        return legal_moves


    def calc_knight_moves(self,x,y):
        candidate_moves = [[x + 1, y + 2], [x - 1, y + 2],
                           [x + 2, y + 1], [x + 2, y - 1],
                           [x - 2, y + 1], [x - 2, y - 1],
                           [x + 1, y - 2], [x - 1, y - 2]]
        return self.get_checked_moves(candidate_moves,self.board[x][y])

    def calc_pawn_moves(self,x,y):
        legal_moves = []
        promotion = []
        promotes = [Piece.KNIGHT, Piece.BISHOP, Piece.ROOK, Piece.QUEEN]

        pawn = self.board[x][y]

        starting_rank = 1
        promotion_rank = 6
        direction = 1

        if pawn < 0:
            starting_rank = 6
            promotion_rank = 1
            direction = -1

        #En pessant

        if y == starting_rank + direction * 3:
            print("pawn on rank for possible en pessant")
            print("last move : ", self.last_move)
            if self.last_move [0] == -direction and self.last_move[2] == starting_rank + direction * 3:
                if self.last_move[1] == x + 1 or self.last_move[1] == x - 1:
                    print("en pessant available!")
                    legal_moves.append([self.last_move[1], self.last_move[2] + direction, 0, 0, 0])


        if self.board[x][y+direction] is None:

            legal_moves.append([x,y+direction])
            if y == starting_rank and self.board[x][y+2*direction] is None:
                legal_moves.append([x,y+2*direction])

        if  x < 7 and self.find_color(self.board[x+1][y+direction]):
            legal_moves.append([x + 1, y + direction])
        if x > 0 and self.find_color(self.board[x-1][y+direction]):
            legal_moves.append([x - 1, y + direction])

        if y == promotion_rank:
            for move in legal_moves:

                for piece in promotes:

                    promotion.append(move+[piece*direction])


            return promotion





        return legal_moves




    def get_checked_moves(self,candidate_moves,piece):
        legal_moves = []
        piece_color = self.find_color(piece)
        for candidate_move in candidate_moves:

            x, y = candidate_move

            if self.is_on_board(x, y):

                if self.board[x][y] is not None:
                    is_same_color = piece_color == self.find_color(self.board[x][y])
                else:
                    is_same_color = False

                if not is_same_color:
                    legal_moves.append(candidate_move)



        return legal_moves

    def find_color(self,piece):
        if piece is None:
            piece_color = 0

        else:
            piece_color = 1 if piece > 0 else -1




        return piece_color




    def is_on_board(self,x,y):
        if (-1<x<8 and -1<y<8):
            return True
        else:
            return False

    def find_king(self, color):
        for i in range(8):

            if color*Piece.KING in self.board[i]:

                y = self.board[i].index(color*Piece.KING)
                x = i
        return([x, y])


    def is_in_check(self, side):
        chk = []

        chk = self.calc_attacked_squares(-side)
        x, y = self.find_king(side)



        if [x, y] in chk:
            return True
        else:
            return False

    def find_all_pieces_of_side(self, side):
        locations = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    if side == self.find_color(self.board[i][j]):

                        locations.append([i, j])
        return locations

    def calc_attacked_squares(self, side):
        moves = []
        locations = self.find_all_pieces_of_side(side)

        pawn_rank = 6 if side == 1 else 1
        for location in locations:
            content = self.board[location[0]][location[1]]
            #preventing recursion error with mild jank
            if abs(content) == Piece.KING:
                moves.extend (self.check_for_blocks(location[0], location[1],
                                                    [(1, (1, 1)),
                                                     (1, (-1, -1)),
                                                     (1, (-1, 1)),
                                                     (1, (1, -1)),
                                                     (1, (0, 1)),
                                                     (1, (0, -1)),
                                                     (1, (1, 0)),
                                                     (1, (-1, 0))]))
            else:

                moves.extend(self.show_moves(location))

            if abs(content) == Piece.PAWN and location[1] == pawn_rank:
                moves.extend([[location[0]+1,location[1]+side],[location[0]-1,location[1]+side]])

        moves = [tuple(item[:2]) for item in moves]

        squares = list(set(moves))
        squares = [list(item) for item in squares]

        return squares

    def is_checkmate(self, side):

        locations = self.find_all_pieces_of_side(side)

        for location in locations:
            moves = self.show_moves(location)
            for move in moves:

                if not self.is_result_in_check(location, move, side):
                    return False

        return True


    def is_result_in_check(self, source, dest, moving_side):
        sx, sy = source
        dx, dy = dest
        
        content = self.board[sx][sy]
        destcontent = self.board[dx][dy]

        self.move_coordinates([sx, sy], [dx, dy])
        chk = self.is_in_check(moving_side)


        self.board[sx][sy] = content
        self.board[dx][dy] = destcontent
        return chk

    def is_promote_move(self, legal_move):
        return len(legal_move) == 3

    def is_castle_move(self, legal_move):
        return len(legal_move) == 4
    def is_en_pessant(self, legal_move):
        return len(legal_move) == 5

    def apply_move(self, source, legal_move):

        content = self.board[source[0]][source[1]]

        self.move_coordinates(source, legal_move[:2])



        if self.is_promote_move(legal_move):

            self.board[legal_move[0]][legal_move[1]] = legal_move[2]

        elif self.is_castle_move(legal_move):

            rook_loc = 7 if legal_move[2] == 5 else 0
            source = [rook_loc, legal_move[3]]
            dest = [legal_move[2], legal_move[3]]
            self.move_coordinates(source, dest)

        elif self.is_en_pessant(legal_move):

            self.board[self.last_move[1]][self.last_move[2]] = None

        self.last_move = [content, legal_move[0], legal_move[1]]













