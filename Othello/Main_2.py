#Christopher Amaya 19164437
import tkinter
import TK_UI_2 as TK_UI

DEFAULT_TEXT = ('Helvetica', 15)
    

class Dialog():
    def __init__(self):
        self._row = '4'
        self._col = '4'
        self._count = 0
        self._count_col = 0
        self._increment = tkinter.StringVar()
        self._increment.set('4')
        self._increment_col = tkinter.StringVar()
        self._increment_col.set('4')
        self._dialog_window = tkinter.Toplevel()
        self._dialog_window.columnconfigure(1,weight = 1)
        self._condition = None

        row_label = tkinter.Label(
            master = self._dialog_window,
            text = "How many rows will the board have?", font = DEFAULT_TEXT)

        row_label.grid(
            row = 0, column = 0, padx = 10,
            pady = 10, sticky = tkinter.W)

        button_frame = tkinter.Frame(master = self._dialog_window)
        button_frame.grid(
            row = 0, column = 1, padx =10, pady =10, sticky  = tkinter.W)
        button_up = tkinter.Button(
            master = button_frame, text = '>', font = DEFAULT_TEXT,
            command = self._on_button_up)
        button_up.grid(
            row = 0, column = 2, padx=10, sticky = tkinter.W)
        button_down = tkinter.Button(
            master = button_frame, text = '<', font = DEFAULT_TEXT,
            command = self._on_button_down)
        button_down.grid(
            row = 0, column = 0, padx = 10, sticky = tkinter.W + tkinter.E)
        self._butt_label = tkinter.Label(
            master = button_frame, textvariable = self._increment,
            font = DEFAULT_TEXT)
        self._butt_label.grid(
            row = 0, column = 1, sticky = tkinter.W)      
        
#################################################################################
        
        col_label = tkinter.Label(
            master = self._dialog_window,
            text = "How many columns will the board have?",
            font = DEFAULT_TEXT)

        col_label.grid(
            row = 1, column = 0, padx = 10,
            pady = 10, sticky = tkinter.W)


        button_frame_col = tkinter.Frame(master = self._dialog_window)
        button_frame_col.grid(
            row = 1, column = 1, padx =10, pady =10, sticky  = tkinter.W)
        button_up = tkinter.Button(
            master = button_frame_col, text = '>', font = DEFAULT_TEXT,
            command = self._on_button_up_col)
        button_up.grid(
            row = 0, column = 2, padx=10, sticky = tkinter.W)
        button_down = tkinter.Button(
            master = button_frame_col, text = '<', font = DEFAULT_TEXT,
            command = self._on_button_down_col)
        button_down.grid(
            row = 0, column = 0, padx = 10, sticky = tkinter.W + tkinter.E)
        self._butt_label = tkinter.Label(
            master = button_frame_col, textvariable = self._increment_col,
            font = DEFAULT_TEXT)
        self._butt_label.grid(
            row = 0, column = 1, sticky = tkinter.W)  

################################################################################
        player_label = tkinter.Label(
            master = self._dialog_window,
            text = "Who will go first?\nInput 'WW' for White, and 'BB' for Black",
            font = DEFAULT_TEXT)

        player_label.grid(
            row = 2, column = 0, padx = 10,
            pady = 10, sticky = tkinter.W)

        self._player = tkinter.Entry(
            master = self._dialog_window, width = 5,
            font = DEFAULT_TEXT)

        self._player.grid(
            row = 2, column = 1, padx = 10, pady = 10,
            sticky =  tkinter.W + tkinter.E)
        
#################################################################################

        format_label = tkinter.Label(
            master = self._dialog_window,
            text = "Who will have the corner piece?\n Input 'WW' for white, and 'BB' for black",
            font = DEFAULT_TEXT)

        format_label.grid(
            row = 3, column = 0, padx = 10,
            pady = 10, sticky = tkinter.W)

        self._format = tkinter.Entry(
            master = self._dialog_window, width = 5,
            font = DEFAULT_TEXT)

        self._format.grid(
            row = 3, column = 1, padx = 10, pady = 10,
            sticky =  tkinter.W + tkinter.E)
        
#################################################################################
        type_label = tkinter.Label(
            master = self._dialog_window,
            text = "Winner has the most or least points?\n Input 'M' for most and 'L' for least",
            font = DEFAULT_TEXT)

        type_label.grid(
            row = 4, column = 0, padx = 10,
            pady = 10, sticky = tkinter.W)

        self._type = tkinter.Entry(
            master = self._dialog_window, width = 5,
            font = DEFAULT_TEXT)

        self._type.grid(
            row = 4, column = 1, padx = 10, pady = 10,
            sticky =  tkinter.W + tkinter.E)
        
