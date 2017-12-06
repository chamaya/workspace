import tkinter
from random import randrange
from os.path import isfile
from collections import defaultdict

DEFAULT_TEXT = ('system', 15)
DEFAULT_TEXT2 = ('Helvetica', 10)


class Generate_life():
    def __init__(self):
        self.elements = {} 
        self.format = []
        self.keys = []
        self.element_sizes = {}
        self.contradictions = defaultdict(set)

    def setup(self):
        if not isfile('Elements.chris'):
            raise Exception("No file found")
        self._reset()
        with open('Elements.chris','r') as E:
            sections = E.read().split('**')
            Elements = sections[0].split('\n')[:-1]
            for element in Elements:
                key, value = element.split(':')
                self.elements[key] = value.split(',')
                self.keys.append(key)
                self.element_sizes[key] = len(self.elements[key])
            self.format = sections[1].strip()
            Contradictions = sections[2].split('\n')[1:-1]
            for i in range(len(Contradictions)):
                key_sep = Contradictions[i].split('+')
                Contradictions[i] = key_sep[1] + ','.join(key_sep[3::2])
            for contradiction in Contradictions:
                keys,value = contradiction.split(':')
                for key in keys.split(','):
                    self.contradictions[key].update(value.split(','))

    def check_key(self,key):
        self.elements[key]
    
    def check_values(self,key,values):
        values_list = values.split(',')
        for i in values_list:
            print(i)
            if i not in self.elements[key]:
                raise KeyError(i)
                    
    def _reset(self):
        self.elements = {} 
        self.format = []
        self.keys = []
        self.element_sizes = {}
        self.contradictions = defaultdict(set)

    def return_keys(self):
        return self.keys

    def Roulette(self):
        sentence = ""
        canthave = set()
        choices = []
        for key in self.keys:
            con_flag = True
            while(con_flag):
                ele = self.elements[key][randrange(self.element_sizes[key])]
                if ele not in canthave:
                    if ele in self.contradictions:
                        canthave = canthave.union(self.contradictions[ele])
                else:
                    continue
                choices.append(ele + '\n')
                con_flag = False
        print(canthave)
        return self.format.format(*choices)

