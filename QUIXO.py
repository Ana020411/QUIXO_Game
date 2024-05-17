import copy
import math

class Quixxo:
    "---------------------------------------------  FUNCIONES BASICAS---------------------------------------------------------"
    def __init__(self, symbol):
        self.board = [[0] * 5 for _ in range(5)]
        self.movements = []
        self.symbol = symbol
        self.transposition_table = {}

    def reset(self, symbol):
        self.symbol = symbol
        self.board = [[0] * 5 for _ in range(5)]
        self.movements = []
    
    def print_board(self):
        for row in self.board:
            print(' | '.join(str(cell) for cell in row))
        print('------------------')
    
    "-------------------------------------------------------MOVIMIENTOS---------------------------------------------------------"

    def move_left(self, board, row, col):
        new_board = copy.deepcopy(board)
        if new_board[row][col] == self.symbol or new_board[row][col] == 0:
            while col < 4:
                new_board[row][col] = new_board[row][col + 1]
                col += 1
            new_board[row][4] = self.symbol

        return new_board
    
    def move_right(self, board, row, col):
        new_board = copy.deepcopy(board)
        if new_board[row][col] == self.symbol or new_board[row][col] == 0:
            while col > 0:
                new_board[row][col] = new_board[row][col - 1]
                col -= 1
            new_board[row][0] = self.symbol

        return new_board

    def move_down(self, board, row, col):
        new_board = copy.deepcopy(board)
        if new_board[row][col] == self.symbol or new_board[row][col] == 0:
            while row > 0:
                new_board[row][col] = new_board[row - 1][col]
                row -= 1
            new_board[0][col] = self.symbol

        return new_board
    
    def move_up(self, board, row, col):
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
            movements.extend(["up", "left"])
        elif row == 0 and col == 4:
            movements.extend(["up", "right"])
        elif row == 4 and col == 0:
            movements.extend(["down", "left"])
        elif row == 4 and col == 4:
            movements.extend(["down", "right"])
        elif 1 <= row <= 3 and col == 0:
            movements.extend(["up", "down", "left"])
        elif 1 <= row <= 3 and col == 4:
            movements.extend(["up", "down", "right"])
        elif row == 0 and 1 <= col <= 3:
            movements.extend(["up", "left", "right"])
        elif row == 4 and 1 <= col <= 3:
            movements.extend(["down", "left", "right"])
        elif 1 <= row <= 3 and 1 <= col <= 3:
            return ("Movimiento invalido. Solo se permiten movimientos en la periferia del tablero ")
        return movements

    def apply_move(self, board, row, col, movement):
        new_board = copy.deepcopy(board)

        if movement == "down":
            new_board = self.move_down(new_board, row, col)
        elif movement == "up":
            new_board  = self.move_up(new_board, row, col)
        elif movement == "right":
            new_board = self.move_right(new_board, row, col)
        elif movement == "left":
            new_board = self.move_left(new_board, row, col)

        return new_board
    
    

    def check_win(self, symbol):
        # Filas y columnas
        for i in range(5):
            if all(self.board[i][j] == symbol for j in range(5)) or all(self.board[j][i] == symbol for j in range(5)):
                return True
        # Diagonales
        if all(self.board[i][i] == symbol for i in range(5)) or all(self.board[i][4 - i] == symbol for i in range(5)):
            return True
        
        return False

    "--------------------------------------------------ALGORITMO MINIMAX---------------------------------------------------------------------"
    
    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_win(-1):  # 'X' wins
            return -1
        elif self.check_win(1):  # 'O' wins
            return 1
        elif depth == 2:  # Profundidad máxima
            return Heuristic.heuristic0(self.symbol)

        if is_maximizing:
            best_score = -math.inf
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == 0 or self.board[i][j] == self.symbol:
                        movements = self.get_movements(i, j)
                        for move in movements:
                            new_board = self.apply_move(self.board, i, j, move)
                            new_board[i][j] = 1
                            score = self.minimax(depth + 1, False, alpha, beta)
                            new_board[i][j] = 0  
                            best_score = max(score, best_score)
                            alpha = max(alpha, best_score)
                            if beta <= alpha:
                                break
            return best_score
        else:
            best_score = math.inf
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == 0 or self.board[i][j] == -self.symbol:
                        movements = self.get_movements(i, j)
                        for move in movements:
                            new_board = self.apply_move(self.board, i, j, move)
                            new_board[i][j] = -1
                            score = self.minimax(depth + 1, True, alpha, beta)
                            new_board[i][j] = 0  
                            best_score = min(score, best_score)
                            beta = min(beta, best_score)
                            if beta <= alpha:
                                break
            return best_score
        
    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0 or self.board[i][j] == self.symbol:
                    movements = self.get_movements(i, j)
                    for move in movements:
                        new_board = self.apply_move(self.board, i, j, move)
                        new_board[i][j] = 1
                        score = self.minimax(0, False, alpha, beta)
                        new_board[i][j] = 0  
                        if score > best_score:
                            best_score = score
                            best_move = (i, j, move)
                            alpha = max(alpha, best_score)
        return best_move

    "----------------------------------------------------------------------PARA JUGAR------------------------------------------"
    def play_turn(self, board):
        self.board = board
        self.print_board()
        
        while not self.check_win(-1) and not self.check_win(1):
            # Turno del jugador 1 (X)
            best_move = self.get_best_move()
            if best_move:
                x, y, move = best_move
                if self.board[x][y] == 0 or self.board[x][y] == self.symbol:
                    self.board = self.apply_move(self.board, x, y, move)
                    self.print_board()
                    if self.check_win(self.symbol):
                        print("Jugador X gana!")
                        break
                else:
                    print("Movimiento inválido")
            else:
                print("Empate")
                break

            # Turno del jugador -1 (O)
            self.symbol = -self.symbol  # Cambiar el símbolo para el otro jugador
            best_move = self.get_best_move()
            if best_move:
                x, y, move = best_move
                if self.board[x][y] == 0 or self.board[x][y] == self.symbol:
                    self.board = self.apply_move(self.board, x, y, move)
                    self.print_board()
                    if self.check_win(self.symbol):
                        print("Jugador O gana!")
                        break
                else:
                    print("Movimiento inválido")
            else:
                print("Empate")
                break

            # Cambiar de nuevo el símbolo para el siguiente turno del jugador 1
            self.symbol = -self.symbol
    
    "------------------------------------------------------------------HeuristicaS---------------------------------------------------------------"
