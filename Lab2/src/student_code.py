import random
import konane
import copy
import sys

# class for individual player.
# student and grader players should be identical except for:
#     - implementation of getMinimaxMove() and getAlphabetaMove(), and
#     - any helper functions and/or members implemented by student


class player:
    def __init__(self, b, s, depth, algo):
        self.b = b                  # board to be played for test
        self.s = s                  # save 'x' or 'o' designation
        # maximum depth for search (in number fo plies)
        self.depth = depth
        self.algo = algo            # name of algorithm for player
        # helper variable for first/last deterministic player algo
        self.prior_move = 'L'

    # should not be needed for autograder, but include to help development
    def makeFirstMove(self, r, c):
        self.b.firstMove(self.s, r, c)

    # returns list of available moves for player as list of
    # [[x_from][y_from],[x_to][y_to]] items
    def getNextMoves(self):
        return(self.b.possibleNextMoves(self.s))

    # makes move specified by move expressed as [[x_from][y_from],[x_to][y_to]]
    def makeNextMove(self, move):
        self.b.nextMove(self.s, move)

    ######
    # next few methods get the next move for each of the available algorithms

    # get the first move of the list of available moves
    def getFirstMove(self):
        moves = self.b.possibleNextMoves(self.s)
        return moves[0]

    # alternative between taking the first and last available move
    def getFirstLastMove(self):
        moves = self.b.possibleNextMoves(self.s)
        if self.prior_move == 'L':
            move = moves[0]
            self.prior_move = 'F'
        else:
            move = moves[len(moves) - 1]
            self.prior_move = 'L'
        return move

    # randomly choose one of the available moves
    def getRandomMove(self):
        moves = self.b.possibleNextMoves(self.s)
        selected = random.randint(0, len(moves) - 1)
        return moves[selected]

    # ask a human player for a move
    def getHumanMove(self):
        print "Possible moves:", self.b.possibleNextMoves(self.s)
        origin = self._promptForPoint(
            "Choose a piece to move (in the format 'row column'): ")
        destination = self._promptForPoint(
            "Choose a destination for (%s, %s) -> " % (origin[0], origin[1]))
        if (origin, destination) in self.b.possibleNextMoves(self.s):
            return (origin, destination)
        else:
            print "Invalid move.", (origin, destination)
            return self.getHumanMove()

    # help for prompting human player
    def _promptForPoint(self, prompt):
        raw = raw_input(prompt)
        (r, c) = raw.split()
        return (int(r), int(c))

    # minimax algorithm to be completed by students
    # note: you may add parameters to this function call
    def getMinimaxMove(self):
        return self.minimaxHelper(self.depth, self.b, True, self.s)[0]

    def minimaxHelper(self, depth, board, maxP, currentPlayer):
        # Available moves for current player this turn
        availableMoves = board.possibleNextMoves(currentPlayer)

        # Judge if Depth == 0 and if there's available moves.
        # If at least 1 is true then:
        if depth is 0 or len(availableMoves) is 0:
            # only return heuristic
            return None, self.heuristic(board, self)

        best = (sys.maxint, -sys.maxint - 1)[maxP]
        bestMv = None

        # judge every nodes possible, select the biggest/smallest one

        newMove = (None, None)

        for mv in availableMoves:

            # restore changes
            if newMove[0] is not None:
                self.restoreMove(board, newMove[0], newMove[1], currentPlayer)

            # save new changes
            newMove = (mv[0], mv[len(mv) - 1])

            board.nextMove(currentPlayer, mv)
            _, v = self.minimaxHelper(
                depth - 1, board, not maxP, self.opposite(currentPlayer))

            bestMv, best = (
                ((bestMv, best), (mv, v))[v < best],
                ((bestMv, best), (mv, v))[v > best]
            )[maxP]

        self.restoreMove(board, newMove[0], newMove[1], currentPlayer)

        return bestMv, best

    def restoreMove(self, board, start, stop, currentPlayer):
        if start[0] - stop[0] == 0:
            direction = (0, (stop[1] - start[1]) / abs(stop[1] - start[1]))
        else:
            direction = ((stop[0] - start[0]) / abs(stop[0] - start[0]), 0)
        step = (start[0] + direction[0], start[1] + direction[1])
        board.state[start[0]][start[1]] = currentPlayer
        board.state[stop[0]][stop[1]] = ' '

        while (step[0] - stop[0]) * direction[0] +\
                (step[1] - stop[1]) * direction[1] < 0:
            board.state[step[0]][step[1]] = self.opposite(currentPlayer)
            step = (step[0] + direction[0] * 2,
                    step[1] + direction[1] * 2)

    def printCurrentInfo(self, depth, h, move):
        s = ""
        for i in range(self.depth - depth):
            s += "\t"
        print s, "depth:, ", self.depth - depth, " h: ", h, " move: ", move

    # alphabeta algorithm to be completed by students
    # note: you may add parameters to this function call
    def getAlphaBetaMove(self):
        return self.alphaBetaHelper(
            self.depth, self.b, True, self.s, -sys.maxint - 1, sys.maxint)[0]

    def alphaBetaHelper(self, depth, board, maxP, currentPlayer, alpha, beta):
        # Available moves for current player this turn
        availableMoves = board.possibleNextMoves(currentPlayer)

        # Judge if Depth == 0 and if there's available moves.
        # If at least 1 is true then:
        if depth is 0 or len(availableMoves) is 0:
            # only return heuristic
            # self.printCurrentInfo(depth, self.heuristic(board, self), None)
            return None, self.heuristic(board, self)

        best = (sys.maxint, -sys.maxint - 1)[maxP]
        bestMv = None

        newMove = (None, None)

        # judge every nodes possible, select the biggest/smallest one
        for mv in availableMoves:

            # restore changes
            if newMove[0] is not None:
                self.restoreMove(board, newMove[0], newMove[1], currentPlayer)

            # save new changes
            newMove = (mv[0], mv[len(mv) - 1])

            board.nextMove(currentPlayer, mv)
            _, v = self.alphaBetaHelper(
                depth - 1, board, not maxP,
                self.opposite(currentPlayer), alpha, beta)

            bestMv, best = (
                ((bestMv, best), (mv, v))[v < best],
                ((bestMv, best), (mv, v))[v > best]
            )[maxP]

            # self.printCurrentInfo(depth, best, mv)

            if maxP:
                alpha = (alpha, best)[alpha <= best]
            else:
                beta = (beta, best)[beta >= best]
            if beta <= alpha:
                break

        self.restoreMove(board, newMove[0], newMove[1], currentPlayer)

        return bestMv, best

    def opposite(self, s):
        if s == 'x':
            return 'o'
        else:
            return 'x'

    def heuristic(self, board, player):
        score = len(board.possibleNextMoves(self.s)) - \
            len(board.possibleNextMoves(self.opposite(self.s))) + \
            int(board.state[0][0] == self.s) + \
            int(board.state[0][board.size - 1] == self.s) + \
            int(board.state[board.size - 1][0] == self.s) + \
            int(board.state[board.size - 1][board.size - 1] == self.s)
        # print "heuristic", board, player, score
        return score

    # member function called by test() which specifies move
    # to be made for player's turn, with move
    # expressed as [[x_from][y_from],[x_to][y_to]]
    # if no moves available, return Python 'None' value
    def takeTurn(self):
        moves = self.b.possibleNextMoves(self.s)

        # return Python 'None' if no moves available
        if len(moves) == 0:
            return [True, None]

        if self.algo == 'First Move':  # select first avaliable move
            move = self.getFirstMove()

        if self.algo == 'First/Last Move':  # alternate first and last moves
            move = self.getFirstLastMove()

        # select random move Note: not determinisic, just used to exercise code
        if self.algo == 'Random':
            move = self.getRandomMove()

        # player must select best move based upon MiniMax algorithm
        if self.algo == 'MiniMax':
            move = self.getMinimaxMove()

        # player must select best move based upon AlphaBeta algorithm
        if self.algo == 'AlphaBeta':
            move = self.getAlphaBetaMove()

        if self.algo == 'Human':
            move = self.getHumanMove()

        # makes move on board being used for evaluation
        self.makeNextMove(move)
        return [False, move]
