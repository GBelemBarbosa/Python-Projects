# import all the required modules 
import socket 
import threading
from tkinter import *
from tkinter import font, ttk, filedialog, messagebox
import customtkinter as ctk
import random
import numpy as np
from datetime import datetime
from colour import Color
from time import sleep
from tkinter.colorchooser import *
import sys
#from PyQt5 import QtWidgets, QtCore, QtGui #pyqt stuff

#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

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

class IntSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 from_: int = -100,
                 to_: int = 100,
                 color: str = None,
                 variable: StringVar = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.from_ = from_
        self.to_ = to_
        self.variable = variable

        self.configure(fg_color="gray20")  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="▼", width=height-6, border_color=color, border_width=2,
                                                       fg_color="gray25", hover_color="gray35", command = self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), border_width=0, fg_color="gray25")
        self.entry.grid(row=0, column=1, columnspan=1, padx=10/3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="▲", width=height-6, border_color=color, border_width=2,
                                                  fg_color="gray25", hover_color="gray35", command = self.add_button_callback)
        self.add_button.grid(row=0, column=2)

        # default value
        self.entry.insert(0, self.variable.get())

    def add_button_callback(self):
        try:
            value = min(int(self.entry.get()) + self.step_size, self.to_)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.variable.set(value)
        except ValueError:
            return

    def subtract_button_callback(self):
        try:
            value = max(int(self.entry.get()) - self.step_size, self.from_)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.variable.set(value)
        except ValueError:
            return

    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.variable.set(value)

class premod:
    def __init__(self, adv, const):
        self.adv=adv
        self.const=const

class posmod:
    def __init__(self, typ, timing, num1, num2):
        self.typ=typ
        self.timing=timing
        self.value=num1*(num2+1)*25*(typ!="adv")+num1*(typ=="adv")
        self.subresName=timing+" Advan"*(typ=="adv")+" "+"+"*(num1>0)+str(num1)+(typ=="dice")*("d"+str(num2))

class resource:
    def __init__(self, qnt, resName):
        self.qnt=qnt
        self.resName=resName
        self.mainFrame=Frame()
        self.mainButton=Frame()
        self.listSubres=[]
        self.subButtons=[]
        self.qntLabel=Frame()
        self.deleteButton=Frame()

class resourceSend:
    def __init__(self, qnt, resName, listSubres):
        self.qnt=qnt
        self.resName=resName
        self.listSubres=listSubres

class bloco:
    def __init__(self, premods, posmods, sn, crit, mini):
        self.premods=premods
        self.posmods=posmods
        self.sn=sn
        self.crit=crit
        self.min=mini

class status:
    def __init__(self, num):
        self.num=num

class msg:
    def __init__(self, destiny, content):
        self.destiny=destiny
        self.content=content

class roll:
    def __init__(self, receiver, who):
        self.receiver=receiver
        self.who=who

class res:
    def __init__(self, p, crit, r, adv):
        self.p=p
        self.r=r
        self.crit=crit
        self.adv=adv
        self.mods=''

    def __lt__(self, other):
         return self.p < other.p

