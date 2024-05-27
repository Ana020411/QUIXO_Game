
import copy
import math

class Quixxo:
    "---------------------------------------------  FUNCIONES BASICAS---------------------------------------------------------"
    def __init__(self, symbol):
        self.board = [[0] * 5 for _ in range(5)]
        self.symbol = symbol
        self.transposition_table = {}

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
            return ("Movimiento invalido. Solo se permiten movimientos en la periferia del tablero")
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
        elif depth == 3:  
            return Heuristic.heuristic4(board, self.symbol)

        if is_maximizing:
            best_score = -math.inf
            for i in range(5):
                for j in range(5):#CHECAR LOS FORS*****************************
                    if board[i][j] == 0 or board[i][j] == self.symbol:
                        movements = self.get_movements(i, j)
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
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0 or self.board[i][j] == self.symbol:
                    movements = self.get_movements(i, j)
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
        player_turn = False
        fin= False

        while not fin:
            if self.symbol == 1:  # Turno del bot
                print("********************Turno del bot*************************")
                best_move = self.get_best_move()
                if best_move is None:
                    print("empate!")
                    fin = True
                    break
                else:
                    x, y, move = best_move
                    self.board = self.apply_move(self.board, x, y, move)
                    self.print_board()
                    if self.check_win(self.board, 1):
                        print(f"Jugador 1 gana!")
                        fin = True
                        
            else:  # Turno del jugador
                print("=================Turno del jugador===================")
                x, y = input("Introduce fila, columna (fila columna): ").split()
                x, y = int(x), int(y)
                movements = self.get_movements(x, y)
                if movements:
                    movement = input(f"Movimientos válidos: {', '.join(movements)}. Ingresa tu movimiento: ")
                    if movement in movements:
                        self.board = self.apply_move(self.board, x, y, movement)
                        self.print_board()
                        if self.check_win(self.board, -1):
                            print(f"¡Jugador -1 gana!")
                            fin = True
                    else:
                        print("Movimiento inválido. Intenta de nuevo.")
                        continue

    
            # Cambia de turno
            self.symbol = -self.symbol

        return self.board

class Heuristic:
    heuristic_cache = {}

    @staticmethod
    def calculate_game_phase(board):
        total_moves = sum(board[i].count(0) for i in range(5))
        if total_moves < 12:
            return "initial"
        else:
            return "advanced"

    @staticmethod
    def calculate_board_key(board):
        return hash(str(board))

    @staticmethod
    def heuristic4(board, symbol):
        heuristic_value = 0

        phase = Heuristic.calculate_game_phase(board)

        if phase == "initial":
            position_values = [
                [3, 4, 5, 4, 3],
                [4, 6, 8, 6, 4],
                [5, 8, 10, 8, 5],
                [4, 6, 8, 6, 4],
                [3, 4, 5, 4, 3]
            ]
        else:
            position_values = [
                [5, 4, 3, 4, 5],
                [4, 6, 8, 6, 4],
                [3, 8, 10, 8, 3],
                [4, 6, 8, 6, 4],
                [5, 4, 3, 4, 5]
            ]

        if Heuristic.check_immediate_win(board, symbol):
            return float('inf') 
        for i in range(5):
            player_row_count = sum(1 for j in range(5) if board[i][j] == symbol)
            opponent_row_count = sum(1 for j in range(5) if board[i][j] == -symbol)
            player_col_count = sum(1 for j in range(5) if board[j][i] == symbol)
            opponent_col_count = sum(1 for j in range(5) if board[j][i] == -symbol)
            
            heuristic_value += player_row_count ** 2
            heuristic_value -= opponent_row_count ** 2
            heuristic_value += player_col_count ** 2
            heuristic_value -= opponent_col_count ** 2
            
            if player_row_count == 4 and 0 in board[i]:
                heuristic_value += 2000
            elif player_col_count == 4 and 0 in [board[j][i] for j in range(5)]:
                heuristic_value += 2000

        player_diag1_count = sum(1 for i in range(5) if board[i][i] == symbol)
        opponent_diag1_count = sum(1 for i in range(5) if board[i][i] == -symbol)
        player_diag2_count = sum(1 for i in range(5) if board[i][4 - i] == symbol)
        opponent_diag2_count = sum(1 for i in range(5) if board[i][4 - i] == -symbol)

        heuristic_value += player_diag1_count ** 2
        heuristic_value -= opponent_diag1_count ** 2
        heuristic_value += player_diag2_count ** 2
        heuristic_value -= opponent_diag2_count ** 2
        
        if player_diag1_count == 4 and 0 in [board[i][i] for i in range(5)]:
            heuristic_value += 2000
        elif player_diag2_count == 4 and 0 in [board[i][4 - i] for i in range(5)]:
            heuristic_value += 2000

        for i in range(5):
            for j in range(5):
                if board[i][j] == symbol:
                    heuristic_value += position_values[i][j]
                    block_value = Heuristic.prevent_opponent_blocks(board, -symbol, i, j)
                    heuristic_value += block_value
                    continuity_value = Heuristic.check_continuity(board, symbol, i, j)
                    heuristic_value += continuity_value
                elif board[i][j] == -symbol:
                    heuristic_value -= position_values[i][j]
                    block_value = Heuristic.prevent_opponent_blocks(board, symbol, i, j)
                    heuristic_value -= block_value
                    continuity_value = Heuristic.check_continuity(board, -symbol, i, j)
                    heuristic_value -= continuity_value

        board_key = Heuristic.calculate_board_key(board)

        if board_key in Heuristic.heuristic_cache:
            return Heuristic.heuristic_cache[board_key]
        else:
            Heuristic.heuristic_cache[board_key] = heuristic_value
            return heuristic_value

    @staticmethod
    def prevent_opponent_blocks(board, opponent_symbol, i, j):
        block_value = 0

        if j > 0 and board[i][j - 1] == opponent_symbol:
            if j < 4 and board[i][j + 1] == 0:
                block_value += 500

        if i > 0 and board[i - 1][j] == opponent_symbol:
            if i < 4 and board[i + 1][j] == 0:
                block_value += 500

        return block_value


    @staticmethod
    def check_continuity(board, symbol, row, col):
        continuity_value = 0
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]

        for direction in directions:
            dx, dy = direction
            count = 1

            x, y = row + dx, col + dy
            while 0 <= x < 5 and 0 <= y < 5 and board[x][y] == symbol:
                count += 1
                x += dx
                y += dy

            x, y = row - dx, col - dy
            while 0 <= x < 5 and 0 <= y < 5 and board[x][y] == symbol:
                count += 1
                x -= dx
                y -= dy

            if count >= 3:
                continuity_value += count

        return continuity_value

    @staticmethod
    def check_immediate_win(board, symbol):
        for i in range(5):
            if sum(1 for j in range(5) if board[i][j] == symbol) == 4 and 0 in board[i]:
                return True
            if sum(1 for j in range(5) if board[j][i] == symbol) == 4 and 0 in [board[j][i] for j in range(5)]:
                return True

        if sum(1 for i in range(5) if board[i][i] == symbol) == 4 and 0 in [board[i][i] for i in range(5)]:
            return True
        if sum(1 for i in range(5) if board[i][4 - i] == symbol) == 4 and 0 in [board[i][4 - i] for i in range(5)]:
            return True

        return False

        
# Prueba del juego
print(" 0 : Cara neutra / 1: Marca de círculo / -1: Marca de cruz\n")

bot = Quixxo(1)
initial_board = [[0] * 5 for _ in range(5)]  # Tablero inicial
bot.board = bot.play_turn(initial_board)