class Heuristic:
    @staticmethod
    def heuristic0(node):
       return 0
   
    def check_win(self, board, symbol):
        # Se checan filas y columnas
        for i in range(5):
            if all(board[i][j] == symbol for j in range(5)) or all(board[j][i] == symbol for j in range(5)):
                return True

        # Se checan diagonales
        if all(board[i][i] == symbol for i in range(5)) or all(board[i][4-i] == symbol for i in range(5)):
            return True

        return False
    
    def heuristic1(self, board, symbol):
        heuristic_value = 0

        # Símbolo del jugador y del oponente
        player_symbol = symbol
        opponent_symbol = -symbol

        # Se checa el tablero según la ficha que se coloca o la amenaza del oponente
        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    # se inserta la ficha temporalmente
                    board[i][j] = player_symbol
                    # Checa si el movimiento completa la jugada
                    if self.check_win(board, player_symbol):
                        heuristic_value += 1
                    # Se checa si el movimiento bloquea la victoria del oponente
                    board[i][j] = opponent_symbol
                    if self.check_win(board, opponent_symbol):
                        heuristic_value -= 1

                    heuristic_value += self.check_continuity(board, player_symbol, i, j)

                    # Se regresa el tablero al estado original
                    board[i][j] = 0

        return heuristic_value

    def check_continuity(self, board, symbol, row, col):
        continuity_value = 0
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Checa vertical, horizontal y diagonalmente

        for direction in directions:
            dx, dy = direction
            count = 1  

            # Checa en la dirección positiva
            x, y = row + dx, col + dy
            while 0 <= x < 5 and 0 <= y < 5 and board[x][y] == symbol:
                count += 1
                x += dx
                y += dy

            # Checa en la dirección negativa
            x, y = row - dx, col - dy
            while 0 <= x < 5 and 0 <= y < 5 and board[x][y] == symbol:
                count += 1
                x -= dx
                y -= dy

            # Se actualiza el valor de acuerdo a la cuenta
            if count >= 3:  
                continuity_value += count

        return continuity_value
    
    # Matriz de puntuaciones
    def heuristic2(self, board, symbol):
        score_matrix = [[0]*5 for _ in range(5)]  

        player_symbol = symbol
        opponent_symbol = -symbol

        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    # Se le asigna puntuación más grande a las casillas del medio
                    score_matrix[i][j] += 5 - abs(2 - i) - abs(2 - j)

                    # Se coloca la pieza temporalmente
                    board[i][j] = player_symbol
                    if self.check_win(board, player_symbol):
                        score_matrix[i][j] += 100  # Mayor puntuación para el movimiento ganador

                    # Se coloca pieza del oponente temporalmente
                    board[i][j] = opponent_symbol
                    if self.check_win(board, opponent_symbol):
                        score_matrix[i][j] -= 100  # Menos puntación para bloquear el ganado del oponente

                    board[i][j] = 0

        return sum(map(sum, score_matrix))  # Suma de los scores
    
    # Tablas de transposición
    def heuristic3(self, board, symbol, t_table):
        # Se checa si el resultado se encuentra en la tabla
        board_tuple = tuple(map(tuple, board))
        if board_tuple in t_table:
            return t_table[board_tuple]

        heuristic_value = 0
        player_symbol = symbol
        opponent_symbol = -symbol

        # Solo se evalúa la celda que se modificó y sus vecinos
        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    # se inserta la ficha temporalmente
                    board[i][j] = player_symbol
                    # Checa si el movimiento completa la jugada
                    if self.check_win(board, player_symbol):
                        heuristic_value += 1
                    # Se checa si el movimiento bloquea la victoria del oponente
                    board[i][j] = opponent_symbol
                    if self.check_win(board, opponent_symbol):
                        heuristic_value -= 1

                    heuristic_value += self.check_continuity(board, player_symbol, i, j)

                    # Se regresa el tablero al estado original
                    board[i][j] = 0

        # Se guarda el resultado en la tabla de transposición
        t_table[board_tuple] = heuristic_value

        return heuristic_value
"--------------------------------------------------------IMPLEMENTACION--------------------------------------------"

print(" 0 : Cara neutra / 1: Marca de círculo / -1: Marca de cruz\n")

bot = Quixxo(1)
initial_board = [[0] * 5 for _ in range(5)]  # Tablero inicial
bot.board = bot.play_turn(initial_board)