#################################################################################


        start_butt = tkinter.Button(
            master = self._dialog_window, text = 'Game on!',
            font = DEFAULT_TEXT, command = self._on_start_butt)
        start_butt.grid(row = 5, column = 1, columnspan = 1,
                        padx = 10, pady = 10, sticky = tkinter.W)
        self._info = []

        
    def show(self):
        '''Running this keeps dialog in control'''

        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def _on_start_butt(self):
        '''Connected to start button. Stores all information gathered
then destroys the window'''
        self._info = [(self._row,self._col),
                       self._player.get(),self._format.get(),self._type.get()]
        self._condition = _check_components(self._info)
        self._dialog_window.destroy()

    def _condition_state(self)->bool:
        '''activates if there is an error. False if error, true if not'''
        return self._condition

    def _get_info(self)->list:
        '''returns a list of all the inputs gotten from the entries'''
        return self._info

    def _on_button_up(self):
        '''when mouse clicks on this button, rotates self._row through
a set of values upward'''
        self._count += 1
        button_list = ['4','6','8','10','12','14','16']
        self._row = button_list[self._count % 7]
        self._increment.set((str(self._row)))

    def _on_button_down(self):
        '''when mouse clicks on this button, rotates self._row through
a set of values downward'''
        self._count -= 1
        button_list = ['4','6','8','10','12','14','16']
        self._row = button_list[self._count % 7]
        self._increment.set(str(self._row))
        

    def _on_button_up_col(self):
        '''when mouse clicks on this button, rotates self._col through
a set of values upward'''
        self._count_col += 1
        button_list = ['4','6','8','10','12','14','16']
        self._col = button_list[self._count_col % 7]
        self._increment_col.set(str(self._col))

    def _on_button_down_col(self):
        '''when mouse clicks on this button, rotates self._col through
a set of values downward'''
        self._count_col -= 1
        button_list = ['4','6','8','10','12','14','16']
        self._col = button_list[self._count_col % 7]
        self._increment_col.set(str(self._col))

####################################################################

class Othello_App:
    def __init__(self):

        self._start_window = tkinter.Tk()

        self._start_text = tkinter.StringVar()
        self._start_text.set('WELCOME TO OTHELLO!')

        self._butt_text = tkinter.StringVar()
        self._butt_text.set('START')


        start_label = tkinter.Label(
            master = self._start_window, textvariable = self._start_text,
            font = DEFAULT_TEXT)

        start_label.grid(row = 0, column = 0, padx = 10, pady = 10,
                         sticky = tkinter.S)

        butt_frame = tkinter.Frame(master = self._start_window)
        butt_frame.grid( row = 1, column = 0, padx=10, pady =10,sticky = tkinter.N)

        start_butt = tkinter.Button(
            master = butt_frame, textvariable = self._butt_text,
            font = DEFAULT_TEXT,command = self._on_start)
        start_butt.grid(row = 0, column = 0)

        cancel_butt = tkinter.Button(
            master = butt_frame, text = 'CANCEL', font = DEFAULT_TEXT,
            command = self._on_cancel)
        cancel_butt.grid(row = 0, column = 1, padx = 5)

        self._start_window.columnconfigure(0,weight = 1)

    def start(self):
        '''initiates program'''
        self._start_window.mainloop()
        
    def _on_start(self):
        '''When start button pressed, initiates Dialog class. Ones it returns,
it checks all the entries from Dialog and decides whether or not to go to the
next step.'''
        dialog = Dialog()
        dialog.show()

        if dialog._condition_state():
            INFO = dialog._get_info()
    
            UI_BOARD = TK_UI.UI(INFO[0],INFO[1].strip().upper(),
                                INFO[2].strip().upper(),
                                INFO[3].strip().upper())
            UI_BOARD.show()
            self._start_text.set('PLAY AGAIN?')
            self._butt_text.set('RESTART')
            
        elif dialog._condition_state() == None:
            pass
        else:
            self._start_text.set('YOUR INFORMATION IS INVALID')
            self._butt_text.set('RE-INPUT')

    def _on_cancel(self):
        '''when cancel is pressed, it goes here and destroy window'''
        self._start_window.destroy()
        
                      
def _check_components(components:tuple)->bool:
    '''Goes from _on_start to here and checks entries returns False
if any had an error'''
    bool_list = []
    bool_list.append(_check_dim(components[0]))
    bool_list.append(_check_player(components[1]))
    bool_list.append(_check_player(components[2]))
    bool_list.append(_check_type(components[3]))
    if False in bool_list:
        return False
    return True

def _check_dim(size:tuple)->bool:
    try:
        if int(size[0]) < 4 or int(size[1]) < 4:
            return False
        if int(size[0]) > 16 or int(size[1]) > 16:
            return False
        if len(size) > 2:
            return False
        if (int(size[0]) % 2) == 1 or (int(size[1]) % 2) == 1:
            return False
        return True

    except:
        return False

def _check_player(SP:str)->bool:
    try:
        SP = SP.strip().upper()
        if SP not in ['WW','BB']:
            return False
        return True

    except:
        return False

def _check_type(game:str)->bool:
    game = game.strip().upper()
    if game not in ['M','L']:
        return False
    return True
    

            
        

if __name__ == '__main__':
    Othello_App().start()
