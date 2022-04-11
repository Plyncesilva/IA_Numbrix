# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys

from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1
        
    def get_board(self):
        return self.board
    
    def get_id(self):
        return self.id

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, size: int, board: list) -> None:
        self.size = size
        self.board = board

    def set_number(self, row: int, col: int, num: int) -> None:
        self.board[row][col] = num

    def get_board(self) -> list:
        return self.board
    
    def get_size(self) -> int:
        return self.size
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board[row][col]      
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if row == 0:
            return (self.get_number(row+1, col), None)
        elif row == self.get_size()-1:
            return (None, self.get_number(row-1, col))
        else:
            return (self.get_number(row+1, col), self.get_number(row-1, col))
            
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        if col == 0:
            return (None, self.get_number(row, col+1))
        elif col == self.get_size()-1:
            return (self.get_number(row, col-1), None)
        else:
            return (self.get_number(row, col-1), self.get_number(row, col+1))
    
    def get_filled_positions(self):
        """ Devolve uma lista de tuplos com posicoes dos elementos do quadro
        que ja estao preenchidas, com o respetivo numero """
        res = []
        for row in range(self.get_size()):
            for col in range(self.get_size()):
                if self.get_number(row, col) != 0:
                    res += [(row, col, self.get_number(row, col))]
        return res
        
    def get_ordered_filled_positions(self):
        filled = self.get_filled_positions()
        return sorted(filled, key=lambda n: n[-1])
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        fp = open(filename, "r")
        size =  int(fp.readline())
        board = []

        for text_line in fp.readlines():
            line = []
            elements = text_line.split("\t")
            for index in range(size):
                line += [int(elements[index])]
            board += [line]

        fp.close()

        return Board(size, board) 

    # TODO: outros metodos da classe
    def __str__(self) -> str:
        res = ""
        for line in self.board:
            for element in line:
                res += str(element) + "\t"
            res += "\n"
        return res

class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.board = board

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. Uma acao e representada
        por (row, col, num)"""
        
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        board = state.get_board() # verificar validade da action???
        board.set_number(action[0], action[1], action[2])
        return NumbrixState(board)

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        def next_to(position1, position2):
            row1 = position1[0]
            row2 = position2[0]
            col1 = position1[1]
            col2 = position2[1]
            
            return ((row1 == row2 + 1 or row1 == row2 - 1) and (col1 == col2)) or \
                    ((row1 == row2) and (col1 == col2 + 1 or col1 == col2 - 1)) and\
                        position1[2] == position2[2]-1
        
        positions = board.get_ordered_filled_positions()
        if len(positions) != board.get_size()**2:
            return False
        
        for index in range(len(positions) - 1):
            if (not next_to(positions[index], positions[index+1])):
                return False
        
        return True
        

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    board = Board.parse_instance(sys.argv[1])
    print(board) #debug    
    print(board.get_ordered_filled_positions()) # debug
    # Usar uma técnica de procura para resolver a instância,
    #debug
    numbrix = Numbrix(board)
    state = NumbrixState(board)
    print(numbrix.goal_test(state))
    
    # Retirar a solução a partir do nó resultante,
    
    # Imprimir para o standard output no formato indicado.
    
    pass
