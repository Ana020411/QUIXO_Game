import copy
import math

class Opcion1:
    "---------------------------------------------  FUNCIONES BASICAS---------------------------------------------------------"
    def __init__(self, symbol):
       self.board = [[0] * 5 for _ in range(5)]
       self.symbol = symbol
       self.transposition_table = {}
       self.name = 'prueba1'

    def reset(self, symbol):
       self.symbol = symbol
       self.board = [[0] * 5 for _ in range(5)]
   
    def print_board(self):
       for row in self.board:
           print(' | '.join(f"{cell: ^3}" for cell in row))
       print('---------------------------')
   
    "-------------------------------------------------------MOVIMIENTOS---------------------------------------------------------"

    def move_right(self, board, row, col):
       new_board = copy.deepcopy(board)
       if new_board[row][col] == self.symbol or new_board[row][col] == 0:
           while col < 4:
               new_board[row][col] = new_board[row][col + 1]
               col += 1
           new_board[row][4] = self.symbol

       return new_board
   
    def move_left(self, board, row, col):
       new_board = copy.deepcopy(board)
       if new_board[row][col] == self.symbol or new_board[row][col] == 0:
           while col > 0:
               new_board[row][col] = new_board[row][col - 1]
               col -= 1
           new_board[row][0] = self.symbol
       return new_board

    def move_up(self, board, row, col):
       new_board = copy.deepcopy(board)
       if new_board[row][col] == self.symbol or new_board[row][col] == 0:
           while row > 0:
               new_board[row][col] = new_board[row - 1][col]
               row -= 1
           new_board[0][col] = self.symbol
       return new_board
   
    def move_down(self, board, row, col):
       new_board = copy.deepcopy(board)
       if new_board[row][col] == self.symbol or new_board[row][col] == 0:
           while row < 4:
               new_board[row][col] = new_board[row + 1][col]
               row += 1
           new_board[4][col] = self.symbol
       return new_board
   
    def get_movements(self, row, col):
       movements = []
       if row == 0 and col == 0:
           movements.extend(["down", "right"])
       elif row == 0 and col == 4:
           movements.extend(["down", "left"])
       elif row == 4 and col == 0:
           movements.extend(["up", "right"])
       elif row == 4 and col == 4:
           movements.extend(["up", "left"])
       elif 1 <= row <= 3 and col == 0:
           movements.extend(["up", "down", "right"])
       elif 1 <= row <= 3 and col == 4:
           movements.extend(["up", "down", "left"])
       elif row == 0 and 1 <= col <= 3:
           movements.extend(["down", "left", "right"])
       elif row == 4 and 1 <= col <= 3:
           movements.extend(["up", "left", "right"])
       elif 1 <= row <= 3 and 1 <= col <= 3:
           return "Movimiento invalido. Solo se permiten movimientos en la periferia del tablero"
       return movements

    def apply_move(self, board, row, col, movement):
       new_board = copy.deepcopy(board)
       if movement == "up":
           new_board = self.move_up(new_board, row, col)
       elif movement == "down":
           new_board = self.move_down(new_board, row, col)
       elif movement == "left":
           new_board = self.move_left(new_board, row, col)
       elif movement == "right":
           new_board = self.move_right(new_board, row, col)
       return new_board

    def undo_move(self, board, row, col, movement):
       if movement == "up":
           for i in range(row, 0, -1):
               board[i][col] = board[i - 1][col]
           board[0][col] = 0
       elif movement == "down":
           for i in range(row, 4):
               board[i][col] = board[i + 1][col]
           board[4][col] = 0
       elif movement == "left":
           for j in range(col, 0, -1):
               board[row][j] = board[row][j - 1]
           board[row][0] = 0
       elif movement == "right":
           for j in range(col, 4):
               board[row][j] = board[row][j + 1]
           board[row][4] = 0
       return board

    def check_win(self, board, symbol):
       for i in range(5):
           if all(board[i][j] == symbol for j in range(5)) or all(board[j][i] == symbol for j in range(5)):
               return True
       if all(board[i][i] == symbol for i in range(5)) or all(board[i][4 - i] == symbol for i in range(5)):
           return True
       return False

    "--------------------------------------------------ALGORITMO MINIMAX---------------------------------------------------------------------"
    def minimax(self, board, depth, is_maximizing, alpha, beta):
       state_tuple = tuple(tuple(row) for row in board)
       if state_tuple in self.transposition_table:
           return self.transposition_table[state_tuple]

       if self.check_win(board, -self.symbol):
           return -1
       elif self.check_win(board, self.symbol):
           return 1
       elif depth == 1:  
           return Heuristica.heu(board, self.symbol)

       if is_maximizing:
           best_score = -math.inf
           for i in range(5):
               for j in range(5):
                   if board[i][j] == 0 or board[i][j] == self.symbol:
                       movements = self.get_movements(i, j)
                       if movements != "Movimiento invalido. Solo se permiten movimientos en la periferia del tablero":
                           for move in movements:
                               new_board = self.apply_move(board, i, j, move)
                               if self.check_win(new_board, self.symbol):  # Checa victoria inmediata
                                   self.transposition_table[state_tuple] = 1
                                   return 1
                               score = self.minimax(new_board, depth + 1, False, alpha, beta)
                               new_board = self.undo_move(new_board, i, j, move)
                               best_score = max(score, best_score)
                               alpha = max(alpha, best_score)
                               if beta <= alpha:
                                   break
           self.transposition_table[state_tuple] = best_score
           return best_score
       else:
            best_score = math.inf
            for i in range(5):
               for j in range(5):
                   if board[i][j] == 0 or board[i][j] == -self.symbol:
                       movements = self.get_movements(i, j)
                       if movements != "Movimiento invalido. Solo se permiten movimientos en la periferia del tablero":
                           for move in movements:
                                new_board = self.apply_move(board, i, j, move)
                                if self.check_win(new_board, -self.symbol):  # Checa victoria inmediata
                                    self.transposition_table[state_tuple] = -1
                                    return -1
                                score = self.minimax(new_board, depth + 1, True, alpha, beta)
                                new_board = self.undo_move(new_board, i, j, move)
                                best_score = min(score, best_score)
                                beta = min(beta, best_score)
                                if beta <= alpha:
                                    break
            self.transposition_table[state_tuple] = best_score
            return best_score

        
    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        
        # Itera sobre las casillas en la periferia del tablero
        for i in range(5):
            for j in range(5):
                if i == 0 or i == 5 - 1 or j == 0 or j == 5 - 1:
                    if self.board[i][j] == 0 or self.board[i][j] == self.symbol:
                        movements = self.get_movements(i, j)
                        if movements != "Movimiento invalido. Solo se permiten movimientos en la periferia del tablero":
                            for move in movements:
                                new_board = self.apply_move(self.board, i, j, move)
                                if self.check_win(new_board, self.symbol):  # Checa por la victoria inmediata
                                    return (i, j, move)
                                score = self.minimax(new_board, 0, False, alpha, beta)
                                new_board = self.undo_move(new_board, i, j, move)
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j, move)
                                    alpha = max(alpha, best_score)
                                    if beta <= alpha:
                                        break
        return best_move

    def play_turn(self, board):
        self.board = board
        best_move = self.get_best_move() 
        x, y, move = best_move
        self.board = self.apply_move(self.board, x, y, move)
        self.print_board() 
                 
        return self.board
    
