import random
import itertools
import collections
import time

class Node:
    """
    A class representing an Solver node
    - 'puzzle' is a Puzzle instance
    - 'parent' is the preceding node generated by the solver, if any
    - 'action' is the action taken to produce puzzle, if any
    """
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle #initialize the local properties
        self.parent = parent 
        self.action = action

	
    def setCost(self):  #compute the number of tiles out of placedef setCost(self):
        #cost as h2
        i = 0
        j = 0
        cost = 0
        procPuzzle = []
        procPuzzle.append(str(self.puzzle)[0:3]) #create the matrix through a series of string taken by self.puzzle
        procPuzzle.append(str(self.puzzle)[3:6])
        procPuzzle.append(str(self.puzzle)[6:9])

        # solPuzzle: 0 = 3,3,= 1,1 etc
        solPuzzle = [ [2,2] , [0,0] , [0,1] , [0,2] , [1,0] , [1,1] , [1,2], [2,0] , [2,1]]

        while i < 3:
            j = 0
            while j < 3:
                x = solPuzzle[int(procPuzzle[i][j])][0]
                y = solPuzzle[int(procPuzzle[i][j])][1]
                cost = abs(i - x) + abs(j - y) + cost # cost = manhattan distance
                j = j + 1
            i = i + 1
        self.cost = cost
        
    @property #assosiate the name of a property to its getter and setter method
    def state(self):
        """
        Return a hashable representation of self
        ritorna lo stato attuale della matrice
        """
        return str(self)

    @property 
    def path(self):
        """
        Reconstruct a path from to the root 'parent'
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        """ Wrapper to check if 'puzzle' is solved """
        return self.puzzle.solved

    @property
    def actions(self):
        """ Wrapper for 'actions' accessible at current state """
        return self.puzzle.actions

    def __str__(self):
        return str(self.puzzle)
		
	

class Solver:
    """
    An '8-puzzle' solver
    - 'start' is a Puzzle instance
    """
    def __init__(self, start):
        self.start = start

    def sortByCost(self, queue, child): #method to sort by cost the queue
        i = 0
        while i < len(queue):
            if queue != []:
                if child.cost <= queue[i].cost:
                    queue.insert(i, child)
                    print(len(queue), " \t ", self.stepcount)
                    return queue
                i = i+1
        print(len(queue), " \t " , self.stepcount)
        queue.append(child)
        return queue

    def solve(self):
        """
        Perform breadth first search and return a path
        to the solution, if it exists 
        """
        self.stepcount = 0
        queue = collections.deque([Node(self.start)]) #initialize the OPEN list
        seen  = set()  #initialize the CLOSED list
        seen.add(queue[0].state)
        while queue:
            node = queue.popleft()
            self.stepcount = self.stepcount + 1
            if node.solved:
                return node.path #return the list of all the moves made to get solutions

            for move, action in node.actions:  # node.actions returns a list of objects
                child = Node(move(), node, action)
                child.setCost()
                if child.state not in seen:
                    queue = self.sortByCost(queue, child) #add the unseen states in queue ordered by cost
                    seen.add(child.state)

class Puzzle:
    """
    A class representing an '8-puzzle'.
    - 'board' should be a square list of lists with integer entries 0...width^2 - 1
       e.g. [[1,2,3],[4,0,6],[7,5,8]]
    """
    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        """
        The puzzle is solved if the flattened board's numbers are in
        increasing order from left to right and the '0' tile is in the
        last position on the board
        """
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property 
    def actions(self):
        """
        Return a list of 'move', 'action' pairs. 'move' can be called
        to return a new puzzle that results in sliding the '0' tile in
        the direction of 'action'.
        """
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'R':(i, j-1),
                      'L':(i, j+1),
                      'D':(i-1, j),
                      'U':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    def shuffle(self):
        """
        Return a new puzzle that has been shuffled with 1000 random moves
        """
        puzzle = self
        for _ in range(1000):
            puzzle = random.choice(puzzle.actions)[0]() #shuffle is used to generate random moves and states
        return puzzle

    def copy(self):
        """
        Return a new puzzle with the same board as 'self'
        """
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        """
        Return a new puzzle where 'at' and 'to' tiles have been swapped.
        NOTE: all moves should be 'actions' that have been executed
        """
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j] # the  move is done by using a copy of the current state
        return copy

    def pprint(self):
        for row in self.board: #print the rows
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self)) #not actual used in this code

    def __iter__(self):
        for row in self.board: #not actual used in this code
            yield from row


# example of use
board = [[1,2,3],[4,0,6],[7,5,8]]

puzzle = Puzzle(board)
puzzle = puzzle.shuffle() #shuffle = mescolamento

start = time.time()

s = Solver(puzzle)
p = s.solve()

for node in p:
    print(node.action)
    node.puzzle.pprint()



done = time.time()
elapsed = done - start
print("Time elapsed: ", elapsed)
print("Steps done: ", s.stepcount)


x = input("bye")
