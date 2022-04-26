# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 84:
# 95656 Pedro Lynce Silva
# 95591 Hugo Verissimo

import sys
from datetime import datetime

from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, size: int, board: list=[]) -> None:
        self.size = size
        self.family = []
        self.remaining = list(range(1, size**2 +1))
        self.map = {}
        if board == []:
            for i in range(self.size):
                aux = []
                for j in range(self.size):
                    aux += [0]
                board += [aux]
        else:
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] != 0:
                        self.family += [board[row][col]]
                        self.map[board[row][col]] = (row, col)
                        self.remaining.remove(board[row][col])

        self.board = board


    def set_number(self, row: int, col: int, num: int):
        self.family += [num]
        self.map[num] = (row, col)
        self.board[row][col] = num
        self.remaining.remove(num)

    def get_board(self) -> list:
        return self.board
    
    def get_size(self) -> int:
        return self.size
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        
        if self.get_size() > row >= 0 and self.get_size() > col >= 0:
            return self.board[row][col]
        else:
            return None       
    
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
        for num in self.family:
            res += [(self.map[num][0], self.map[num][1], num)]

        return res

    def get_goals(self, num: int) -> list:
        if num == 1:
            goals = [num+1]
        elif num == self.get_size()**2:
            goals = [num-1]
        else:
            goals = [num-1, num+1]
        return goals

    def get_neighbors(self, row: int, col: int) -> list:
        #                   left            righ            down            up
        return self.adjacent_horizontal_numbers(row, col) + self.adjacent_vertical_numbers(row, col)
            
    def number_exists(self, num: int) -> bool:
        return num in self.family

    def copy(self):
        board = []
        for row in self.board:
            board.append(row.copy())
        return board

    def manhattanDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # check the closest only
    def possible_from_manhattan(self, row, col, num, upper_goal: bool):
        # looking for max below
        if upper_goal:
            target = self.get_max_below(num)

        # looking for min above
        else:
            target = self.get_min_above(num)

        if target == num:
            return True

        target_position = self.get_coordinates(target)

        return self.manhattanDistance((row, col), (target_position[0], target_position[1])) <= abs(target - num)

    def get_coordinates(self, num: int):
        if num in self.map:
            return self.map[num]
        return ()

    def get_max(self):
        return max(self.family)

    def get_min(self):
        return min(self.family)

    def get_min_above(self, num: int):
        fam: list = self.family.copy()
        mx = max(fam)
        prev = num
        while mx > num:
            prev = mx
            fam.remove(mx)
            mx = max(fam)

        return prev

    def get_max_below(self, num: int):
        fam: list = self.family.copy()
        mn = min(fam)
        prev = num

        while mn < num:
            prev = mn
            fam.remove(mn)
            mn = min(fam)

        return prev

    def remove_number(self, row: int, col: int):
        self.family.remove(self.board[row][col])
        self.board[row][col] = 0

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

class NumbrixState:
    state_id = 0

    def __init__(self, board, h):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1
        self.h = h
        
    def get_board(self) -> Board:
        return self.board
    
    def get_id(self):
        return self.id

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe

