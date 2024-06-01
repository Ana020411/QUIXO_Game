import copy
import math


class Quixxo:
    "---------------------------------------------  FUNCIONES BASICAS---------------------------------------------------------"
    def __init__(self, symbol):
        # Constructor para inicializar el tablero, símbolo y tablas de transposición
       self.board = [[0] * 5 for _ in range(5)]
       self.symbol = symbol
       self.transposition_table = {}
       self.name = 'Botchocolate'

    def reset(self, symbol):
        # Reinicia el tablero y el símbolo del jugador
       self.symbol = symbol
       self.board = [[0] * 5 for _ in range(5)]
   
    def print_board(self):
       for row in self.board:
           print(' | '.join(f"{cell: ^3}" for cell in row))
       print('---------------------------')
   
    "------------------------------------------------------- MOVIMIENTOS---------------------------------------------------------"

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
    "---------------------------------------------------------Operaciones con movimientos----------------------------------------------------------" 
    
    # Almacena la lista de movimientos posibles según la casilla
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
    

    # Aplica el movimiento
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
    
    # Deshace el movimiento
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

    # Función para checar si se completó línea ganadora
    def check_win(self, board, symbol):
       for i in range(5):
           if all(board[i][j] == symbol for j in range(5)) or all(board[j][i] == symbol for j in range(5)):
               return True
       if all(board[i][i] == symbol for i in range(5)) or all(board[i][4 - i] == symbol for i in range(5)):
           return True
       return False

    "--------------------------------------------------ALGORITMO MINIMAX---------------------------------------------------------------------"
    # Implementación del algoritmo Minimax con poda alpha-beta
    
    def minimax(self, board, depth, is_maximizing, alpha, beta):
       # Se usa tabla de transposición para verificar si ya se había accedido al estado o no
       state_tuple = tuple(tuple(row) for row in board)
       if state_tuple in self.transposition_table:
           return self.transposition_table[state_tuple]

       if self.check_win(board, -self.symbol):
           return -1
       elif self.check_win(board, self.symbol):
           return 1
       elif depth == 0:  # Llama a la heurística una vez que ya alcanzó la profundidad
           return Heuristica.heu(board, self.symbol)

       if is_maximizing:
           best_score = -math.inf
           for i in range(5):
               for j in range(5):
                if i == 0 or i == 5 - 1 or j == 0 or j == 5 - 1:   
                   if board[i][j] == 0 or board[i][j] == self.symbol:
                       movements = self.get_movements(i, j)
                       if movements != "Movimiento invalido. Solo se permiten movimientos en la periferia del tablero":
                           for move in movements:
                               new_board = self.apply_move(board, i, j, move) # Se simula movimiento
                               if self.check_win(new_board, self.symbol):  # Checa victoria inmediata
                                   self.transposition_table[state_tuple] = 1
                                   return 1
                               score = self.minimax(new_board, depth + 1, False, alpha, beta)
                               new_board = self.undo_move(new_board, i, j, move) # Se regresa el tablero a estado original
                               best_score = max(score, best_score)
                               # Poda alpha-beta
                               alpha = max(alpha, best_score)
                               if beta <= alpha:
                                   break
           self.transposition_table[state_tuple] = best_score
           return best_score
       else:
            best_score = math.inf
            for i in range(5):
               for j in range(5):
                    if i == 0 or i == 5 - 1 or j == 0 or j == 5 - 1:
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
                                        # Poda alpha-beta
                                        beta = min(beta, best_score)
                                        if beta <= alpha:
                                            break
                    self.transposition_table[state_tuple] = best_score
                    return best_score

    # Encuentra el mejor movimiento utilizando Minimax    
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
                                    # Poda alpha-beta
                                    alpha = max(alpha, best_score)
                                    if beta <= alpha:
                                        break
        return best_move

    def play_turn(self, board):
        # Recibe el estado del tablero y regresa el tablero con una jugada
        
        self.board = board
        best_move = self.get_best_move() 
        x, y, move = best_move
        self.board = self.apply_move(self.board, x, y, move)
        self.print_board() 
                 
        return self.board
  
