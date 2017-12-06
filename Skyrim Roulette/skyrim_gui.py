from skyrim import Generate_tool
from threading import Thread
import tkinter
import time

DEFAULT_TEXT = ('system', 15)
DEFAULT_TEXT2 = ('Helvetica', 10)

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