class Heuristica:
    
    @staticmethod
    def count_line(line, symbol):
        symbol_count = 0
        empty_count = 0
        for cell in line:
            if cell == symbol:
                symbol_count += 1
            elif cell == 0:
                empty_count += 1
        return symbol_count, empty_count

    @staticmethod
    def heu(board, symbol):
        score = 0
        
        
        center_positions = {(1, 1), (1, 3), (3, 1), (3, 3)}
        corner_positions = {(0, 0), (0, 4), (4, 0), (4, 4)}
        
    
        for i in range(5):
            row = board[i]
            col = [board[j][i] for j in range(5)]
            diag1 = [board[i][i] for i in range(5)]
            diag2 = [board[i][4-i] for i in range(5)]
            
            row_symbol_count, row_empty_count = Heuristica.count_line(row, symbol)
            col_symbol_count, col_empty_count = Heuristica.count_line(col, symbol)
            diag1_symbol_count, diag1_empty_count = Heuristica.count_line(diag1, symbol)
            diag2_symbol_count, diag2_empty_count = Heuristica.count_line(diag2, symbol)
            
            for symbol_count, empty_count in [(row_symbol_count, row_empty_count), (col_symbol_count, col_empty_count), 
                                              (diag1_symbol_count, diag1_empty_count), (diag2_symbol_count, diag2_empty_count)]:
                if symbol_count == 5:
                    score += 1000
                elif symbol_count == 4 and empty_count == 1:
                    score += 100
                elif symbol_count == 3 and empty_count == 2:
                    score += 10
                elif symbol_count == 2 and empty_count == 3:
                    score += 5
                opponent_count = 4 - symbol_count
                if opponent_count == 4 and empty_count == 1:
                    score -= 100
                elif opponent_count == 3 and empty_count == 2:
                    score -= 10
                elif opponent_count == 2 and empty_count == 3:
                    score -= 5

            for j in range(5):
                if (i, j) in center_positions:
                    if board[i][j] == symbol:
                        score += 10
                    elif board[i][j] == -symbol:
                        score -= 10
                elif (i, j) in corner_positions:
                    if board[i][j] == symbol:
                        score += 5
                    elif board[i][j] == -symbol:
                        score -= 5
                else:
                    if board[i][j] == symbol:
                        score += 1
                    elif board[i][j] == -symbol:
                        score -= 1
        
        return score