class Numbrix(Problem):
    great_moves = []
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.board: Board = board
        self.initial = NumbrixState(board, 1000)
        super().__init__(self.initial)

    def get_jackpot_action(self, lower: tuple, upper: tuple, num: int, board: Board):
        res = []
        # COLUMN
        if lower[1] == upper[1] and abs(lower[0] - upper[0]) == 2:
            # empty position to put number
            if board.get_number(min(lower[0], upper[0])+1, lower[1]) == 0:
                res += [(min(lower[0], upper[0]) +1, lower[1], num)]
        # ROW
        elif lower[0] == upper[0] and abs(lower[1]-upper[1]) == 2:
            # empty position to put number
            if board.get_number(lower[0], min(lower[1], upper[1]) + 1) == 0:
                res += [(lower[0], min(lower[1], upper[1]) + 1, num)]
        # FORM A DIAGONAL
        else:
            if board.get_number(lower[0], upper[1]) != 0:
                if board.get_number(upper[0], lower[1]) == 0:
                    res += [(upper[0], lower[1], num)]
            elif board.get_number(upper[0], lower[1]) != 0:
                if board.get_number(lower[0], upper[1]) == 0:
                    res += [(lower[0], upper[1], num)]
            else:
                # both positions are possible
                res += [(lower[0], upper[1], num), (upper[0], lower[1], num)]

        return res

    def actions(self, state: NumbrixState):
        actions = []
        board = state.get_board()
        size = board.get_size()
        EOL = [1, size**2]
        

        for num in board.remaining:

            # num has NO GOALS on board
            if not board.number_exists(num-1) and not board.number_exists(num+1):
                continue
            # num has BOTH GOALS on board (jackpot)
            elif board.number_exists(num-1) and board.number_exists(num+1): 
                lower = board.get_coordinates(num-1)
                upper = board.get_coordinates(num+1)
                return self.get_jackpot_action(lower, upper, num, board)

            # only ONE GOAL EXISTS, upper or lower targets
            else:
                # only lower goal exists
                if board.number_exists(num-1):
                    upper_goal = False
                    target = board.get_coordinates(num-1)
                # only upper goal exists
                else:
                    upper_goal = True
                    target = board.get_coordinates(num+1)
                
                #               left                            right                   down                    up
                positions = ((target[0], target[1]-1), (target[0], target[1]+1), (target[0]+1, target[1]), (target[0]-1, target[1]))
                neighbours = board.get_neighbors(target[0], target[1])
                
                for i in range(len(neighbours)):
                    if neighbours[i] == 0:
                        target_neighbours = board.get_neighbors(positions[i][0], positions[i][1])

                        # check for space or END OF LINE
                        if target_neighbours.count(0) >= 1 or num in EOL:
                            # check manhattan distance to the closest successor/antecessor
                            if board.possible_from_manhattan(positions[i][0], positions[i][1], num, upper_goal):
                                actions += [(positions[i][0], positions[i][1], num)]
                return actions
        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        board: Board = Board(state.get_board().size, state.board.copy()) # verificar validade da action???
        board.set_number(action[0], action[1], action[2])
        return NumbrixState(board, state.h)

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        def next_to(row: int, col: int, goal: int):
            return board.get_number(row-1, col) == goal or\
                    board.get_number(row+1, col) == goal or\
                        board.get_number(row, col-1) == goal or\
                            board.get_number(row, col+1) == goal
        
        board = state.get_board()
        size = board.size
        EOL = [1, size**2]

        if board.number_exists(0):
            return False

        for row in range(size):
            for col in range(size):
                curr = board.get_number(row, col)
                if curr not in EOL and next_to(row, col, curr+1) and next_to(row, col, curr-1):
                    continue
                elif curr == EOL[0] and next_to(row, col, curr+1):
                    continue
                elif curr == EOL[1] and next_to(row, col, curr-1):
                    continue
                else:
                    return False
        
        return True
        
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. 
            Procura maior caminho de numeros consecutivos.
        """
        board: Board = node.state.board
        size = board.get_size()
        res = 0
        # Penalties
        ZERO_GOALS = 20
        ONE_GOAL = 4
        EOL = 6

        for num in board.family:
            pos = board.get_coordinates(num)
            neighbours = board.get_neighbors(pos[0], pos[1])
            
            if num-1 not in neighbours and num+1 not in neighbours:
                res += ZERO_GOALS
            elif num-1 not in neighbours or num+1 not in neighbours:
                res += ONE_GOAL
            elif num == 1 and num + 1 not in neighbours:
                res += EOL
            elif num == size**2 and num-1 not in neighbours:
                res += EOL


        return res

if __name__ == "__main__":
    #start_time = datetime.now()

    # Ler o ficheiro de input de sys.argv[1],
    board = Board.parse_instance(sys.argv[1])
    
    # Usar uma técnica de procura para resolver a instância,
    #debug
    problem = Numbrix(board)

    node: Node = depth_first_tree_search(problem)
    #node: Node = depth_first_tree_search(problem)
    #node: Node = depth_first_tree_search(problem)
    #node: Node = depth_first_tree_search(problem)
    #node: Node = astar_search(problem)
    # Retirar a solução a partir do nó resultante,
    
    solution_board = node.state.board
    print(solution_board)

    #end_time = datetime.now()
    #print('Duration: {}'.format(end_time - start_time))

    # Retirar a solução a partir do nó resultante,
    
    # Imprimir para o standard output no formato indicado.
    
    pass
