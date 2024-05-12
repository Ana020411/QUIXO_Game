import random
import copy
from queue import PriorityQueue

class QuixoReferee:
    def __init__(self):
        self.board = [["-"]* 5 for _ in range(5)]

    def check_win(self, symbol):
        # Se checan filas y columnas
        for i in range(5):
            if all(self.board[i][j] == symbol for j in range(5)) or all(self.board[j][i] == symbol for j in range(5)):
                return True

        # Se checan diagonales
        if all(self.board[i][i] == symbol for i in range(5)) or all(self.board[i][4-i] == symbol for i in range(5)):
            return True

        return False

# Tomar en cuenta que la ficha no se puede poner en el mismo lugar de donde se sacó
# Si para completar la alineación de 5 también se alineó 5 del oponente, pierdes
class QuixoBot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.board = [["-"]* 5 for _ in range(5)]

    def play_turn(self, board):
        # Aquí se utilizaría el algoritmo de búsqueda para resolverlo
        # Debe regresar un tablero con tu movimiento del bot
        pass
    
    #CADA FICAH TIENE 3 POSIBLES MOVIMIENTOS POR TURNO 
    "---------------------------------MOVIMIENTOS----------------------------------------"
    def move_left(self, board, row, col):
        if board[row][col] == self.symbol or self.board[row][col] == "-":
            while col < 4:
                board[row][col] = board[row][col + 1]
                col += 1
            self.board[row][4] = self.symbol
            self.board = copy.deepcopy(board)
        return self.board
    
    def move_right(self, board, row, col):
        if board[row][col] == self.symbol or self.board[row][col] == "-":
            while col > 0:
                board[row][col] = board[row][col - 1]
                col -= 1
            self.board[row][0] = self.symbol
            self.board = copy.deepcopy(board)
        return self.board

    def move_down(self, board, row, col):
        if board[row][col] == self.symbol or self.board[row][col] == "-":
            while row > 0:
                board[row][col] = board[row - 1][col]
                row -= 1
            self.board[0][col] = self.symbol
            self.board = copy.deepcopy(board)
        return self.board
    
    def move_up(self, board, row, col):
        if board[row][col] == self.symbol or self.board[row][col] == "-":
            while row < 4:
                board[row][col] = board[row + 1][col]
                row += 1
            self.board[4][col] = self.symbol
            self.board = copy.deepcopy(board)
        return self.board
    

    def __movements(self, row, col):
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

    def movimientos(self, row, col):
        movimientos_posibles = self.__movements(row, col)
        print("Movimientos posibles:", movimientos_posibles)
        
        movimiento_elegido = random.choice(movimientos_posibles)
        print(f"Movimiento elegido: {movimiento_elegido}")
        
        # Se ejecuta el movimiento elegido
        if movimiento_elegido == "up":
            self.move_up(self.board, row, col)
            
        elif movimiento_elegido == "down":
            self.move_down(self.board, row, col)
            
        elif movimiento_elegido == "left":
            self.move_left(self.board, row, col)
            
        elif movimiento_elegido == "right":
            self.move_right(self.board, row, col)
            

        self.board = copy.deepcopy(self.board)

        
            
    "*----------------------------------EJECUCION-----------------------------------"
    def print_board(self):
        for row in self.board:
            print(' | '.join(str(cell) for cell in row))
            print('------------------')

    def reset(self):
        self.board = [["-"]* 5 for _ in range(5)]
        
"------------------------------CLASE NODO A*--------------------------------------------------"    
class Node:
    def __init__(self, state, path=None):
        self.state = state
        self.path = path if path is not None else []
        self.heuristic = None

    def calculate_heuristic(self, other, heuristic):
        self.heuristic_value = heuristic(self, other)

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
    
    def __init__(self, state,  path=None):
        super()._init_(state,  path=path)
        self.distance = 0

    def _lt_(self, other):
        if not isinstance(other, NodeAStar):
            return False
        return (self.distance + self.heuristic_value) < (other.distance + other.heuristic_value)
    
    def _gt_(self, other):
        if not isinstance(other, NodeAStar):
            return False
        return (self.distance + self.heuristic_value) > (other.distance + other.heuristic_value)

"---------------------------HEURISTICA------------------------"
class Heuristica:
    @staticmethod
    def heuristic0(node_a, node_b):
        return 0
"---------------------------------A*---------------------------"



print(" 0 : Cara neutra / o: Marca de circulo / x: Marca de cruz\n")
#symbol = input("¿Qué marca quieres? Escribe o/x\n")

quixo = QuixoBot('x')
print("Tablero antes de realizar movimientos:")
quixo.print_board()

print("\nTablero después de realizar el movimiento:")

quixo.movimientos(0, 0)
quixo.movimientos(4, 4)
quixo.movimientos(3, 0)
quixo.movimientos(0, 1)
quixo.movimientos(0, 1)


quixo.print_board()