# GUI class for the chat 
class GUI(ctk.CTk): 

        # constructor method 
        def __init__(self):
                super().__init__()
                
                self.not_closing=1
                self.rescale=8
                
                # chat window which is currently hidden
                self.configure(fg_color="gray15")
                self.withdraw()

                for filename in os.listdir('Past configs/'):
                    os.remove('Past configs/'+filename)
                
                # login window 
                self.login = ctk.CTkToplevel(fg_color="gray15") 
                # set the title 
                self.login.title("Login") 
                self.login.geometry("400x115")
                self.login.grid_columnconfigure(0, weight=1)
                self.login.resizable(width = False, height = False)
                self.login.protocol("WM_DELETE_WINDOW", self.on_closing)  

                # create a Label
                self.plsFrame=ctk.CTkFrame(self.login, fg_color="gray20")
                self.plsFrame.grid_columnconfigure(0, weight=1)
                self.plsFrame.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")
                
                self.pls = ctk.CTkLabel(self.plsFrame, text = "Please login to continue") 
                self.pls.grid(row=0, column=0)
                
                # create a Label 
                self.labelName = ctk.CTkLabel(self.login) 
                self.labelName.grid(row=1, column=0)
                self.labelName.grid_rowconfigure(0, weight=1)
                
                # create a entry box for 
                # typing the message 
                self.entryName = ctk.CTkEntry(self.labelName, fg_color="gray20", border_width=0, placeholder_text_color="gray30", placeholder_text="Username") 
                self.entryName.grid(row=0, column=0)
                self.entryName.bind('<Return>',(lambda event: self.goAhead(self.entryName.get())))
                
                # set the focus of the curser 
                #self.entryName.after(20, self.entryName.focus)
                
                # create a Continue Button 
                # along with action 
                self.go = ctk.CTkButton(self.login, 
                                                text = "Login", 
                                                fg_color="gray20", hover_color="gray30", command = lambda: self.goAhead(self.entryName.get()))
                self.go.grid(row=2, column=0, pady=self.rescale) 
                

        def askDice(self, name):
            self.login2 = ctk.CTkToplevel(fg_color="gray15") 
            self.login2.title("Display modes")
            self.login2.geometry('400x132')
            self.login2.grid_columnconfigure(0, weight=1)
            self.login2.resizable(width = False, height = False)
            self.login2.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.login2.bind('<Return>',(lambda event: self.goAhead2(name)))

            self.displayFrame=ctk.CTkFrame(self.login2, fg_color="gray20")
            self.displayFrame.grid_columnconfigure(0, weight=1)
            self.displayFrame.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")
                
            self.display = ctk.CTkLabel(self.displayFrame, text="Display mode") 
            self.display.grid(row=0, column=0)

            self.displaymode=StringVar(value='bar')

            self.barbtt=ctk.CTkRadioButton(self.login2, 
                                                                    variable = self.displaymode, 
                                                                    value = 'bar',
                                                                    text = ' Bar', fg_color=self.color, border_color="gray20", hover_color=self.color)
            self.barbtt.grid(row=1, column=0, padx=(44, 0))

            self.dicebtt=ctk.CTkRadioButton(self.login2, 
                                                                    variable = self.displaymode, 
                                                                    value = 'dice',
                                                                    text = 'Dice', fg_color=self.color, border_color="gray20", hover_color=self.color)
            self.dicebtt.grid(row=2, column=0, padx=(44, 0)) 
            
            # create a Continue Button 
            # along with action 
            self.go2 = ctk.CTkButton(self.login2, 
                                            text = "Continue", border_color=self.color, border_width=2, 
                                            fg_color="gray20", hover_color="gray30", command = lambda: self.goAhead2(name))
            self.go2.grid(row=3, column=0, pady=self.rescale)
                
            self.options = [
                "Chico",
                "Picardía",
                "Pascal",
                "Tobey",
                "Hide the pain"
                ]

            self.dice_style = StringVar()
            self.dice_style.set(self.options[0])
                                
        def goAhead2(self, name):
            if self.displaymode.get()=='dice':
                self.login2.destroy()
                self.login3 = ctk.CTkToplevel(fg_color="gray15") 
                self.login3.title("Critical styles")
                self.login3.geometry('400x115')
                self.login3.grid_columnconfigure(0, weight=1)
                self.login3.resizable(width = False, height = False)
                self.login3.protocol("WM_DELETE_WINDOW", self.on_closing)
                self.login3.bind('<Return>',(lambda event: self.goAhead3(name)))

                self.displayCritical=ctk.CTkFrame(self.login3, fg_color="gray20")
                self.displayCritical.grid_columnconfigure(0, weight=1)
                self.displayCritical.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.dicebar= ctk.CTkLabel(self.displayCritical, text='Critical style')
                self.dicebar.grid(row=0, column=0)
                
                self.dice_style_drop = ctk.CTkComboBox(self.login3, variable=self.dice_style, values=self.options, state='readonly', dropdown_hover_color="gray25", fg_color="gray20", border_width=0, button_color="gray25")
                self.dice_style_drop.grid(row=1, column=0)

                self.go3 = ctk.CTkButton(self.login3, 
                                            text = "Continue", border_color=self.color, border_width=2,
                                            fg_color="gray20", hover_color="gray30", command = lambda: self.goAhead3(name)) 
                self.go3.grid(row=2, column=0, pady=self.rescale)
            else:
                self.goAhead3(name)

        def goAhead3(self, name):
            try:
                self.login3.destroy()
            except:
                self.login2.destroy()
            self.receive()
            self.layout(name)
            # the thread to receive messages 
            self.rcv = threading.Thread(target=self.receive) 
            self.rcv.start()
            
        def goAhead(self, name):
            my_username = name.encode(FORMAT)
            my_username_header = f"{len(my_username):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(my_username_header + my_username)
            server_message_header=client.recv(HEADER_LENGTH)
            server_message_length = int(server_message_header.decode(FORMAT).strip())
            server_message=client.recv(server_message_length).decode(FORMAT)
            if server_message=='ok':
                try:
                    self.color=askcolor(color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), title ="Escolha a cor do seu usuário")[1]
                    color=self.color.encode(FORMAT)
                except:
                    self.on_closing()
                color_header=f"{len(color):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(color_header + color)
                self.login.destroy()
                self.askDice(name)
            else:
                self.pls.configure(text=server_message)

        def onPlayerClick(self, c):
            if self.players[c]['selected']:
                self.playerBtts[c].configure(fg_color="gray25")
            else:
                self.playerBtts[c].configure(fg_color="gray35")
            self.players[c]['selected'] = not self.players[c]['selected']

        def onPlayerSelec(self, c):
            tempLabel = ctk.CTkButton(self.label,
                                                    fg_color="gray25",
                                                    hover=False,
                                                    border_color=self.players[c]['color'],
                                                    border_width=2,
                                                    text = self.players[c]['name'])
            self.playerSelected.append(tempLabel)
            self.playerSelected[-1].grid(row=len(self.playerSelected)-1, column=0, pady=(0,self.rescale), sticky="ew")

        def rollerrola(self):
            message_sent = pickle.dumps(roll(self.roll_list,self.who.get()))
            message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(message_sent_header+message_sent)
            self.roll_list=[]
            for playerLabel in self.playerSelected:
                playerLabel.destroy()
                            
        def AllClick(self):
            if self.allButton.cget('text')=='Select all':
                self.allButton.configure(text='Exclude all')
                for c in range(len(self.playerBtts)):
                    self.playerBtts[c].configure(fg_color='gray95')
                    self.players[c]['selected'] = True
            else:
                self.allButton.configure(text='Select all')
                for c in range(len(self.playerBtts)):
                    self.playerBtts[c].configure(fg_color='gray85')
                    self.players[c]['selected'] = False

        def createSidebarButtons(self):
            for playerBtt in self.playerBtts:
                playerBtt.destroy()
            for playerBtt in self.playerBtts2:
                playerBtt.destroy()

            self.playerBtts = []
            self.playerBtts2 = []

            for i in range(len(self.players)):
                tempButton = ctk.CTkButton(self.sidebar,
                                                fg_color="gray25", hover_color="gray35",
                                                border_color=self.players[i]['color'],
                                                border_width=2,
                                                text = self.players[i]['name'],
                                                command=lambda c=i: self.onPlayerClick(c))
                self.playerBtts.append(tempButton)
                self.playerBtts[-1].grid(row=i, column=0, pady=(0,self.rescale), sticky="ew")

                tempButton = ctk.CTkButton(self.sidebaroll,
                                                    fg_color="gray25", hover_color="gray35",
                                                    border_color=self.players[i]['color'],
                                                    border_width=2,
                                                    text = self.players[i]['name'],
                                                    command=lambda c=i: self.onPlayerSelec(c))
                self.playerBtts2.append(tempButton)
                self.playerBtts2[-1].grid(row=i, column=0, pady=(0,self.rescale), sticky="ew")

        def transl(self, res):
            p, crit, r=(2000-res.p)/100, (2000-res.crit)/100, (2000-res.r)/100
            if (r >= p):
                if(r >= crit):
                    resultStr = "Critical success"
                else:
                    resultStr = "Success"
            else:
                if (r<p/2):
                    resultStr = "Critical fail"
                else:
                    resultStr = "Fail"
            return p, crit, r, resultStr
                
        def displayres(self, p, crit, r, resultStr, send_type):
            if send_type:
                if not self.hiddenres.winfo_viewable():
                    self.hiddenres.deiconify()
                if self.displaymode.get()=='bar':    
                    if self.progresswindow.winfo_viewable():
                        self.progresswindow.withdraw()
                else:
                    if self.dicewindow.winfo_viewable():
                        self.dicewindow.withdraw()
                self.hiddenres.focus()

                opposite_message=(send_type=='No')*'Yes'+(send_type=='Yes')*'No'
                aux=(resultStr=="Success" or resultStr=="Critical success")*send_type+(resultStr=="Fail" or resultStr=="Critical fail")*opposite_message
                self.hidden_label.configure(text=aux)
            else:
                if self.displaymode.get()=='bar':
                    self.progress['value']=0
                    self.InfoLabel2.configure(text = "Success: "+str(p)+"\nCritical success: "+str(crit)+"\n")
                    self.ResultLabel2.configure(text = "")

                    p=round(25*p)-1
                    r_bar=max(0, 1.02*r/20-0.02)
                    crit=round(25*crit)-1

                    if not self.progresswindow.winfo_viewable():
                        self.progresswindow.deiconify()
                    self.progresswindow.focus()
                    
                    self.barracrit1.place(relwidth=0.0025, x=crit-1)
                    self.barrap1.place(relwidth=0.0025, x=p-1)
                    self.barracrit2.place(relwidth=0.0025, x=crit+1)
                    self.barrap2.place(relwidth=0.0025, x=p+1)

                    x=0;
                    n=random.randint(2, 15)
                    for i in range(159):
                        sleep(0.01)
                        x+=0.00625
                        y=r_bar*n*x/(1+(n-1)*x)
                        self.progress.set(value=y)
                    
                    self.ResultLabel2.configure(text = resultStr)
                    self.InfoLabel2.configure(text = self.InfoLabel2.cget("text")+"Rolled: "+str(r))
                else:
                    self.InfoLabel.configure(text = "Success: "+str(p)+"\nCritical success: "+str(crit)+"\n")
                    self.ResultLabel.configure(text = "")

                    if not self.dicewindow.winfo_viewable():
                        self.dicewindow.deiconify()
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
                        img = img.convert("RGBA")
                        self.img = ctk.CTkImage(img, size=(250,250))
                        self.panel.configure(image = self.img)
                        
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

                    if resultStr=="Critical success":
                        img = Image.open("Dice_Images/20"+self.dice_style.get()+'.png')
                    elif resultStr=="Critical fail":
                        img = Image.open("Dice_Images/0"+self.dice_style.get()+'.png')
                    else:
                        img = Image.open("Dice_Images/"+str(roundedRealDiceRoll)+".png")
                    img = img.convert("RGBA")
                    self.img = ctk.CTkImage(img, size=(250,250))
                    self.panel.configure(image = self.img)

                    self.ResultLabel.configure(text = resultStr)
                    self.InfoLabel.configure(text = self.InfoLabel.cget("text")+"Rolled: "+str(r))

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
                self.blocbtt.configure(text='◄')
            else:
                self.Window2.withdraw()
                self.blocbtt.configure(text='►')

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

        def build_resor(self):  
            self.aFrame=ctk.CTkFrame(self.terFrame, fg_color="gray25")
            self.aFrame.columnconfigure((0,1) , weight=1)
            self.aFrame.grid(row=0, column=0, sticky="ew", pady=(0,self.rescale))

            self.anteriorLabel=ctk.CTkLabel(self.aFrame, text="Anterior", fg_color="gray30", corner_radius=6)
            self.anteriorLabel.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale, columnspan=2)

            self.aconLabel=ctk.CTkLabel(self.aFrame, text="Constant", fg_color="gray30", corner_radius=6)
            self.aconLabel.grid(row=1, column=0, sticky="w", padx=(self.rescale,0), pady=(0,self.rescale))

            self.aadvLabel=ctk.CTkLabel(self.aFrame, text="Advantage", fg_color="gray30", corner_radius=6)
            self.aadvLabel.grid(row=2, column=0, sticky="w", padx=(self.rescale,0), pady=(0,self.rescale))

            self.acontotal=ctk.CTkLabel(self.aFrame, text=(self.premod.const>0)*"+"+str(self.premod.const), fg_color="gray30", corner_radius=6, width=36)
            self.acontotal.grid(row=1, column=1, sticky="e", padx=(0,self.rescale), pady=(0,self.rescale))

            self.aadvtotal=ctk.CTkLabel(self.aFrame,text=(self.premod.adv>0)*"+"+str(self.premod.adv), fg_color="gray30", corner_radius=6, width=36)
            self.aadvtotal.grid(row=2, column=1, sticky="e", padx=(0,self.rescale), pady=(0,self.rescale))
            
            for i in range(len(self.resor)):
                aux=("Resource #"+str(i+1))*(self.resor[i].resName.replace(" ", "")=="")+self.resor[i].resName*(self.resor[i].resName.replace(" ", "")!="")
                self.resor[i].mainFrame=ctk.CTkFrame(self.terFrame, fg_color="gray25")
                self.resor[i].mainFrame.columnconfigure((0,1) , weight=1)
                self.resor[i].mainFrame.grid(row=i+1, column=0, sticky="ew", pady=(0,self.rescale))

                self.resor[i].mainButton=ctk.CTkRadioButton(self.resor[i].mainFrame, 
                                                                        variable = self.selectRes, 
                                                                        value = i+1,
                                                                        text = aux, fg_color=self.color, bg_color="gray25", border_color="gray30", hover_color=self.color)
                self.resor[i].mainButton.grid(row=0, column=0, sticky="w", padx=self.rescale, pady=self.rescale)

                self.resor[i].qntLabel=ctk.CTkLabel(self.resor[i].mainFrame, text=self.resor[i].qnt, fg_color="gray30", corner_radius=6)
                self.resor[i].qntLabel.grid(row=0, column=1, sticky="e", padx=(0,self.rescale), pady=self.rescale)
    
                self.resor[i].subButtons=[]
                for j in range(len(self.resor[i].listSubres)):
                    self.resor[i].subButtons.append(ctk.CTkButton(self.resor[i].mainFrame, 
                                                                        text = self.resor[i].listSubres[j].subresName,
                                                                        border_color=self.color,
                                                                        border_width=2, 
                                                                        fg_color="gray30", hover_color="gray40", command = lambda c=(i, j): self.destroy_subres(c))
                    )
                    self.resor[i].subButtons[-1].grid(row=j+1, column=0, sticky="ew", padx=self.rescale, pady=(0,self.rescale), columnspan=2)

                self.resor[i].deleteButton=ctk.CTkButton(self.resor[i].mainFrame, 
                                                                        text = "Delete resource",
                                                                        border_color=self.color,
                                                                        border_width=2,
                                                                        fg_color="gray30", hover_color="gray40", command = lambda c=i: self.destroy_res(c))
                self.resor[i].deleteButton.grid(row=len(self.resor[i].listSubres)+1, column=0, padx=self.rescale, sticky="ew", pady=(0,self.rescale), columnspan=2)

        def destroy_all(self):
            self.aFrame.destroy()

            self.anteriorLabel.destroy()

            self.aconLabel.destroy()

            self.aadvLabel.destroy()

            self.acontotal.destroy()

            self.aadvtotal
            for i in range(len(self.resor)):
                self.resor[i].mainButton.destroy()
                self.resor[i].deleteButton.destroy()
                self.resor[i].qntLabel.destroy()
                for j in range(len(self.resor[i].subButtons)):
                    self.resor[i].subButtons[j].destroy()
                self.resor[i].mainFrame.destroy()

        def destroy_subres(self, pos):
            self.resor[pos[0]].listSubres.pop(pos[1])
            self.destroy_all()
            self.build_resor()
            self.modified=1 

        def destroy_res(self, pos):
            self.destroy_all()
            self.resor.pop(pos)
            self.build_resor()
            self.selectRes.set(0)
            self.modified=1 

        def resourcepaste(self, num, name):
            if int(num):
                self.resor.append(resource(num, name))
                self.destroy_all()
                self.build_resor()
                self.selectRes.set(len(self.resor))
                self.modified=1
            
        def anteadvpaste(self, num):
            try:
                if num:
                    self.premod.adv+=num
                    self.destroy_all()
                    self.build_resor()                
                    self.modified=1
            except:
                pass
        
        def antepaste(self, num1, num2):
            try:
                if num1 and num2:
                    self.premod.const+=int(num1*(num2+1)/2)
                    self.destroy_all()
                    self.build_resor()
                    self.modified=1
            except:
                pass

        def postpaste(self, num1, num2, typ, timing):
            if self.selectRes.get():
                if typ=="dice":
                    if not num1 or not num2:
                        return
                elif not num1:
                    return
                self.resor[self.selectRes.get()-1].listSubres.append(posmod(typ, timing, num1, num2))
                self.destroy_all()
                self.build_resor()
                self.modified=1

        def conversao(self): 
            try:
                return bloco(self.premod, self.clean_resor(), self.sn.get(), int(self.crit.get())/100, int(self.mini.get()))
            except:
                print(traceback.format_exc())
                messagebox.showerror(parent=self.Window2, title="Erro de conversão", message="Algo deu errado, confira seu envio.")
                return

        def clean_resor(self):
            posmods=[]
            for i in range(len(self.resor)):
                aux=("Resource #"+str(i+1))*(self.resor[i].resName.replace(" ", "")=="")+self.resor[i].resName*(self.resor[i].resName.replace(" ", "")!="")
                if self.resor[i].listSubres:
                    posmods.append(resourceSend(int(self.resor[i].qnt), aux, self.resor[i].listSubres))
            return posmods

        def send_block(self):
            message_sent = self.conversao()
            if message_sent:
                try:
                    with open('Past configs/'+str(self.past_index_max)+'.txt', 'xb') as file:
                        pickle.dump(message_sent, file)
                except Exception:
                    print(traceback.format_exc())
                    self.on_closing()
                self.past_index_max+=1
                if self.unmoved:
                    self.past_index=self.past_index_max
                    messagebox.showinfo(parent=self.Window2, title="Dica", message="Browse through past settings with ^ or ⌄.")
                    self.unmoved=False
                message_sent=pickle.dumps(message_sent)
                message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(message_sent_header+message_sent)

        def load_content(self, content):
            block=pickle.loads(content)
            resor, self.premod, crit, mini=block.posmods, block.premods, block.crit, block.min
            self.selectRes.set(0)

            self.destroy_all()
            self.resor=[]
            for i in resor:
                self.resor.append(resource(str(i.qnt), i.resName))
                self.resor[-1].listSubres=i.listSubres
        
            self.critbox.set(int(100*crit))
            self.minbox.set(mini)

            self.build_resor()

        def flip_values(self):
            self.premod.adv*=-1
            self.premod.const*=-1
            
            for i in self.resor:
                for j in range(len(i.listSubres)):
                    i.listSubres[j].num1*=-1
        
            self.build_resor()

        def savefile(self):             
            if self.path != '':
                block = self.conversao()
                with open(self.path, 'wb') as file:
                    pickle.dump(block, file)
                    self.modified=0                       
            else:
                self.savefileas()     

        def savefileas(self):    
            try:
                self.path = filedialog.askopenfile(parent=self.Window2, filetypes = [("Text files", "*.txt")]).name
                block = self.conversao()
                with open(self.path, 'wb') as file:
                    pickle.dump(block, file)
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
                    messagebox.showerror(parent=self.Window2, title="Path error", message="Invalid path, try again.")
                    return               
            else:
                answer = messagebox.askyesno(parent=self.Window2, title='Confirmation', message='There are unsaved changes. Do you want to save current settings first?')
                if answer:
                    self.savefileas()                      
                self.modified=0             
                self.openfile(pre_path)

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

        def callbackRes(self, name):
            if self.selectRes.get():
                if int(self.res.get()):
                    self.resor[self.selectRes.get()-1].qnt=self.res.get()
                    if name:
                        self.resor[self.selectRes.get()-1].resName=name
                    self.destroy_all()
                    self.build_resor()
                else:
                    self.destroy_res(self.selectRes.get()-1)
                
        # The main layout of the chat 
        def layout(self,name):
                self.path=''
                self.past_index_max=0
                self.past_index=0
                self.modified=0
                self.who=StringVar(value='we')
                self.crit=StringVar(value='10')
                self.crit.trace_variable('w', self.modify)
                self.mini=StringVar(value='0')
                self.mini.trace_variable('w', self.modify)
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
                self.geometry("800x504")
                self.columnconfigure(1 , weight=1)
                self.rowconfigure(1, weight=1)

                self.sidebarLabel=ctk.CTkLabel(self, text="Players online", fg_color="gray20", corner_radius=6)
                self.sidebarLabel.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.sidebar=ctk.CTkScrollableFrame(self,
                                                    fg_color="gray20",
                                                    scrollbar_button_color="gray25",
                                                    scrollbar_button_hover_color="gray35")
                self.sidebar.columnconfigure(0 , weight=1)
                self.sidebar.grid(row=1, column=0, padx=self.rescale, sticky="ns")

                self.allButton = ctk.CTkButton(self,
                                    text="Select all",
                                    border_color=self.color,
                                    border_width=2,
                                    fg_color="gray20", hover_color="gray30", command = lambda: self.AllClick())
                self.allButton.grid(row=2, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.blocbtt= ctk.CTkButton(self, 
                                                    text = '►',
                                                    width=26,                      
                                                    border_color=self.color,
                                                    border_width=2,
                                                    fg_color="gray20", hover_color="gray30", command = lambda: self.blocswitch())
                self.blocbtt.grid(row=0, column=3, padx=self.rescale, pady=self.rescale, sticky="ns", rowspan=3)
                                
                self.entryMsg = ctk.CTkEntry(self, fg_color="gray20", border_width=0, placeholder_text_color="gray30", placeholder_text="Write a message") 
                self.entryMsg.grid(row=2, column=1, padx=(0,self.rescale), pady=self.rescale, sticky="ew")
                #self.entryMsg.after(20, self.entryMsg.focus)
                
                self.buttonMsg = ctk.CTkButton(self, 
                                                            text = "Send",
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray20", hover_color="gray30", command = lambda : self.sendButton(self.entryMsg.get())) 
                self.buttonMsg.grid(row=2, column=2, pady=self.rescale, sticky="ew")
                
                self.textCons=ctk.CTkTextbox(self, fg_color="gray20")
                self.textCons.grid(row=0, column=1, pady=(self.rescale,0), sticky="nsew", rowspan=2, columnspan=2)
                self.textCons.configure(cursor = "arrow") 
                self.textCons.configure(state = DISABLED) 
                self.bind('<Return>', (lambda event: self.sendButton(self.entryMsg.get())))
                self.bind("<Up>", self.up_down)
                self.bind("<Down>", self.up_down)
                self.protocol("WM_DELETE_WINDOW", self.on_closing)
                self.textCons.tag_config('date', foreground="gray30")
                
                self.Window2=ctk.CTkToplevel(fg_color="gray15")
                self.Window2.title("Roll") 
                self.Window2.resizable(width = False, height = False)
                self.Window2.geometry("1200x524")
                self.Window2.columnconfigure(1 , weight=1)
                self.Window2.rowconfigure((1, 3), weight=1)

                self.menubar = Menu(self.Window2)
                self.Window2.config(menu=self.menubar)

                self.openmenu=Menu(self.menubar, tearoff=0)
                self.build_menu()

                self.selecLabel=ctk.CTkLabel(self.Window2, text="Select to roll", fg_color="gray20", corner_radius=6)
                self.selecLabel.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.sidebaroll=ctk.CTkScrollableFrame(self.Window2,
                                                    fg_color="gray20",
                                                    scrollbar_button_color="gray25",
                                                    scrollbar_button_hover_color="gray35")
                self.sidebaroll.columnconfigure(0 , weight=1)
                self.sidebaroll.grid(row=1, column=0, padx=self.rescale, sticky="ns")

                self.selectedLabel=ctk.CTkLabel(self.Window2, text="Selected", fg_color="gray20", corner_radius=6)
                self.selectedLabel.grid(row=2, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.label=ctk.CTkScrollableFrame(self.Window2, 
                                                    fg_color="gray20",
                                                    scrollbar_button_color="gray25",
                                                    scrollbar_button_hover_color="gray35")
                self.label.columnconfigure(0 , weight=1)
                self.label.grid(row=3, column=0, padx=self.rescale, sticky="ns")

                self.rollBtt = ctk.CTkButton(self.Window2,
                                    text="Roll",
                                    border_color=self.color,
                                    border_width=2,
                                    fg_color="gray20", hover_color="gray30", command = lambda: self.rollerrola())
                self.rollBtt.grid(row=4, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.resourcesLabel=ctk.CTkLabel(self.Window2, text="Resources", fg_color="gray20", corner_radius=6)
                self.resourcesLabel.grid(row=0, column=2, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.terFrame=ctk.CTkScrollableFrame(self.Window2,
                                                    fg_color="gray20",
                                                    scrollbar_button_color="gray25",
                                                    scrollbar_button_hover_color="gray35")
                self.terFrame.columnconfigure(0 , weight=1)
                self.terFrame.grid(row=1, column=2, padx=self.rescale, sticky="ns", rowspan=3)

                self.button_block = ctk.CTkButton(self.Window2, 
                                                            text = "Send",
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray20", hover_color="gray30", command = lambda : self.send_block())
                self.button_block.grid(row=4, column=2, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.resor=[]

                self.selectRes=IntVar(value=0)

                self.secFrame=ctk.CTkFrame(self.Window2, fg_color="gray15")
                self.secFrame.columnconfigure(0 , weight=1)
                self.secFrame.grid(row=0, column=1, pady=self.rescale, sticky="nsew", rowspan=5)

                self.stypebar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.stypebar.columnconfigure(5 , weight=1)
                self.stypebar.grid(row=0, column=0, sticky="ew", pady=(0,self.rescale))

                self.meBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'me',
                                                                        text = 'Me', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15)
                
                self.hiddenBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'hidden',
                                                                        text = 'Hidden', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15)
                self.weBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'we',
                                                                        text = 'We', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15)

                self.youBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'you',
                                                                        text = 'You', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15)

                self.sbtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 's',
                                                                        text = 'Yes', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15)

                self.nbtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 'n',
                                                                        text = 'No', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15)

                self.sdtypelabel= ctk.CTkLabel(self.stypebar, text='Send type:')
                self.separator0= ctk.CTkLabel(self.stypebar, text="")
                self.messagelabel= ctk.CTkLabel(self.stypebar, text='Hidden essage:')
                self.sdtypelabel.grid(row=0, column=0, padx=self.rescale)
                self.weBtt.grid(row=0, column=1, padx=(0,self.rescale))
                self.meBtt.grid(row=0, column=2, padx=(0,self.rescale))
                self.youBtt.grid(row=0, column=3, padx=(0,self.rescale))
                self.hiddenBtt.grid(row=0, column=4)
                self.separator0.grid(row=0, column=5, sticky="ew")
                self.messagelabel.grid(row=0, column=6, padx=(0,self.rescale))
                self.sbtt.grid(row=0, column=7)
                self.nbtt.grid(row=0, column=8, padx=self.rescale)

                self.resourcebar=ctk.CTkFrame(self.secFrame, fg_color="gray15")
                self.resourcebar.columnconfigure((0,1,2), weight=1)
                self.resourcebar.rowconfigure(0, weight=1)
                self.resourcebar.grid(row=2, column=0, sticky="ew", pady=(0,self.rescale))

                self.resourcebar1=ctk.CTkFrame(self.resourcebar, fg_color="gray20")
                self.resourcebar1.columnconfigure(0, weight=1)
                self.resourcebar1.grid(row=0, column=0, sticky="ew")
                
                self.resourcebar2= ctk.CTkFrame(self.resourcebar, fg_color="gray20")
                self.resourcebar2.columnconfigure((0,4), weight=1)
                self.resourcebar2.grid(row=0, column=1, sticky="ew", padx=self.rescale)
                
                self.resourcebar3= ctk.CTkFrame(self.resourcebar, fg_color="gray20")
                self.resourcebar3.columnconfigure(0, weight=1)
                self.resourcebar3.grid(row=0, column=2, sticky="ew")

                self.separator7= ctk.CTkLabel(self.resourcebar2, text="")
                self.separator7.grid(row=0, column=0, sticky="ew")

                self.reslabel = ctk.CTkEntry(self.resourcebar2, fg_color="gray25", border_width=0, placeholder_text_color="gray35", placeholder_text="Resource name")
                self.reslabel.grid(row=0, column=1, padx=self.rescale, pady=self.rescale, columnspan=3)

                self.separator8= ctk.CTkLabel(self.resourcebar2, text="")
                self.separator8.grid(row=0, column=4, sticky="ew")

                self.resbtt2 = ctk.CTkButton(self.resourcebar2, 
                                                            text = '◄', 
                                                            width=26,
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.callbackRes(self.reslabel.get())) 
                self.resbtt2.grid(row=1, column=1, padx=(0,self.rescale), pady=(0,self.rescale))
                
                self.resbox = IntSpinbox(self.resourcebar2,
                                    color=self.color, variable = self.res,
                                    from_ = 0)
                self.resbox.grid(row=1, column=2, padx=(0,self.rescale), pady=(0,self.rescale))

                self.resbtt = ctk.CTkButton(self.resourcebar2, 
                                                            text = "+", 
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.resourcepaste(self.res.get(), self.reslabel.get())) 
                self.resbtt.grid(row=1, column=3, pady=(0,self.rescale))

                self.critlabel= ctk.CTkLabel(self.resourcebar1, text='Crit chance (%)', fg_color="gray25", corner_radius=6)
                self.critlabel.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew", columnspan=2)

                self.critbox = IntSpinbox(self.resourcebar1,
                                    color=self.color, variable = self.crit,
                                    from_ = 0,
                                    step_size = 10)
                self.critbox.grid(row=1, column=0, pady=(0,self.rescale))

                self.minlabel= ctk.CTkLabel(self.resourcebar3, text='Minimum roll', fg_color="gray25", corner_radius=6)
                self.minlabel.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.minbox = IntSpinbox(self.resourcebar3,
                                    color=self.color, variable = self.mini,
                                    from_ = 0,
                                    to_ = 2000,
                                    step_size = 100,
                                    width=112)

                self.minbox.grid(row=1, column=0, padx=self.rescale, pady=(0,self.rescale))

                self.antebar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.antebar.columnconfigure((2,7), weight=1)
                self.antebar.grid(row=1, column=0, sticky="ew", pady=(0,self.rescale))

                self.antelabel= ctk.CTkLabel(self.antebar, text='Anterior', fg_color="gray25", corner_radius=6)           
                self.antelabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=self.rescale, columnspan=11)

                self.aconlabel= ctk.CTkLabel(self.antebar,text='Constant', fg_color="gray25", corner_radius=6)           
                self.aconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), sticky="ew", columnspan=2)
                
                self.acon = IntSpinbox(self.antebar,
                                        color=self.color, variable = self.ac)
                self.acon.grid(row=2, column=0, padx=self.rescale, pady=self.rescale)

                self.aconbtt = ctk.CTkButton(self.antebar, 
                                                            text = "+", 
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda : self.antepaste(int(self.ac.get()), 1)) 
                self.aconbtt.grid(row=2, column=1)

                self.separator1= ctk.CTkLabel(self.antebar, text="")
                self.separator1.grid(row=2, column=2, sticky="ew")

                self.aadvlabel= ctk.CTkLabel(self.antebar,text='Advantage', fg_color="gray25", corner_radius=6)           
                self.aadvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), sticky="ew", columnspan=2)

                self.aadv = IntSpinbox(self.antebar,
                                        color=self.color, variable = self.aa)
                self.aadv.grid(row=2, column=8)

                self.aadvbtt = ctk.CTkButton(self.antebar, 
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda : self.anteadvpaste(int(self.aa.get()))) 
                
                self.aadvbtt.grid(row=2, column=9, padx=self.rescale)

                self.separator2= ctk.CTkLabel(self.antebar, text="")
                self.separator2.grid(row=2, column=7, sticky="ew")

                self.adlabel= ctk.CTkLabel(self.antebar,text='Dice', fg_color="gray25", corner_radius=6)           
                self.adlabel.grid(row=1, column=3, padx=self.rescale, sticky="ew", columnspan=4)

                self.adic = IntSpinbox(self.antebar,
                                    color=self.color, variable = self.ad[0])
                self.adic.grid(row=2, column=3)

                self.addlabel= ctk.CTkLabel(self.antebar, text='d', width=0)           
                self.addlabel.grid(row=2, column=4, padx=10/3)

                self.adic2 = IntSpinbox(self.antebar,
                                    color=self.color, variable = self.ad[1],
                                    from_ = 0)
                self.adic2.grid(row=2, column=5, padx=(0,self.rescale))

                self.adicbtt = ctk.CTkButton(self.antebar, 
                                                            text = "+", 
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda : self.antepaste(int(self.ad[0].get()), int(self.ad[1].get()))) 
                self.adicbtt.grid(row=2, column=6)

                self.interbar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.interbar.columnconfigure((2, 7), weight=1)
                self.interbar.grid(row=3, column=0, sticky="ew")

                self.interlabel= ctk.CTkLabel(self.interbar, text='Intermediate', fg_color="gray25", corner_radius=6)           
                self.interlabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=self.rescale, columnspan=11)

                self.iconlabel= ctk.CTkLabel(self.interbar,text='Constant', fg_color="gray25", corner_radius=6)           
                self.iconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), sticky="ew", columnspan=2)
                
                self.icon = IntSpinbox(self.interbar,
                                        color=self.color, variable = self.ic)
                self.icon.grid(row=2, column=0, padx=self.rescale, pady=self.rescale)

                self.iconbtt = ctk.CTkButton(self.interbar, 
                                                            text = "+", 
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.postpaste(int(self.ic.get()), 1, "c", "Inter")) 
                
                self.iconbtt.grid(row=2, column=1)

                self.separator3= ctk.CTkLabel(self.interbar, text="")
                self.separator3.grid(row=2, column=2, sticky="ew")

                self.iadvlabel= ctk.CTkLabel(self.interbar,text='Advantage', fg_color="gray25", corner_radius=6)           
                self.iadvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), sticky="ew", columnspan=2)

                self.iadv = IntSpinbox(self.interbar,
                                        color=self.color, variable = self.ia)

                self.iadv.grid(row=2, column=8)

                self.iadvbtt = ctk.CTkButton(self.interbar, 
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.postpaste(int(self.ia.get()), 0, "adv", "Inter")) 
                
                self.iadvbtt.grid(row=2, column=9, padx=self.rescale)

                self.separator4= ctk.CTkLabel(self.interbar, text="")
                self.separator4.grid(row=2, column=7, sticky="ew")

                self.idlabel= ctk.CTkLabel(self.interbar,text='Dice', fg_color="gray25", corner_radius=6)           
                self.idlabel.grid(row=1, column=3, padx=self.rescale, sticky="ew", columnspan=4)

                self.idic = IntSpinbox(self.interbar,
                                    color=self.color, variable = self.id[0])
                self.idic.grid(row=2, column=3)

                self.iddlabel= ctk.CTkLabel(self.interbar, text='d', width=0)           
                self.iddlabel.grid(row=2, column=4, padx=10/3)

                self.idic2 = IntSpinbox(self.interbar,
                                    color=self.color, variable = self.id[1],
                                    from_ = 0)
                self.idic2.grid(row=2, column=5, padx=(0,self.rescale))

                self.idicbtt = ctk.CTkButton(self.interbar, 
                                                            text = "+", 
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.postpaste(int(self.id[0].get()), int(self.id[1].get()), "dice", "Inter")) 
                self.idicbtt.grid(row=2, column=6)

                self.postbar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.postbar.columnconfigure((2, 7), weight=1)
                self.postbar.grid(row=4, column=0, sticky="ew", pady=self.rescale)

                self.postlabel= ctk.CTkLabel(self.postbar, text='Posterior', fg_color="gray25", corner_radius=6)           
                self.postlabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=self.rescale, columnspan=11)

                self.pconlabel= ctk.CTkLabel(self.postbar,text='Constant', fg_color="gray25", corner_radius=6)           
                self.pconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), sticky="ew", columnspan=2)
                
                self.pcon = IntSpinbox(self.postbar,
                                        color=self.color, variable = self.pc)
                self.pcon.grid(row=2, column=0, padx=self.rescale, pady=self.rescale)

                self.pconbtt = ctk.CTkButton(self.postbar, 
                                                            text = "+", 
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.postpaste(int(self.pc.get()), 1, "c", "Post")) 
                
                self.pconbtt.grid(row=2, column=1)

                self.separator5= ctk.CTkLabel(self.postbar, text="")
                self.separator5.grid(row=2, column=2, sticky="ew")

                self.padvlabel= ctk.CTkLabel(self.postbar,text='Advantage', fg_color="gray25", corner_radius=6)           
                self.padvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), sticky="ew", columnspan=2)

                self.padv = IntSpinbox(self.postbar,
                                        color=self.color, variable = self.pa)

                self.padv.grid(row=2, column=8)

                self.padvbtt = ctk.CTkButton(self.postbar, 
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.postpaste(int(self.pa.get()), 0, "adv", "Post")) 
                
                self.padvbtt.grid(row=2, column=9, padx=self.rescale)

                self.separator6= ctk.CTkLabel(self.postbar, text="")
                self.separator6.grid(row=2, column=7, sticky="ew")

                self.pdlabel= ctk.CTkLabel(self.postbar,text='Dice', fg_color="gray25", corner_radius=6)           
                self.pdlabel.grid(row=1, column=3, padx=self.rescale, sticky="ew", columnspan=4)

                self.pdic = IntSpinbox(self.postbar,
                                    color=self.color, variable = self.pd[0])
                self.pdic.grid(row=2, column=3)

                self.pddlabel= ctk.CTkLabel(self.postbar, text='d', width=0)           
                self.pddlabel.grid(row=2, column=4, padx=10/3)

                self.pdic2 = IntSpinbox(self.postbar,
                                    color=self.color, variable = self.pd[1],
                                    from_ = 0)
                self.pdic2.grid(row=2, column=5, padx=(0,self.rescale))

                self.pdicbtt = ctk.CTkButton(self.postbar, 
                                                            text = "+", 
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", command = lambda: self.postpaste(int(self.pd[0].get()), int(self.pd[1].get()), "dice", "Post")) 
                self.pdicbtt.grid(row=2, column=6)

                #------------------------
                self.hiddenres=ctk.CTkToplevel(fg_color="gray15")
                self.hiddenres.title("Result (hidden)")
                self.hiddenres.resizable(width = False, height = False)
                self.hiddenres.geometry('300x100')
                self.hiddenres.protocol("WM_DELETE_WINDOW", self.hiddenres.withdraw)
                self.hiddenres.columnconfigure(0, weight=1)
                
                self.hidden_label=ctk.CTkLabel(self.hiddenres, text="", text_color=self.color, font=("Roboto", 25), fg_color="gray20", corner_radius=6)
                self.hidden_label.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale)

                self.dicewindow = self.progresswindow=ctk.CTkToplevel(fg_color="gray15")
                self.dicewindow.title("Result (dice)")
                self.dicewindow.resizable(width = False, height = False)
                self.dicewindow.columnconfigure(0, weight=1)
                self.dicewindow.protocol("WM_DELETE_WINDOW", self.dicewindow.withdraw)

                self.progresswindow=ctk.CTkToplevel(fg_color="gray15")
                self.progresswindow.title("Result (bar)")
                self.progresswindow.resizable(width = False, height = False)
                self.progresswindow.columnconfigure(0, weight=1)
                self.progresswindow.protocol("WM_DELETE_WINDOW", self.progresswindow.withdraw)

                self.InfoLabel = ctk.CTkLabel(self.dicewindow, text="", fg_color="gray20", corner_radius=6)
                self.InfoLabel.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale)
                self.ResultFrame = ctk.CTkFrame(self.dicewindow, fg_color="gray20")
                self.ResultFrame.columnconfigure(0, weight=1)
                self.ResultFrame.grid(row=1, column=0, sticky="ew", padx=self.rescale, pady=(0,self.rescale))
                
                self.ResultLabel=ctk.CTkLabel(self.ResultFrame, text="", text_color=self.color, font=("Roboto", 25), fg_color="gray20")
                self.ResultLabel.grid(row=0, column=0, pady=self.rescale)
                self.panel = ctk.CTkLabel(self.ResultFrame, text="", fg_color=self.color)
                self.panel.grid(row=1, column=0)

                self.InfoLabel2 = ctk.CTkLabel(self.progresswindow, text="", fg_color="gray20", corner_radius=6)
                self.InfoLabel2.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale)
                self.ResultFrame2 = ctk.CTkFrame(self.progresswindow, fg_color="gray20")
                self.ResultFrame2.columnconfigure(0, weight=1)
                self.ResultFrame2.grid(row=1, column=0, sticky="ew", padx=self.rescale, pady=(0,self.rescale))

                self.ResultLabel2=ctk.CTkLabel(self.ResultFrame2, text="", text_color=self.color, font=("Roboto", 25), fg_color="gray20")
                self.ResultLabel2.grid(row=0, column=0, pady=self.rescale)
                self.progress = ctk.CTkProgressBar(self.ResultFrame2, width=400, fg_color="gray25", progress_color=self.color)
                self.progress.grid(row=1, column=0, padx=self.rescale, pady=(0,self.rescale))

                self.hiddenres.withdraw()
                self.progresswindow.withdraw()
                self.dicewindow.withdraw()

                self.barrap1=Label(self.progress, bg = 'white')                 
                self.barrap2=Label(self.progress, bg = 'white')                 
                self.barracrit1=Label(self.progress, bg = 'white')                 
                self.barracrit2=Label(self.progress, bg = 'white') 

                

                #----------------------------------------

                self.premod=premod(0, 0)

                self.build_resor()

                self.unmoved=True
                
                #----------------------------------------

                self.Window2.protocol("WM_DELETE_WINDOW", self.blocswitch)
                self.Window2.withdraw()

                self.playerBtts = []
                self.playerBtts2 = []
                self.playerSelected =[]
                self.roll_list=[]
                self.createSidebarButtons()

                self.Window2.bind('<Return>', (lambda event: self.send_block()))
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
                        # insert messages to text box 
                        self.textCons.configure(state = NORMAL)
                        textlis=wrap(message.content, width=86)
                        for u in range(len(textlis)):
                            if textlis[u].startswith('\j'):
                                textlis[u]=textlis[u].replace('\j','',1)
                                textlis[u]=textlis[u].rstrip()
                            else:
                                textlis[u]=textlis[u].strip()
                        textlis.append('')
                        current_line=int(self.textCons.index(END)[:-2])-1
                        if message.cor not in self.textCons.tag_names(index=None):
                            self.textCons.tag_config(message.cor, foreground=message.cor)
                        self.textCons.insert(END, message.sender+' ', message.cor)
                        self.textCons.insert(END, datetime.now().strftime("%d/%m/%Y %H:%M")+'\n', 'date')
                        for u in range(len(textlis)-1):
                            if textlis[u]=='':
                                self.textCons.insert(END,'\n')
                            elif textlis[u+1]!='' and not textlis[u+1].startswith(' '):
                                linha=justify(textlis[u],42)
                                self.textCons.insert(END, linha+'\n')
                            else:
                                self.textCons.insert(END, textlis[u]+'\n')
                        self.textCons.insert(END,'\n')
                        self.textCons.see(END)
                        self.textCons.configure(state = DISABLED)
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
                            self.blocbtt.configure(text='◄')
                        else:
                            self.Window2.deiconify()
                        self.roll_list=[]
                        if message.num!=0:
                            self.selecLabel.configure(text='Restam '+str(message.num)+" rolagens")
                        else:
                            self.selecLabel.configure(text='Select to roll')
                    else:
                        if not message or type(message[0]).__name__!='res':
                            self.players = []
                            for dics in message:
                                dics['selected'] = False
                                self.players.append(dics)
                            break
                        else:
                            possibs=ctk.CTkToplevel(fg_color="gray15")
                            possibs.title('Possibilities')
                            possibs.resizable(width = False, height = False)
                            send_type=message.pop(-1)
                            m=max(max(len(i.mods) for i in message), 11)
                            
                            
                            
                            aux_2=ctk.CTkLabel(possibs, text='Net advantage', fg_color="gray20", corner_radius=6)
                            aux_2.grid(row=0, column=3, padx=(self.rescale, 0), pady=self.rescale)
                            aux_3=ctk.CTkLabel(possibs, text='Resources', fg_color="gray20", corner_radius=6)
                            aux_3.grid(row=0, column=4, padx=self.rescale, pady=self.rescale, sticky="ew")

                            
                            
                            
                            aux_2_mor=ctk.CTkFrame(possibs, fg_color="gray20")
                            aux_2_mor.grid_columnconfigure(0, weight=1)
                            aux_2_mor.grid(row=1, column=3, padx=(self.rescale, 0), sticky="ew")
                            aux_3_mor=ctk.CTkFrame(possibs, fg_color="gray20")
                            aux_3_mor.grid_columnconfigure(0, weight=1)
                            aux_3_mor.grid(row=1, column=4, padx=self.rescale, sticky="ew")

                            diff=[]
                            diff_crit=[]
                            diff_fail=[]
                            border=[]
                            border_crit=[]
                            border_fail=[]
                            p, crit, r, resultStr=self.transl(message[0])
                            for i in message:
                                p_old, crit_old=p, crit
                                p, crit, r, resultStr=self.transl(i)
                                diff.append(p_old-p)
                                diff_crit.append(crit_old-crit)
                                diff_fail.append((p_old-p)/2)
                                border.append(p)
                                border_crit.append(crit)
                                border_fail.append(p/2)
                            probs=["0%"*(diff[i]!=0)+"-"*(diff[i]==0) for i in range(len(message))]
                            probs_crit=["0%"*(diff_crit[i]!=0)+"-"*(diff_crit[i]==0) for i in range(len(message))]
                            probs_fail=["0%"*(diff_fail[i]!=0)+"-"*(diff_fail[i]==0) for i in range(len(message))]
                            
                            percent=min(0.5, max(np.random.normal(0.25, 0.1), 0))
                            aux1=[i for i in range(1, len(diff)) if (r<border[i-1] and r>=border[i]-percent*diff[i])]
                            if aux1:
                                ind=random.choice(aux1)
                                probs[ind:]=["-" for i in range(ind, len(message))]
                                probs[ind]="{:.1%}".format(1-percent)
                                aux_1=ctk.CTkLabel(possibs, text='% of f->s+', fg_color="gray20", corner_radius=6)
                                aux_1.grid(row=0, column=0, padx=(self.rescale, 0), pady=self.rescale)
                                aux_1_mor=ctk.CTkFrame(possibs, fg_color="gray20")
                                aux_1_mor.grid_columnconfigure(0, weight=1)
                                aux_1_mor.grid(row=1, column=0, padx=(self.rescale, 0), sticky="ew")

                            percent=min(0.5, max(np.random.normal(0.25, 0.1), 0))
                            aux2=[i for i in range(1, len(diff_crit)) if (r<border_crit[i-1] and r>=border_crit[i]-percent*diff_crit[i])]
                            if aux2:
                                ind=random.choice(aux2)
                                probs_crit[ind:]=["-" for i in range(ind, len(message))]
                                probs_crit[ind]="{:.1%}".format(1-percent)
                                aux_12=ctk.CTkLabel(possibs, text='% of s->cs', fg_color="gray20", corner_radius=6)
                                aux_12.grid(row=0, column=1, padx=(self.rescale, 0), pady=self.rescale)
                                aux_12_mor=ctk.CTkFrame(possibs, fg_color="gray20")
                                aux_12_mor.grid_columnconfigure(0, weight=1)
                                aux_12_mor.grid(row=1, column=1, padx=(self.rescale, 0), sticky="ew")
                                
                            percent=min(0.5, max(np.random.normal(0.25, 0.1), 0))
                            aux3=[i for i in range(1, len(diff_fail)) if (r<border_fail[i-1] and r>=border_fail[i]-percent*diff_fail[i])]
                            if aux3:
                                ind=random.choice(aux3)
                                probs_fail[ind:]=["-" for i in range(ind, len(message))]
                                probs_fail[ind]="{:.1%}".format(1-percent)
                                aux_13=ctk.CTkLabel(possibs, text='% of cf->f+', fg_color="gray20", corner_radius=6)
                                aux_13.grid(row=0, column=2, padx=(self.rescale, 0), pady=self.rescale)
                                aux_13_mor=ctk.CTkFrame(possibs, fg_color="gray20")
                                aux_13_mor.grid_columnconfigure(0, weight=1)
                                aux_13_mor.grid(row=1, column=2, padx=(self.rescale, 0), sticky="ew")
                                
                            for i in range(len(message)):
                                p, crit, r, resultStr=self.transl(message[i])
                                if aux1:
                                    aux_1=ctk.CTkLabel(aux_1_mor, text=probs[i], fg_color="gray25", corner_radius=6)
                                    aux_1.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                if aux2:
                                    aux_12=ctk.CTkLabel(aux_12_mor, text=probs_crit[i], fg_color="gray25", corner_radius=6)
                                    aux_12.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                if aux3:
                                    aux_13=ctk.CTkLabel(aux_13_mor, text=probs_fail[i], fg_color="gray25", corner_radius=6)
                                    aux_13.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                                
                                aux_2=ctk.CTkLabel(aux_2_mor, text='+'*(message[i].adv>0)+str(message[i].adv), fg_color="gray25", corner_radius=6)
                                aux_2.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                
                                resButton = ctk.CTkButton(aux_3_mor,
                                                text = message[i].mods[:-2]+'N/A'*(not message[i].mods[:-2]),
                                                fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                command= lambda p=p, crit=crit, r=r, resultStr=resultStr, send_type=send_type: threading.Thread(target = self.displayres, args=[p, crit, r, resultStr, send_type]).start())
                                resButton.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                            
                            resButton = ctk.CTkButton(possibs,
                                                text = 'Show results',
                                                fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                command=partial(self.show_res, message, send_type))
                            resButton.grid(row=2, column=0, columnspan=5, padx=self.rescale, pady=self.rescale, sticky="ew")

                            possibs.focus()
                except Exception:
                    print(traceback.format_exc())
                    if self.not_closing:
                        self.on_closing()
                    else:
                        break

        def show_res(self, message, send_type):                
            possibs=ctk.CTkToplevel(fg_color="gray15")
            possibs.title('Possibilities')
            possibs.resizable(width = False, height = False)
            aux_1=ctk.CTkLabel(possibs, text='Result', fg_color="gray20", corner_radius=6)
            aux_1.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")
            aux_2=ctk.CTkLabel(possibs, text='Net advantage', fg_color="gray20", corner_radius=6)
            aux_2.grid(row=0, column=1, padx=(0, self.rescale), pady=self.rescale, sticky="ew")
            aux_3=ctk.CTkLabel(possibs, text='Resources', fg_color="gray20", corner_radius=6)
            aux_3.grid(row=0, column=2, padx=(0, self.rescale), pady=self.rescale, sticky="ew")

            aux_1_mor=ctk.CTkFrame(possibs, fg_color="gray20")
            aux_1_mor.grid_columnconfigure(0, weight=1)
            aux_1_mor.grid(row=1, column=0, padx=self.rescale, pady=(0, self.rescale), sticky="ew")
            aux_2_mor=ctk.CTkFrame(possibs, fg_color="gray20")
            aux_2_mor.grid_columnconfigure(0, weight=1)
            aux_2_mor.grid(row=1, column=1, padx=(0, self.rescale), pady=(0, self.rescale), sticky="ew")
            aux_3_mor=ctk.CTkFrame(possibs, fg_color="gray20")
            aux_3_mor.grid_columnconfigure(0, weight=1)
            aux_3_mor.grid(row=1, column=2, padx=(0, self.rescale), pady=(0, self.rescale), sticky="ew")

            for i in range(len(message)):
                p, crit, r, resultStr=self.transl(message[i])
                if send_type:
                    opposite_message=(send_type=='Yes')*'No'+(send_type=='No')*'Yes'
                    resultStr=(resultStr=="Success" or resultStr=="Critical success")*send_type+(resultStr=="Fail" or resultStr=="Critical fail")*opposite_message
                    
                aux_1=ctk.CTkLabel(aux_1_mor, text=resultStr, fg_color="gray25", corner_radius=6)
                aux_2=ctk.CTkLabel(aux_2_mor, text='+'*(message[i].adv>=0)+str(message[i].adv), fg_color="gray25", corner_radius=6)
                aux_3=ctk.CTkLabel(aux_3_mor, text=message[i].mods[:-2]+'N/A'*(not message[i].mods[:-2]), fg_color="gray25", corner_radius=6)

                aux_1.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                    
                aux_2.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                
                aux_3.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
            possibs.focus()
            
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
            aux=mx/max(1, (mn+mx))
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
                
                canvas=FigureCanvasTkAgg(f, master=frame)
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

                    canvas0=FigureCanvasTkAgg(f, master=frame)
                    canvas0.draw()
                    canvas.get_tk_widget().destroy()
                    canvas0.get_tk_widget().pack()
                    sleep(0.5)
                    if j!=l-1:
                        p.bar(i, values[mini-i-1], color='w')
                        f.tight_layout()

                        canvas=FigureCanvasTkAgg(f, master=frame)
                        canvas.draw()
                        canvas0.get_tk_widget().destroy()
                        canvas.get_tk_widget().pack()
                        sleep(0.3)
                p.set_title('r='+str(roll)+', p(r)='+"{:.1e}".format(dic[roll]/total)+', p(x>=r)='+"{:.1e}".format(values[mini-roll-1]), color='w')
                f.tight_layout()
                
                canvas = FigureCanvasTkAgg(f, master=frame)
                canvas.draw()
                canvas0.get_tk_widget().destroy()
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

