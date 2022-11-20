# import all the required modules 
import socket 
import threading
from tkinter import *
from tkinter import font, ttk, filedialog, messagebox
import random
from colour import Color
from time import sleep
from tkinter.colorchooser import *
import sys
import re
import pickle
import numpy as np
from PIL import ImageTk, Image
from math import exp
from math import floor, ceil
import os
import traceback
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.figure import Figure
from collections import OrderedDict
import itertools
import math
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

__all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']

_whitespace = '\t\n\x0b\x0c\r '

def justify(words, width):
    if len(words)==width:
        return(words)
    line = re.split("(\s+)",words)
    if line[0]=='':
        line.pop(0)
    i=0
    while True:
            for u in range(1,len(line)):
                if i==width-len(words):
                    corrigida=''
                    for elemen in line:
                        corrigida+=elemen
                    return(corrigida)
                elem=line[u]
                if elem.replace(' ','')=='' and line[u+1]!='>' and line[u-1]!='>':
                    line[u]+=" "
                    i+=1
            if i==0:
                while True:
                    if i==width-len(words):
                            corrigida=''
                            for elemen in line:
                                corrigida+=elemen
                            return(corrigida)
                    i+=1
                    line.append(' ')
class TextWrapper:
    unicode_whitespace_trans = {}
    uspace = ord(' ')
    for x in _whitespace:
        unicode_whitespace_trans[ord(x)] = uspace
    word_punct = r'[\w!"\'&.,?]'
    letter = r'[^\d\W]'
    whitespace = r'[%s]' % re.escape(_whitespace)
    nowhitespace = '[^' + whitespace[1:]
    wordsep_re = re.compile(r'''
        ( # any whitespace
          %(ws)s+
        | # em-dash between words
          (?<=%(wp)s) -{2,} (?=\w)
        | # word, possibly hyphenated
          %(nws)s+? (?:
            # hyphenated word
              -(?: (?<=%(lt)s{2}-) | (?<=%(lt)s-%(lt)s-))
              (?= %(lt)s -? %(lt)s)
            | # end of word
              (?=%(ws)s|\Z)
            | # em-dash
              (?<=%(wp)s) (?=-{2,}\w)
            )
        )''' % {'wp': word_punct, 'lt': letter,
                'ws': whitespace, 'nws': nowhitespace},
        re.VERBOSE)
    del word_punct, letter, nowhitespace
    wordsep_simple_re = re.compile(r'(%s+)' % whitespace)
    del whitespace
    sentence_end_re = re.compile(r'[a-z]'           
                                 r'[\.\!\?]'         
                                 r'[\"\']?'           
                                 r'\Z')               

    def __init__(self,
                 width=70,
                 initial_indent="",
                 subsequent_indent="",
                 expand_tabs=True,
                 replace_whitespace=False,
                 fix_sentence_endings=False,
                 break_long_words=False,
                 drop_whitespace=False,
                 break_on_hyphens=True,
                 tabsize=8,
                 *,
                 max_lines=None,
                 placeholder=' [...]'):
        self.width = width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.expand_tabs = expand_tabs
        self.replace_whitespace = replace_whitespace
        self.fix_sentence_endings = fix_sentence_endings
        self.break_long_words = break_long_words
        self.drop_whitespace = drop_whitespace
        self.break_on_hyphens = break_on_hyphens
        self.tabsize = tabsize
        self.max_lines = max_lines
        self.placeholder = placeholder

    # -- Private methods -----------------------------------------------

    def _munge_whitespace(self, text):
        if self.expand_tabs:
            text = text.expandtabs(self.tabsize)
        if self.replace_whitespace:
            text = text.translate(self.unicode_whitespace_trans)
        return text


    def _split(self, text):
        if self.break_on_hyphens is True:
            chunks = self.wordsep_re.split(text)
        else:
            chunks = self.wordsep_simple_re.split(text)
        chunks = [c for c in chunks if c]
        return chunks

    def _fix_sentence_endings(self, chunks):
        i = 0
        patsearch = self.sentence_end_re.search
        while i < len(chunks)-1:
            if chunks[i+1] == " " and patsearch(chunks[i]):
                chunks[i+1] = "  "
                i += 2
            else:
                i += 1

    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        if width < 1:
            space_left = 1
        else:
            space_left = width - cur_len
        if self.break_long_words:
            cur_line.append(reversed_chunks[-1][:space_left])
            reversed_chunks[-1] = reversed_chunks[-1][space_left:]
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

    def _wrap_chunks(self, chunks):
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if len(indent) + len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")
        chunks.reverse()

        while chunks:
            cur_line = []
            cur_len = 0
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            width = self.width - len(indent)
            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]

            while chunks:
                if '\n' in chunks[-1]:
                    chunks.pop()
                    chunks.append('\j'+' -*- '*10)
                elif '\k' in chunks[-1] and not '\\\k' in chunks[-1]:
                        yob=chunks[-1].split('\k')
                        chunks.pop()
                        if yob[1]!='':
                            chunks.append(yob[1])
                        elif len(chunks)>1:
                            z=chunks.pop()
                            chunks[-1]='\j'+z+chunks[-1]
                        else:
                            chunks.append('\j')
                        if yob[0]!='':
                            if len(yob[0])<(width-cur_len):
                                chunks.append((width-cur_len-len(yob[0]))*' ')
                            else:
                                chunks.append((width-len(yob[0]))*' ')
                            chunks.append(yob[0])
                        else:
                            chunks.append((width-cur_len)*' ')
                elif '\\n' in chunks[-1] and not '\\\\n' in chunks[-1]:
                        yob=chunks[-1].split('\\n')
                        chunks.pop()
                        if yob[1]:
                            chunks.append(yob[1])
                        elif len(chunks)>1:
                            z=chunks.pop()
                            chunks[-1]='\j'*(width-cur_len-len(yob[0])>0)+z.replace(' ','')+chunks[-1]
                        else:
                            if not yob[0] and (width-cur_len-len(yob[0])==0):
                                chunks.append(' '*width)
                            else:
                                chunks.append('\j'*(width-cur_len-len(yob[0])>0))
                        if yob[0]:
                            if len(yob[0])<(width-cur_len):
                                chunks.append((width-cur_len-len(yob[0]))*' ')
                            else:
                                chunks.append((width-len(yob[0]))*' ')
                            chunks.append(yob[0])
                        else:
                            chunks.append((width-cur_len)*' ')
                elif '\g' in chunks[-1] and not '\\\g' in chunks[-1]:
                        yob=chunks[-1].split('\g')
                        chunks.pop()
                        if yob[1]!='':
                            chunks.append('\j         '+yob[1])
                        elif len(chunks)>1:
                            z=chunks.pop()
                            chunks[-1]='\j         '+z+chunks[-1]
                        if yob[0]!='':
                            if len(yob[0])<(width-cur_len):
                                chunks.append((width-cur_len-len(yob[0]))*' ')
                            else:
                                chunks.append((width-len(yob[0]))*' ')
                            chunks.append(yob[0])
                        else:
                            chunks.append((width-cur_len)*' ')
                            
                l = len(chunks[-1])-2*(chunks[-1].startswith('\j') and cur_len==0)
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l
                else:
                    break
            if chunks and len(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
                cur_len = sum(map(len, cur_line))
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                cur_len -= len(cur_line[-1])
                del cur_line[-1]

            if cur_line:
                if (self.max_lines is None or
                    len(lines) + 1 < self.max_lines or
                    (not chunks or
                     self.drop_whitespace and
                     len(chunks) == 1 and
                     not chunks[0].strip()) and cur_len <= width):
                    lines.append(indent + ''.join(cur_line))
                else:
                    while cur_line:
                        if (cur_line[-1].strip() and
                            cur_len + len(self.placeholder) <= width):
                            cur_line.append(self.placeholder)
                            lines.append(indent + ''.join(cur_line))
                            break
                        cur_len -= len(cur_line[-1])
                        del cur_line[-1]
                    else:
                        if lines:
                            prev_line = lines[-1].rstrip()
                            if (len(prev_line) + len(self.placeholder) <=
                                    self.width):
                                lines[-1] = prev_line + self.placeholder
                                break
                        lines.append(indent + self.placeholder.lstrip())
                    break

        return lines

    def _split_chunks(self, text):
        text = self._munge_whitespace(text)
        return self._split(text)

    # -- Public interface ----------------------------------------------

    def wrap(self, text):
        chunks = self._split_chunks(text)
        if self.fix_sentence_endings:
            self._fix_sentence_endings(chunks)
        return self._wrap_chunks(chunks)

    def fill(self, text):
        return "\n".join(self.wrap(text))
    
# -- Convenience interface ---------------------------------------------

def wrap(text, width=70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)

def fill(text, width=70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.fill(text)

def shorten(text, width, **kwargs):
    w = TextWrapper(width=width, max_lines=1, **kwargs)
    return w.fill(' '.join(text.strip().split()))    

# -- Loosely related functionality -------------------------------------

_whitespace_only_re = re.compile('^[ \t]+$', re.MULTILINE)
_leading_whitespace_re = re.compile('(^[ \t]*)(?:[^ \t\n])', re.MULTILINE)

def dedent(text):
    margin = None
    text = _whitespace_only_re.sub('', text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent
        elif indent.startswith(margin):
            pass
        elif margin.startswith(indent):
            margin = indent
        else:
            for i, (x, y) in enumerate(zip(margin, indent)):
                if x != y:
                    margin = margin[:i]
                    break
    if 0 and margin:
        for line in text.split("\n"):
            assert not line or line.startswith(margin), \
                   "line = %r, margin = %r" % (line, margin)

    if margin:
        text = re.sub(r'(?m)^' + margin, '', text)
    return text


def indent(text, prefix, predicate=None):
    if predicate is None:
        def predicate(line):
            return line.strip()

    def prefixed_lines():
        for line in text.splitlines(True):
            yield (prefix + line if predicate(line) else line)
    return ''.join(prefixed_lines())


HEADER_LENGTH = 10
PORT = 1234
hostname = socket.gethostname()
SERVER = socket.gethostbyname(hostname)
ADDRESS = (SERVER, PORT) 
FORMAT = "utf-8"

# Create a new client socket 
# and connect to the server 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(ADDRESS)

class bloco:
    def __init__(self,premod,posmod,sn,crit):
        self.premod=premod
        self.posmod=posmod
        self.sn=sn
        self.crit=crit

class status:
    def __init__(self,num):
        self.num=num

class msg:
    def __init__(self,destiny,content):
        self.destiny=destiny
        self.content=content

class roll:
    def __init__(self,receiver,who):
        self.receiver=receiver
        self.who=who
        self.crit=crit

class res:
    def __init__(self,p,crit,r,advan):
        self.p=p
        self.r=r
        self.crit=crit
        self.advan=advan
        self.mods=''

    def __lt__(self, other):
         return self.p < other.p

# GUI class for the chat 
class GUI(Tk): 

        # constructor method 
        def __init__(self):
                super().__init__()
                
                self.not_closing=1
                
                red=Color('#ff0000')
                violet=Color('#ff00ff')
                self.colors = list(red.range_to(violet,50))
                self.colors+=list(violet.range_to(red,50))
                # chat window which is currently hidden 

                self.withdraw() 
                
                # login window 
                self.login = Toplevel() 
                # set the title 
                self.login.title("Login") 
                self.login.resizable(width = False, 
                                                        height = False) 
                self.login.configure(width = 700, 
                                                        height = 300) 
                # create a Label 
                self.pls = Label(self.login, 
                                        text = "Please login to continue", 
                                        justify = CENTER,
                                        font = "Consolas 14 bold") 
                
                self.pls.place(relheight = 0.15, 
                                        relx = 0.5, 
                                        rely = 0.09,
                                        anchor=CENTER)
                
                # create a Label 
                self.labelName = Label(self.login, 
                                                        text = "Username: ",
                                                        font = "Consolas 14") 
                
                self.labelName.place(relheight = 0.2, 
                                                        relx = 0.25, 
                                                        rely = 0.16) 
                
                # create a entry box for 
                # typing the message 
                self.entryName = Entry(self.login, 
                                                        font = "Consolas 14") 
                
                self.entryName.place(relwidth = 0.3, 
                                                        relheight = 0.12, 
                                                        relx = 0.45, 
                                                        rely = 0.2) 
                
                # set the focus of the curser 
                self.entryName.focus() 
                
                # create a Continue Button 
                # along with action 
                self.go = Button(self.login, 
                                                text = "CONTINUE", 
                                                font = "Consolas 14 bold", 
                                                command = lambda: self.goAhead(self.entryName.get())) 

                self.entryName.bind('<Return>',(lambda event: self.goAhead(self.entryName.get())))
                self.login.protocol("WM_DELETE_WINDOW", self.on_closing)  
                self.go.place(relx = 0.4, 
                                        rely = 0.55)

        def onPlayerClick(self, c):
            self.playerBtts[c].config(bg=self.playerBtts[c].cget('fg'), fg=self.playerBtts[c].cget('bg'))
            self.players[c]['selected'] = not self.players[c]['selected']

        def onPlayerSelec(self, c):
            if self.label.cget('text').startswith('Select'):
                nomiz=self.playerBtts2[c].cget('text')
                self.roll_list.append(nomiz)
                aux=1
                if self.label.cget('text')=='Select the players to roll':
                    aux=0
                    self.label.config(text='Selected: ')
                self.label.config(text=self.label.cget('text')+aux*' - '+nomiz)

        def rollerrola(self):
            message_sent = pickle.dumps(roll(self.roll_list,self.who.get()))
            message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(message_sent_header+message_sent)
            self.roll_list=[]
            self.label.config(text='Select the players to roll')
            
        def AllClick(self):
            if self.allButton.cget('text')=='Select all':
                self.allButton.config(text='Exclude all')
                for c in range(len(self.playerBtts)):
                    self.playerBtts[c].config(bg=self.players[c]['color'], fg='black')
                    self.players[c]['selected'] = True
            else:
                self.allButton.config(text='Select all')
                for c in range(len(self.playerBtts)):
                    self.playerBtts[c].config(bg='black', fg=self.players[c]['color'])
                    self.players[c]['selected'] = False

        def createSidebarButtons(self):
            for playerBtt in self.playerBtts:
                playerBtt.destroy()
            for playerBtt in self.playerBtts2:
                playerBtt.destroy()

            self.playerBtts = []
            self.playerBtts2 = []

            for i in range(len(self.players)):
                tempButton = Button(self.sidebar,
                                                fg = self.players[i]['color'],
                                                bg = 'black', text = self.players[i]['name'],
                                                font = "Consolas 14 bold",
                                                command=lambda c=i: self.onPlayerClick(c))
                self.playerBtts.append(tempButton)
                self.playerBtts[-1].place(relwidth=1, relheight=0.1, rely = 0.1*(len(self.playerBtts)-1))

                tempButton = Button(self.sidebaroll,
                                                    fg = self.players[i]['color'],
                                                    bg = 'black', text = self.players[i]['name'],
                                                    font = "Consolas 14 bold",
                                                    command=lambda c=i: self.onPlayerSelec(c))
                self.playerBtts2.append(tempButton)
                self.playerBtts2[-1].place(relwidth=1, relheight=0.1, rely = 0.1*(len(self.playerBtts2)-1))

        def transl(self, res):
            p, crit, r=(2000-res.p)/100, (2000-res.crit)/100, (2000-res.r+1)/100
            r=19.66
            if (r > p):
                if(r > crit):
                    resultStr = "SUCESSO CRÍTICO"
                else:
                    resultStr = "SUCESSO"
            else:
                if (r<=p/10):
                    resultStr = "FALHA CRÍTICA"
                else:
                    resultStr = "FALHA"
            return [p, crit, r, resultStr]
                
        def displayres(self, p, crit, r, resultStr):
            if self.displaymode.get()=='bar':
                self.progress['value']=0
                self.minRollLabel2.config(text = "Precisa: "+str(p))
                self.critRollLabel2.config(text = "Crítico a partir de: "+str(crit))
                self.realRollLabel2.config(text = "")
                self.ResultLabel2.config(text = "")
                
                p=4*((p*100+19)//20)
                r_bar=(r*100+19)//20
                crit=4*((crit*100+19)//20)

                if not self.progresswindow.winfo_viewable():
                    self.progresswindow.deiconify()
                if self.dicewindow.winfo_viewable():
                    self.dicewindow.withdraw()
                self.progresswindow.focus()
                
                self.barracrit1.place(relwidth=0.0025,x=crit-1)
                self.barrap1.place(relwidth=0.0025,x=p-1)
                self.barracrit2.place(relwidth=0.0025,x=crit+1)
                self.barrap2.place(relwidth=0.0025,x=p+1)

                x=0;
                n=random.randint(2,15)
                for i in range(159):
                    sleep(0.01)
                    x+=0.00625
                    y=int(r_bar*n*x/(1+(n-1)*x))
                    self.progress['value']=y
                
                self.ResultLabel2.config(text = resultStr)
                self.realRollLabel2.config(text = "Rolou: "+str(r))
            else:
                self.minRollLabel.config(text = "Precisa: "+str(p))
                self.critRollLabel.config(text = "Crítico a partir de: "+str(crit))
                self.realRollLabel.config(text = "")
                self.ResultLabel.config(text = "")

                if not self.dicewindow.winfo_viewable():
                    self.dicewindow.deiconify()
                if self.progresswindow.winfo_viewable():
                    self.progresswindow.withdraw()
                self.dicewindow.focus()

                ##### CONSTANTES PARA ADEQUACAO DOS TEMPOS DE ROLAGEM (EM 10^-2s)

                sleepTime = random.randint(self.minST,self.maxST)/100
                maxSleepTime = random.randint(self.minMST,self.maxMST)/100
                
                currentRoll = random.randint(0, 20)
                while maxSleepTime-sleepTime > 0.1 and maxSleepTime > sleepTime:
                    rolagem = random.randint(0, 20)
                    while rolagem == currentRoll:
                        rolagem = random.randint(0, 20)

                    currentRoll = rolagem

                    img = Image.open("Dice_Images/"+str(rolagem)+".png")
                    img = img.resize((250,250))
                    self.img = ImageTk.PhotoImage(img)
                    self.panel.config(image = self.img)
                    
                    sleep(sleepTime)
                    sleepTime = self.nextSleepTime(sleepTime, maxSleepTime)

                sleep(self.maxMST/100 - maxSleepTime)

                roundedRealDiceRoll = floor(r)
                if (r > crit):
                    if roundedRealDiceRoll<crit:
                        roundedRealDiceRoll = ceil(r)
                elif(r > p):
                    if roundedRealDiceRoll<p:
                        roundedRealDiceRoll = ceil(r)

                if roundedRealDiceRoll==0 or roundedRealDiceRoll==20:
                    img = Image.open("Dice_Images/"+str(roundedRealDiceRoll)+self.dice_style.get()+'.png')
                else:
                    img = Image.open("Dice_Images/"+str(roundedRealDiceRoll)+".png")
                img = img.resize((250,250))
                self.img = ImageTk.PhotoImage(img)
                self.panel.config(image = self.img)

                self.realRollLabel.config(text = "Rolou: "+str(r))
                self.ResultLabel.config(text = resultStr)

        def nextSleepTime(self, currentTime, limitTime): # 3 opcoes de incremento de tempo
            # return currentTime + currentTime**2 / 2
            # return currentTime + incrementFraction*currentTime
            return currentTime+limitTime*(1-exp(-currentTime*self.incrementFraction))

        def on_closing(self):
            self.not_closing=0
            for filename in os.listdir('Past configs/'):
                os.remove('Past configs/'+filename)
            self.destroy()
            client.close()
            sys.exit()
        
        def blocswitch(self):
            if not self.Window2.winfo_viewable():
                self.Window2.deiconify()
                self.blocbtt.config(text='<')
            else:
                self.Window2.withdraw()
                self.blocbtt.config(text='>')            

        def goAhead(self, name):
            my_username = name.encode(FORMAT)
            my_username_header = f"{len(my_username):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(my_username_header + my_username)
            server_message_header=client.recv(HEADER_LENGTH)
            server_message_length = int(server_message_header.decode(FORMAT).strip())
            server_message=client.recv(server_message_length).decode(FORMAT)
            if server_message=='ok':
                try:
                    self.color=askcolor(title ="Escolha a cor do seu usuário")[1]
                    color=self.color.encode(FORMAT)
                except:
                    self.on_closing()
                color_header=f"{len(color):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(color_header + color)
                self.login.destroy()
                self.receive()
                self.layout(name)
                # the thread to receive messages 
                self.rcv = threading.Thread(target=self.receive) 
                self.rcv.start()
            else:
                self.pls.config(text=server_message)

        ##-----------------------------------------------
        def build_menu(self):
            for filename in os.listdir('Saved configs/'):
                self.openmenu.add_command(label=filename[:-4], command=lambda filepath='Saved configs/'+filename: self.openfile(filepath))
            self.openmenu.add_separator()
            self.openmenu.add_command(label="Open new", command=lambda: self.openfile(0))
            self.menubar.add_cascade(label="Open", menu=self.openmenu)            

            self.menubar.add_command(label="Save", command=self.savefile)
            self.menubar.add_command(label="Save as...", command=self.savefileas)
                
        def modify(self, a, b, c):
            self.modified=1
            
        def load_content(self, content):
            content, crit=pickle.loads(content)
            
            self.crit.set(str(crit))
            self.value_entry.delete(0, END)
            self.value_entry.insert(END, str(content.premod[0]))
            self.advan_entry.delete(0, END)
            self.advan_entry.insert(END, str(content.premod[1]))
            converted_pos=''
            for i in content.posmod:
                converted_pos+="("+str(i[0])+", ["
                for j in i[1]:
                    if type(j)==list:
                        converted_pos+="<"+str(j[0])+", "+str(j[1])+">, "
                    else:
                        converted_pos+="{"+str(j[0])+", "+str(j[1])+"}, "
                converted_pos=converted_pos[:-2]+"]), "
            converted_pos=converted_pos[:-2]
            self.block_entry.delete(0, END)
            self.block_entry.insert(END, converted_pos)
            self.block_entry.icursor(self.block_entry.index(INSERT))

        def openfile(self, pre_path):
            if not self.modified:
                try:
                    if pre_path:
                        self.path=pre_path
                    else:
                        self.path = filedialog.askopenfile(parent=self.Window2, filetypes = [("Text files", "*.txt")]).name                              
                    with open(self.path, 'rb') as file:             
                        content = file.read()
                        self.load_content(content)                                      
                        self.modified=0
                    self.Window2.title(os.path.basename(os.path.normpath(self.path))[:-4])
                    self.past_index=self.past_index_max
                except Exception:
                    print(traceback.format_exc())
                    messagebox.showerror(parent=self.Window2, title="Erro de path", message="Path inválido, tente novamente.")
                    return               
            else:
                answer = messagebox.askyesno(parent=self.Window2, title='Confirmação', message='Existem mudanças não salvas. Deseja salvar as configurações atuais primeiro?')
                if answer:
                    self.savefileas()                      
                self.modified=0             
                self.openfile(pre_path)

        def savefile(self):             
            if self.path != '':                
                with open(self.path, 'wb') as file:
                    content=self.conversao()
                    if content:
                        pickle.dump([content, self.critbox.get()], file)
                        self.modified=0                       
            else:
                self.savefileas()                

        def savefileas(self):    
            try:
                self.path = filedialog.askopenfile(parent=self.Window2, filetypes = [("Text files", "*.txt")]).name
                with open(self.path, 'wb') as file:
                    content=self.conversao()
                    if content:
                        pickle.dump([content, self.critbox.get()], file)
                        self.modified=0
                self.Window2.title(os.path.basename(os.path.normpath(self.path))[:-4])
                self.menubar.delete(0,"end")
                self.openmenu.delete(0,"end")
                self.build_menu()
                self.past_index=self.past_index_max
            except Exception:
                print(traceback.format_exc())
                messagebox.showerror(parent=self.Window2, title="Erro de path", message="Path inválido, tente novamente.")
                return

        def build_resor(self):
            general=Label(self.terFrame, text="Advan: "+(self.advanint>=0)*"+"+str(self.advanint)+", Constant: "+str(self.const),
                                                bg = 'black',
                                                fg='white',
                                                font = "Consolas 12 bold")
            general.pack(fill=x)
            for i in range(len(self.resor)):
                self.resor[i][2]=Radiobutton(self.terFrame, 
                                                                        variable = self.selectRes, 
                                                                        value = i,
                                                                        text = str(i)+"-ésimo recurso\nQnt. "+self.resor[i][1], 
                                                                        fg="white",
                                                                        bg='black',
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')
                self.resor[i][2].pack(fill=x)
                self.resor[i][4]=[]
                for j in range(len(self.resor[i][3])):
                    self.resor[i][4].append(Button(self.terFrame, 
                                                                        text = self.resor[i][3][j][1], 
                                                                        fg="white",
                                                                        bg='black',
                                                                        font = 'Consolas 10 bold'
                                                                        command = lambda c=(i, j): self.destroy_subres(c))
                    )
                    self.resor[i][4][-1].pack(fill=x)                    

            #self.resor[self.selectRes][2]

        def destroy_subres(self, pos):
            self.resor[pos[1]][3].pop(pos[2])
            self.build_resor()

        def resourcepaste(self, num):
            self.resor.append([num, [], [], []])
            self.build_resor()
            
        def anteadvpaste(self, num):
            try:
                self.advanint+=int(num)
                self.build_resor()
            except:
                pass
        
        def antepaste(self, num1, num2):
            try:
                self.const+=int(int(num1)*(int(num2)+1)/2))
                self.build_resor()
            except:
                pass
            
        def interpaste(self, num1, num2):
            if type(num2)!=str:
                num2=num2.get()
            self.block_entry.insert(self.block_entry.index(INSERT), "<"+num1.get()+","+num2+">, ")
            self.block_entry.focus()

        def postpaste(self, num1, num2):
            if type(num2)!=str:
                num2=num2.get()
            self.block_entry.insert(self.block_entry.index(INSERT), "{"+num1.get()+","+num2+"}, ")
            self.block_entry.focus()

        def send_block(self):
            message_sent = self.conversao()
            if message_sent:
                try:
                    with open('Past configs/'+str(self.past_index_max)+'.txt', 'xb') as file:
                        pickle.dump([message_sent, self.critbox.get()], file)
                except Exception:
                    print(traceback.format_exc())
                    self.on_closing()
                self.past_index_max+=1
                self.past_index=self.past_index_max
                message_sent=pickle.dumps(message_sent)
                message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(message_sent_header+message_sent)             
        
        def conversao(self): 
            try:
                bloco_text=self.block_entry.get().replace(" ", "").replace(">,",">").replace("),",")").replace("},","}")

                rec=bloco((int(self.value_entry.get()),int(self.advan_entry.get())),[],self.sn.get(),int(self.crit.get())/100)

                recursos=re.findall("\(.+?\)", bloco_text)
                rec.posmod=[]
                for i in recursos:
                    quant=int(re.search("\d+", i).group())
                    rec.posmod.append([quant, []])
                    recurso=re.search("(?<=,\[).+(?=\])", i).group()
                    pos_pre=re.findall("\<.+?\>", recurso)
                    for j in pos_pre:
                        j=re.sub("\<|\>","",j)
                        singular=[int(x) for x in re.split(",", j)]
                        rec.posmod[-1][1].append(singular)  
                    pos_pos=re.findall("\{.+?\}", recurso)
                    for j in pos_pos:
                        j=re.sub("\{|\}","",j)
                        singular=(int(re.split(",", j)[0]),int(re.split(",", j)[1]))
                        rec.posmod[-1][1].append(singular)
                return rec
            except:
                messagebox.showerror(parent=self.Window2, title="Erro de conversão", message="Algo deu errado, confira seu envio.")
                return 0

        def up_down2(self, event):
            if self.past_index_max:
                alt=1
                if event.keysym == 'Up':
                    if self.past_index:
                        self.past_index-=1
                        if self.past_index==self.past_index_max-1:
                            self.path='Past configs/'+str(self.past_index)+'.txt'
                            self.openfile(self.path)
                            self.past_index-=1
                            alt=0
                            self.Window2.title('#'+str(self.past_index+1))
                    else:
                        alt=0
                else:
                    if self.past_index<self.past_index_max-1:
                        self.past_index+=1
                    else:
                        alt=0
                if alt:
                    self.path='Past configs/'+str(self.past_index)+'.txt'
                    with open(self.path, 'rb') as file:             
                        content = file.read()
                        self.load_content(content)                                      
                        self.modified=0
                        self.Window2.title('#'+str(self.past_index+1))
                
        # The main layout of the chat 
        def layout(self,name):
                self.path=''
                self.past_index_max=0
                self.past_index=0
                self.modified=0
                self.who=StringVar(value='we')
                self.crit=StringVar(value='10')
                self.crit.trace_variable('w', self.modify)
                self.res=StringVar(value='0')
                self.ac=StringVar(value='0')
                self.ic=StringVar(value='0')
                self.pc=StringVar(value='0')
                self.aa=StringVar(value='0')
                self.ia=StringVar(value='0')
                self.pa=StringVar(value='0')
                self.ad=[StringVar(value='0'),StringVar(value='0')]
                self.id=[StringVar(value='0'),StringVar(value='0')]
                self.pd=[StringVar(value='0'),StringVar(value='0')]
                self.sn=StringVar(value='s')
                self.displaymode=StringVar(value='bar')
                self.minST = 1               #ST = sleepTime
                self.maxST = 10
                self.minMST = 60             #MST = maxSleepTime
                self.maxMST = 100    
                self.incrementFraction = 1/10    #sometimes not used
                self.name = name 
                
                # to show chat window 
                self.deiconify() 
                self.title("Chatroom") 
                self.resizable(width = False, height = False) 
                self.configure(width = 800, height = 500, bg = 'black')

                self.sidebar = Frame(self, bg = 'black', width=200, height=500)
                self.sidebar.pack(expand = False, fill = 'both', side = 'left')
                
                self.sep = Label(self, bg = self.color)
                self.sep.pack(expand = False, fill = 'both', side = 'left')

                self.mainFrame = Frame(self, width=562, height=500)
                self.mainFrame.pack(expand=False, side='left')

                self.sep2 = Label(self, bg=self.color)
                self.sep2.pack(expand = False, fill = 'both', side = 'left')

                self.bttframe = Frame(self, width=30, height=500)
                self.bttframe.pack(expand=False, side='left')
                self.blocbtt= Button(self.bttframe, 
                                                    text = ">", 
                                                    font = "Consolas 12 bold", 
                                                    fg = "white",
                                                    bg='black',
                                                    command = lambda: self.blocswitch())
                self.blocbtt.place(relheight=1,relwidth=1)
                
                self.Window2=Toplevel()
                self.Window2.title("Roll") 
                self.Window2.resizable(width = False, height = False)
                self.Window2.configure(width = 1075, height = 530, bg = 'black')
                self.Window2.pack_propagate(0)

                self.menubar = Menu(self.Window2)
                self.Window2.config(menu=self.menubar)

                self.openmenu=Menu(self.menubar, tearoff=0)
                self.build_menu()

                self.label = Label(self.Window2,
                                                text='Select the players to roll',
                                                bg = 'black',
                                                fg='white',
                                                width=30,
                                                font = "Consolas 14 bold",
                                                pady=5) 
                self.label.pack(expand=True, fill="y", side="top")
                
                self.sidebaroll = Frame(self.Window2, bg = 'black', width=200, height=530)
                self.sidebaroll.pack(expand = False, fill = 'both', side = 'left')
                
                self.sep3 = Label(self.Window2, bg = self.color)
                self.sep3.pack(expand = False, fill = 'both', side = 'left')
        
                self.secFrame = Frame(self.Window2, width=662, height=530, bg='black')
                self.secFrame.pack(expand=True, fill = 'both', side='left')

                self.sep5 = Label(self.Window2, bg = self.color)
                self.sep5.pack(expand = False, fill = 'both', side = 'left')

                self.terFrame = Frame(self.Window2, width=200, height=530, bg='black')
                self.terFrame.pack(expand=True, fill = 'both', side='left')

                self.resor=[]

                self.selectRes=IntVar(value=0)

                self.labelBottom2 = Label(self.secFrame, bg = 'black', height = 79, width = 562)     
                self.labelBottom2.place(y=415) 

                self.line4 = Label(self.Window2, bg=self.color)
                self.line4.place(relwidth=1,relheight=0.012,y=36)

                self.stypebar= Label(self.secFrame, bg = 'black')
                self.stypebar.place(relwidth=1,relheight=0.05*50/53,y=1)

                self.sep4 = Label(self.Window2, bg = self.color)
                self.sep4.pack(expand = False, fill = 'both', side = 'left')

                self.antebar= Label(self.secFrame, bg = 'black')
                self.antebar.place(relwidth=1,relheight=0.14*50/53,rely=0.05*50/53)

                self.antebar2= Label(self.secFrame, bg = 'black')
                self.antebar2.place(relwidth=1,relheight=0.09*50/53,rely=0.19*50/53)

                self.line8 = Label(self.secFrame, bg=self.color)                 
                self.line8.place(relwidth=1,relheight=0.012*50/53,rely=0.05*50/53)

                self.interbar= Label(self.secFrame, bg = 'black')
                self.interbar.place(relwidth=1,relheight=0.17*50/53,rely=0.286*50/53)

                self.line5 = Label(self.secFrame, bg=self.color)                 
                self.line5.place(relwidth=1,relheight=0.012*50/53,rely=0.286*50/53)

                self.postbar= Label(self.secFrame, bg = 'black')
                self.postbar.place(relwidth=1,relheight=0.17*50/53,rely=0.456*50/53)

                self.line6 = Label(self.secFrame, bg=self.color)                 
                self.line6.place(relwidth=1,relheight=0.012*50/53,rely=0.456*50/53)
                
                self.resourcebar= Label(self.secFrame, bg = 'black')
                self.resourcebar.place(relwidth=1,relheight=0.25,rely=0.626*50/53)

                self.line3 = Label(self.secFrame, bg=self.color)                 
                self.line3.place(relwidth=1,relheight=0.012*50/53,rely=0.83)

                self.line7 = Label(self.secFrame, bg=self.color)                 
                self.line7.place(relwidth=1,relheight=0.012*50/53,rely=0.626*50/53)

                self.progresswindow=Toplevel(bg='black')
                self.progresswindow.title("Result")
                self.progresswindow.protocol("WM_DELETE_WINDOW", self.progresswindow.withdraw)

                self.dicewindow = Toplevel(bg='black')
                self.dicewindow.title("Result")
                self.dicewindow.protocol("WM_DELETE_WINDOW", self.dicewindow.withdraw)

                self.minRollLabel = Label(self.dicewindow, text='', fg='white', bg='black', font=('Consolas', 12))
                self.minRollLabel.pack()
                self.critRollLabel = Label(self.dicewindow, text='', fg='white', bg='black', font=('Consolas', 12))
                self.critRollLabel.pack()
                self.realRollLabel = Label(self.dicewindow, text='', fg='white', bg='black', font=('Consolas', 12))
                self.realRollLabel.pack()
                self.ResultLabel = Label(self.dicewindow, text='', bg='black', font=('Consolas', 25), fg=self.color)
                self.ResultLabel.pack()

                self.panel = Label(self.dicewindow, bg='black')
                self.panel.pack()

                self.minRollLabel2 = Label(self.progresswindow, text='', fg='white', bg='black', font=('Consolas', 12))
                self.minRollLabel2.pack()
                self.critRollLabel2 = Label(self.progresswindow, text='', fg='white', bg='black', font=('Consolas', 12))
                self.critRollLabel2.pack()
                self.realRollLabel2 = Label(self.progresswindow, text='', fg='white', bg='black', font=('Consolas', 12))
                self.realRollLabel2.pack()
                self.ResultLabel2 = Label(self.progresswindow, text='', bg='black', font=('Consolas', 25), fg=self.color)
                self.ResultLabel2.pack() 

                self.progress = ttk.Progressbar(self.progresswindow,style="black.Horizontal.TProgressbar", orient=HORIZONTAL, length = 402, mode='determinate')
                self.progress.pack(expand=False, padx=10, pady=10)
                self.progresswindow.withdraw()
                self.dicewindow.withdraw()

                self.barrap1=Label(self.progress, bg = 'orange')                 
                self.barrap2=Label(self.progress, bg = 'orange')                 
                self.barracrit1=Label(self.progress, bg = 'red')                 
                self.barracrit2=Label(self.progress, bg = 'red') 

                self.meBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'me',
                                                                        text = 'Me', 
                                                                        fg="white",
                                                                        bg='black',
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')
                
                self.hiddenBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'hidden',
                                                                        text = 'Hidden', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')
                self.weBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'we',
                                                                        text = 'We', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')

                self.youBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'you',
                                                                        text = 'You', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')

                self.sbtt=Radiobutton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 's',
                                                                        text = 'Sim', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')

                self.nbtt=Radiobutton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 'n',
                                                                        text = 'Não', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')

                self.sdtypelabel= Label(self.stypebar,fg="white",text='Send type: ',bg='black', width=11, font = 'Consolas 10 bold')
                self.messagelabel= Label(self.stypebar,fg="white",text='Message: ',bg='black', width=9, font = 'Consolas 10 bold')
                self.sdtypelabel.pack(side='left')
                self.weBtt.pack(side='left')
                self.meBtt.pack(side='left')
                self.youBtt.pack(side='left')
                self.hiddenBtt.pack(side='left')
                self.nbtt.pack(side='right')
                self.sbtt.pack(side='right')
                self.messagelabel.pack(side='right')

                self.antelabel= Label(self.antebar,fg="white",text='Anterior',bg='black', width=8, font = 'Consolas 12 bold')           
                self.antelabel.pack(side='top')

                #----------------------------------------

                self.valuelabel= Label(self.antebar2,fg="white",text='        Total value: ',bg= 'black', width=25, font = 'Consolas 10 bold')           
                self.valuelabel.pack(side='left')

                self.const=0
                self.value=StringVar(value='0')
                self.value.trace_variable('w', self.modify)
                self.value_entry = ttk.Entry(self.antebar2, font = "Consolas 12", width = 4, textvariable=self.value) 
                self.value_entry.pack(side='left')

                self.advanlabel= Label(self.antebar2,fg="white",text='  Total advantage: ',bg= 'black', width=19, font = 'Consolas 10 bold')           
                self.advanlabel.pack(side='left')
                
                self.advanint=0
                self.advan=StringVar(value='0')
                self.advan.trace_variable('w', self.modify)
                self.advan_entry = ttk.Entry(self.antebar2, font = "Consolas 12", width = 4, textvariable=self.advan) 
                self.advan_entry.pack(side='left')

                #----------------------------------------

                self.aconlabel= Label(self.antebar,fg="white",text='Constant: ',bg= 'black', width=10, font = 'Consolas 10 bold')           
                self.aconlabel.pack(side='left', padx=(36,0))
                
                self.acon = ttk.Spinbox(self.antebar,
                                    textvariable = self.ac,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.acon.pack(side='left')

                self.pixelVirtual = PhotoImage(width=1, height=1)

                self.aconbtt = Button(self.antebar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c",
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.antepaste(self.ac.get(), 1)) 
                
                self.aconbtt.pack(side='left', pady=(1, 0))

                self.aadvlabel= Label(self.antebar,fg="white",text='  Advantage: ',bg='black', width=13, font = 'Consolas 10 bold')           
                self.aadvlabel.pack(side='left')

                self.aadv = ttk.Spinbox(self.antebar,
                                    textvariable = self.aa,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.aadv.pack(side='left')

                self.aadvbtt = Button(self.antebar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.anteadvpaste(self.aa)) 
                
                self.aadvbtt.pack(side='left', pady=(1, 0))

                self.adlabel= Label(self.antebar,fg="white",text='  Dice: ',bg='black', width=8, font = 'Consolas 10 bold')           
                self.adlabel.pack(side='left')

                self.adic = ttk.Spinbox(self.antebar,
                                    textvariable = self.ad[0],
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.adic.pack(side='left')

                self.addlabel= Label(self.antebar,fg="white",text='d',bg='black', width=1, font = 'Consolas 10 bold')           
                self.addlabel.pack(side='left')

                self.adic2 = ttk.Spinbox(self.antebar,
                                    textvariable = self.ad[1],
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = 0,
                                    to = 100)

                self.adic2.pack(side='left')

                self.adicbtt = Button(self.antebar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.antepaste(self.ad[0].get(), self.ad[1].get())) 
                
                self.adicbtt.pack(side='left', pady=(1, 0))
                
                self.interlabel= Label(self.interbar,fg="white",text='Intermediate',bg='black', width=12, font = 'Consolas 12 bold')
                self.interlabel.pack(side='top')

                self.iconlabel= Label(self.interbar,fg="white",text='Constant: ',bg='black', width=10, font = 'Consolas 10 bold')
                self.iconlabel.pack(side='left', padx=(36,0))

                self.icon = ttk.Spinbox(self.interbar,
                                    textvariable = self.ic,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.icon.pack(side='left')

                self.iconbtt = Button(self.interbar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.interpaste(self.ic, "1")) 
                
                self.iconbtt.pack(side='left', pady=(1, 0))

                self.iadvlabel= Label(self.interbar,fg="white",text='  Advantage: ',bg='black', width=13, font = 'Consolas 10 bold')           
                self.iadvlabel.pack(side='left')

                self.iadv = ttk.Spinbox(self.interbar,
                                    textvariable = self.ia,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.iadv.pack(side='left')

                self.iadvbtt = Button(self.interbar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.interpaste(self.ia, "0")) 
                
                self.iadvbtt.pack(side='left', pady=(1, 0))

                self.idlabel= Label(self.interbar,fg="white",text='  Dice: ',bg='black', width=8, font = 'Consolas 10 bold')           
                self.idlabel.pack(side='left')

                self.idic = ttk.Spinbox(self.interbar,
                                    textvariable = self.id[0],
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.idic.pack(side='left')

                self.iddlabel= Label(self.interbar,fg="white",text='d',bg='black', width=1, font = 'Consolas 10 bold')           
                self.iddlabel.pack(side='left')

                self.idic2 = ttk.Spinbox(self.interbar,
                                    textvariable = self.id[1],
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = 0,
                                    to = 100)

                self.idic2.pack(side='left')

                self.idicbtt = Button(self.interbar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.interpaste(self.id[0], self.id[1])) 
                
                self.idicbtt.pack(side='left', pady=(1, 0))

                self.postlabel= Label(self.postbar,fg="white",text='Posterior',bg='black', width=9, font = 'Consolas 12 bold')
                self.postlabel.pack(side='top')

                self.pconlabel= Label(self.postbar,fg="white",text='Constant: ',bg='black', width=10, font = 'Consolas 10 bold')
                self.pconlabel.pack(side='left', padx=(36,0))

                self.pcon = ttk.Spinbox(self.postbar,
                                    textvariable = self.pc,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.pcon.pack(side='left')

                self.pconbtt = Button(self.postbar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.postpaste(self.pc, "1")) 

                self.pconbtt.pack(side='left', pady=(1, 0))

                self.padvlabel= Label(self.postbar,fg="white",text='  Advantage: ',bg='black', width=13, font = 'Consolas 10 bold')           
                self.padvlabel.pack(side='left')

                self.padv = ttk.Spinbox(self.postbar,
                                    textvariable = self.pa,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.padv.pack(side='left')

                self.padvbtt = Button(self.postbar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.postpaste(self.pa, "0")) 

                self.padvbtt.pack(side='left', pady=(1, 0))

                self.pdlabel= Label(self.postbar,fg="white",text='  Dice: ',bg='black', width=8, font = 'Consolas 10 bold')           
                self.pdlabel.pack(side='left')

                self.pdic = ttk.Spinbox(self.postbar,
                                    textvariable = self.pd[0],
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = -100,
                                    to = 100)

                self.pdic.pack(side='left')

                self.pddlabel= Label(self.postbar,fg="white",text='d',bg='black', width=1, font = 'Consolas 10 bold')           
                self.pddlabel.pack(side='left')

                self.pdic2 = ttk.Spinbox(self.postbar,
                                    textvariable = self.pd[1],
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = 0,
                                    to = 100)

                self.pdic2.pack(side='left')

                self.pdicbtt = Button(self.postbar, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            bg = 'black',
                                                            compound="c",
                                                            fg="white",
                                                            command = lambda : self.postpaste(self.pd[0], self.pd[1])) 

                self.pdicbtt.pack(side='left', pady=(1, 0))

                self.resourcebar1= Label(self.resourcebar, bg='black')
                self.resourcebar1.pack(side='left')
                self.resourcebar11= Label(self.resourcebar1, bg='black')
                self.resourcebar11.pack()
                self.resourcebar12= Label(self.resourcebar1, bg='black')
                self.resourcebar12.pack()
                self.resourcebar13= Label(self.resourcebar1, bg='black')
                self.resourcebar13.pack()


                self.sep5= Label(self.resourcebar, bg=self.color)
                self.sep5.pack(expand = False, fill = 'both', side = 'left')

                self.resourcebar2= Label(self.resourcebar, bg='black')
                self.resourcebar2.pack(side='left', expand=True, fill="both")

                self.sep6= Label(self.resourcebar, bg=self.color)
                self.sep6.pack(expand = False, fill = 'both', side = 'left')

                self.resourcebar3= Label(self.resourcebar, bg='black')
                self.resourcebar3.pack(side='left')
                
                self.reslabel= Label(self.resourcebar2,fg="white",text='Resource quantity:',bg='black', width=18, font = 'Consolas 12 bold')
                self.reslabel.pack()

                self.resbox = ttk.Spinbox(self.resourcebar2,
                                    textvariable = self.res,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = 0,
                                    to = 100)

                self.resbox.pack(pady=(14, 15))

                self.resbtt = Button(self.resourcebar2, 
                                                            text = "+", 
                                                            font = "Consolas 10 bold",
                                                            image=self.pixelVirtual,
                                                            width = 12,
                                                            height=15,
                                                            compound="c", 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda: self.resourcepaste(self.res)) 
                
                self.resbtt.pack()

                self.critlabel= Label(self.resourcebar11,fg="white",text=' Crit chance: ',bg='black', width=13, font = 'Consolas 12 bold')
                self.critlabel.pack()

                self.critbox = ttk.Spinbox(self.resourcebar12,
                                    textvariable = self.crit,
                                    font='Consolas 10',
                                    width = 3,
                                    from_ = 0,
                                    to = 100,
                                    increment = 10)

                self.critbox.pack(side="left")

                self.percelabel= Label(self.resourcebar12,fg="white",text='%',bg='black', width=1, font = 'Consolas 12 bold')
                self.percelabel.pack(side='left')

                self.dicebar= Label(self.resourcebar3,fg="white",text='Display mode:', bg='black', width=13, font = 'Consolas 12 bold')
                self.dicebar.pack(padx=(6, 0))

                self.barbtt=Radiobutton(self.resourcebar3, 
                                                                        variable = self.displaymode, 
                                                                        value = 'bar',
                                                                        text = 'Bar', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')
                
                self.barbtt.pack()

                self.dicebtt=Radiobutton(self.resourcebar3, 
                                                                        variable = self.displaymode, 
                                                                        value = 'dice',
                                                                        text = 'Dice', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Consolas 10 bold')
                
                self.dicebtt.pack()

                self.options = [
                "Chico",
                "Hide the pain",
                "Chorrindo",
                "Picardía",
                "Tobey"
                ]

                self.dice_style = StringVar()
                self.dice_style.set(self.options[0])

                self.dice_style_drop = ttk.Combobox(self.resourcebar13, textvariable=self.dice_style, values=self.options, state='readonly', width=14)
                self.dice_style_drop.pack()

                self.Window2.protocol("WM_DELETE_WINDOW", self.blocswitch)
                self.Window2.withdraw()

                self.playerBtts = []
                self.playerBtts2 = []
                self.roll_list=[]
                self.createSidebarButtons()

                self.labelHead = Label(self.mainFrame, bg = 'black', fg = "white", text = self.name, font = "Consolas 14 bold", pady=5) 
                self.labelHead.place(relwidth=1)

                self.line = Label(self.mainFrame, bg = self.color)                 
                self.line.place(relwidth=1,relheight=0.012,y=36)
                
                self.textCons = Text(self.mainFrame, 
                                                        width = 20, 
                                                        height = 2, 
                                                        bg = 'black',  
                                                        font = "Consolas 14", 
                                                        padx = 5, 
                                                        pady = 5) 
                self.textCons.place(y=42, relheight = 0.745, relwidth = 1)

                self.line2 = Label(self.mainFrame, bg = self.color)                 
                self.line2.place(relwidth=1,relheight=0.012,y=415)
                
                self.labelBottom = Label(self.mainFrame, bg = 'black', height = 79)     
                self.labelBottom.place(relwidth=1,y=421) 
                
                self.entryMsg = ttk.Entry(self.labelBottom, font = "Consolas 12") 
                self.entryMsg.place(width = 417, 
                                                height = 65, 
                                                y = 5, 
                                                x = 5) 
                self.entryMsg.focus() 
                
                self.buttonMsg = Button(self.labelBottom, 
                                                            text = "Send", 
                                                            font = "Consolas 12 bold", 
                                                            width = 10, 
                                                            bg = 'black',
                                                            fg = "white",
                                                            command = lambda : self.sendButton(self.entryMsg.get())) 
                self.buttonMsg.place(x = 428, 
                                            y = 5, 
                                            height = 66, 
                                            width = 126) 
                
                self.rollBtt = Button(self.sidebaroll, 
                                                        text = "Roll", 
                                                        font = "Consolas 14 bold", 
                                                        bg = 'black', fg="white",
                                                        command = lambda : self.rollerrola()) 
                self.rollBtt.place(relwidth=1, relheight=0.1,rely=0.9)
    
                self.allButton = Button(self.sidebar,
                                    fg = "white",
                                    bg = 'black', text = 'Select all',
                                    font = "Consolas 14 bold",
                                    command=lambda: self.AllClick())
                self.allButton.place(relwidth=1, relheight=0.1,rely=0.9)

                self.textCons.config(cursor = "arrow") 
                self.textCons.config(state = DISABLED) 

                self.bind_all("<MouseWheel>", self.on_mousewheel)
                self.bind('<Return>',(lambda event: self.sendButton(self.entryMsg.get())))
                self.bind("<Up>", self.up_down)
                self.bind("<Down>", self.up_down)
                self.protocol("WM_DELETE_WINDOW", self.on_closing)

                self.Window2.bind('<Return>',(lambda event: self.send_block()))
                self.Window2.bind("<Up>", self.up_down2)
                self.Window2.bind("<Down>", self.up_down2)
                
                self.option_add("*TCombobox*Listbox*Background", 'black')
                self.option_add("*TCombobox*Listbox*Foreground", 'white')
                self.option_add("*TCombobox*Listbox*selectBackground", 'black')
                self.option_add("*TCombobox*Listbox*selectForeground", 'white')
                self.s = ttk.Style()
                self.s.theme_use('default')
                self.s.configure("black.Horizontal.TProgressbar", foreground='black', background='black')
                #self.s.theme_use("classic")
                self.s.configure("TCombobox", arrowcolor="white")
                self.s.configure("TSpinbox", foreground="white", background= "black", fieldbackground="black", arrowcolor="white", selectbackground='white',
                             selectforeground='black')
                self.s.configure("TEntry", foreground="white", background= "black", fieldbackground="black", selectbackground='white',
                             selectforeground='black')
                self.s.map('TCombobox', fieldbackground=[('readonly', "black")])
                self.s.map('TCombobox', selectbackground=[('readonly', "black")])
                self.s.map('TCombobox', selectforeground=[('readonly', "white")])
                self.s.map('TCombobox', background=[('readonly', "black")])
                self.s.map('TCombobox', foreground=[('readonly', "white")])

                self.height=0
                self.indexs=[2]

        def on_mousewheel(self, event):
            self.textCons.yview_scroll(-1*int(event.delta/120), "units")

        def up_down(self, event):
                if event.keysym == 'Up':
                    if self.height!=0 and self.indexs:
                        self.height-=1
                        line=str(self.indexs[self.height])+'.'
                        line2=str(self.indexs[self.height+1]-1)+'.'
                        col=str(re.search('> |$', self.textCons.get(line+'0', line+"end")).start()+2)
                        self.entryMsg.focus()
                        self.entryMsg.delete(0, END) 
                        self.entryMsg.insert(END, self.textCons.get(line+col, line2+"end").replace('\n', ''))
                else:
                    if self.height<len(self.indexs)-2:
                        self.height+=1
                        line=str(self.indexs[self.height])+'.'
                        line2=str(self.indexs[self.height+1]-1)+'.'
                        col=str(re.search('> |$', self.textCons.get(line+'0', line+"end")).start()+2)
                        self.entryMsg.focus()
                        self.entryMsg.delete(0, END) 
                        self.entryMsg.insert(END, self.textCons.get(line+col, line2+"end").replace('\n', ''))
        
        # function to basically start the thread for sending messages 
        def sendButton(self, msg):
                self.msg=msg 
                self.entryMsg.delete(0, END) 
                self.snd= threading.Thread(target = self.sendMessage) 
                self.snd.start() 

        # function to receive messages 
        def receive(self):
           while True: 
                try:
                    message_header = client.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode(FORMAT).strip())
                    message = client.recv(message_length)
                    message=pickle.loads(message)
                    if type(message).__name__=='msg':
                        message_final = message.sender+' > '+message.content
                        # insert messages to text box 
                        self.textCons.config(state = NORMAL)
                        self.textCons.tag_configure(message.cor,foreground=message.cor)
                        textlis=wrap(message_final,width=42)
                        for u in range(len(textlis)):
                            if textlis[u].startswith('\j'):
                                textlis[u]=textlis[u].replace('\j','',1)
                                textlis[u]=textlis[u].rstrip()
                            else:
                                textlis[u]=textlis[u].strip()
                        textlis.append('')
                        current_line=int(self.textCons.index(END)[:-2])-1
                        for u in range(len(textlis)-1):
                            if textlis[u]=='':
                                self.textCons.insert(END,'\n')
                            elif textlis[u+1]!='' and not textlis[u+1].startswith(' '):
                                linha=justify(textlis[u],42)
                                self.textCons.insert(END, linha+'\n',message.cor)
                            else:
                                self.textCons.insert(END, textlis[u]+'\n',message.cor)
                        self.textCons.insert(END,'\n')
                        self.textCons.see(END)
                        self.textCons.config(state = DISABLED)
                        end_line=int(self.textCons.index(END)[:-2])-1
                        self.indexs.pop()
                        self.indexs+=[current_line, end_line]
                        self.height=len(self.indexs)-1
                    elif type(message).__name__=='dict':
                        playerFlag = True
                        for i in range(len(self.players)):
                            if self.players[i]['name'] == message['name']:
                                self.players.pop(i)
                                playerFlag = False
                                break
                        if playerFlag:
                            message['selected'] = False
                            self.players.append(message)
                        self.createSidebarButtons()                        
                    elif type(message).__name__=='status':                                    
                        if not self.Window2.winfo_viewable():
                            self.Window2.deiconify()
                            self.blocbtt.config(text='<')
                        else:
                            self.Window2.deiconify()
                        self.roll_list=[]
                        if message.num!=0:
                            self.label.config(text='Restam '+str(message.num)+" rolagens")
                        else:
                            self.label.config(text='Select the players to roll')
                    else:
                        if not message or type(message[0]).__name__!='res':
                            self.players = []
                            for dics in message:
                                dics['selected'] = False
                                self.players.append(dics)
                            break
                        else:
                            possibs=Toplevel(bg='black')
                            possibs.title('Possibildiades')
                            possibs.resizable(width = False, height=False)
                            m=max(max(len(i.mods) for i in message), 10)
                            w=round(68+m*1.44)
                            aux_mor=Label(possibs, bg='black', width = w, height = 1)
                            aux_mor.pack_propagate(0)
                            aux_mor.pack()
                            aux_1=text=Label(aux_mor, bg='black', text='% of f->s+|', fg='white', font=('Consolas', 12))
                            aux_1.pack(side='left')
                            aux_12=text=Label(aux_mor, bg='black', text='% of s->cs|', fg='white', font=('Consolas', 12))
                            aux_12.pack(side='left')
                            aux_13=text=Label(aux_mor, bg='black', text='% of cf->f+|', fg='white', font=('Consolas', 12))
                            aux_13.pack(side='left')
                            aux_2=text=Label(aux_mor, bg='black', text='Net advantage|', fg='white', font=('Consolas', 12))
                            aux_2.pack(side='left')
                            aux_3=text=Label(aux_mor, bg='black', text='Recursos', fg='white', font=('Consolas', 12))
                            aux_3.pack(side='left')
                            p_old, crit_old, r, resultStr=self.transl(message[0])
                            ahead=1
                            ahead_c=1
                            ahead_cf=1
                            prob_old=0
                            prob_old_c=0
                            prob_old_cf=0
                            poss_str=''
                            p_last, crit_last, r, resultStr=self.transl(message[-1])   
                            for i in message:
                                aux_mor=Label(possibs, bg='black', width = w, height = 1)
                                aux_mor.pack_propagate(0)
                                aux_mor.pack()
                                p, crit, r, resultStr=self.transl(i)
                                aux=(p_old!=p)
                                prob_old, bol=self.calc_change(p_old, p, r, prob_old)
                                prob_old_c, bol_c=self.calc_change(crit_old, crit, r, prob_old_c)
                                prob_old_cf, bol_cf=self.calc_change(p_old/10, p/10, r, prob_old_cf)
                                if ahead and aux:
                                    if bol:
                                        ahead=0
                                        if not self.calc_change(crit, crit_last, r, prob_old_c)[1] and not bol_c:
                                            ahead_c=0
                                        if not self.calc_change(p/10, p_last/10, r, prob_old_cf)[1] and not bol_cf:
                                            ahead_cf=0
                                    poss_str="{:.1e}".format(prob_old)
                                else:
                                    poss_str=''
                                aux_1=Label(aux_mor, bg='black', text=poss_str+(10-len(poss_str))*' '+'|', fg='white', font=('Consolas', 12))
                                if ahead_c and aux: 
                                    if bol_c:
                                        ahead_c=0
                                        if not self.calc_change(p, p_last, r, prob_old)[1] and not bol:
                                            ahead=0
                                            aux_1.config(text='          |')
                                        if not self.calc_change(p/10, p_last/10, r, prob_old_cf)[1] and not bol_cf:
                                            ahead_cf=0
                                    poss_str="{:.1e}".format(prob_old_c)
                                else:
                                    poss_str=''
                                aux_12=Label(aux_mor, bg='black', text=poss_str+(10-len(poss_str))*' '+'|', fg='white', font=('Consolas', 12))
                                if ahead_cf and aux:
                                    if bol_cf:
                                        ahead_cf=0
                                        if not self.calc_change(p, p_last, r, prob_old)[1] and not bol:
                                            ahead=0
                                            aux_1.config(text='          |')
                                        if not self.calc_change(crit, crit_last, r, prob_old_c)[1] and not bol_c:
                                            ahead_c=0
                                            aux_12.config(text='          |')
                                    poss_str="{:.1e}".format(prob_old_cf)
                                else:
                                    poss_str=''
                                aux_13=Label(aux_mor, bg='black', text=poss_str+(11-len(poss_str))*' '+'|', fg='white', font=('Consolas', 12))
                                
                                aux_1.pack(side='left')
                                
                                aux_12.pack(side='left')
                                
                                aux_13.pack(side='left')
                                
                                aux_2=Label(aux_mor, bg='black', text='+'*(i.advan>=0)+str(i.advan)+11*' '+'|', fg='white', font=('Consolas', 12))
                                aux_2.pack(side='left')
                                
                                resButton = Button(aux_mor,
                                                fg = 'white',
                                                bg = 'black', text = i.mods[:-2]+'N/A'*(not i.mods[:-2]),
                                                font = "Consolas 12 bold",
                                                command= lambda p=p, crit=crit, r=r, resultStr=resultStr: threading.Thread(target = self.displayres, args=[p, crit, r, resultStr]).start())
                                resButton.pack(side='left')

                                p_old=p
                                crit_old=crit
                            aux_mor=Label(possibs, bg='black', width = w, height = 1)
                            aux_mor.pack()
                            resButton = Button(possibs,
                                                fg = 'white',
                                                bg = 'black', text = 'Show results',
                                                font = "Consolas 14 bold",
                                                command=partial(self.show_res, possibs, message))
                            resButton.pack(pady=(0, 12))                            
                except Exception:
                    print(traceback.format_exc())
                    if self.not_closing:
                        self.on_closing()
                    else:
                        break

        def calc_change(self, old, new, r, prob_old):
            old*=100
            new*=100
            if prob_old==1:
                return (1, 0)
            bol, prob=self.prob_func(old, new, r)
            return (prob, bol)

        def prob_func(self, old, new, r):
            mn=min(old, new)/2000
            mx=max(old, new)/2000
            interval=mx-mn
            r/=20
            aux=mx/(mn+mx)
            prob=4*(interval-1)/(3*interval-4)
            prob_old=prob
            if r<=mn or r>mx: 
                prob=1-prob
            bol=(random.random()<=prob)
            if bol:
                prob=4/5
            else:
                prob=interval*(1-prob_old)/(prob_old*(1-interval)+(1-prob_old)*interval)
            return (bol, prob)

        def show_res(self, possibs, message):
            try:
                self.possibs.destroy()
            except Exception:
                print(traceback.format_exc())
            p_old, crit_old, r, resultStr=self.transl(message[0])
            self.possibs=Toplevel(bg='black')
            self.possibs.title('Possibildiades')
            self.possibs.resizable(width = False, height=False)
            m=max(max(len(i.mods) for i in message), 11)
            w=round(42+(m-1)*1.44)
            aux_mor=Label(self.possibs, bg='black', width = w, height = 1)
            aux_mor.pack_propagate(0)
            aux_mor.pack()
            aux_1=text=Label(aux_mor, bg='black', text='Resultado      |', fg='white', font=('Consolas', 12))
            aux_1.pack(side='left')
            aux_2=text=Label(aux_mor, bg='black', text='Net advantage|', fg='white', font=('Consolas', 12))
            aux_2.pack(side='left')
            aux_3=text=Label(aux_mor, bg='black', text='Recursos', fg='white', font=('Consolas', 12))
            aux_3.pack(side='left')
            for i in message:
                p, crit, r, resultStr=self.transl(i)
                aux_mor=Label(self.possibs, bg='black', width = w, height = 1)
                aux_mor.pack_propagate(0)
                aux_mor.pack()
                aux_1=text=Label(aux_mor, bg='black', text=resultStr+(15-len(resultStr))*' '+'|', fg='white', font=('Consolas', 12))
                aux_1.pack(side='left')
                aux_2=text=Label(aux_mor, bg='black', text='+'*(i.advan>=0)+str(i.advan)+11*' '+'|', fg='white', font=('Consolas', 12))
                aux_2.pack(side='left')
                aux_3=text=Label(aux_mor, bg='black', text=i.mods[:-2], fg='white', font=('Consolas', 12))
                aux_3.pack(side='left')

        def rec(self, tot, num, dice_list, index):
                if index!=len(dice_list)-1:
                    if dice_list[index][1]>1:
                        dic={}
                        number=abs(dice_list[index][0])
                        sgn=np.sign(dice_list[index][0])
                        tt_aux=math.factorial(number)
                        for k in list(itertools.combinations_with_replacement([i for i in range(1, dice_list[index][1]+1)], number)):
                            tt=tt_aux
                            for i in range(1, dice_list[index][1]+1):
                                tt/=math.factorial(k.count(i))
                            dic_aux=self.rec(tot+sgn*sum(k), num+tt, dice_list, index+1)
                            for i in dic_aux.keys():
                                if i in dic.keys():
                                    dic[i]+=dic_aux[i]
                                else:
                                    dic[i]=dic_aux[i]
                        return dic
                    else:
                        return self.rec(tot+dice_list[index][0], num, dice_list, index+1)
                else:
                    if dice_list[index][1]>1:
                        dic={}
                        number=abs(dice_list[index][0])
                        sgn=np.sign(dice_list[index][0])
                        tt_aux=math.factorial(number)
                        for k in list(itertools.combinations_with_replacement([i for i in range(1, dice_list[index][1]+1)], number)):
                            aux=sgn*sum(k)
                            tt=tt_aux
                            for i in range(1, dice_list[index][1]+1):
                                tt/=math.factorial(k.count(i))
                            if tot+aux in dic.keys():
                                dic[tot+aux]+=num+tt
                            else:
                                dic[tot+aux]=num+tt
                        return dic
                    else:
                        return {tot+dice_list[index][0]: num}
                    
        def rolldic(self, stri):
            try:
                stri=re.search("'.*?'", stri).group().replace("'","").replace(' ', '')
                stri_con=re.findall('-.*?(?=-|\+|$)', stri)+re.findall('(?=^|\+)(?!-).*?(?=-|\+|$)', stri)
                dice_list=[]
                roll=0
                for i in stri_con:
                    dice=re.split('d', i)
                    if dice[0]:
                        dice[0]=int(dice[0])
                        if len(dice)>1:
                            dice[1]=int(dice[1])
                            sgn=np.sign(dice[0])
                            for j in range(sgn*dice[0]):
                                roll+=sgn*random.randint(1, dice[1])
                            dice_list.append((dice[0], dice[1]))
                        else:
                            roll+=dice[0]
                            dice_list.append((dice[0], 1))
                dice_list=sorted(dice_list, key=lambda tup: abs(tup[0]))
                tot=0
                num=0
                mini=0
                maxi=0
                for i in dice_list:
                    if i[0]>0:
                        mini+=i[0]
                        maxi+=i[0]*i[1]
                    else:
                        mini+=i[0]*i[1]
                        maxi+=i[0]
                dic=OrderedDict(sorted(self.rec(tot, num, dice_list, 0).items(), reverse=True))
                total=sum(dic.values())
                values=[x/total for x in dic.values()]
                tot=0
                for i in range(len(values)):
                    tot+=values[i]
                    values[i]=tot
                try:
                    self.possi.destroy()
                except Exception:
                    print(traceback.format_exc())
                self.possi=Toplevel(bg='black')
                self.possi.resizable(width = False, height=False)
                self.possi.configure(width = 500, height = 300)
                self.possi.pack_propagate(0)
                self.possi.title("Dice roll")
                frame=Label(self.possi, bg='black')
                frame.pack()

                f = Figure(facecolor='k')
                
                canvas = FigureCanvasTkAgg(f, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack()
                
                p=f.gca()
                p.set_facecolor('k')
                p.set(xlabel='r', ylabel='p(x>=r)')
                p.xaxis.label.set_color('w')
                p.yaxis.label.set_color('w')
                p.tick_params(axis='x', colors='w')
                p.tick_params(axis='y', colors='w')
                p.bar(dic.keys(), values, color='w')
                rolls=[random.randint(mini, maxi)]
                p.set_title(' ')

                for i in range(random.randint(5, 10)):
                    c=random.randint(mini, maxi)
                    while c==rolls[-1]:
                        c=random.randint(mini, maxi)
                    rolls.append(c)
                if rolls[-1]!=roll:
                    rolls.append(roll)
                l=len(rolls)
                for j in range(l):
                    i=rolls[j]
                    p.bar(i, values[mini-i-1], color=self.color)
                    f.tight_layout()

                    canvas0 = FigureCanvasTkAgg(f, master=frame)
                    canvas0.draw()
                    canvas.get_tk_widget().pack_forget()
                    canvas0.get_tk_widget().pack()
                    sleep(0.5)
                    if j!=l-1:
                        p.bar(i, values[mini-i-1], color='w')
                        f.tight_layout()

                        canvas = FigureCanvasTkAgg(f, master=frame)
                        canvas.draw()
                        canvas0.get_tk_widget().pack_forget()
                        canvas.get_tk_widget().pack()
                        sleep(0.3)
                p.set_title('r='+str(roll)+', p(r)='+"{:.1e}".format(dic[roll]/total)+', p(x>=r)='+"{:.1e}".format(values[mini-roll-1]), color='w')
                f.tight_layout()
                
                canvas = FigureCanvasTkAgg(f, master=frame)
                canvas.draw()
                canvas0.get_tk_widget().pack_forget()
                canvas.get_tk_widget().pack()
            except Exception:
                print(traceback.format_exc())
                
        # function to send messages 
        def sendMessage(self):
            destinatários = []
            for player in self.players:
                if player['selected']:
                    destinatários.append(player['name'])
            message_sent = pickle.dumps(msg(destinatários, self.msg))
            message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(message_sent_header+message_sent)
            try:
                plt.close()
            except Exception:
                print(traceback.format_exc())
            self.rldc = threading.Thread(target=self.rolldic(self.msg)) 
            
# create a GUI class object
g = GUI()
g.mainloop()
