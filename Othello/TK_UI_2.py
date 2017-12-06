#Christopher Amaya 19164437
import tkinter
import Gamelogic



class UI:

    def __init__ (self,dimensions, player, b_format, gametype):
        self._board = _create_board(dimensions)
        self._Othello = Gamelogic.Iago(self._board,player,b_format,gametype)
        
        self._columns = int(dimensions[1])
        self._rows = int(dimensions[0])

        self._player = player

        self._root_window = tkinter.Toplevel()

        self._info = self._Othello.return_info()
        self._score_text = tkinter.StringVar()
        self._player_text = tkinter.StringVar()
        self._score_text.set('White has {} | Black has {}'.format(self._info[0][0],
                                                                self._info[0][1]))
        if self._info[1] == 'WW': 
            self._player_text.set('Player turn: White'.format(self._info[1]))
        else:
            self._player_text.set('Player turn: Black'.format(self._info[1]))
        
        canvas_ratio = self._rows/self._columns
        if self._rows <= self._columns:
            DEFAULT_FONT = ('Helvetica', 15)
            self._canvas = tkinter.Canvas(
                master = self._root_window,
                width = (350*(1/canvas_ratio)), height = (350),
                background = 'yellow')
        if self._rows > self._columns:
            DEFAULT_FONT = ('Helvetica', 10)
            self._canvas = tkinter.Canvas(
                master = self._root_window,
                width = (175), height = (175*canvas_ratio),
                background = 'blue')
            
        self._canvas.grid(
            row = 2, column = 0, padx=10, pady=0,
            sticky = tkinter.N+ tkinter.S + tkinter.W + tkinter.E)

        info_frame = tkinter.Frame(
            master = self._root_window,background = 'Green')
        info_frame.grid(row = 0, column = 0, rowspan = 2, padx = 1, pady = 0,
                        sticky = tkinter.S)

        info_labelA = tkinter.Label(master = info_frame, textvariable = self._score_text,
                                   font = DEFAULT_FONT)
        info_labelA.grid(row = 0, column = 0)
        info_labelB = tkinter.Label(master = info_frame,
                                    textvariable = self._player_text,
                                    font = DEFAULT_FONT)
        info_labelB.grid(row = 1, column = 0, pady = 5)

        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)


        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()

        self._canvas.bind('<Button-1>', self._on_button_down)
        self._canvas.bind('<Configure>', self._on_canvas_resized)

        self._display(self._rows, self._columns)


    def _display(self,rows:int,columns:int):
        '''displays all necessary components of board'''
        self._draw_pieces(rows,columns)
        self._draw_lines(rows, columns)

    def _on_button_down(self,event:'tkinter'):
        '''When mouse is clicked, this finds coordinates and inputs them
into gamelogic. Gamelogic then accesses.'''

        pixels_per_col = self._canvas_width/self._columns 
        pixels_per_row = self._canvas_height/self._rows

        cell_x = int(event.x/pixels_per_col)
        cell_y = int(event.y/pixels_per_row)

        O_indic = self._Othello.player_input((str(cell_y + 1) +
                                                  ',' + str(cell_x + 1)))
        
        if O_indic[1]:
            self._board = self._Othello.board()
            self._draw_lines(self._rows, self._columns)
            self._draw_pieces(self._rows,self._columns)
            self._player = self._Othello.change_player()
                
            self._info = self._Othello.return_info()
            if self._info[1] == 'WW': 
                self._player_text.set('Player turn: White'.format(self._info[1]))
            else:
                self._player_text.set('Player turn: Black'.format(self._info[1]))

            self._score_text.set(
                'White has {} | Black has {}'.format(self._info[0][0],
                                               self._info[0][1]))
            if not self._Othello.check_moves():
                self._player = self._Othello.change_player()
                if not self._Othello.check_moves():
                    winner = self._Othello.end_game()
                    self._player_text.set('Game Over! {}'.format(winner))
                    
                

        
        
    def _on_canvas_resized(self,event:'tkinter'):
        '''if the canvas is resized, deletes the window and reprints it'''
        self._canvas.delete(tkinter.ALL)
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()
        
        self._display(self._rows,self._columns)
        

    def _draw_pieces(self,rows:int,columns:int):
        '''Using a board, places pieces on the canvas'''
        piece_coor = []
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] == 'WW':
                    h_corner_x = (col/columns) * self._canvas_width
                    h_corner_y = row/rows * self._canvas_height
                    l_corner_x = (col+1)/columns * self._canvas_width
                    l_corner_y = (row+1)/rows * self._canvas_height
                    self._canvas.create_oval(h_corner_x,h_corner_y,
                                             l_corner_x,l_corner_y,
                                             fill = 'white')
                if self._board[row][col] == 'BB':
                    h_corner_x = (col/columns) * self._canvas_width
                    h_corner_y = row/rows * self._canvas_height
                    l_corner_x = (col+1)/columns * self._canvas_width
                    l_corner_y = (row+1)/rows * self._canvas_height
                    self._canvas.create_oval(h_corner_x,h_corner_y,
                                             l_corner_x,l_corner_y,
                                             fill = 'black')
        
    def _draw_lines(self, rows,columns):
        '''Given the dimensions of a board, creates grid'''
        line_coor_x = []
        line_coor_y = []
        for row in range(rows):
            line_coor_y.append(row/rows)
        for column in range(columns):
            line_coor_x.append(column/columns)
        for x in line_coor_x:
            x_abs = x * self._canvas_width
            self._canvas.create_line(x_abs,0,x_abs,self._canvas_height,
                                     fill = 'black')                       
        for y in line_coor_y:
            y_abs = y * self._canvas_height
            self._canvas.create_line(0,y_abs,self._canvas_width,y_abs,
                                     fill = 'black') 
        
        
    def show(self):
        '''Gives control to this window'''
        self._root_window.grab_set()
        self._root_window.wait_window()
        
        
def _create_board(size:(str)) -> 'board':
    '''creates a basic board layout'''
      
    board = []
    for i in range(int(size[0])):
        board.append([])
        for j in range(int(size[1])):
            board[i].append(j+1)
    return board
