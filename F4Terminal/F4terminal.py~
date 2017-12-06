#Cheat for Fallout 4 Terminal. 
from collections import namedtuple
w_like = namedtuple('w_like', 'word likeness')
def Terminal():
    terminal = input("Put in all the words separated by spaces\n").split()
    while(len(terminal) != 1):
        try:
            terminal = sort_teminal(terminal)
            print_terminal(terminal)
            kill_list = []
            w_pair = input("[word] [likeness] ").split()
            w_pair[1] = int(w_pair[1])
            t_pair = w_like(word = w_pair[0], likeness = w_pair[1])
            terminal.pop(terminal.index(t_pair.word))
            for w in terminal:
                like = calc_likeness(w, t_pair.word)
                if like != t_pair.likeness:
                     kill_list.append(w)
            for death in kill_list:
                terminal.pop(terminal.index(death))
        except:
            pass
    print "\n\nThe answer is {} \n\n".format(terminal.pop())

def print_terminal(terminal):
    print_str = '\n'
    for w in range(len(terminal)):
        print_str += '{}.\t{}\n'.format(w+1, terminal[w])
    print(print_str)
   
def sort_teminal(terminal):
    winning = []
    for word in terminal:
        likes = 0
        for comparee in terminal:
            likes += calc_likeness(word, comparee)
        winning.append((word,likes))
    winning.sort(key = lambda winning: winning[1], reverse = True)
    terminal = []
    for pair in winning:
        terminal.append(pair[0])
    return terminal
        
def calc_likeness(s0,s1):
    like = 0
    for let in range(len(s1)):
        if s0[let] == s1[let]:
            like += 1
    return like
    
                
try:        
    Terminal()
except:
    raise
    
