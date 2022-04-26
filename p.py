# Grupo 39:
# 90398 Joao Silva
# 95633 Maria Varanda

#v63

import sys
import copy
from search import InstrumentedProblem, Problem, Node, astar_search, breadth_first_tree_search, compare_searchers, depth_first_tree_search, greedy_search, recursive_best_first_search
from utils import distance


class NumbrixState:
    state_id = 0

    # O(1) v
    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # O(1) v
    def at_least_two_adjacent_numbers_are_sequential(self, number, position):

        # O(1)
        horizontal_adjacent_numbers = self.board.adjacent_horizontal_numbers(position[0], position[1])
        vertical_adjacent_numbers = self.board.adjacent_vertical_numbers(position[0], position[1])

        # O(1)
        return self.board.at_least_two_adjacent_numbers_are_sequential(number, horizontal_adjacent_numbers, vertical_adjacent_numbers)

    # O(1) v
    def are_sequential(self, n, n1, n2):
        sequential = [n-1, n+1]
        return n1 in sequential and n2 in sequential

    # O(N^2) v
    def set_board_value(self, row, col, value):

        # O(N^2)
        self.board.set_value(row, col, value)

    def to_string(self):
        return("board:\n" + self.board.to_string() + "\nid:\n" + str(self.id))


class Board:

    # O(N) v
    """ Representação interna de um tabuleiro de Numbrix. """
    def __init__(self, lines):

        # a primeira linha de linhas e' da forma [N]
        N = lines[0][0]

        self.N = N

        # O(N)
        self.lines = lines[1:]
        self.max = N**2

        self.last_changed_position = (-1, -1)
        self.last_set_value = 0

        self.impossible_board = False

        # O(1)
        self.number_of_filled_values = 0

        # O(1)
        self.missing_values = []

    # O(1) v
    def set_number_of_filled_values(self, number_of_filled_values):
        self.number_of_filled_values = number_of_filled_values

    # O(1) v
    def set_missing_values(self, missing_values):
        self.missing_values = missing_values
    
    # O(1) v
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """

        # O(1)
        return self.lines[row][col]
    
    # O(1) v
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """

        # Caso N == 1
        if self.N == 1:
            return (None, None)

        # Caso N > 1
        elif self.N > 1:

            # Caso primeira linha
            if row == 0:
                return (self.get_number(row + 1, col), None)
            # Caso ultima linha
            elif row == self.N - 1:
                return (None, self.get_number(row - 1, col))
            # Caso linha intermedia
            else:
                return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    # O(1) v
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """

        # Caso N == 1
        if self.N == 1:
            return (None, None)

        # Caso N > 1
        elif self.N > 1:

            # Caso primeira coluna
            if col == 0:
                return (None, self.get_number(row, col + 1))
            # Caso ultima coluna
            elif col == self.N - 1:
                return (self.get_number(row, col - 1), None)
            # Caso coluna intermedia
            else:
                return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    # O(N^4) v
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """

        # Abrir ficheiro e ler conteudo
        file = open(filename, "r")

        # O(N)
        lines_strings = file.readlines()

        # Coverter linhas de strings para linhas de ints
        lines_ints = []
        # O(N^2)
        for line in lines_strings:
            line_ints = [int(string_number) for string_number in line.split()]
            lines_ints.append(line_ints)

        # O(N)
        # Criar e retornar board
        board = Board(lines_ints)

        # O(N^2)
        board.set_number_of_filled_values(len(board.get_filled_values()))

        # O(N^4)
        missing_values = board.get_missing_values()

        sorted_missing_values = board.sort_missing_values(missing_values)

        # O(1)
        board.set_missing_values(sorted_missing_values)

        return board

    def sort_missing_values(self, missing_values):

        N = self.N
        first_filled_value = self.get_first_filled_value()

        smaller_values = self.get_smaller_values(first_filled_value, missing_values)
        greater_values = self.get_greater_values(first_filled_value, missing_values)

        smaller_values.sort(reverse = True)
        greater_values.sort()

        return smaller_values + greater_values

    def get_first_filled_value(self):

        N = self.N
        first_filled_value = 0

        for row in range(N):
            for col in range(N):
                number = self.get_number(row, col)
                if number != 0:
                    return number

        return -1
        
    def get_smaller_values(self, number, values):

        smaller_values = []

        for value in values:
            if value < number:
                smaller_values.append(value)
        
        return smaller_values

    def get_greater_values(self, number, values):

        greater_values = []

        for value in values:
            if value > number:
                greater_values.append(value)
        
        return greater_values

    # O(N^2) v
    def get_filled_values(self):

        filledValues = []
        
        # O(N^2)
        for line in self.lines:
            for element in line:
                if element != 0:
                    filledValues.append(element)

        return filledValues

    # O(N^2) v
    def set_value(self, row, col, value):

        self.lines[row][col] = value
        self.last_changed_position = (row, col)
        self.last_set_value = value
        self.number_of_filled_values += 1
        
        # O(N^2)
        self.missing_values.remove(value)

        # Add new
        # O(1)
        horizontal_adjacent = self.adjacent_horizontal_numbers(row, col)
        vertical_adjacent = self.adjacent_vertical_numbers(row, col)

        number_of_walls = 0
        # O(1)
        for number in horizontal_adjacent:
            if number == None:
                number_of_walls += 1
        for number in vertical_adjacent:
            if number == None:
                number_of_walls += 1

        number_of_filled_adjacent = 0
        for number in horizontal_adjacent:
            if number != 0 and number != None:
                number_of_filled_adjacent += 1
        for number in vertical_adjacent:
            if number != 0 and number != None:
                number_of_filled_adjacent += 1

        number_of_free_positions = 4 - number_of_walls
        if number_of_filled_adjacent == number_of_free_positions and value != 1 and value != self.max:
            # O(1)
            if not self.at_least_two_adjacent_numbers_are_sequential(value, horizontal_adjacent, vertical_adjacent):
                self.impossible_board = True
                
        return self

    # O(N^2) v
    def goal_test_old(self):

        goal = True

        # O(N^2)
        for row in range(self.N):
            for col in range(self.N):

                # O(1)
                horizontal_adjacent_numbers = self.adjacent_horizontal_numbers(row, col)
                vertical_adjacent_numbers = self.adjacent_vertical_numbers(row, col)

                # if a single position is empty then this is not a goal state
                if self.lines[row][col] == 0:
                    return False

                # if not a single adjacent number is sequential then this is not a goal state
                # O(1)
                if not self.at_least_one_adjacent_number_is_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    return False

                # if for a number != 1 and != N**2 no two sequential numbers are adjacent then this is not a goal state 
                # O(1)
                if not self.at_least_two_adjacent_numbers_are_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    return False

        return goal

    # O(1)
    def goal_test(self):

        return self.missing_values == []

    # O(1) v
    def at_least_one_adjacent_number_is_sequential(self, current_number, horizontal_adjacent_numbers, vertical_adjacent_numbers):

        at_least_one_adjacent_is_sequential = False

        if current_number < 1 or current_number > self.N ** 2:
            raise Exception("at_least_one_adjacent_number_is_sequential: Input incorreto.")

        if current_number == 1:
            # O(1)
            for number in horizontal_adjacent_numbers:
                if number != None and number != 0:
                    if number == current_number + 1:
                        return True
            for number in vertical_adjacent_numbers:
                if number != None and number != 0:
                    if number == current_number + 1:
                        return True
            return False

        # O(1)
        for number in horizontal_adjacent_numbers:
            if number != None:
                if number == current_number + 1 or number == current_number - 1:
                    at_least_one_adjacent_is_sequential = True

        # O(1)
        for number in vertical_adjacent_numbers:
            if number != None:
                if number == current_number + 1 or number == current_number - 1:
                    at_least_one_adjacent_is_sequential = True

        return at_least_one_adjacent_is_sequential

    # O(1) v
    def at_least_two_adjacent_numbers_are_sequential(self, current_number, horizontal_adjacent_numbers, vertical_adjacent_numbers):

        sequential_numbers = 0
        if current_number > 1 and current_number < self.N ** 2:
            # O(1)
            for number in horizontal_adjacent_numbers:
                if number != None:
                    if number == current_number + 1 or number == current_number - 1:
                        sequential_numbers += 1
            # O(1)
            for number in vertical_adjacent_numbers:
                if number != None:
                    if number == current_number + 1 or number == current_number - 1:
                        sequential_numbers += 1
            if sequential_numbers != 2:
                return False
        return True

    # O(N^4) v
    def get_missing_values(self):

        missing_values = []

        # O(N^2)
        filled_values = self.get_filled_values()

        # O(N^2)
        for i in range(1, self.max + 1): # 1, 2, ..., N^2
            missing_values.append(i)

        # O(N^4)
        for filled_value in filled_values: # O(N^2)
            missing_values.remove(filled_value) # O(N^2)

        return missing_values

    # O(1) v
    def distance_between_positions(self, position1, position2):

        if position1 == (-1, -1):
            return self.max * 100

        distance_x = abs(position1[0] - position2[0])
        distance_y = abs(position1[1] - position2[1])
        distance = distance_x + distance_y

        if distance == 0:
            return 1

        return distance_x + distance_y

    # O(N^2) v (values.len == N^2)
    def get_difference_to_all_values(self, target, values):

        difference = 0
        for value in values:
            difference += abs(value - target)

        return difference

    # O(N^2)
    def acceptable_distance_to_all_filled_values(self, value, position):

        N = self.N

        # O(N^2)
        for row in range(N):
            for col in range(N):
                
                number = self.get_number(row, col)
                if number == 0:
                    continue
                
                difference = abs(value - number)
                distance = self.distance_between_positions(position, (row, col))
                if distance > difference:
                    return False

        return True

    # O(N^2)
    def get_filled_values_dict(self):

        filled_values_dict = {}

        N = board.N
        for row in range(N):
            for col in range(N):
                number = self.get_number(row, col)
                if number != 0:
                    filled_values_dict[number] = (row, col)
        return filled_values_dict

    def to_string(self):
        board_string = ""

        for line in self.lines:
            for number in line:
                board_string += str(number)
                if number != line[-1]:
                    board_string += '\t'
            if line != self.lines[-1]:
                board_string += "\n"
        
        return board_string


