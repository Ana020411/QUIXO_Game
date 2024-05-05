import random
import copy

class QuixoReferee:
    def __init__(self):
        self.board = [[0]* 5 for _ in range(5)]

    def check_win(self, symbol):
        pass

# Tomar en cuenta que la ficha no se puede poner en el mismo lugar de donde se sacó
# Si para completar la alineación de 5 también se alineó 5 del oponente, pierdes
class QuixoBot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.board = [[0]* 5 for _ in range(5)]

    def play_turn(self, board):
        # Aquí se utilizaría el algoritmo de búsqueda para resolverlo
        # Debe regresar un tablero con tu movimiento del bot
        pass

    def __move_right(self, board, row, col):
        if board[row][col] == self.symbol:
            while col < 4:
                board[row][col] = board[row][col + 1]
                col += 1
            board[row][col] = self.symbol
            self.board = copy.deepcopy(board)

    def __move_left(self, board, row, col):
        if board[row][col] == self.symbol:
            while col > 0:
                board[row][col] = board[row][col - 1]
                col -= 1
            board[row][col] = self.symbol
            self.board = copy.deepcopy(board)

    def __move_up(self, board, row, col):
        if board[row][col] == self.symbol:
            while row > 0:
                board[row][col] = board[row - 1][col]
                row -= 1
            board[row][col] = self.symbol
            self.board = copy.deepcopy(board)

    def __move_down(self, board, row, col):
        if board[row][col] == self.symbol:
            while row < 4:
                board[row][col] = board[row + 1][col]
                row += 1
            board[row][col] = self.symbol
            self.board = copy.deepcopy(board)

    def print_board(self):
        for row in self.board:
            print('|'.join(str(cell) for cell in row))
            print('-----')


    def reset(self):
        pass


quixo = QuixoBot(1)
quixo.print_board()