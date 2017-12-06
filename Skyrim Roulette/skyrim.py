from random import randrange
from os.path import isfile
from collections import defaultdict

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
        
                                        
                                    
        
#Gt = Generate_tool()
#Gt.add_element('Weapons', 'Hammer, screwdriver', 'use the weapon')
#Gt.remove_element('Weapons')
##Gt.print_life()
##Gt.add_inside_element("Race", "Demon")
##
##Gt.print_life()
##Gt.add_element('Spells', 'fire, ice', 'use the spell')
##Gt.print_life()
##print(Gt.read_contradictions())
##Gt.add_contradiction("Race", ['Dunmer','Argonian'], ["Followers", "Playstyle"], [["Sven,Agmaer"],['Wizard,Knight']])
#print(Gt.read_contradictions())
#Gt.remove_contradiction("Race", "Altmer", "Playstyle", "Knight")
#Gt.add_contradiction("Race", ["Brenton", "Redguard"], ["Followers"], [["Golldir"]])
