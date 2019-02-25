from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        output1 = []
        output2 = []
        output3 = []

        disks1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1'))
        disks2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2'))
        disks3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3'))

        if disks1:
            for disks in disks1:
                output1.append(int(str(disks.bindings[0].constant)[-1]))
        if disks2:
            for disks in disks2:
                output2.append(int(str(disks.bindings[0].constant)[-1]))
        if disks3:
            for disks in disks3:
                output3.append(int(str(disks.bindings[0].constant)[-1]))

        output1.sort()
        output2.sort()
        output3.sort()

        gs_hanoi = (tuple(output1), tuple(output2), tuple(output3))

        return gs_hanoi



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        game_state = self.getGameState()
        disk =  str(movable_statement.terms[0].term)
        init_peg = str(movable_statement.terms[1].term)
        init_peg_num = int(init_peg[-1])
        target_peg = str(movable_statement.terms[2].term)
        target_peg_num = int(target_peg[-1])

        if len(game_state[target_peg_num - 1]) > 0:
            self.kb.kb_retract(parse_input('fact: (top disk' + str(game_state[target_peg_num - 1][0]) + ' ' + target_peg + ')'))
        else:
            self.kb.kb_retract(parse_input('fact: (empty ' + target_peg + ')'))

        self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + init_peg + ')'))
        self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + init_peg + ')'))
        self.kb.kb_add(parse_input('fact: (on ' + disk + ' ' + target_peg + ')'))
        self.kb.kb_add(parse_input('fact: (top ' + disk + ' ' + target_peg + ')'))

        if len(game_state[init_peg_num - 1]) <= 1:
            self.kb.kb_add(parse_input('fact: (empty ' + init_peg + ')'))

        else:
            self.kb.kb_add(
                parse_input('fact: (top disk' + str(game_state[init_peg_num - 1][1]) + ' ' + init_peg + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        currentstate= [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        positions = {"pos1": ("pos1", "pos2", "pos3"),
                "pos2": ("pos1", "pos2", "pos3"),
                "pos3": ("pos1", "pos2", "pos3")}

        for ys in positions:
            y = int(ys[3]) - 1
            for xs in positions[ys]:
                x = int(xs[3]) - 1
                ask = self.kb.kb_ask(Fact(Statement(["coordinate", "?tile", xs, ys])))[0]
                tile = ask.bindings_dict["?tile"][4]
                tile_val = 0
                if tile == 'y':
                    tile_val = -1
                else:
                    tile_val = int(tile)
                currentstate[y][x] = tile_val

        return tuple([tuple(currentstate[0]), tuple(currentstate[1]), tuple(currentstate[2])])
        
    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        tile = str(movable_statement.terms[0].term)
        x = str(movable_statement.terms[1].term)
        y =  str(movable_statement.terms[2].term)
        targetx =  str(movable_statement.terms[3].term)
        targety =  str(movable_statement.terms[4].term)

        self.kb.kb_retract(parse_input('fact: (coordinate ' + tile + ' ' + x + ' ' + y + ')'))
        self.kb.kb_retract(parse_input('fact: (coordinate empty ' + targetx + ' ' + targety + ')'))
        self.kb.kb_add(parse_input('fact: (coordinate empty ' + x + ' ' + y + ')'))
        self.kb.kb_add(parse_input('fact: (coordinate ' + tile + ' ' + targetx + ' ' + targety + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
