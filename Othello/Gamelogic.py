# Christopher Amaya 19164437
import copy

#########
##CLASS##
#########

class Iago:
    def __init__(self, board, player,b_format, gametype):
        self._board = board
        self._player = player
        self._dimensions = _dimensions(self._board)
        self._board = _board_format(self._board,b_format,self._dimensions)
        self._turn_indic = False
        self._gametype = gametype
        if self._turn_indic:
            _make_opposite(self._player)
              
    def board(self):
        '''Returns the board to be accessed by some menu
        '''
        return self._board

    def player_input(self,coor:tuple)->tuple:
        '''Takes in some coordinates representing a move and manages
how the board reactes to the move. Retruns message and boolean statement
signifying if it is an error or not
        '''


        try:

            coor = str.split(coor,',')
            if not len(coor) == 2:
                return ('Your input is formatted incorrectly',False)
            row = (int(coor[0]))-1
            col = (int(coor[1]))-1
            check = _check_inputs(self._board,(row,col),self._player,self._dimensions)
            if not check[1]:
                return ('that is an invalid move',False)
            check[0][row][col] = self._player
            self._board = check[0]
            return ('',True)

        except:
            return('There is something wrong with your submission',False)

            
    def change_player(self):
        '''Switches the player in the class
        '''
        self._player = _make_opposite(self._player)

    def check_moves(self)->bool:
        '''Goes through every single combination of moves and determines
if it is possible to continue         '''
        board_copy = copy.deepcopy(self._board)
        for i in range(self._dimensions[0]):
            for j in range(self._dimensions[1]):
                check = _check_inputs(board_copy,[i,j],self._player,self._dimensions)[1]
                if check:
                    return True
        return False

    def return_info(self)->tuple:
        '''Returns the total score and player turn
        '''
        return(_score(self._board),self._player)
        

    def end_game(self):
        '''Given a triggering event, prints the results of the game
        '''
        score = _score(self._board)
        winner = 'BLAH'
        self._player = 'END'
        if self._gametype == 'M':
            if score[0]>score[1]:
                winner = 'White wins!'
            if score[1]>score[0]:
                winner = 'Black wins!'
            if score[1] == score [0]:
                winner = 'Tie!'
                return winner
        if self._gametype == 'L':
            if score[0]<score[1]:
                winner = 'White wins!'
            if score[1]<score[0]:
                winner = 'Black wins!'
            if score[1] == score [0]:
                winner = 'Tie!'
                return winner
        return winner


####################
##HELPER FUNCTIONS##
####################

def _board_format(board,s_player,dim)->'board':
    '''Creates the starting position of the board'''
    h_row = int(dim[0]/2)
    h_col = int(dim[1]/2)
    opp_player = _make_opposite(s_player)
    board[h_row-1][h_col-1] = s_player
    board[h_row][h_col] = s_player
    board[h_row-1][h_col] = opp_player
    board[h_row][h_col-1] = opp_player
    return board

def _check_inputs(board,coor,p_turn,dimensions)->tuple:
    '''Takes inputs and changes board direction by direction'''
    UP = True
    LEFT = True
    DOWN = True
    RIGHT = True
    b_stor = copy.deepcopy(board)
    if board[coor[0]][coor[1]] == 'WW' or board[coor[0]][coor[1]] == 'BB':
        return (board, False)
    if coor[1] == 0:
        LEFT = False
        
    if coor[1] == (dimensions[1]-1):
        RIGHT == False

    if coor[0] == 0:
        UP = False

    if coor[0] == (dimensions[0]-1):
        DOWN = False

    if LEFT:
        board = _base_adder(coor,0,-1,board,p_turn)

    if RIGHT:
        board = _base_adder(coor,0,1,board,p_turn)

    if UP:
        board = _base_adder(coor,-1,0,board,p_turn)

    if DOWN:
        board = _base_adder(coor,1,0,board,p_turn)

    if LEFT and UP:
        board = _base_adder(coor,-1,-1,board,p_turn)

    if LEFT and DOWN:
        board = _base_adder(coor,1,-1,board,p_turn)
    
    if RIGHT and UP:
        board = _base_adder(coor,-1,1,board,p_turn)
    
    if RIGHT and DOWN:
        board = _base_adder(coor,1,1,board,p_turn)

    if board == b_stor:
        return (board, False)
    
    return (board,True)

def _base_adder(coor,row_adder,col_adder,board,p_turn):
    '''Using directional adders, manages logic that changes the board'''
    try:
        board_copy = copy.deepcopy(board)
        opp_p = _make_opposite(p_turn)
        new_row = coor[0]+row_adder
        new_col = coor[1]+col_adder
        if not board[new_row][new_col] == opp_p:
            return board
        board_copy[new_row][new_col] = p_turn
        while True:
            new_row += row_adder
            new_col += col_adder
            if new_row < 0 or new_col < 0:
                return board
            if board[new_row][new_col] == p_turn:
                board = board_copy
                return board
            if board[new_row][new_col] == opp_p:
                board_copy[new_row][new_col] = p_turn
            if (not board[new_row][new_col] == opp_p) and (not board[new_row][new_col] == p_turn):
                return board               

    except IndexError:
        return board



def _make_opposite(p_turn:str)->str:
    '''Function outside class that changes the turn'''
    if p_turn == 'WW':
        return 'BB'
    if p_turn == 'BB':
        return 'WW'
        
    
def _dimensions(board)->list:
    '''returns dimensions of a board'''
    rows = len(board)
    columns = len(board[0])
    return [rows,columns]

def _score(board)->tuple:
    '''returns the score of a game'''
    WW = 0
    BB = 0
    for row in board:
        for col in row:
            if col == 'WW':
                WW += 1
            if col == 'BB':
                BB += 1
    return(WW,BB)



