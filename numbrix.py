# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 84:
# 95656 Pedro Lynce Silva
# 00000 Nome2

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

    def get_reserved(self):
        res: dict = {}
        for pos in self.get_ordered_filled_positions_not_satisfied():
            if len(pos[3]) == self.blank_neighbors_count(pos[0], pos[1]):
                blank_neighbours = self.get_blank_neighbors(pos[0], pos[1])
                for bn in blank_neighbours:
                    res[bn] = pos[2]
        return res

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
        for row in range(self.get_size()):
            for col in range(self.get_size()):
                if self.get_number(row, col) != 0:
                    res += [(row, col, self.get_number(row, col))]
        return res
        
    def get_ordered_filled_positions(self):
        filled = self.get_filled_positions()
        return sorted(filled, key=lambda n: n[-1])

    def get_goals(self, num: int) -> list:
        if num == 1:
            goals = [num+1]
        elif num == self.get_size()**2:
            goals = [num-1]
        else:
            goals = [num-1, num+1]
        return goals

    def get_radar_goals(self, num: int) -> list:
        if num == 2 or num == 1:
            goals = [num+2]
        elif num == (self.get_size()**2)-1 or num == self.get_size()**2:
            goals = [num-2]
        else:
            goals = [num - 2, num + 2]
        return goals 

    def get_ordered_filled_positions_not_satisfied(self):
        '''
        (row, col, num, missing_goals)
        '''
        filled = self.get_ordered_filled_positions()
        res = []

        for position in filled:
            row = position[0]
            col = position[1]
            num = position[2]
            missing_el = []

            goal: list = self.get_goals(row, col, num)

            neighbors = self.adjacent_horizontal_numbers(row, col) + self.adjacent_vertical_numbers(row, col)
            for el in goal:
                if el not in neighbors:
                    missing_el += [el]
            if missing_el != []:
                res += [(row, col, num, missing_el)]

        return res

    def get_diagonal_neighbors(self, row: int, col: int):
        return [self.get_number(row-1, col-1), self.get_number(row-1, col+1), self.get_number(row+1, col-1), self.get_number(row+1, col+1)]

    def get_blank_neighbors(self, row: int, col: int) -> list:
                    # esquerda, direita                               baixo, cima
        neighbors = self.adjacent_horizontal_numbers(row, col) + self.adjacent_vertical_numbers(row, col)
        res = []
        possibilities = [(row, col-1), (row, col+1), (row+1, col), (row-1, col)]

        for i in range(len(neighbors)):
            if neighbors[i] == 0:
                res += [possibilities[i]]
        return res

    def get_circle_blank_neighbours(self, row: int, col: int):
        res = self.get_blank_neighbors(row, col)
        diagonals = [(row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
        nums = self.get_diagonal_neighbors(row, col)

        for i in range(len(nums)):
            if nums[i] == 0:
                res += [diagonals[i]]
        return res


    def blank_neighbors_count(self, row: int, col: int) -> int:
        neighbors: list = self.adjacent_horizontal_numbers(row, col) + self.adjacent_vertical_numbers(row, col)
        return neighbors.count(0)

    def get_neighbors(self, row: int, col: int) -> list:
                    # left righ down up
        return self.adjacent_horizontal_numbers(row, col) + self.adjacent_vertical_numbers(row, col)

    def get_neighbors_coordinates(self, row: int, col: int):
        res = []
        neighbours = self.get_neighbors(row, col)
        for i in range(len(neighbours)):
            if neighbours[i] != None:
                if i == 0:
                    res += [(row, col-1, neighbours[i])]
                elif i == 1:
                    res += [(row, col+1, neighbours[i])]
                elif i == 2:
                    res += [(row+1, col, neighbours[i])]
                else:
                    res += [(row-1, col, neighbours[i])]

        return res
            
    def number_exists(self, num: int) -> bool:
        return num in self.family

    def get_radar_neighbours(self, row: int, col: int) -> list:
        return self.get_neighbors(row, col) + (self.get_number(row-1, col-1), self.get_number(row-1, col-1), self.get_number(row+1, col-1), self.get_number(row-1, col+1), self.get_number(row+1, col+1))


    def copy(self):
        board = []
        for row in self.board:
            board.append(row.copy())
        return board

    def position_satisified(self, row: int, col: int, num) -> bool:
        if num == None:
            return True
        goals = self.get_goals(row, col, num)
        neighbors = self.get_neighbors(row, col)
        for goal in goals:
            if goal not in neighbors:
                return False
        return True

    def trapped_position(self, row: int, col: int):
        return 0 not in self.get_neighbors(row, col)

    def check_writing_possibility(self, num: int, row: int, col: int):
        # first requirement:
        # num to be written must have at least 1 blank neighbor or be the end of line
        end_of_line = [1, self.get_size()**2]
        
        return self.blank_neighbors_count(row, col) > 0 or num in end_of_line or self.position_satisified(row, col, num)

    def on_wall(self, row: int, col: int):
        return None in self.get_neighbors(row, col)

    
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

    def all_neighbours_satisfied(self, row: int, col: int):
        return self.position_satisified(row-1, col, self.get_number(row-1, col)) \
            and self.position_satisified(row+1, col, self.get_number(row+1, col))\
                 and self.position_satisified(row, col-1, self.get_number(row, col-1))\
                      and self.position_satisified(row, col+1, self.get_number(row, col+1))

    def no_writing_possible(self, row: int, col: int):
        nb = self.get_neighbors_coordinates(row, col)
        for position in nb:
            if position != None:
                goals = self.get_goals(position[0], position[1], position[2])
                for goal in goals:
                    if self.check_writing_possibility(goal, row, col):
                        return False
        return True

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

    def impossible_board(self, row: int, col: int, num: int, upper: bool) -> bool:
        '''
        True if the board becomes impossible by some action
        '''
        
        # Case 1: number already written
        if self.board_contains(row, col, num):
            return True 

        board: Board = self.get_board()

        # Case 2: not possible to write the number there
        if not self.check_writing_possibility(num, row, col) and not self.position_satisified(row, col, num):
            return True

        self.set_number(row, col, num)
        filled = self.get_ordered_filled_positions_not_satisfied()

        # CASE 2: Distance to other numbers must be consistent
        if not self.position_satisified(row, col, num):
            if upper:
                closest = self.get_max()
            else:
                closest = self.get_min()
            for position in filled:
                if upper and num < position[2] < closest:
                    closest = position[2]
                elif not upper and closest < position[2] < num:
                    closest = position[2]
            dist = minDistance(self.get_board(), row, col, closest)
            
            if not abs(num-closest) >= dist or dist == -1:
                self.remove_number(row, col)
                return True
        # Case 3: there is a hole
        for bn in self.get_circle_blank_neighbours(row, col):
            if self.trapped_position(bn[0], bn[1]):
                if self.all_neighbours_satisfied(bn[0], bn[1]):
                    self.remove_number(row, col)
                    return True
                if self.no_writing_possible(bn[0], bn[1]):
                    self.remove_number(row, col)
                    return True
        

        self.remove_number(row, col)        
        return False

    def not_satisfiable(self, row: int, col: int):
        neighbours = self.get_neighbors(row, col)
        for n in neighbours:
            if n != None:
                if n+2 in neighbours and n-2 in neighbours:
                    return False
                elif 2 in neighbours or self.size**2-1 in neighbours:
                    return False

        return True

    def get_goals(self, row: int, col: int, num: int) -> list:
        EOL = [1, self.size**2]
        nb = self.get_neighbors(row, col)

        if num in EOL:
            if num == 1 and 2 not in nb:
                return [2]
            elif num == self.size**2 and num-1 not in nb:
                return [num-1]
            else:
                return []
        else:
            goals = []
            if num-1 not in nb:
                goals += [num-1]
            if num+1 not in nb:
                goals += [num+1]
            return goals

    def unsolvable(self):
        board = self.get_board()

        for row in range(self.get_size()):
            for col in range(self.get_size()):
                if self.get_number(row, col) == 0 and self.trapped_position(row, col) and not self.position_satisified(row, col, self.get_number(row, col)):
                    if not self.position_satisified(row, col, 1) and not self.position_satisified(row, col, self.size**2):
                        return True
        return False

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
        return res[:-1]

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

    def extract_unique_moves(self, moves):
        uniques = {}
        res = []
        removed = []
        counter = 0
        for action in moves:
            if action[2] in uniques:
                uniques.pop(action[2], None)
                removed += [action[2]]
            elif action[2] not in uniques and action[2] not in removed:
                uniques[action[2]] = counter
            if self.board.trapped_position(action[0], action[1]) and self.board.position_satisified(action[0], action[1], action[2]):
                res += [(action[0], action[1], action[2])]
            counter += 1
        for unique in uniques:
            if moves[uniques[unique]] not in res:
                res += [moves[uniques[unique]]]
        return res
        
    def execute(self, actions, state: NumbrixState):
        board = state.get_board()
        for a in actions:
            board.set_number(a[0], a[1], a[2])

    def remove_action_in_cell(self, row: int, col: int, actions: list):
        for action in actions:
            if action[0] == row and action[1] == col:
                actions.remove((row, col, action[2]))
        return actions

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
        
    def neighbours_far(self, num: int, neighbors: list):
        for n in neighbors:
            if n != None and n != 0 and abs(n-num) > 5:
                return True
        return False

    def blocked_neighbour(self, neighbours: list, num: int,row, col, board: Board):
        counter = 0
        positions = [(row, col-1), (row, col+1), (row+1, col), (row-1, col)]
        for n in neighbours:
        
            if n != None and n != 0 and n != num-1 and n != num+1:
                pos = positions[counter]
                if board.trapped_position(pos[0], pos[1]) and not board.position_satisified(pos[0], pos[1], board.get_number(pos[0], pos[1])):
                    return True
            counter += 1
                
        return False

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. 
            Procura maior caminho de numeros consecutivos.
        """
        board: Board = node.state.board
        size = board.get_size()
        res = 0

        for row in range(size):
            for col in range(size):
                neighbours = board.get_neighbors(row, col)
                curr = board.get_number(row, col)
                if curr == 1:
                    if 2 not in neighbours:
                        res += 3
                elif curr == size**2:
                    if curr-1 not in neighbours:
                        res += 3
                elif curr-1 not in neighbours and curr+1 not in neighbours:
                    res += 10
                elif curr-1 not in neighbours or curr+1 not in neighbours:
                    res += 2
        return res

    
    # TODO: outros metodos da classe


# QItem for current location and distance
# from source location
class QItem:
    def __init__(self, row, col, dist):
        self.row = row
        self.col = col
        self.dist = dist
 
    def __repr__(self):
        return f"QItem({self.row}, {self.col}, {self.dist})"
 
def minDistance(grid, row, col, d):
    source: QItem = QItem(row, col, 0)
 
    # To maintain location visit status
    visited = [[False for _ in range(len(grid[0]))]
               for _ in range(len(grid))]
     
    # applying BFS on matrix cells starting from source
    queue = []
    queue.append(source)
    visited[source.row][source.col] = True
    while len(queue) != 0:
        source = queue.pop(0)
 
        # Destination found;
        if (grid[source.row][source.col] == d):
            return source.dist
 
        # moving up
        if isValid(source.row - 1, source.col, grid, visited, d):
            queue.append(QItem(source.row - 1, source.col, source.dist + 1))
            visited[source.row - 1][source.col] = True
 
        # moving down
        if isValid(source.row + 1, source.col, grid, visited, d):
            queue.append(QItem(source.row + 1, source.col, source.dist + 1))
            visited[source.row + 1][source.col] = True
 
        # moving left
        if isValid(source.row, source.col - 1, grid, visited, d):
            queue.append(QItem(source.row, source.col - 1, source.dist + 1))
            visited[source.row][source.col - 1] = True
 
        # moving right
        if isValid(source.row, source.col + 1, grid, visited, d):
            queue.append(QItem(source.row, source.col + 1, source.dist + 1))
            visited[source.row][source.col + 1] = True
 
    return -1
 
 
# checking where move is valid or not
def isValid(x, y, grid, visited, d):
    if ((x >= 0 and y >= 0) and
        (x < len(grid) and y < len(grid[0])) and
            (grid[x][y] == 0 or grid[x][y] == d) and (visited[x][y] == False)):
        return True
    
    return False

if __name__ == "__main__":
    start_time = datetime.now()

    # Ler o ficheiro de input de sys.argv[1],
    board = Board.parse_instance(sys.argv[1])
    
    # Usar uma técnica de procura para resolver a instância,
    #debug
    problem = Numbrix(board)


    node: Node = depth_first_tree_search(problem)
    # Retirar a solução a partir do nó resultante,
    
    solution_board = node.state.board
    print(solution_board)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

    # Retirar a solução a partir do nó resultante,
    
    # Imprimir para o standard output no formato indicado.
    
    pass