class Numbrix(Problem):

    # O(N^2) v
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # O(N^2)
        self.initial = NumbrixState(copy.deepcopy(board))
        self.number_of_actions = 0
        self.last_number_of_actions = float('inf')

    # O(N^2) v (por causa da ordenação inicial de missing_values)
    # actions_incremental
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        missing_values = state.board.missing_values

        # O(N^2)
        number_of_missing_values = len(missing_values)

        # se tabuleiro esta completamente preenchido
        if number_of_missing_values == 0:
            return []

        actions = []
        N = state.board.N
        max = state.board.max

        # O(N^2) (por causa da ordenação inicial de missing_values)
        for missing_value in missing_values: # O(N^2)

            actions = []

            # O(N^2)
            for row in range(N):
                for col in range(N):
                    
                    # O(1)
                    number = state.board.get_number(row, col)
                    if number == 0:
                        
                        # O(1)
                        if self.test_sequence(missing_value, row, col, state):
                            action = self.createAction((row, col), missing_value)
                            actions.append(action)
                            return actions

                        # O(1)
                        horizontal_adjacent = state.board.adjacent_horizontal_numbers(row, col)
                        vertical_adjacent = state.board.adjacent_vertical_numbers(row, col)

                        # O(1)
                        number_of_blank_adjacent_positions = self.get_number_of_blank_adjacent_positions(horizontal_adjacent, vertical_adjacent)
                        if number_of_blank_adjacent_positions == 0 and number != 1 and number != max:
                            if not state.board.at_least_two_adjacent_numbers_are_sequential(missing_value, horizontal_adjacent, vertical_adjacent):
                                continue
                        
                        # O(1)
                        if state.board.at_least_one_adjacent_number_is_sequential(missing_value, horizontal_adjacent, vertical_adjacent):
                            action = self.createAction((row, col), missing_value)
                            actions.append(action)

            if actions != []:
                self.last_number_of_actions = len(actions)
                return actions

        self.last_number_of_actions = len(actions)
        return actions

    # actions_novo
    def actions_(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        missing_values = state.board.missing_values

        # O(N^2)
        filled_values_dict = state.board.get_filled_values_dict()

        # O(1)
        number_of_missing_values = len(missing_values)

        # se tabuleiro esta completamente preenchido
        if number_of_missing_values == 0:
            return []

        actions = []
        N = state.board.N
        max = state.board.max

        # O(N^2) (por causa da ordenação inicial de missing_values)
        for missing_value in missing_values: # O(1) (por causa da ordenação inicial de missing_values)

            actions = []

            # O(1)
            possible_positions = self.get_possible_positions(missing_value, filled_values_dict, state)

            for possible_position in possible_positions: # O(1)
                row = possible_position[0]
                col = possible_position[1]
                
                # O(1)
                if self.test_sequence(missing_value, row, col, state):
                    action = self.createAction((row, col), missing_value)
                    actions.append(action)
                    return actions

                # O(1)
                horizontal_adjacent = state.board.adjacent_horizontal_numbers(row, col)
                vertical_adjacent = state.board.adjacent_vertical_numbers(row, col)

                # O(1)
                number_of_blank_adjacent_positions = self.get_number_of_blank_adjacent_positions(horizontal_adjacent, vertical_adjacent)
                if number_of_blank_adjacent_positions == 0:
                    if not state.board.at_least_two_adjacent_numbers_are_sequential(missing_value, horizontal_adjacent, vertical_adjacent):
                        continue

                # O(N^2)
                if not state.board.acceptable_distance_to_all_filled_values(missing_value, (row, col)):
                    continue
                
                # O(1)
                #if state.board.at_least_one_adjacent_number_is_sequential(missing_value, horizontal_adjacent, vertical_adjacent):
                action = self.createAction((row, col), missing_value)
                actions.append(action)

            if actions != []:
                self.last_number_of_actions = len(actions)
                return actions

        self.last_number_of_actions = len(actions)
        return actions

    # O(1) v
    def get_possible_positions(self, missing_value, filled_values_dict, state):

        board = state.board
        maximum = board.max
        N = board.N
        possible_positions = []

        if missing_value == 1:
            values_to_look_for = [2]
        elif missing_value == max:
            values_to_look_for = [max - 1]
        else:
            values_to_look_for = [missing_value - 1, missing_value + 1]

        for value in values_to_look_for: # O(1)

            if value in filled_values_dict:
                position = filled_values_dict[value]
                row = position[0]
                col = position[1]

                if row - 1 >= 0:
                    number = board.get_number(row - 1, col)
                    if number == 0:
                        possible_positions.append((row - 1, col))
                if col - 1 >= 0:
                    number = board.get_number(row, col - 1)
                    if number == 0:
                        possible_positions.append((row, col - 1))
                if row + 1 < N:
                    number = board.get_number(row + 1, col)
                    if number == 0:
                        possible_positions.append((row + 1, col))
                if col + 1 < N:
                    number = board.get_number(row, col + 1)
                    if number == 0:
                        possible_positions.append((row, col + 1))

        return possible_positions

    # O(1) v
    def test_sequence(self, missing_value, row, col, state):

        N = state.board.N
        max = state.board.max

        if missing_value == 1 or missing_value == max:
            return False

        # esquerda - direita
        if col - 1 >= 0 and col + 1 < N:
            left = state.board.get_number(row, col - 1)
            right = state.board.get_number(row, col + 1)

            # O(1)
            if state.are_sequential(missing_value, left, right):
                return True

        # cima - baixo
        if row - 1 >= 0 and row + 1 < N:
            up = state.board.get_number(row - 1, col)
            down = state.board.get_number(row + 1, col)

            # O(1)
            if state.are_sequential(missing_value, up, down):
                return True

        return False

    # O(N^2) v
    def choose_value(self, choice_values, state):

        # O(N^2)
        filled_values = state.board.get_filled_values()
        
        if len(choice_values) > 0:
            min_value = choice_values[0]

            # O(N^2)
            min_diff = state.board.get_difference_to_all_values(min_value, filled_values)

        # O(N^2) (choice_values.N + filled_values.N <= N^2)
        for value in choice_values:
            this_diff = state.board.get_difference_to_all_values(value, filled_values)
            if this_diff < min_diff:
                min_value = value
                min_diff = this_diff

        return min_value

    # O(1) v
    def createAction(self, position, possibleValue):
        return (position[0], position[1], possibleValue)

    # O(N^2) v
    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """

        row = action[0]
        col = action[1]
        value = action[2]

        # O(N^2) ???
        """ new_state = copy.deepcopy(state) """

        # O(N^2)
        new_board = copy.deepcopy(state.board)

        # O(1)
        new_state = NumbrixState(new_board)

        # O(N^2)
        new_state.set_board_value(row, col, value)

        return new_state

    # O(1) v
    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """

        return state.board.goal_test()

    # O(N^2) v
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """

        # O(N^2)
        return self.heuristic_7(node)

        #return self.heuristic_l(node)

    # O(N^2) v
    def heuristic_7(self, node):

        if node.state.board.impossible_board == True:
            return float('inf')

        number_of_blank_adjacent_positions = 0

        last_changed_position = node.state.board.last_changed_position
        row = last_changed_position[0]
        col = last_changed_position[1]

        # root state
        if last_changed_position == (-1, -1):
            return float('inf')

        # O(1)
        horizontal_numbers = node.state.board.adjacent_horizontal_numbers(row, col)
        vertical_numbers = node.state.board.adjacent_vertical_numbers(row, col)

        # O(1)
        """ number_of_blank_adjacent_positions = self.get_number_of_blank_adjacent_positions(horizontal_numbers, vertical_numbers) """

        # O(N^2)
        if not self.acceptable_distance_to_all_filled_values(node):
            return float('inf')

        # O(N^2)
        compactness = self.get_compactness(node.state)
        # O(N^2)
        #sequentialness = self.get_sequentialness(node.state)
        # O(N^2)
        """ distance = self.distance_from_last_changed_position_to_closest_value(node.state) """
         # O(N^2)
        number_of_sequences = self.get_number_of_sequences(node.state)

        if last_changed_position == (-1, -1):
            return float('inf')

        number_of_missing_values = len(node.state.board.missing_values)
        #return compactness * number_of_blank_adjacent_positions * number_of_missing_values
        #return compactness * number_of_missing_values
        #return compactness * distance / sequentialness
        #return compactness / sequentialness
        return compactness / number_of_sequences
        #return 1 / sequentialness
        #return compactness

    # O(N^2) v
    def heuristic_l(self, node):

        board = node.state.board
        state = node.state
        missing_values = board.missing_values
        number_of_missing_values = len(missing_values)
        last_number_of_actions = self.last_number_of_actions
        number_of_sequences = self.get_number_of_sequences(state)
        #sequentialness = self.get_sequentialness(node.state)
        compactness = self.get_compactness(node.state)

        return number_of_missing_values * last_number_of_actions * compactness / number_of_sequences

    # O(N^2) v
    def get_number_of_sequences(self, state):

        board = state.board
        N = board.N
        Max = board.max
        number_of_sequences = 0

        # O(N^2)
        for row in range(N):
            for col in range(N):

                current_number = board.get_number(row, col)
                if current_number == 0:
                    continue

                horizontal_adjacent = board.adjacent_horizontal_numbers(row, col)
                vertical_adjacent = board.adjacent_vertical_numbers(row, col)
                adjacent = horizontal_adjacent + vertical_adjacent

                if current_number == 1:
                    for number in adjacent:
                        if number == 2:
                            number_of_sequences += 1
                elif current_number == Max:
                    for number in adjacent:
                        if number == Max - 1:
                            number_of_sequences += 1
                else:
                    for number in adjacent:
                        if number == current_number - 1 or number == current_number + 1:
                            number_of_sequences += 1

        if number_of_sequences == 0:
            number_of_sequences = 1

        return number_of_sequences

    # O(N^2) v
    def acceptable_distance_to_all_filled_values(self, node):
        
        N = node.state.board.N
        board = node.state.board
        last_set_value = board.last_set_value
        last_changed_position = board.last_changed_position

        # O(N^2)
        for row in range(N):
            for col in range(N):
                
                number = board.get_number(row, col)
                if number == 0 or number == last_set_value:
                    continue

                difference = abs(last_set_value - number)
                distance = board.distance_between_positions([row, col], last_changed_position)

                if distance > difference:
                    return False
        return True

    # O(N^2) v
    def get_compactness(self, state):

        N = state.board.N
        max = state.board.max
        compactness = 0

        # O(N^2)
        for row in range(N):
            for col in range(N):
                
                number_of_blank_adjacent_positions = 0
                number = state.board.get_number(row, col)
                if number == 0:
                    continue

                # O(1)
                adjacent_horizontal = state.board.adjacent_horizontal_numbers(row, col)
                adjacent_vertical = state.board.adjacent_vertical_numbers(row, col)

                # O(1)
                number_of_blank_adjacent_positions = self.get_number_of_blank_adjacent_positions(adjacent_horizontal, adjacent_vertical)

                # O(1)
                """ if number == 0 and number_of_blank_adjacent_positions == 0:
                    if not state.board.number_1_is_adjacent(adjacent_horizontal, adjacent_vertical):
                        state.board.is_possible = False
                        return state.board.max * 100 """
                if number == 1 or number == max:
                    if not state.board.at_least_one_adjacent_number_is_sequential(number, adjacent_horizontal, adjacent_vertical):
                        state.board.is_possible = False
                        return state.board.max * 100
                if number_of_blank_adjacent_positions == 0:
                    if not state.board.at_least_two_adjacent_numbers_are_sequential(number, adjacent_horizontal, adjacent_vertical):
                        state.board.is_possible = False
                        return state.board.max * 100

                # O(1)
                for value in adjacent_horizontal:
                    if value == 0:
                        compactness += 1
                for value in adjacent_vertical:
                    if value == 0:
                        compactness += 1

        return compactness

    # O(N^2) v
    def get_sequentialness(self, state):

        N = state.board.N
        sequentialness = 0

        # O(N^2)
        for row in range(N):
            for col in range(N):
                
                number = state.board.get_number(row, col)
                if number == 0:
                    continue

                # O(1)
                adjacent_horizontal = state.board.adjacent_horizontal_numbers(row, col)
                adjacent_vertical = state.board.adjacent_vertical_numbers(row, col)

                """ # O(1)
                if number_of_blank_adjacent_positions == 0:
                    if not state.board.at_least_two_adjacent_numbers_are_sequential(number, adjacent_horizontal, adjacent_vertical):
                        state.board.is_possible = False
                        return state.board.max * 100 """

                # O(1)
                for value in adjacent_horizontal:
                    if value != 0 and (value == number + 1 or value == number - 1):
                        sequentialness += 1
                for value in adjacent_vertical:
                    if value != 0 and (value == number + 1 or value == number - 1):
                        sequentialness += 1

        return sequentialness

    # O(N^2)
    """ def distance_from_last_changed_position_to_closest_value(self, state):
        missing_values = state.board.missing_values
        last_set_value = state.board.last_set_value
        last_chaged_position = state.board.last_changed_position
        max = state.board.max
        if len(missing_values) == 0:
            return 0
        
        closest_value = missing_values[0]
        minimum_difference = abs(last_set_value - closest_value)
        # find closest value
        # O(N^2)
        for value in range(1, max + 1):
            if value in missing_values:
                continue
            if abs(value - last_set_value) < minimum_difference:
                minimum_difference = abs(value - last_set_value)
                closest_value = value
        # find position ([row, col]) of closest value
        # O(N^2)
        closest_position = state.board.get_position_by_value(closest_value)
        # get distance
        # O(1)
        distance = state.board.distance_between_positions(last_chaged_position, closest_position)
        return distance """

    # O(1) v
    def get_number_of_blank_adjacent_positions(self, adjacent_horizontal, adjacent_vertical):

        number_of_blank_adjacent_positions = 0
        for number in adjacent_horizontal:
            if number == 0:
                number_of_blank_adjacent_positions += 1
        for number in adjacent_vertical:
            if number == 0:
                number_of_blank_adjacent_positions += 1

        return number_of_blank_adjacent_positions

if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Obter o nome do ficheiro do command line
    input_file = sys.argv[1]
    #input_file = "i1.txt"
    #input_file = "i2.txt"
    #input_file = "i3.txt"
    #input_file = "i4.txt"
    #input_file = "i5.txt"
    #input_file = "tests_final_public/input2.txt"
    
    # Criar board
    board = Board.parse_instance(input_file) 

    # Criar uma instância de Numbrix:
    problem = Numbrix(board)

    # Criar uma instancia de InstrumentedProblem
    #instrumentedProblem = InstrumentedProblem(problem)

    # Comparar estatisticas
    #compare_searchers([problem], "teste", [greedy_search, astar_search])
    #compare_searchers([problem], "teste", [greedy_search, astar_search, recursive_best_first_search])
    #compare_searchers([problem], "teste", [breadth_first_tree_search, depth_first_tree_search, greedy_search, astar_search])

    # Obter o nó solução usando a procura A*:
    #goal_node = breadth_first_tree_search(problem)
    #goal_node = depth_first_tree_search(problem)
    goal_node = greedy_search(problem)
    #goal_node = astar_search(problem)

    # Verificar se foi atingida a solução
    print(goal_node.state.board.to_string())