class Generate_tool:
    def __init__(self):
        self.life = Generate_life()
        self.life.setup()
        self.keys = self.life.keys
    def print_life(self):
        self.reset_life()
        print(self.life.Roulette())

    def return_life(self):
        self.reset_life()
        return self.life.Roulette()
        
    def reset_life(self):
        self.life.setup()
        self.keys = self.life.keys

    def strip_file(self):
        with open('Elements.chris', 'r+') as f:
            new = f.read().strip()
            f.seek(0)
            f.truncate()
            f.write(new)
    
            
    def add_element(self,key,values, form_edit):
        self.reset_life()
        with open('Elements.chris', 'r+') as f:
            old = f.read()
            file = old.split('**')
            
            elements = file[0].split('\n')[:-1]
            elements.append(key + ':' + values + '\n')
            elements = '\n'.join(elements)
            file[0] = elements

            form = file[1]
            form = form.strip().strip(':')
            form = '\n' + form + form_edit + ': ' + '{}' + '\n'
            file[1] = form
            
            f.seek(0)
            f.write('**'.join(file))

    def read_elements(self):
         self.reset_life()
         with open('Elements.chris', 'r') as f:
            old = f.read()
            file = old.split('**')
            elements = file[0].split('\n')[:-1]
            for e in range(len(elements)):
                k,v = elements[e].split(':')
                elements[e] = k + ': \n' + '\t' + ', '.join(v.split(','))
            return '\n\n'.join(elements)
            
    def add_inside_element(self,key,value):
        self.reset_life()
        with open('Elements.chris', '+r') as f:
            old = f.read()
            file = old.split('**')
            elements = file[0].split('\n')
            loc = self.keys.index(key)
            k, v = elements[loc].split(':')
            v = v.strip() + ',' + value
            elements[loc] = k + ':' + v
            file[0] = '\n'.join(elements)

            f.seek(0)
            f.truncate()
            f.write('**'.join(file))

    def remove_element(self, key):
        self.reset_life()
        if key not in self.keys:
            raise Exception("key does not exist")
        else:
            with open('Elements.chris','+r') as f:
                old = f.read()
                file = old.split('**')

                loc = 0
                for i in reversed(range(len(self.keys))):
                    if self.keys[i] == key:
                        loc = i
                        self.keys.pop(i)
                        
                elements = file[0].split('\n')
                elements.pop(loc)
                file[0] = '\n'.join(elements)

                form = file[1].split('{}')
                form.pop(loc)
                file[1] = '{}'.join(form)

                contradictions = file[2].strip().split('\n')
                for i in reversed(range(len(contradictions))):
                    contradiction = contradictions[i].split('+')
                    if(contradiction[0] == key):
                        contradictions.pop(i)
                    else:
                        for j in range(2,len(contradiction),2):
                            if contradiction[j] == key:
                                contradiction.pop(j+1)
                                contradiction.pop(j)
                                if(len(contradiction) == 2):
                                    contradictions.pop(i)
                                    break
                                else:
                                    contradictions[i] = "+".join(contradiction)
                                    break

                if(len(contradictions) > 0):
                    contradictions[0] = '\n' + contradictions[0]
                file[2] = '\n'.join(contradictions)
                f.seek(0)
                f.truncate()
                f.write('**'.join(file))

    def remove_inside_element(self, key, value):
        self.reset_life()
        if key not in self.keys:
            raise Exception("key does not exist")
        else:
            with open('Elements.chris','+r') as f:
                old = f.read()
                file = old.split('**')
                elements = file[0].split('\n')
                for e in range(len(elements)):
                    k, values = elements[e].split(':')
                    values = values.split(',')
                    if k == key:
                        if value not in values:
                            raise Exception("value does not exist")
                        values.pop(values.index(value))
                        values = ','.join(values)
                        elements[e] = k + ':' + values
                        break
                file[0] = '\n'.join(elements)

                contradictions = file[2].split('\n')
                for c in reversed(range(len(contradictions))):
                    contradiction = contradictions[c].split('+')
                    if contradiction[0] == key:
                        values = contradiction[1].strip(':').split(',')
                        if value not in values:
                            continue
                        if len(values) == 1:
                            contradictions.pop(c)
                        else:
                            values.pop(values.index(value))
                            values[-1] = values[-1] + ':'
                            values = ','.join(values)
                            contradictions[c] = '+'.join([key] + [values] +contradiction[2:])
                            print(contradictions[c])
                                
                                
                    else:
                        for k in reversed(range(2,len(contradiction),2)):
                            if key == contradiction[k]:
                                values = contradiction[k+1].split(',')
                                if value not in values:
                                    continue
                                values.pop(values.index(value))
                                contradiction[k+1] = ",".join(values)
                                if len(values) == 0:
                                    contradiction.pop(k+1)
                                    contradiction.pop(k)
                                if len(contradiction) == 2:
                                    contradictions.pop(c)
                                else:
                                    contradictions[c] = '+'.join(contradiction)
                                break
                file[2] = '\n'.join(contradictions)                      
                
                f.seek(0)
                f.truncate()
                f.write('**'.join(file))

    def add_contradiction(self, key:str, key_list:[str], o_key:[str], o_key_list:[[str],[str]]):
        self.reset_life()
        self.strip_file()
        with open("Elements.chris", "a") as f:
            format_string = ("{}+" + ("{},"*len(key_list))[:-1] + ":").format(key, *key_list)
            for k in range(len(o_key)):
                format_string += ("+{}+" + ("{}," * len(o_key_list[k]))[:-1]).format(o_key[k], *o_key_list[k])
            f.write('\n' + format_string.strip())

    def read_contradictions(self):
        self.strip_file()
        with open("Elements.chris", "r") as f:
            old = f.read()
            file = old.split('**')
            file = file[2]
            print_string = ''
            contradictions = file.split('\n')[1:]
            for contradiction in contradictions:
                c = contradiction.split('+')
                print_string += '\n' + c[0] + ' ' + c[1][:-1] + ' disabled with:\n'
                for ele in range(2,len(c),2):
                    print_string += '\t' + c[ele] + ':\n' + '\t\t' + c[ele + 1] + '\n' 

            return print_string                

    def remove_contradiction(self, k1, k1_v, k2, v_con):
        self.reset_life()
        self.strip_file()
        with open("Elements.chris", "r+") as f:
            print("Hello There:{}\n{}\n{}\n{}".format(k1,k1_v,k2,v_con))
            old = f.read()
            file = old.split('**')
            replace = []
            contradictions = file[2].split('\n')[1:]
            for c in reversed(range(len(contradictions))):
                contradiction = contradictions[c].split('+')
                k,v = contradiction[0],contradiction[1]
                v = v[:-1].split(',')
                if k == k1:
                    if k1_v in v and k2 in contradiction:
                        loc = contradiction.index(k2)
                        k2_v = contradiction[loc+1].split(',')
                        r_name = contradiction[1][:-1].split(',')
                        r_name.pop(r_name.index(k1_v))
                        contradiction[1] = ','.join(r_name) + ':'
                        replace.append(contradiction[0])
                        replace.append(k1_v + ':')
                        for i in range(2, len(contradiction)):
                            replace.append(contradiction[i])
                        if len(k2_v) == 1:
                            replace.pop(loc + 1)
                            replace.pop(loc)
                        else:
                            k2_v.pop(k2_v.index(v_con))
                            replace[loc+1] = ','.join(k2_v)
                        if len(replace) > 2:
                            contradictions.append('+'.join(replace))
                        if r_name == []:
                            contradictions.pop(c)
                        else:
                            contradictions[c] = '+'.join(contradiction)
                                
            file[2] = '\n'.join([''] + contradictions + [''])                      
            #print(file[2])
            f.seek(0)
            f.truncate()
            f.write('**'.join(file))

    def default(self):
        defalt = ''
        with open("Elements.chris.default", "r") as f:
            default = f.read()
        with open("Elements.chris", "w") as f:
            f.seek(0)
            f.truncate()
            f.write(default)

    def change_default(self):
        with open("Elements.chris", "r") as f:
            default = f.read()
        with open("Elements.chris.default", "w") as f:
            f.seek(0)
            f.truncate()
            f.write(default)

    def restore(self):
        with open("Elements.chris.default.restore", "r") as f:
            default = f.read()
        with open("Elements.chris.default", "w") as f:
            f.seek(0)
            f.truncate()
            f.write(default)
        with open("Elements.chris", "w") as f:
            f.seek(0)
            f.truncate()
            f.write(default)

    def check_key(self, key):
        self.life.check_key(key)

    def check_values(self, key, values):
        self.life.check_values(key,values)
        
                                        



