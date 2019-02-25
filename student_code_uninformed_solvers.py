
from solver import *
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        dfsflag = True
        movables = self.gm.getMovables()


        if self.currentState.state == self.victoryCondition:
            return True

        if movables and not self.currentState.children:
            for move in movables:
                self.gm.makeMove(move)
                newstate = self.gm.getGameState()
                if self.currentState.parent and newstate == self.currentState.parent.state:
                    self.gm.reverseMove(move)
                else:
                    newstate = GameState(newstate, self.currentState.depth + 1, move)
                    newstate.parent = self.currentState
                    self.currentState.children.append(newstate)
                    self.gm.reverseMove(move)

        if movables and self.currentState.children:
            while dfsflag == True:
                if not self.currentState.parent and self.currentState.nextChildToVisit == len(self.currentState.children):
                    dfsflag = False

                if self.currentState.nextChildToVisit >= len(self.currentState.children):
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                    continue

                else:
                    if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                        self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
                        self.currentState.parent.nextChildToVisit = self.currentState.parent.nextChildToVisit + 1
                        self.visited[self.currentState] = True
                        self.gm.makeMove(self.currentState.requiredMovable)
                        dfsflag = False
                    else:
                        self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
                        continue
        return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        newsteps = []

        if self.currentState.state == self.victoryCondition:
            return True
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True

        while True:
            movables = self.gm.getMovables()
            if movables and not self.currentState.children:
                for move in movables:
                    self.gm.makeMove(move)
                    newstate = self.gm.getGameState()
                    if self.currentState.parent and newstate == self.currentState.parent.state:
                        self.gm.reverseMove(move)
                        continue
                    else:
                        newstate = GameState(newstate, self.currentState.depth + 1, move)
                        newstate.parent = self.currentState
                        self.currentState.children.append(newstate)
                        self.queue.put(newstate)
                        self.gm.reverseMove(move)

            nextup = self.queue.get()
            if nextup in self.visited:
                continue

            while nextup.requiredMovable:
                newsteps.append(nextup.requiredMovable)
                nextup = nextup.parent
            while self.currentState.requiredMovable:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
            while newsteps:
                move = newsteps.pop()
                self.gm.makeMove(move)
                newstate = self.gm.getGameState()
                for child in self.currentState.children:
                    if child.state == newstate:
                        self.currentState = child
                        self.visited[self.currentState] = True
                        break
            break

        return False