"----------------------------------------------------CLASE PARA LA HEURISTICA---------------------------------------"  
class Heuristica:
    
    @staticmethod
    # Cuenta las fichas del jugador y las casillas vacías en una línea
    def count_line(line, symbol):
        symbol_cell = 0
        empty_cell = 0
        for cell in line:
            if cell == symbol:
                symbol_cell += 1
            elif cell == 0:
                empty_cell += 1
        return symbol_cell, empty_cell

    @staticmethod
     # Cuenta los movimientos posibles para un jugador en el tablero
    def count_possible_moves(board, symbol):
        possible_moves = 0
        for i in range(5):
            for j in range(5):
                if board[i][j] == symbol or board[i][j] == 0:
                    possible_moves += 1
        return possible_moves

    @staticmethod
    def evaluate_patterns(board, symbol, patterns):
        pattern_score = 0
        for pattern in patterns:
            for i in range(5):
                for j in range(5):
                    matched = True
                    for pi in range(5):
                        for pj in range(5):
                            if (0 <= i + pi < 5) and (0 <= j + pj < 5):
                                if pattern[pi][pj] != 0 and board[i + pi][j + pj] != pattern[pi][pj]:
                                    matched = False
                                    break
                        if not matched:
                            break
                    if matched:
                        pattern_score += 1
        return pattern_score

    @staticmethod
    def heu(board, symbol):
        heuristic_value = 0
        
        center_position = (2, 2)
        adjacent_positions = {(1, 2), (2, 1), (2, 3), (3, 2)}
        center_axis_positions = {(1, 1), (1, 3), (3, 1), (3, 3)}
        corner_positions = {(0, 0), (0, 4), (4, 0), (4, 4)}
        
        patterns = [
            [[symbol, symbol, symbol, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, symbol], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[symbol, symbol, symbol, symbol, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[symbol, 0, 0, 0, 0], [symbol, 0, 0, 0, 0], [symbol, 0, 0, 0, 0], [symbol, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[symbol, 0, 0, 0, 0], [0, symbol, 0, 0, 0], [0, 0, symbol, 0, 0], [0, 0, 0, symbol, 0], [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, symbol], [0, 0, 0, symbol, 0], [0, 0, symbol, 0, 0], [0, symbol, 0, 0, 0], [symbol, 0, 0, 0, 0]],
            [[0, 0, symbol, 0, 0], [0, 0, symbol, 0, 0], [symbol, symbol, symbol, symbol, symbol], [0, 0, symbol, 0, 0], [0, 0, symbol, 0, 0]],
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [symbol, symbol, symbol, symbol, symbol], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[0, 0, symbol, 0, 0], [0, 0, symbol, 0, 0], [0, 0, symbol, symbol, symbol], [0, 0, symbol, 0, 0], [0, 0, symbol, 0, 0]]
        ]
        
        row_scores = [0] * 5
        col_scores = [0] * 5
        diag1_scores = [0] * 5
        diag2_scores = [0] * 5
        
        for i in range(5):
            row = board[i]
            col = [board[j][i] for j in range(5)]
            diag1 = [board[i][i] for i in range(5)]
            diag2 = [board[i][4-i] for i in range(5)]
            
            row_symbol_count, row_empty_count = Heuristica.count_line(row, symbol)
            col_symbol_count, col_empty_count = Heuristica.count_line(col, symbol)
            diag1_symbol_count, diag1_empty_count = Heuristica.count_line(diag1, symbol)
            diag2_symbol_count, diag2_empty_count = Heuristica.count_line(diag2, symbol)
            
            row_scores[i] += row_symbol_count
            col_scores[i] += col_symbol_count
            diag1_scores[i] += diag1_symbol_count
            diag2_scores[i] += diag2_symbol_count

        heuristic_value += Heuristica.evaluate_patterns(board, symbol, patterns)
        
        for score_list in [row_scores, col_scores, diag1_scores, diag2_scores]:
            for score in score_list:
                if score == 5:
                    heuristic_value += 2000
                elif score == 4:
                    heuristic_value += 1000
                elif score == 3:
                    heuristic_value += 10
                elif score == 2:
                    heuristic_value += 5

        

        for i in range(5):
            for j in range(5):
                cell = (i, j)
                if cell == center_position:
                    if board[i][j] == symbol:
                        heuristic_value += 15
                    elif board[i][j] == -symbol:
                        heuristic_value -= 15
                elif cell in adjacent_positions:
                    if board[i][j] == symbol:
                        heuristic_value += 10
                    elif board[i][j] == -symbol:
                        heuristic_value -= 10
                elif cell in center_axis_positions:
                    if board[i][j] == symbol:
                        heuristic_value += 8
                    elif board[i][j] == -symbol:
                        heuristic_value -= 8
                elif cell in corner_positions:
                    if board[i][j] == symbol:
                        heuristic_value += 5
                    elif board[i][j] == -symbol:
                        heuristic_value -= 5
                else:
                    if board[i][j] == symbol:
                        heuristic_value += 1
                    elif board[i][j] == -symbol:
                        heuristic_value -= 1
        
        possible_moves = Heuristica.count_possible_moves(board, symbol)
        heuristic_value += possible_moves * 5

        opponent_possible_moves = Heuristica.count_possible_moves(board, -symbol)
        heuristic_value -= opponent_possible_moves * 5

        return heuristic_value