class Skyrim_GUI_main():
    def __init__(self):
        self._start_window = tkinter.Tk()
        self._g_tool = Generate_tool()
        self.num = 0


        #text variables#
        self._life = tkinter.StringVar()
        self._life.set('Generate a life?')
        self._life = 'Press Roulette!\n'
        ################

        main_frame = tkinter.Frame(master = self._start_window)
        main_frame.grid(row = 0, column = 0,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        start_label = tkinter.Label(
            master = main_frame, text = 'Generate your Life!',
            font = DEFAULT_TEXT2)
        start_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)
        
        roulette_button = tkinter.Button(
            master = main_frame, text = "Start Roulette",
            font = DEFAULT_TEXT, command = self._on_roulette)
        roulette_button.grid(row = 1, column = 0, padx = 10, pady = 10,
                             sticky = tkinter.N)

        self._roulette_text = tkinter.Text(
            master = main_frame,
            height = 10, width = 50)
        self._roulette_text.grid(
            row = 1, column = 2, padx = 0, pady = 10)
        self._roulette_text.insert(tkinter.END, str(self._life))
        self._roulette_text.config(state = 'disabled')

        roulette_scroll = tkinter.Scrollbar(
            master = main_frame)
        roulette_scroll.grid(row = 1, column = 3, padx = 0, pady = 10,
                             sticky = tkinter.N + tkinter.S)
        roulette_scroll.config(command = self._roulette_text.yview)
        self._roulette_text.config(yscrollcommand = roulette_scroll.set)

        self._image_text = tkinter.Text(master = self._start_window,
                                  height = 34, width = 42)
        self._image_text.grid(row = 0, rowspan = 2, column = 1, padx = 10, pady = 10)
        self._image_text.config(state = 'disabled')
        img = tkinter.PhotoImage(file="skyrim_main2.png")
        self._image_text.image_create(tkinter.END, image=img)


        bottom_frame = tkinter.Frame(master = self._start_window)
        bottom_frame.grid(row = 1, column = 0,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        settings_button = tkinter.Button(
            master = bottom_frame, text = "Settings",
            font = DEFAULT_TEXT, command = self._on_advanced_settings)
        settings_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        restore_button = tkinter.Button(
            master = bottom_frame, text = "Restore to Default",
            font = DEFAULT_TEXT, command = self._on_restore)
        restore_button.grid(row = 0, column = 1, padx = 10, pady = 10,
                             sticky = tkinter.N)

        self._start_window.mainloop()
        

    def start(self):
        self._start_window.mainloop()


    def _on_advanced_settings(self):
        advanced_settings = Skyrim_advanced_settings(self._g_tool)
        advanced_settings.show()

    def _on_roulette(self):
        #self._life.set(self._g_tool.return_life())
        self._roulette_text.config(state = 'normal')
        self._roulette_text.insert(tkinter.END, self._g_tool.return_life() + '\n' +'\n')
        self._roulette_text.see(tkinter.END)
        self._roulette_text.config(state = 'disabled')

    def _on_restore(self):
        self._g_tool.restore()
        self._roulette_text.config(state = 'normal')
        self._roulette_text.delete('1.0', tkinter.END)
        self._roulette_text.insert(tkinter.END, 'Press Roulette!\n')
        self._roulette_text.see(tkinter.END)
        self._roulette_text.config(state = 'disabled')


class Skyrim_advanced_settings():
    def __init__(self, g_tool):
        self._advanced_window = tkinter.Toplevel()
        self._g_tool = g_tool
        ###Labels###
        add_elements_label = tkinter.Label(
            master = self._advanced_window, text = 'Add Element',
            font = DEFAULT_TEXT2)

        add_inside_elements_label = tkinter.Label(
            master = self._advanced_window, text = 'Add item into existing Element',
            font = DEFAULT_TEXT2)

        remove_element_label = tkinter.Label(
            master = self._advanced_window, text = 'Remove Element',
            font = DEFAULT_TEXT2)

        remove_inside_element_label = tkinter.Label(
            master = self._advanced_window, text = 'Remove item inside Element',
            font = DEFAULT_TEXT2)

        add_contradiction_label = tkinter.Label(
            master = self._advanced_window, text = 'Add Exclusions',
            font = DEFAULT_TEXT2)

        remove_contradiction_label = tkinter.Label(
            master = self._advanced_window, text = 'Remove an Exclusions from an Element',
            font = DEFAULT_TEXT2)

        ###Buttons###
        
        p_element_button = tkinter.Button(
            master = self._advanced_window, text = "+",
            font = DEFAULT_TEXT, command = self._on_p_element_button)
        
        p_inside_element_button = tkinter.Button(
            master = self._advanced_window, text = "+",
            font = DEFAULT_TEXT, command = self._on_p_inside_element_button)

        m_element_button = tkinter.Button(
            master = self._advanced_window, text = "-",
            font = DEFAULT_TEXT, command = self._on_m_element_button)

        m_inside_element_button = tkinter.Button(
            master = self._advanced_window, text = "-",
            font = DEFAULT_TEXT, command = self._on_m_inside_element_button)

        p_contradiction_button = tkinter.Button(
            master = self._advanced_window, text = "+",
            font = DEFAULT_TEXT, command = self._on_p_contradiction_button)

        m_contradiction_button = tkinter.Button(
            master = self._advanced_window, text = "-",
            font = DEFAULT_TEXT, command = self._on_m_contradiction_button)

        default_button = tkinter.Button(
            master = self._advanced_window, text = 'Restore Default',
            command = self._on_default_button)

        read_elements_button = tkinter.Button(
            master = self._advanced_window, text = 'View Elements',
            command = self._on_read_elements_button)

        read_contradictions_button = tkinter.Button(
            master = self._advanced_window, text = 'View Exclusions',
            command = self._on_read_contradictions_button)

        change_default_button = tkinter.Button(
            master = self._advanced_window, text = 'Change default to current',
            command = self._on_change_default_button)

        ###Frame###

        bottom_frame = tkinter.Frame(master = self._advanced_window)
        
        top_frame = tkinter.Frame(master = self._advanced_window)


        ###Scrolls###
        scroll01 = tkinter.Scrollbar(
            master = top_frame, orient='horizontal')
        scroll02 = tkinter.Scrollbar(
            master = top_frame, orient='horizontal')


        scroll41 = tkinter.Scrollbar(
            master = bottom_frame, orient='horizontal')


        scroll42 = tkinter.Scrollbar(
            master = bottom_frame, orient='horizontal')


        scroll43 = tkinter.Scrollbar(
            master = bottom_frame, orient='horizontal')
        
        scroll_TV = tkinter.Scrollbar(master = self._advanced_window)
        #roulette_scroll.grid(row = 1, column = 3, padx = 0, pady = 10,
        #                     sticky = tkinter.N + tkinter.S)




        ###Entry###
        #xscrollcommand = *something

        eb_size = 15
        
        self._eb00 = tkinter.Entry(master = top_frame)
        self._eb00.insert(0,'Weapons')
        self._eb00.config(width = eb_size)

        self._eb01 = tkinter.Entry(master = top_frame)
        self._eb01.insert(0,'hammer,axe,bow')
        scroll01.config(command = self._eb01.xview)
        self._eb01.config(width = 23, xscrollcommand = scroll01.set)

        self._eb02 = tkinter.Entry(master = top_frame)
        self._eb02.insert(0,'with the weapon')
        scroll02.config(command = self._eb02.xview)
        self._eb02.config(width = 23, xscrollcommand = scroll02.set)


        self._eb10 = tkinter.Entry(master = self._advanced_window)
        self._eb10.insert(0,'Followers')
        self._eb10.config(width = eb_size)

        self._eb11 = tkinter.Entry(master = self._advanced_window)
        self._eb11.insert(0,'Master Chief')
        self._eb11.config(width = eb_size)

        self._eb20 = tkinter.Entry(master = self._advanced_window)
        self._eb20.insert(0,'Race')
        self._eb20.config(width = eb_size)

        self._eb30 = tkinter.Entry(master = self._advanced_window)
        self._eb30.insert(0,'Race')
        self._eb30.config(width = eb_size)

        self._eb31 = tkinter.Entry(master = self._advanced_window)
        self._eb31.insert(0,'Dunmer')
        self._eb31.config(width = eb_size)

        self._eb40 = tkinter.Entry(master = bottom_frame)
        self._eb40.insert(0,'Race')
        self._eb40.config(width = eb_size)

        self._eb41 = tkinter.Entry(master = bottom_frame)
        self._eb41.insert(0,'Dunmer,Argonian')
        self._eb41.config(width = 23, xscrollcommand = scroll41.set)
        scroll41.config(command = self._eb41.xview)

        self._eb42 = tkinter.Entry(master = bottom_frame)
        self._eb42.insert(0,'Followers/Playstyle')
        self._eb42.config(width = 23, xscrollcommand = scroll42.set)
        scroll42.config(command = self._eb42.xview)

        self._eb43 = tkinter.Entry(master = bottom_frame)
        self._eb43.insert(0,'Sven,Agmaer/Wizard,Knight')
        self._eb43.config(width = 23, xscrollcommand = scroll43.set)
        scroll43.config(command = self._eb43.xview)

        self._eb50 = tkinter.Entry(master = self._advanced_window)
        self._eb50.insert(0,'Race')
        self._eb50.config(width = eb_size)

        self._eb51 = tkinter.Entry(master = self._advanced_window)
        self._eb51.insert(0,'Altmer')
        self._eb51.config(width = eb_size)

        self._eb52 = tkinter.Entry(master = self._advanced_window)
        self._eb52.insert(0,'Playstyle')
        self._eb52.config(width = eb_size)

        self._eb53 = tkinter.Entry(master = self._advanced_window)
        self._eb53.insert(0,'Knight')
        self._eb53.config(width = eb_size)


        ###Textbox###
        
        self._TV_text = tkinter.Text(
            master = self._advanced_window,
            height = 40, width = 70)
        self._TV_text.grid(
            row = 0, rowspan = 15, column = 6, columnspan = 2, padx = 10,
            pady = 10,sticky = tkinter.N +tkinter.S + tkinter.E + tkinter.W)
        self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
        self._TV_text.config(state = 'disabled')
        scroll_TV.config(command = self._TV_text.yview)
        self._TV_text.config(yscrollcommand = scroll_TV.set)
        scroll_TV.grid(
            row = 0, rowspan = 15, column = 8, sticky =
            tkinter.N +tkinter.S + tkinter.W)
        


        ###allocation of space#####
        px = 5
        py = 5
                          
        add_elements_label.grid(
            row = 0, column = 0, columnspan = 5, padx = px, pady = py,
            sticky = tkinter.S + tkinter.W)

        p_element_button.grid(row = 1, column = 0, padx = px, pady = py,
                             sticky = tkinter.S)
        
        top_frame.grid(row = 1, column = 1, columnspan = 3)
        
        self._eb00.grid(row = 0, column = 0, padx = px, pady = 0,
                        sticky = tkinter.S)

        self._eb01.grid(row = 0, column = 1, padx = px, pady = 0,
                        sticky = tkinter.S)
        scroll01.grid(row = 1, column = 1, padx = px, pady = 0,
                     sticky = tkinter.N + tkinter.E + tkinter.W )

        self._eb02.grid(row = 0, column = 2, padx = px, pady = 0,
                        sticky = tkinter.S)
        scroll02.grid(row = 1, column = 2, padx = px, pady = 0,
                     sticky = tkinter.N + tkinter.E + tkinter.W )

        add_inside_elements_label.grid(row = 3, column = 0,
                                       columnspan = 5, padx = px, pady = py,
                                       sticky = tkinter.S + tkinter.W)

        p_inside_element_button.grid(row = 4, column = 0, padx = px, pady = py,
                             sticky = tkinter.N)

        self._eb10.grid(row = 4, column = 1, padx = px, pady = py)

        self._eb11.grid(row = 4, column = 2, padx = px, pady = py,
                        sticky = tkinter.W)

        remove_element_label.grid(
            row = 5, column = 0, columnspan = 5, padx = px, pady = py,
            sticky = tkinter.S + tkinter.W)

        m_element_button.grid(row = 6, column = 0, padx = px, pady = py,
                             sticky = tkinter.N)

        self._eb20.grid(row = 6, column = 1, padx = px, pady = py)

        remove_inside_element_label.grid(
            row = 7, column = 0, columnspan = 5, padx = px, pady = py,
            sticky = tkinter.S + tkinter.W)

        m_inside_element_button.grid(row = 8, column = 0, padx = px, pady = py,
                             sticky = tkinter.N)
                        
        self._eb30.grid(row = 8, column = 1, padx = px, pady = py)

        self._eb31.grid(row = 8, column = 2, padx = py, pady = px,
                        sticky = tkinter.W)

        add_contradiction_label.grid(
            row = 10, column = 0, columnspan = 5, padx = px, pady = py,
            sticky = tkinter.S + tkinter.W)

        p_contradiction_button.grid(row = 11, column = 0, padx = px, pady = py,
                             sticky = tkinter.N)


        bottom_frame.grid(row = 11, column = 1, columnspan = 4)
        
        self._eb40.grid(row = 0, column = 0, padx = px, pady = 0,
                        sticky = tkinter.S)


        self._eb41.grid(row = 0, column = 1, padx = px, pady = 0,
                        sticky = tkinter.S)
        scroll41.grid(row = 1, column = 1, padx = px, pady = 0,
                     sticky = tkinter.N + tkinter.W + tkinter.E)

        self._eb42.grid(row = 0, column = 2, padx = px, pady = 0,
                        sticky = tkinter.S)
        scroll42.grid(row = 1, column = 2, padx = px, pady = 0,
                     sticky = tkinter.N + tkinter.W + tkinter.E)

        self._eb43.grid(row = 0, column = 3, padx = px, pady = 0,
                        sticky = tkinter.S)
        scroll43.grid(row = 1, column = 3, padx = px, pady = 0,
                     sticky = tkinter.N + tkinter.W + tkinter.E)

        remove_contradiction_label.grid(
            row = 13, column = 0, columnspan = 5, padx = px, pady = py,
            sticky = tkinter.S + tkinter.W)

        m_contradiction_button.grid(row = 14, column = 0, padx = px, pady = py,
                             sticky = tkinter.N)

        self._eb50.grid(row = 14, column = 1, padx = px, pady = py,
                        sticky = tkinter.E +tkinter.W)

        self._eb51.grid(row = 14, column = 2, padx = px, pady = py,
                        sticky = tkinter.W)

        self._eb52.grid(row = 14, column = 3, padx = px, pady = py,
                        sticky = tkinter.E)

        self._eb53.grid(row = 14, column = 4, padx = px, pady = py,
                        sticky = tkinter.W)

        default_button.grid(row = 15, column = 0, columnspan = 3,
                            padx = px, pady = py,
                            sticky = tkinter.N + tkinter.W + tkinter.E)
        
        change_default_button.grid(row = 15, column = 3, columnspan = 2,
                            padx = px, pady = py,
                            sticky = tkinter.N + tkinter.W + tkinter.E)

        read_elements_button.grid(row = 15, column = 6, columnspan = 1,
                            padx = px, pady = py,
                            sticky = tkinter.N + tkinter.W + tkinter.E)

        read_contradictions_button.grid(row = 15, column = 7, columnspan = 7,
                            padx = px, pady = py,
                            sticky = tkinter.N + tkinter.W + tkinter.E)


    def show(self):
        self._advanced_window.grab_set()
        self._advanced_window.wait_window()

    def _on_p_element_button(self):
        try:
            element = self._eb00.get()
            items = self._eb01.get()
            sentence = self._eb02.get().strip()
            items = items.strip().strip(',')
            items = items.split(',')
            for i in range(len(items)):
                items[i] = items[i].strip()
            items = ','.join(items)
            self._TV_text.config(state = 'normal')
            self._TV_text.delete('1.0', tkinter.END)
            self._g_tool.add_element(element, items, sentence)
            self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
            self._TV_text.config(state = 'disabled')
        except:
            self._TV_text.config(state = 'normal')
            message = '''Make sure you are following the configuration:\nChoose an element you would like to add, like "Weapons", then add the items assoicated with that element. Like Hammer's or axes. Do this for all, separated by commas. For the third box, put in what you would like the generator to say about that item.'''
            self._TV_text.delete('1.0', tkinter.END)
            self._TV_text.insert(tkinter.END, message)
            self._TV_text.config(state = 'disabled')
        

    def _on_p_inside_element_button(self):
        try:
            element = self._eb10.get().strip()
            item = self._eb11.get()
            self._TV_text.config(state = 'normal')
            self._TV_text.delete('1.0', tkinter.END)
            self._g_tool.add_inside_element(element, item)
            self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
            self._TV_text.config(state = 'disabled')
        except:
            self._TV_text.config(state = 'normal')
            message = '''Make sure you are following the configuration:\nChoose one element that already exists, like "Followers" then add an item that follows that description.'''
            self._TV_text.delete('1.0', tkinter.END)
            self._TV_text.insert(tkinter.END, message)
            self._TV_text.config(state = 'disabled')

    def _on_m_element_button(self):
        try:
            element = self._eb20.get().strip()
            self._TV_text.config(state = 'normal')
            self._TV_text.delete('1.0', tkinter.END)
            self._g_tool.remove_element(element)
            self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
            self._TV_text.config(state = 'disabled')
        except:
            self._TV_text.config(state = 'normal')
            message = '''Make sure you are following the configuration:\nChoose an element you would like to remove from the list.'''
            self._TV_text.delete('1.0', tkinter.END)
            self._TV_text.insert(tkinter.END, message)
            self._TV_text.config(state = 'disabled')
        

    def _on_m_inside_element_button(self):
        try:
            element = self._eb30.get().strip()
            item = self._eb31.get().strip()
            self._TV_text.config(state = 'normal')
            self._TV_text.delete('1.0', tkinter.END)
            self._g_tool.remove_inside_element(element, item)
            self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
            self._TV_text.config(state = 'disabled')
        except:
            self._TV_text.config(state = 'normal')
            message = '''Make sure you are following the configuration:\nChoose one element that already exists, like "Race" then add an item that follows that description.'''
            self._TV_text.delete('1.0', tkinter.END)
            self._TV_text.insert(tkinter.END, message)
            self._TV_text.config(state = 'disabled')

    def _on_p_contradiction_button(self):
        try:
            key = self._eb40.get().strip()
            key_list = self._eb41.get().strip().strip(',').split(',')
            o_key = self._eb42.get().strip().strip('/').split('/')
            o_key_list = self._eb43.get().strip().strip(',').strip('/').split('/')
            for i in range(len(o_key_list)):
                o_key_list[i] = o_key_list[i].split(',')
                for j in range(len(o_key_list[i])):
                    o_key_list[i][j] = o_key_list[i][j].strip()
            self._g_tool.check_key(key)
            self._g_tool.check_values(key, ','.join(key_list))
            for i in range(len(o_key)):
                self._g_tool.check_values(o_key[i], ','.join(o_key_list[i]).strip(','))
            self._TV_text.config(state = 'normal')
            self._TV_text.delete('1.0', tkinter.END)
            self._g_tool.add_contradiction(key, key_list, o_key, o_key_list)
            self._TV_text.insert(tkinter.END, self._g_tool.read_contradictions())
            self._TV_text.config(state = 'disabled')
        except(KeyError or ValueError):
            self._TV_text.config(state = 'normal')
            message = '''Make sure you are following the configuration:\nChoose one or more items from the same elements to add exclusions to. You separate the items you want to add exlusions to with commas. The exclusions must be apart of another element and more than one element can be chosen to gather exclusions from. These elements are separated by a slash in the third box. The fourth box is the list of exclusions from the elements. Lists from respective elements are separated by '/' as well.\nFormat = [Element] [item_in_element, item_in_element,...] [Element_A/Element_B/...][item_A,item_A.../item_B,item_B...]'''
            self._TV_text.delete('1.0', tkinter.END)
            self._TV_text.insert(tkinter.END, message)
            self._TV_text.config(state = 'disabled')
        
    def _on_m_contradiction_button(self):
        #print("Hi")
        try:
            k1 = self._eb50.get().strip()
            k1_v = self._eb51.get().strip()
            k2 = self._eb52.get().strip()
            v_con = self._eb53.get().strip()
            self._g_tool.check_values(k1,k1_v)
            self._g_tool.check_values(k2,v_con)
            self._TV_text.config(state = 'normal')
            self._TV_text.delete('1.0', tkinter.END)
            self._g_tool.remove_contradiction( k1, k1_v, k2, v_con)
            self._TV_text.insert(tkinter.END, self._g_tool.read_contradictions())
            self._TV_text.config(state = 'disabled')
        except(KeyError or ValueError):
            self._TV_text.config(state = 'normal')
            message = '''Make sure you are following the configuration:\n For one element, remove one item from another Element\nFormat = [Element_A] [item_A] [Element_B] [item_B] '''
            self._TV_text.delete('1.0', tkinter.END)
            self._TV_text.insert(tkinter.END, message)
            self._TV_text.config(state = 'disabled')
    def _on_default_button(self):
        self._TV_text.config(state = 'normal')
        self._TV_text.delete('1.0', tkinter.END)
        self._g_tool.default()
        self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
        self._TV_text.config(state = 'disabled')

    def _on_read_elements_button(self):
        self._TV_text.config(state = 'normal')
        self._TV_text.delete('1.0', tkinter.END)
        self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
        self._TV_text.config(state = 'disabled')

    def _on_read_contradictions_button(self):
        self._TV_text.config(state = 'normal')
        self._TV_text.delete('1.0', tkinter.END)
        self._TV_text.insert(tkinter.END, self._g_tool.read_contradictions())
        self._TV_text.config(state = 'disabled')

    def _on_change_default_button(self):
        self._TV_text.config(state = 'normal')
        self._TV_text.delete('1.0', tkinter.END)
        self._g_tool.change_default()
        self._TV_text.insert(tkinter.END, self._g_tool.read_elements())
        self._TV_text.config(state = 'disabled')    

        

GUI = Skyrim_GUI_main()
GUI.start()
