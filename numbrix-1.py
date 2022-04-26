# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, \
    recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, board):
        self.N = len(board)
        self.board = board

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        res = [None, None]
        if row < self.N - 1:
            res[0] = self.board[row + 1][col]
        if row > 0:
            res[1] = self.board[row - 1][col]

        return tuple(res)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        res = [None, None]
        if col > 0:
            res[0] = self.board[row][col - 1]
        if col < self.N - 1:
            res[1] = self.board[row][col + 1]

        return tuple(res)

    @staticmethod
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        with open(filename, "r") as fp:
            N = int(fp.readline())
            board = []
            for i in range(N):
                line = fp.readline()[:-1]
                new_row = list(map(lambda x: int(x), line.split('\t')))
                board.append(new_row)

        return Board(board)

    # TODO: outros metodos da classe
    def to_string(self):
        res = ""
        for i in range(self.N):
            res = res + '\t'.join([str(x) for x in self.board[i]]) + '\n'
        return res

    def set_number(self, row: int, col: int, val: int):
        """ Devolve o valor na respetiva posição do tabuleiro. """
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] == val:
                    return
        if self.board[row][col] == 0:
            self.board[row][col] = val

    def copy(self):
        board = []
        for row in self.board:
            board.append(row.copy())
        return Board(board)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        initial = NumbrixState(board)
        super().__init__(initial)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []
        done = []
        done_coords = []
 
        for i in range(state.board.N):  # Get filled positions, basically
            for j in range(state.board.N):
                curr = state.board.get_number(i, j)
                if curr != 0:
                    done.append(curr)
                    done_coords.append((i, j))

        for (i, j) in done_coords: 
            curr = state.board.get_number(i, j)
            poss = [x for x in range(curr - 1, curr + 2) if 0 < x <= state.board.N ** 2 and x not in done]
            adj = state.board.adjacent_horizontal_numbers(i, j)
            if adj[0] == 0:
                for p in poss:
                    actions.append((i, j - 1, p))
            if adj[1] == 0:
                for p in poss:
                    actions.append((i, j + 1, p))
            adj = state.board.adjacent_vertical_numbers(i, j)
            if adj[0] == 0:
                for p in poss:
                    actions.append((i + 1, j, p))
            if adj[1] == 0:
                for p in poss:
                    actions.append((i - 1, j, p))
        print("Possible actions are " + str(actions))
        return set(actions)

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        board: Board = state.board.copy()
        board.set_number(*action)
        print(board.to_string())
        return NumbrixState(board)

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        for i in range(state.board.N):
            for j in range(state.board.N):
                flags = [False, False]
                curr = state.board.get_number(i, j)
                adj = list(state.board.adjacent_horizontal_numbers(i, j)) + list(
                    state.board.adjacent_vertical_numbers(i, j))
                for a in adj:
                    if a is None:
                        continue
                    if curr - a == 1:
                        flags[0] = True
                    if a - curr == 1:
                        flags[1] = True
                if not ((flags[0] or curr == 1) and (flags[1] or curr == state.board.N ** 2)):
                    return False

        return True

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        h = 0
        board = node.state.board
        N = board.N
        for i in range(N):
            for j in range(N):
                curr = board.get_number(i, j)
                if curr == 0:
                    continue
                adj = list(board.adjacent_horizontal_numbers(i, j)) + list(board.adjacent_vertical_numbers(i, j))
                if curr + 1 in adj and curr + 1 <= N ** 2:
                    h += 1
                if curr - 1 in adj and curr > 0:
                    h += 1
                if h == 2:
                    a = 1

        return 2 * board.N**2 - h

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance(sys.argv[1])  # Criar uma instância de Numbrix:
    problem = Numbrix(board)
    # Criar um estado com a configuração inicial:
    s0 = NumbrixState(board)
    print("Initial:\n", s0.board.to_string(), sep="")
    # Usar uma técnica de procura para resolver a instância,
    node = astar_search(problem)
    # Retirar a solução a partir do nó resultante,
    solution_board = node.state.board
    # Imprimir para o standard output no formato indicado.
    print("Solution:\n", solution_board.to_string(), sep="")
