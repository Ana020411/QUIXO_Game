import copy
from queue import PriorityQueue

class QuixoReferee:
    def __init__(self, symbol):
       self.board = [[0] * 5 for _ in range(5)]
       self.symbol = symbol
       self.movements = []

   # Tomar en cuenta que la ficha no se puede poner en el mismo lugar de donde se sacó
   # Si para completar la alineación de 5 también se alineó 5 del oponente, pierdes

    def check_win(self, board, symbol):
       # Se checan filas y columnas
       for i in range(5):
           if all(board[i][j] == symbol for j in range(5)) or all(board[j][i] == symbol for j in range(5)):
               return True
       # Se checan diagonales
       if all(board[i][i] == symbol for i in range(5)) or all(board[i][4 - i] == symbol for i in range(5)):
           return True

       return False

    def play_turn(self, board):
       new_board, path = self.a_star()
       if new_board is None:
           return self.board  # No se encontró una solución
       else:
           self.board = new_board
           return self.board

    def reset(self, symbol):
       self.symbol = symbol
       self.board = [[0] * 5 for _ in range(5)]
       self.movements = []

    "---------------------------------MOVIMIENTOS----------------------------------------"
    def move_right(self, board, row, col):
       if board[row][col] == self.symbol or board[row][col] == 0:
           while col < 4:
               board[row][col] = board[row][col + 1]
               col += 1
           board[row][4] = self.symbol
       return board

    def move_left(self, board, row, col):
       if board[row][col] == self.symbol or board[row][col] == 0:
           while col > 0:
               board[row][col] = board[row][col - 1]
               col -= 1
           board[row][0] = self.symbol
       return board

    def move_up(self, board, row, col):
       if board[row][col] == self.symbol or board[row][col] == 0:
           while row > 0:
               board[row][col] = board[row - 1][col]
               row -= 1
           board[0][col] = self.symbol
       return board

    def move_down(self, board, row, col):
       if board[row][col] == self.symbol or board[row][col] == 0:
           while row < 4:
               board[row][col] = board[row + 1][col]
               row += 1
           board[4][col] = self.symbol
       return board

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
            movements.extend(["down", "up", "right"])
        elif 1 <= row <= 3 and col == 4:
            movements.extend(["down", "up", "left"])
        elif row == 0 and 1 <= col <= 3:
            movements.extend(["down", "right", "left"])
        elif row == 4 and 1 <= col <= 3:
            movements.extend(["up", "right", "left"])
        else:
            return "Movimiento inválido. Solo se permiten movimientos en la periferia del tablero."
        return movements

    def apply_move(self, move):
        row, col, movement = move
        new_board = copy.deepcopy(self.board)

        if movement == "down":
            new_board = self.move_down(new_board, row, col)
        elif movement == "up":
            new_board = self.move_up(new_board, row, col)
        elif movement == "right":
            new_board = self.move_right(new_board, row, col)
        elif movement == "left":
            new_board = self.move_left(new_board, row, col)

        return new_board

    def a_star(self):
            visited = []
            pq = PriorityQueue()
            source = NodeAStar(self.board, path=[])
            pq.put((0, source))

            while not pq.empty():
                _, current = pq.get()
                
                if current not in visited:
                    current_board = current.state

                    if self.check_win(current_board, self.symbol):
                        return current_board, current.path

                    visited.append(current)

                    for row in range(5):
                        for col in range(5):
                            if current_board[row][col] == self.symbol or current_board[row][col] == 0:
                                movements = self.get_movements(row, col)
                                for move in movements:
                                    new_board = self.apply_move((row, col, move))
                                    new_node = NodeAStar(new_board, current.path + [(row, col, move)])
                                    new_node.distance = current.distance + 1
                                    new_node.calculate_heuristic(current_board, self.symbol)
                                    pq.put((new_node.distance + new_node.heuristic_value, new_node))
                else:
                    continue

            return None, []

    def print_board(self):
       for row in self.board:
           print(' | '.join(str(cell) for cell in row))
           print('------------------')

class Node:
    def __init__(self, state, path=None):
       self.state = state
       self.path = path if path is not None else []
       self.heuristic = None

    '''def calculate_heuristic(self, heuristic):
       self.heuristic_value = heuristic(self)'''

    def calculate_heuristic(self, board, symbol):
       self.heuristic_value = Heuristic().heuristic1(board, symbol)

    def __eq__(self, other):
       if not isinstance(other, Node):
           return False
       return self.state == other.state

    def __lt__(self, other):
       if not isinstance(other, Node):
           return False
       return self.heuristic_value < other.heuristic_value

    def __gt__(self, other):
       if not isinstance(other, Node):
           return False
       return self.heuristic_value > other.heuristic_value

class NodeAStar(Node):
   def __init__(self, state, path=None):
       super().__init__(state, path=path)
       self.distance = 0

   def __lt__(self, other):
       if not isinstance(other, NodeAStar):
           return False
       return (self.distance + self.heuristic_value) < (other.distance + other.heuristic_value)

   def __gt__(self, other):
       if not isinstance(other, NodeAStar):
           return False
       return (self.distance + self.heuristic_value) > (other.distance + other.heuristic_value)

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
    def heuristic3(self, board, last_move, symbol, t_table):
        # Se checa si el resultado se encuentra en la tabla
        board_tuple = tuple(map(tuple, board))
        if board_tuple in t_table:
            return t_table[board_tuple]

        heuristic_value = 0
        player_symbol = symbol
        opponent_symbol = -symbol

        # fila y columna del último movimiento
        row, col = last_move

        # Solo se evalúa la celda que se modificó y sus vecinos
        for i in range(max(0, row-1), min(5, row+2)):
            for j in range(max(0, col-1), min(5, col+2)):
                if board[i][j] == 0:
                    board[i][j] = player_symbol
                    if self.check_win(board, player_symbol):
                        heuristic_value += 1
                    board[i][j] = opponent_symbol
                    if self.check_win(board, opponent_symbol):
                        heuristic_value -= 1

                    heuristic_value += self.check_continuity(board, player_symbol, i, j)
                    board[i][j] = 0

        # Se guarda el resultado en la tabla de transposición
        t_table[board_tuple] = heuristic_value

        return heuristic_value

print(" 0 : Cara neutra / 1: Marca de círculo / -1: Marca de cruz\n")

# Crear un tablero inicial con algunas fichas colocadas
initial_board = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Colocar algunas fichas en el tablero inicial
initial_board[0][0] = 1

# Crear una instancia de QuixoReferee con el símbolo del jugador
quixo = QuixoReferee(1)

print("Tablero inicial:")
quixo.board = initial_board
quixo.print_board()

print("\nRealizando un movimiento...")
quixo.play_turn(quixo.board)

print("\nTablero después de realizar el movimiento:")
quixo.print_board()
