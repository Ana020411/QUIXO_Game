#ESTE ARCHIVO ES SOLO INFORMACION EXTRA. PARA EVALUAR, USAR UNICAMENTE EL ARCHIVO NOMBRADO QUIXO PORFAVOR

#A estrella que decidimos no usar

'''def get_best_move(self):
        best_heuristic_value = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        max_depth = 4  # Reducir la profundidad de búsqueda a 2

        for i in range(5):
            for j in range(5):
                if i == 0 or i == 4 or j == 0 or j == 4:
                    if self.board[i][j] == 0 or self.board[i][j] == self.symbol:
                        movements = self.get_movements(i, j)
                        if movements != "Movimiento invalido. Solo se permiten movimientos en la periferia del tablero":
                            for move in movements:
                                new_board = self.apply_move(self.board, i, j, move)
                                if self.check_win(new_board, self.symbol):  # Checar por la victoria inmediata
                                    return (i, j, move)
                                heuristic_value, _ = self.a_star(new_board, Heuristica.heu, max_depth)  # Ajustar la profundidad máxima según sea necesario
                                new_board = self.undo_move(new_board, i, j, move)
                                if heuristic_value is not None and heuristic_value > best_heuristic_value:
                                    best_heuristic_value = heuristic_value
                                    best_move = (i, j, move)
                                    alpha = max(alpha, best_heuristic_value)
                                    if beta <= alpha:
                                        break

        return best_move

class NodeAStar:
    def _init_(self, state, path, symbol):
        self.state = state
        self.path = path
        self.distance = 0
        self.heuristic_value = 0
        self.symbol = symbol

    def calculate_heuristic(self, heuristic):
        self.heuristic_value = heuristic(self.state, self.symbol)

    def _eq_(self, other):
        return self.state == other.state

    def _lt_(self, other):
        return (self.distance + self.heuristic_value) < (other.distance + other.heuristic_value)

    def _hash_(self):
        return hash(str(self.state))


    def a_star(self, start_board, heuristic, max_depth):
        visited = set()
        pq = PriorityQueue()
        source = NodeAStar(start_board, path=[], symbol=self.symbol)
        pq.put((0, source))
        alpha = -math.inf
        beta = math.inf

        while not pq.empty():
            _, current = pq.get()

            if tuple(map(tuple, current.state)) not in visited:
                current_board = current.state

                if self.check_win(current_board, self.symbol):
                    return heuristic(current_board, self.symbol), current.path

                visited.add(tuple(map(tuple, current.state)))

                if current.distance < max_depth: 
                    for row in range(5):
                        for col in range(5):
                            if current_board[row][col] == self.symbol or current_board[row][col] == 0:
                                movements = self.get_movements(row, col)
                                for move in movements:
                                    new_board = self.apply_move(current_board, row, col, move)
                                    new_node = NodeAStar(new_board, current.path + [(row, col, move)], self.symbol)
                                    new_node.distance = current.distance + 1
                                    new_node.calculate_heuristic(heuristic)
                                    pq.put((new_node.distance + new_node.heuristic_value, new_node))
                                    if new_node.heuristic_value >= beta:
                                        break
                                    alpha = max(alpha, new_node.heuristic_value)
                else:
                    continue

        return None, []

'''
#SEGUNDA OPCION DE HEURISTICA 

'''
class Heuristica:
    
    @staticmethod
    def cell_line(line, symbol):
        symbol_cell = 0
        empty_cell = 0
        for cell in line:
            if cell == symbol:
                symbol_cell += 1
            elif cell == 0:
                empty_cell += 1
        return symbol_cell, empty_cell

    @staticmethod
    def cell_possible_moves(board, symbol):
        possible_moves = 0
        for i in range(5):
            for j in range(5):
                if board[i][j] == symbol or board[i][j] == 0:
                    possible_moves += 1
        return possible_moves

    @staticmethod
    def heu(board, symbol):
        heuristic_value = 0
        
        center_position = (2, 2)
        adjacent_positions = {(1, 2), (2, 1), (2, 3), (3, 2)}
        center_axis_positions = {(1, 1), (1, 3), (3, 1), (3, 3)}
        corner_positions = {(0, 0), (0, 4), (4, 0), (4, 4)}
        
        for i in range(5):
            row = board[i]
            col = [board[j][i] for j in range(5)]
            diag1 = [board[i][i] for i in range(5)]
            diag2 = [board[i][4-i] for i in range(5)]
            
            row_symbol_cell, row_empty_cell = Heuristica.cell_line(row, symbol)
            col_symbol_cell, col_empty_cell = Heuristica.cell_line(col, symbol)
            diag1_symbol_cell, diag1_empty_cell = Heuristica.cell_line(diag1, symbol)
            diag2_symbol_cell, diag2_empty_cell = Heuristica.cell_line(diag2, symbol)
            
            for symbol_cell, empty_cell in [(row_symbol_cell, row_empty_cell), (col_symbol_cell, col_empty_cell), 
                                              (diag1_symbol_cell, diag1_empty_cell), (diag2_symbol_cell, diag2_empty_cell)]:
                if symbol_cell == 5:
                    heuristic_value += 2000
                elif symbol_cell == 4 and empty_cell == 1:
                    heuristic_value += 1000
                elif symbol_cell == 3 and empty_cell == 2:
                    heuristic_value += 10
                elif symbol_cell == 2 and empty_cell == 3:
                    heuristic_value += 5
                opponent_cell = 4 - symbol_cell
                if opponent_cell == 4 and empty_cell == 1:
                    heuristic_value -= 1000
                elif opponent_cell == 3 and empty_cell == 2:
                    heuristic_value -= 10
                elif opponent_cell == 2 and empty_cell == 3:
                    heuristic_value -= 5

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
        
        possible_moves = Heuristica.cell_possible_moves(board, symbol)
        heuristic_value += possible_moves * 5

        opponent_possible_moves = Heuristica.cell_possible_moves(board, -symbol)
        heuristic_value -= opponent_possible_moves * 5

        return heuristic_value'''