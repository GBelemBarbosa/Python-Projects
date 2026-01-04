# import all the required modules
# Set DPI awareness BEFORE any GUI imports
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAST_CONFIGS_DIR = os.path.join(BASE_DIR, 'Past configs')
SAVED_CONFIGS_DIR = os.path.join(BASE_DIR, 'Saved configs')
DICE_IMAGES_DIR = os.path.join(BASE_DIR, 'Dice_Images')
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.figure import Figure
from collections import OrderedDict
import itertools
import math
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# windll already imported at top of file
import matplotlib.font_manager as fm
### ROBOTO FONT DETECTION ###
roboto_fonts = [f for f in fm.fontManager.ttflist if 'Roboto' in f.name]
if not roboto_fonts:
    print(">>> Roboto NOT in cache. Attempting deep refresh...")
    try:
        font_files = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        for fpath in font_files:
            if 'Roboto' in os.path.basename(fpath):
                fm.fontManager.addfont(fpath)
        roboto_fonts = [f for f in fm.fontManager.ttflist if 'Roboto' in f.name]
        if roboto_fonts:
            print(f">>> SUCCESS: Roboto found after refresh. Names: {[f.name for f in roboto_fonts]}")
        else:
            print(">>> FAILURE: Roboto not found in system fonts.")
    except Exception as e:
        print(f">>> ERROR during font refresh: {e}")
else:
    print(f">>> Roboto ALREADY in cache. Names: {[f.name for f in roboto_fonts]}")
##############################
# Set Matplotlib to use Roboto as the default font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Roboto'] + plt.rcParams['font.sans-serif']

# DPI awareness already set at top of file

__all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']

_whitespace = '\t\n\x0b\x0c\r '

def justify(words, width):
    if len(words)==width:
        return(words)
    line = re.split(r"(\s+)",words)
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
                    chunks.append(r'\j'+' -*- '*10)
                elif r'\k' in chunks[-1] and not r'\\\k' in chunks[-1]:
                        yob=chunks[-1].split(r'\k')
                        chunks.pop()
                        if yob[1]!='':
                            chunks.append(yob[1])
                        elif len(chunks)>1:
                            z=chunks.pop()
                            chunks[-1]=r'\j'+z+chunks[-1]
                        else:
                            chunks.append(r'\j')
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
                            chunks[-1]=r'\j'*(width-cur_len-len(yob[0])>0)+z.replace(' ','')+chunks[-1]
                        else:
                            if not yob[0] and (width-cur_len-len(yob[0])==0):
                                chunks.append(' '*width)
                            else:
                                chunks.append(r'\j'*(width-cur_len-len(yob[0])>0))
                        if yob[0]:
                            if len(yob[0])<(width-cur_len):
                                chunks.append((width-cur_len-len(yob[0]))*' ')
                            else:
                                chunks.append((width-len(yob[0]))*' ')
                            chunks.append(yob[0])
                        else:
                            chunks.append((width-cur_len)*' ')
                elif r'\g' in chunks[-1] and not r'\\\g' in chunks[-1]:
                        yob=chunks[-1].split(r'\g')
                        chunks.pop()
                        if yob[1]!='':
                            chunks.append(r'\j         '+yob[1])
                        elif len(chunks)>1:
                            z=chunks.pop()
                            chunks[-1]=r'\j         '+z+chunks[-1]
                        if yob[0]!='':
                            if len(yob[0])<(width-cur_len):
                                chunks.append((width-cur_len-len(yob[0]))*' ')
                            else:
                                chunks.append((width-len(yob[0]))*' ')
                            chunks.append(yob[0])
                        else:
                            chunks.append((width-cur_len)*' ')
                            
                l = len(chunks[-1])-2*(chunks[-1].startswith(r'\j') and cur_len==0)
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
                                                       fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), border_width=0, fg_color="gray25", font=("Roboto", 12))
        self.entry.grid(row=0, column=1, columnspan=1, padx=10/3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="▲", width=height-6, border_color=color, border_width=2,
                                                  fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = self.add_button_callback)
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
                self.options = [
                    "Chico",
                    "Picardía",
                    "Pascal",
                    "Tobey",
                    "Hide the pain"
                    ]
                
                self.rolldic_style = StringVar(value='Cumulative')
                self.displaymode = StringVar(value='bar')
                self.dice_style = StringVar(value=self.options[0])
                self.who = StringVar(value='me')
                self.sn = StringVar(value='s')
                
                # chat window which is currently hidden
                self.configure(fg_color="gray15")
                self.withdraw()

                os.makedirs(PAST_CONFIGS_DIR, exist_ok=True)
                for filename in os.listdir(PAST_CONFIGS_DIR):
                    os.remove(os.path.join(PAST_CONFIGS_DIR, filename))
                
                # login window 
                self.login = ctk.CTkToplevel(fg_color="gray15") 
                # set the title 
                self.login.title("Login") 
                self.login.geometry("400x125")
                self.login.grid_columnconfigure(0, weight=1)
                self.login.grid_rowconfigure(1, weight=1) # ONLY center row expands
                self.login.grid_rowconfigure((0, 2), weight=0) # Keep bars at edges
                self.login.resizable(width = False, height = False)
                self.login.protocol("WM_DELETE_WINDOW", self.on_closing)  

                # create a Label
                self.plsFrame=ctk.CTkFrame(self.login, fg_color="gray20")
                self.plsFrame.grid_columnconfigure(0, weight=1)
                self.plsFrame.grid(row=0, column=0, padx=self.rescale, pady=(self.rescale, 0), sticky="ew")
                
                self.pls = ctk.CTkLabel(self.plsFrame, text = "Please login to continue", font=("Roboto", 14)) 
                self.pls.grid(row=0, column=0)
                
                # create a Label 
                self.labelName = ctk.CTkLabel(self.login, text="", font=("Roboto", 12)) 
                self.labelName.grid(row=1, column=0, pady=0) # Centered vertically
                
                # create a entry box for 
                # typing the message 
                self.entryName = ctk.CTkEntry(self.labelName, fg_color="gray20", border_width=0, placeholder_text_color="gray30", placeholder_text="Username", font=("Roboto", 12), justify="center") 
                self.entryName.grid(row=0, column=0)
                self.entryName.bind('<Return>',(lambda event: self.goAhead(self.entryName.get())))
                
                # set the focus of the curser 
                self.login.focus_force()
                self.entryName.after(200, self.entryName.focus)
                
                # create a Continue Button 
                # along with action 
                self.go = ctk.CTkButton(self.login, 
                                                text = "Login", 
                                                fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.goAhead(self.entryName.get()))
                self.go.grid(row=2, column=0, pady=(0, self.rescale), padx=self.rescale, sticky="ew") 
                

        def askDice(self, name):
            self.login2 = ctk.CTkToplevel(fg_color="gray15") 
            self.login2.title("Display modes")
            self.login2.geometry('400x185')
            self.login2.grid_columnconfigure(0, weight=1)
            self.login2.grid_rowconfigure((1, 2, 3), weight=1) # Centering interactive elements
            self.login2.grid_rowconfigure((0, 4), weight=0) # Keep bars at edges
            self.login2.resizable(width = False, height = False)
            self.login2.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.login2.bind('<Return>',(lambda event: self.goAhead2(name)))
            self.login2.bind('<Up>', self.cycle_display_mode)
            self.login2.bind('<Down>', self.cycle_display_mode)
            self.login2.focus_force()

            self.displayFrame=ctk.CTkFrame(self.login2, fg_color="gray20")
            self.displayFrame.grid_columnconfigure(0, weight=1)
            self.displayFrame.grid(row=0, column=0, padx=self.rescale, pady=(self.rescale, 0), sticky="ew")
                
            self.display = ctk.CTkLabel(self.displayFrame, text="Display mode", font=("Roboto", 14)) 
            self.display.grid(row=0, column=0)

            self.displaymode=StringVar(value='bar')

            self.barbtt=ctk.CTkRadioButton(self.login2, 
                                                                    variable = self.displaymode, 
                                                                    value = 'bar',
                                                                    text = '  Bar', fg_color=self.color, border_color="gray20", hover_color=self.color, font=("Roboto", 12))
            self.barbtt.grid(row=1, column=0, padx=(44, 0), pady=(4, 2))

            self.dicebtt=ctk.CTkRadioButton(self.login2, 
                                                                    variable = self.displaymode, 
                                                                    value = 'dice',
                                                                    text = ' Dice', fg_color=self.color, border_color="gray20", hover_color=self.color, font=("Roboto", 12))
            self.dicebtt.grid(row=2, column=0, padx=(44, 0), pady=2)

            self.wheelbtt=ctk.CTkRadioButton(self.login2, 
                                                                    variable = self.displaymode, 
                                                                    value = 'wheel',
                                                                    text = 'Wheel', fg_color=self.color, border_color="gray20", hover_color=self.color, font=("Roboto", 12))
            self.wheelbtt.grid(row=3, column=0, padx=(44, 0), pady=(2, 4))

            self.nonebtt=ctk.CTkRadioButton(self.login2, 
                                                                    variable = self.displaymode, 
                                                                    value = 'none',
                                                                    text = 'None', fg_color=self.color, border_color="gray20", hover_color=self.color, font=("Roboto", 12))
            self.nonebtt.grid(row=4, column=0, padx=(44, 0), pady=(2, 4))
            
            # create a Continue Button 
            # along with action 
            self.go2 = ctk.CTkButton(self.login2, 
                                            text = "Continue", border_color=self.color, border_width=2, 
                                            fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.goAhead2(name))
            self.go2.grid(row=4, column=0, pady=(0, self.rescale), padx=self.rescale, sticky="ew")


            self.dice_style = StringVar()
            self.dice_style.set(self.options[0])
                                
        def goAhead2(self, name):
            if self.displaymode.get()=='dice':
                self.login2.destroy()
                self.login3 = ctk.CTkToplevel(fg_color="gray15") 
                self.login3.title("Critical styles")
                self.login3.geometry('400x125')
                self.login3.grid_columnconfigure(0, weight=1)
                self.login3.grid_rowconfigure(1, weight=1) # ONLY center row expands
                self.login3.grid_rowconfigure((0, 2), weight=0) # Keep bars at edges
                self.login3.resizable(width = False, height = False)
                self.login3.protocol("WM_DELETE_WINDOW", self.on_closing)
                self.login3.bind('<Return>',(lambda event: self.goAhead3(name)))
                self.login3.bind('<Up>', self.cycle_dice_style_login)
                self.login3.bind('<Down>', self.cycle_dice_style_login)
                self.login3.focus_force()

                self.displayCritical=ctk.CTkFrame(self.login3, fg_color="gray20")
                self.displayCritical.grid_columnconfigure(0, weight=1)
                self.displayCritical.grid(row=0, column=0, padx=self.rescale, pady=(self.rescale, 0), sticky="ew")

                self.dicebar= ctk.CTkLabel(self.displayCritical, text='Critical style', font=("Roboto", 14))
                self.dicebar.grid(row=0, column=0)
                
                self.dice_style_drop = ctk.CTkComboBox(self.login3, variable=self.dice_style, values=self.options, state='readonly', dropdown_hover_color="gray25", fg_color="gray20", border_width=0, button_color="gray25", font=("Roboto", 12), width=200, justify="center")
                self.dice_style_drop.grid(row=1, column=0, pady=0) # Centered horizontally by removing sticky="ew"

                self.go3 = ctk.CTkButton(self.login3, 
                                            text = "Continue", border_color=self.color, border_width=2,
                                            fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.goAhead3(name)) 
                self.go3.grid(row=2, column=0, pady=(0, self.rescale), padx=self.rescale, sticky="ew")
            else:
                self.goAhead3(name)

        def goAhead3(self, name):
            self.receive()
            self.layout(name)
            # the thread to receive messages 
            self.rcv = threading.Thread(target=self.receive) 
            self.rcv.start()

        def cycle_display_mode(self, event):
            modes = ['bar', 'dice', 'wheel', 'none']
            current = self.displaymode.get()
            try:
                idx = modes.index(current)
            except ValueError:
                idx = 0
            
            if event.keysym == 'Up':
                idx = (idx - 1) % len(modes)
            elif event.keysym == 'Down':
                idx = (idx + 1) % len(modes)
            
            self.displaymode.set(modes[idx])

        def cycle_dice_style_login(self, event):
            current = self.dice_style.get()
            try:
                idx = self.options.index(current)
            except ValueError:
                idx = 0
                
            if event.keysym == 'Up':
                idx = (idx - 1) % len(self.options)
            elif event.keysym == 'Down':
                idx = (idx + 1) % len(self.options)
                
            self.dice_style.set(self.options[idx])

            
        def goAhead(self, name):
            my_username = name.encode(FORMAT)
            my_username_header = f"{len(my_username):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(my_username_header + my_username)
            server_message_header=client.recv(HEADER_LENGTH)
            server_message_length = int(server_message_header.decode(FORMAT).strip())
            server_message=client.recv(server_message_length).decode(FORMAT)
            if server_message=='ok':
                try:
                    self.color=askcolor(color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), title ="Choose your user color")[1]
                    color=self.color.encode(FORMAT)
                except:
                    self.on_closing()
                color_header=f"{len(color):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(color_header + color)
                self.login.destroy()
                self.goAhead3(name)
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
                                                    text = self.players[c]['name'],
                                                    font=("Roboto", 12))
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
                                                font=("Roboto", 12),
                                                command=lambda c=i: self.onPlayerClick(c))
                self.playerBtts.append(tempButton)
                self.playerBtts[-1].grid(row=i, column=0, pady=(0,self.rescale), sticky="ew")

                tempButton = ctk.CTkButton(self.sidebaroll,
                                                    fg_color="gray25", hover_color="gray35",
                                                    border_color=self.players[i]['color'],
                                                    border_width=2,
                                                    text = self.players[i]['name'],
                                                    font=("Roboto", 12),
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
                
        def displayres(self, p, crit, r, resultStr, send_type, resources):
            limits_msg = rf"\n Limits: \g CF: <{p/2:.1f}; F: <{p:.1f}; S: <{crit:.1f}; CS: >={crit:.1f} \g Rolled: {r:.1f}"
            if send_type:
                message = r"Resource option selected! The result is a secret...\g Post: "+resources + limits_msg
                
                if not self.hiddenres.winfo_viewable():
                    self.hiddenres.update()
                    self.hiddenres.deiconify()
                if self.progresswindow.winfo_viewable():
                    self.progresswindow.withdraw()
                if self.dicewindow.winfo_viewable():
                    self.dicewindow.withdraw()
                if self.wheelwindow.winfo_viewable():
                    self.wheelwindow.withdraw()
                self.hiddenres.focus()

                opposite_message=(send_type=='No')*'Yes'+(send_type=='Yes')*'No'
                aux=(resultStr=="Success" or resultStr=="Critical success")*send_type+(resultStr=="Fail" or resultStr=="Critical fail")*opposite_message
                self.hidden_label.configure(text=aux)
            else:
                message = r"Resource option selected! The result is: "+resultStr+r".\g Post: "+resources + limits_msg
                
                info_limits = f"Limits:\nCF: <{p/2:.1f}; F: <{p:.1f}; S: <{crit:.1f}; CS: >={crit:.1f}"
                info_header_initial = info_limits + "\n "
                if self.displaymode.get() == 'bar':
                    self.InfoLabel2.configure(text = info_header_initial)
                    self.ResultLabel2.configure(text = "")
                    self.progress.set(0)

                    p_norm = p/20
                    crit_norm = crit/20
                    cf_norm = p_norm / 2
                    
                    self.CFZone.place(relx=0, relwidth=cf_norm, relheight=1)
                    self.FailZone.place(relx=cf_norm, relwidth=p_norm-cf_norm, relheight=1)
                    self.SuccessZone.place(relx=p_norm, relwidth=crit_norm-p_norm, relheight=1)
                    self.CritZone.place(relx=crit_norm, relwidth=1-crit_norm, relheight=1)
                    
                    # Place precision markers
                    self.CFMarker.place(relx=cf_norm, rely=0.5, anchor="center")
                    self.SMarker.place(relx=p_norm, rely=0.5, anchor="center")
                    self.CSMarker.place(relx=crit_norm + 0.0025, rely=0.5, anchor="center") # Shift slightly right for better alignment

                    # Store colors for dynamic color logic during animation
                    self.bar_zone_colors = ["#4d4d4d", "#595959", "#666666", "#737373"] # gray30, 35, 40, 45
                    
                    # Place threshold labels
                    self.CFThreshLabel.place(relx=cf_norm, anchor="n")
                    self.SuccessThreshLabel.place(relx=p_norm, anchor="n")
                    self.CritThreshLabel.place(relx=crit_norm, anchor="n")

                    if not self.progresswindow.winfo_viewable():
                        self.progresswindow.update()
                        self.progresswindow.deiconify()
                    self.progresswindow.focus()
                    
                    x=0
                    n=random.randint(2, 15)
                    r_bar = r/20
                    
                    for i in range(100): # 100 steps for smoother animation
                        sleep(0.02)
                        x+=0.01
                        y=r_bar*n*x/(1+(n-1)*x)
                        
                        # Grayscale animation until final frame - consistent gray jumps
                        if y < cf_norm:
                            self.progress.configure(progress_color="#4d4d4d") # gray30
                        elif y < p_norm:
                            self.progress.configure(progress_color="#595959") # gray35
                        elif y < crit_norm:
                            self.progress.configure(progress_color="#666666") # gray40
                        else:
                            self.progress.configure(progress_color="#737373") # gray45
                        self.progress.set(value=y)
                    
                    self.progress.configure(progress_color=self.color)
                    self.progress.set(value=r_bar)
                    self.ResultLabel2.configure(text = resultStr)
                    self.InfoLabel2.configure(text = info_limits + f"\nRolled: {r:.1f}")
                elif self.displaymode.get() == 'dice':
                    self.InfoLabel.configure(text = info_header_initial)
                    self.ResultLabel.configure(text = "")

                    if not self.dicewindow.winfo_viewable():
                        self.dicewindow.update()
                        self.dicewindow.deiconify()
                    self.dicewindow.focus()
                    
                    # Sync backgrounds to prevent flicker
                    self.panel.configure(fg_color="gray70")
                    self.ResultFrame.configure(fg_color="gray20")
                    self.ResultLabel.configure(fg_color="gray20")

                    ##### CONSTANTES PARA ADEQUACAO DOS TEMPOS DE ROLAGEM (EM 10^-2s)

                    sleepTime = random.randint(self.minST,self.maxST)/100
                    maxSleepTime = random.randint(self.minMST,self.maxMST)/100
                    
                    currentRoll = random.randint(0, 20)
                    while maxSleepTime-sleepTime > 0.1 and maxSleepTime > sleepTime:
                        rolagem = random.randint(0, 20)
                        while rolagem == currentRoll:
                            rolagem = random.randint(0, 20)

                        currentRoll = rolagem
                        
                        # Use cached image
                        self.panel.configure(image = self.dice_images_cache[str(rolagem)+".png"])
                        
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
                        img_name = "20" + self.dice_style.get() + '.png'
                    elif resultStr=="Critical fail":
                        img_name = "0" + self.dice_style.get() + '.png'
                    else:
                        img_name = str(roundedRealDiceRoll) + ".png"

                    # Show final result with user color
                    self.panel.configure(image = self.dice_images_cache[img_name], fg_color=self.color)
                    self.ResultFrame.configure(fg_color="gray20")
                    self.ResultLabel.configure(fg_color="gray20")

                    self.ResultLabel.configure(text = resultStr)
                    self.InfoLabel.configure(text = info_limits + f"\nRolled: {r:.1f}")
                elif self.displaymode.get() == 'wheel':
                    self.InfoLabel3.configure(text = info_header_initial)
                    self.ResultLabel3.configure(text = "")

                    if not self.wheelwindow.winfo_viewable():
                        self.wheelwindow.update()
                        self.wheelwindow.deiconify()
                    self.wheelwindow.focus()

                    # Calculate wedge sizes (as percentages of 0-20 scale)
                    # p and crit are thresholds on 0-20 scale
                    # Critical fail: r < p/2 → range [0, p/2)
                    # Fail: p/2 <= r < p → range [p/2, p)
                    # Success: p <= r < crit → range [p, crit)
                    # Critical success: r >= crit → range [crit, 20]
                    crit_fail_size = (p / 2) / 20 * 100        # [0, p/2)
                    fail_size = (p / 2) / 20 * 100             # [p/2, p)
                    success_size = (crit - p) / 20 * 100       # [p, crit)
                    crit_success_size = (20 - crit) / 20 * 100 # [crit, 20]
                    
                    sizes = [crit_fail_size, fail_size, success_size, crit_success_size]
                    labels = ['Critical\nFail', 'Fail', 'Success', 'Critical\nSuccess']
                    base_colors = ['#404040', '#4d4d4d', '#595959', '#666666']  # gray25, 30, 35, 40
                    
                    # Determine which wedge is the result
                    result_index = {'Critical fail': 0, 'Fail': 1, 'Success': 2, 'Critical success': 3}[resultStr]
                    
                    # Store animation state
                    self.wheel_sizes = sizes
                    self.wheel_labels = labels
                    self.wheel_base_colors = base_colors
                    self.wheel_result_index = result_index
                    self.wheel_resultStr = resultStr
                    self.wheel_p = p
                    self.wheel_crit = crit
                    self.wheel_r = r
                    self.wheel_info_limits = info_limits
                    
                    # Calculate final angle for the result wedge
                    # We want the pointer at the top (90 degrees) to land in the result wedge
                    # Pie starts at startangle=90, wedges go counter-clockwise
                    # To land pointer on precise position: rotate by -(cumulative + rel_pos * size) * 3.6
                    cumulative = 0
                    for i in range(result_index):
                        cumulative += sizes[i]
                    
                    # Calculate relative position within the wedge based on the roll r
                    if result_index == 0:   # Critical Fail: [0, p/2)
                        rel_pos = (r - 0) / (p / 2)
                    elif result_index == 1: # Fail: [p/2, p)
                        rel_pos = (r - p/2) / (p/2)
                    elif result_index == 2: # Success: [p, crit)
                        rel_pos = (r - p) / (crit - p)
                    else:                   # Critical Success: [crit, 20]
                        rel_pos = (r - crit) / (20 - crit)
                    
                    # Map the relative position to the wedge angle
                    target_angle = cumulative + rel_pos * sizes[result_index]
                    
                    # Spin animation: multiple full rotations + landing angle
                    full_rotations = random.randint(3, 5)
                    self.wheel_total_rotation = full_rotations * 360 - target_angle * 3.6  # 3.6 = 360/100
                    self.wheel_current_rotation = 0
                    self.wheel_animation_step = 0
                    self.wheel_total_steps = 60  # 60 frames for smooth animation
                    
                    # Start animation
                    self.animate_wheel()
                elif self.displaymode.get() == 'none':
                    pass

            message_sent = pickle.dumps(msg([player['name'] for player in self.players], message))
            message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
            client.send(message_sent_header+message_sent)

        def nextSleepTime(self, currentTime, limitTime): # 3 opcoes de incremento de tempo
            # return currentTime + currentTime**2 / 2
            # return currentTime + incrementFraction*currentTime
            return currentTime+limitTime*(1-exp(-currentTime*self.incrementFraction))

        def animate_wheel(self):
            try:
                if not self.wheelwindow.winfo_exists():
                    return
                
                # Easing function for smooth slowdown
                t = self.wheel_animation_step / self.wheel_total_steps
                # Ease-out cubic for more dramatic slowdown
                eased_t = 1 - pow(1 - t, 3)
                
                current_rotation = eased_t * self.wheel_total_rotation
                
                # Clear the axis
                self.wheel_ax.clear()
                self.wheel_ax.set_facecolor('#333333') # Match gray20 of ResultFrame3
                self.wheel_ax.axis('equal')
                
                # Determine colors - highlight result on final frame
                if self.wheel_animation_step >= self.wheel_total_steps:
                    colors = []
                    for i in range(4):
                        if i == self.wheel_result_index:
                            colors.append(self.color)  # User's color for result
                        else:
                            colors.append(self.wheel_base_colors[i])
                else:
                    colors = self.wheel_base_colors
                
                # Draw pie chart with rotation
                wedges, texts = self.wheel_ax.pie(
                    self.wheel_sizes,
                    labels=self.wheel_labels if self.wheel_animation_step >= self.wheel_total_steps else [''] * 4,
                    colors=colors,
                    startangle=90 + current_rotation,
                    labeldistance=1.15,  # Standardize label distance from wheel
                    wedgeprops={'linewidth': 2, 'edgecolor': '#333333'}
                )
                
                # Set label properties
                for text in texts:
                    text.set_color('white')
                    text.set_fontsize(10)
                    text.set_fontname('Roboto')
                
                # Draw pointer at top using a polygon triangle
                pointer_x = [0, -0.08, 0.08]
                pointer_y = [1.0, 1.15, 1.15]
                self.wheel_ax.fill(pointer_x, pointer_y, color='white')
                
                self.wheel_canvas.draw()
                
                if self.wheel_animation_step < self.wheel_total_steps:
                    self.wheel_animation_step += 1
                    # Variable delay - faster at start, slower at end
                    delay = int(20 + 80 * t)  # 20ms to 100ms
                    self.wheelwindow.after(delay, self.animate_wheel)
                else:
                    # Animation complete - show result
                    self.ResultLabel3.configure(text=self.wheel_resultStr)
                    self.InfoLabel3.configure(text=self.wheel_info_limits + f"\nRolled: {self.wheel_r:.1f}")
            except Exception:
                print(traceback.format_exc())

        def show_mode_menu(self):
            menu = Menu(self, tearoff=0, bg="#2b2b2b", fg="white", activebackground=self.color, activeforeground="white", font=("Roboto", 10))
            
            # Display Mode section
            menu.add_command(label="-- Result display mode --", state=DISABLED)
            for m in ['Bar', 'Wheel', 'None']:
                label = f"{'✓ ' if self.displaymode.get().lower() == m.lower() else '  '}{m}"
                menu.add_command(label=label, command=lambda m_val=m.lower(): self.set_mode_style(m_val))
            
            # Dice Style as a cascading menu under "Dice"
            dice_menu = Menu(menu, tearoff=0, bg="#2b2b2b", fg="white", activebackground=self.color, activeforeground="white", font=("Roboto", 10))
            for style in self.options:
                label = f"{'✓ ' if (self.displaymode.get().lower() == 'dice' and self.dice_style.get() == style) else '  '}{style}"
                dice_menu.add_command(label=label, command=lambda s=style: self.set_mode_style("dice", s))
            
            dice_label = f"{'✓ ' if self.displaymode.get().lower() == 'dice' else '  '}Dice"
            menu.add_cascade(label=dice_label, menu=dice_menu)
            
            menu.add_separator()
            
            # Rolldic Style section
            menu.add_command(label="-- Dice roll animation style --", state=DISABLED)
            for rs in ['Cumulative', 'Wheel', 'None']:
                label = f"{'✓ ' if self.rolldic_style.get() == rs else '  '}{rs}"
                menu.add_command(label=label, command=lambda s=rs: self.set_rolldic_style(s))
            
            # Show menu at button position
            x = self.mode_button.winfo_rootx()
            y = self.mode_button.winfo_rooty() + self.mode_button.winfo_height()
            menu.post(x, y)

        def set_rolldic_style(self, style):
            self.rolldic_style.set(style)
            # Update button text
            mode = self.displaymode.get()
            disp_text = mode.capitalize()
            if mode.lower() == 'dice':
                disp_text = f"Dice ({self.dice_style.get()})"
            
            self.mode_button.configure(text=f"D: {disp_text} | R: {style}")

        def set_mode_style(self, mode, style=None):
            self.displaymode.set(mode)
            if style:
                self.dice_style.set(style)
            
            # Update button text
            disp_text = mode.capitalize()
            if mode.lower() == 'dice':
                disp_text = f"Dice ({self.dice_style.get()})"
            
            roll_text = self.rolldic_style.get()
            self.mode_button.configure(text=f"D: {disp_text} | R: {roll_text}")
            
            # Show brief confirmation
            # messagebox.showinfo(parent=self.Window2, title="Display Mode", message=f"Display set to {disp_text}")
            # No need for individual window management here, 
            # displayres handles showing/hiding windows on roll

        def update_display_mode(self, mode):
            # This method is now legacy but kept for compatibility if needed elsewhere
            pass

        def on_closing(self):
            self.not_closing=0
            if os.path.exists(PAST_CONFIGS_DIR):
                for filename in os.listdir(PAST_CONFIGS_DIR):
                    os.remove(os.path.join(PAST_CONFIGS_DIR, filename))
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
            os.makedirs(SAVED_CONFIGS_DIR, exist_ok=True)
            for filename in os.listdir(SAVED_CONFIGS_DIR):
                self.openmenu.add_command(label=filename[:-4], command=lambda filepath=os.path.join(SAVED_CONFIGS_DIR, filename): self.openfile(filepath))
            self.openmenu.add_separator()
            self.openmenu.add_command(label="Open new", command=lambda: self.openfile(0))
            self.menubar.add_cascade(label="Open", menu=self.openmenu)            

            self.menubar.add_command(label="Save", command=self.savefile)
            self.menubar.add_command(label="Save as...", command=self.savefileas)
                
        def modify(self, a, b, c):
            self.modified=1           

        def build_resor(self):  
            self.aFrame=ctk.CTkFrame(self.terFrame, fg_color="gray25")
            self.aFrame.columnconfigure((0,1), weight=1, uniform="anterior")
            self.aFrame.grid(row=0, column=0, sticky="ew", pady=(0,self.rescale))

            self.anteriorLabel=ctk.CTkLabel(self.aFrame, text="Anterior", fg_color="gray30", corner_radius=6, font=("Roboto", 14))
            self.anteriorLabel.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale, columnspan=2)

            self.aconLabel=ctk.CTkLabel(self.aFrame, text="Constant", fg_color="gray30", corner_radius=6, font=("Roboto", 12))
            self.aconLabel.grid(row=1, column=0, sticky="ew", padx=(self.rescale,self.rescale/2), pady=(0,self.rescale))

            self.aadvLabel=ctk.CTkLabel(self.aFrame, text="Advantage", fg_color="gray30", corner_radius=6, font=("Roboto", 12))
            self.aadvLabel.grid(row=1, column=1, sticky="ew", padx=(self.rescale/2,self.rescale), pady=(0,self.rescale))

            self.acontotal=ctk.CTkLabel(self.aFrame, text=(self.premod.const>0)*"+"+str(self.premod.const), fg_color="gray30", corner_radius=6, font=("Roboto", 12))
            self.acontotal.grid(row=2, column=0, sticky="ew", padx=(self.rescale,self.rescale/2), pady=(0,self.rescale))

            self.aadvtotal=ctk.CTkLabel(self.aFrame,text=(self.premod.adv>0)*"+"+str(self.premod.adv), fg_color="gray30", corner_radius=6, font=("Roboto", 12))
            self.aadvtotal.grid(row=2, column=1, sticky="ew", padx=(self.rescale/2,self.rescale), pady=(0,self.rescale))
            
            for i in range(len(self.resor)):
                aux=("Resource #"+str(i+1))*(self.resor[i].resName.replace(" ", "")=="")+self.resor[i].resName*(self.resor[i].resName.replace(" ", "")!="")
                self.resor[i].mainFrame=ctk.CTkFrame(self.terFrame, fg_color="gray25")
                self.resor[i].mainFrame.columnconfigure((0,1) , weight=1)
                self.resor[i].mainFrame.grid(row=i+1, column=0, sticky="ew", pady=(0,self.rescale))

                self.resor[i].mainButton=ctk.CTkRadioButton(self.resor[i].mainFrame, 
                                                                        variable = self.selectRes, 
                                                                        value = i+1,
                                                                        text = aux, fg_color=self.color, bg_color="gray25", border_color="gray30", hover_color=self.color, font=("Roboto", 12))
                self.resor[i].mainButton.grid(row=0, column=0, sticky="w", padx=self.rescale, pady=self.rescale)

                self.resor[i].qntLabel=ctk.CTkLabel(self.resor[i].mainFrame, text=self.resor[i].qnt, fg_color="gray30", corner_radius=6, font=("Roboto", 12))
                self.resor[i].qntLabel.grid(row=0, column=1, sticky="e", padx=(0,self.rescale), pady=self.rescale)
    
                self.resor[i].subButtons=[]
                for j in range(len(self.resor[i].listSubres)):
                    self.resor[i].subButtons.append(ctk.CTkButton(self.resor[i].mainFrame, 
                                                                        text = self.resor[i].listSubres[j].subresName,
                                                                        border_color=self.color,
                                                                        border_width=2, 
                                                                        fg_color="gray30", hover_color="gray40", font=("Roboto", 12), command = lambda c=(i, j): self.destroy_subres(c))
                    )
                    self.resor[i].subButtons[-1].grid(row=j+1, column=0, sticky="ew", padx=self.rescale, pady=(0,self.rescale), columnspan=2)

                self.resor[i].deleteButton=ctk.CTkButton(self.resor[i].mainFrame, 
                                                                        text = "Delete resource",
                                                                        text_color="gray30",
                                                                        border_color=self.color,
                                                                        border_width=2,
                                                                        fg_color=self.color, hover_color="gray40", font=("Roboto", 12), command = lambda c=i: self.destroy_res(c))
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
                messagebox.showerror(parent=self.Window2, title="Conversion error", message="Something went wrong, please check your submission.")
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
                    with open(os.path.join(PAST_CONFIGS_DIR, str(self.past_index_max)+'.txt'), 'xb') as file:
                        pickle.dump(message_sent, file)
                except Exception:
                    print(traceback.format_exc())
                    self.on_closing()
                self.past_index_max+=1
                if self.unmoved:
                    self.past_index=self.past_index_max
                    messagebox.showinfo(parent=self.Window2, title="Tip", message="Browse through past settings with ^ or ⌄.")
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
                messagebox.showerror(parent=self.Window2, title="Path error", message="Invalid path, please try again.")
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
                            self.path=os.path.join(PAST_CONFIGS_DIR, str(self.past_index)+'.txt')
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
                    self.path=os.path.join(PAST_CONFIGS_DIR, str(self.past_index)+'.txt')
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
                self.crit.trace_add('write', self.modify)
                self.mini=StringVar(value='0')
                self.mini.trace_add('write', self.modify)
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
                # self.deiconify() - moved to end of layout to prevent jank
                self.title("Chatroom") 
                self.resizable(width = False, height = False) 
                self.geometry("800x504")
                self.columnconfigure(1 , weight=1)
                self.rowconfigure(1, weight=1)

                self.sidebarLabel=ctk.CTkLabel(self, text="Players online", fg_color="gray20", corner_radius=6, font=("Roboto", 14))
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
                                    fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.AllClick())
                self.allButton.grid(row=2, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.blocbtt= ctk.CTkButton(self, 
                                                    text = '►',
                                                    width=26,                      
                                                    border_color=self.color,
                                                    border_width=2,
                                                    fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.blocswitch())
                self.blocbtt.grid(row=0, column=3, padx=self.rescale, pady=self.rescale, sticky="ns", rowspan=3)
                                
                self.entryMsg = ctk.CTkEntry(self, fg_color="gray20", border_width=0, placeholder_text_color="gray30", placeholder_text="Write a message", font=("Roboto", 12)) 
                self.entryMsg.grid(row=2, column=1, padx=(0,self.rescale), pady=self.rescale, sticky="ew")
                #self.entryMsg.after(20, self.entryMsg.focus)
                
                self.buttonMsg = ctk.CTkButton(self, 
                                                            text = "Send",
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda : self.sendButton(self.entryMsg.get())) 
                self.buttonMsg.grid(row=2, column=2, pady=self.rescale, sticky="ew")
                
                self.textCons=ctk.CTkTextbox(self, fg_color="gray20", font=("Roboto", 12))
                self.textCons.grid(row=0, column=1, pady=(self.rescale,0), sticky="nsew", rowspan=2, columnspan=2)
                self.textCons.configure(cursor = "arrow") 
                self.textCons.configure(state = DISABLED) 
                self.bind('<Return>', (lambda event: self.sendButton(self.entryMsg.get())))
                self.bind("<Up>", self.up_down)
                self.bind("<Down>", self.up_down)
                self.protocol("WM_DELETE_WINDOW", self.on_closing)
                self.textCons.tag_config('date', foreground="gray30")
                self.textCons.tag_config('overstrike', overstrike=True)
                
                self.Window2=ctk.CTkToplevel(fg_color="gray15")
                self.Window2.withdraw()
                self.Window2.title("Roll") 
                self.Window2.resizable(width = False, height = False)
                self.Window2.geometry("1350x524")
                self.Window2.columnconfigure(1 , weight=1)
                self.Window2.rowconfigure((1, 3), weight=1)

                self.menubar = Menu(self.Window2)
                self.Window2.config(menu=self.menubar)

                self.openmenu=Menu(self.menubar, tearoff=0)
                self.build_menu()

                self.selecLabel=ctk.CTkLabel(self.Window2, text="Select to roll", fg_color="gray20", corner_radius=6, font=("Roboto", 14))
                self.selecLabel.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.sidebaroll=ctk.CTkScrollableFrame(self.Window2,
                                                    fg_color="gray20",
                                                    scrollbar_button_color="gray25",
                                                    scrollbar_button_hover_color="gray35")
                self.sidebaroll.columnconfigure(0 , weight=1)
                self.sidebaroll.grid(row=1, column=0, padx=self.rescale, sticky="ns")

                self.selectedLabel=ctk.CTkLabel(self.Window2, text="Selected", fg_color="gray20", corner_radius=6, font=("Roboto", 14))
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
                                    fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.rollerrola())
                self.rollBtt.grid(row=4, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.resourcesLabel=ctk.CTkLabel(self.Window2, text="Resources", fg_color="gray20", corner_radius=6, font=("Roboto", 14))
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
                                                            fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda : self.send_block())
                self.button_block.grid(row=4, column=2, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.resor=[]

                self.selectRes=IntVar(value=0)

                self.secFrame=ctk.CTkFrame(self.Window2, fg_color="gray15")
                self.secFrame.columnconfigure(0 , weight=1)
                self.secFrame.grid(row=0, column=1, pady=self.rescale, sticky="nsew", rowspan=5)

                self.stypebar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.stypebar.columnconfigure((5, 9) , weight=1)
                self.stypebar.grid(row=0, column=0, sticky="ew", pady=(0,self.rescale))

                self.meBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'me',
                                                                        text = 'Me', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15, font=("Roboto", 12))
                
                self.hiddenBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'hidden',
                                                                        text = 'Hidden', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15, font=("Roboto", 12))
                self.weBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'we',
                                                                        text = 'We', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15, font=("Roboto", 12))

                self.youBtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'you',
                                                                        text = 'You', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15, font=("Roboto", 12))

                self.sbtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 's',
                                                                        text = 'Yes', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15, font=("Roboto", 12))

                self.nbtt=ctk.CTkRadioButton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 'n',
                                                                        text = 'No', fg_color=self.color, border_color="gray25", hover_color=self.color,
                                                                        width=15, font=("Roboto", 12))

                self.sdtypelabel= ctk.CTkLabel(self.stypebar, text='Send type:', font=("Roboto", 12))
                self.separator0= ctk.CTkLabel(self.stypebar, text="")
                self.messagelabel= ctk.CTkLabel(self.stypebar, text='Hidden message:', font=("Roboto", 12))
                self.sdtypelabel.grid(row=0, column=0, padx=self.rescale)
                self.weBtt.grid(row=0, column=1, padx=(0,self.rescale))
                self.meBtt.grid(row=0, column=2, padx=(0,self.rescale))
                self.youBtt.grid(row=0, column=3, padx=(0,self.rescale))
                self.hiddenBtt.grid(row=0, column=4, padx=(0, self.rescale*4))
                self.separator0.grid(row=0, column=5, sticky="ew")
                self.messagelabel.grid(row=0, column=6, padx=(0,self.rescale))
                self.sbtt.grid(row=0, column=7)
                self.nbtt.grid(row=0, column=8, padx=self.rescale)

                self.separator1= ctk.CTkLabel(self.stypebar, text="")
                self.separator1.grid(row=0, column=9, sticky="ew")

                disp_text = self.displaymode.get().capitalize()
                if self.displaymode.get().lower() == 'dice':
                    disp_text = f"Dice ({self.dice_style.get()})"
                
                self.mode_button = ctk.CTkButton(self.stypebar, 
                                                 text=f"D: {disp_text} | R: {self.rolldic_style.get()}",
                                                 width=260, height=24,
                                                 fg_color="gray25", border_color="gray30",
                                                 border_width=1, hover_color="gray35",
                                                 font=("Roboto", 11),
                                                 command=self.show_mode_menu)
                self.mode_button.grid(row=0, column=11, padx=self.rescale)

                # Remove the old switcher setup
                # self.update_display_mode(self.displaymode.get())

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

                self.reslabel = ctk.CTkEntry(self.resourcebar2, fg_color="gray25", border_width=0, placeholder_text_color="gray35", placeholder_text="Resource name", font=("Roboto", 12), justify="center")
                self.reslabel.grid(row=0, column=1, padx=self.rescale, pady=self.rescale, columnspan=3)

                self.separator8= ctk.CTkLabel(self.resourcebar2, text="")
                self.separator8.grid(row=0, column=4, sticky="ew")

                self.resbtt2 = ctk.CTkButton(self.resourcebar2, 
                                                            text = '◄', 
                                                            width=26,
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.callbackRes(self.reslabel.get())) 
                self.resbtt2.grid(row=1, column=1, padx=(0,self.rescale), pady=(0,self.rescale))
                
                self.resbox = IntSpinbox(self.resourcebar2,
                                    color=self.color, variable = self.res,
                                    from_ = 0)
                self.resbox.grid(row=1, column=2, padx=(0,self.rescale), pady=(0,self.rescale))

                self.resbtt = ctk.CTkButton(self.resourcebar2, 
                                                            text = "+", 
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.resourcepaste(self.res.get(), self.reslabel.get())) 
                self.resbtt.grid(row=1, column=3, pady=(0,self.rescale))

                self.critlabel= ctk.CTkLabel(self.resourcebar1, text='Crit chance (%)', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.critlabel.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew", columnspan=2)

                self.critbox = IntSpinbox(self.resourcebar1,
                                    color=self.color, variable = self.crit,
                                    from_ = 0,
                                    step_size = 10)
                self.critbox.grid(row=1, column=0, pady=(0,self.rescale))

                self.minlabel= ctk.CTkLabel(self.resourcebar3, text='Minimum roll', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
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

                self.antelabel= ctk.CTkLabel(self.antebar, text='Anterior', fg_color="gray25", corner_radius=6, font=("Roboto", 14))           
                self.antelabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=self.rescale, columnspan=11)

                self.aconlabel= ctk.CTkLabel(self.antebar,text='Constant', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
           
                self.aconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), sticky="ew", columnspan=2)
                

                self.acon = IntSpinbox(self.antebar,
                                        color=self.color, variable = self.ac)
                self.acon.grid(row=2, column=0, padx=self.rescale, pady=self.rescale)

                self.aconbtt = ctk.CTkButton(self.antebar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda : self.antepaste(int(self.ac.get()), 1))
                self.aconbtt.grid(row=2, column=1)

                self.separator1= ctk.CTkLabel(self.antebar, text="")
                self.separator1.grid(row=2, column=2, sticky="ew")

                self.aadvlabel= ctk.CTkLabel(self.antebar,text='Advantage', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.aadvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), sticky="ew", columnspan=2)

                self.aadv = IntSpinbox(self.antebar,
                                        color=self.color, variable = self.aa)
                self.aadv.grid(row=2, column=8)

                self.aadvbtt = ctk.CTkButton(self.antebar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda : self.anteadvpaste(int(self.aa.get())))

                self.aadvbtt.grid(row=2, column=9, padx=self.rescale)

                self.separator2= ctk.CTkLabel(self.antebar, text="")
                self.separator2.grid(row=2, column=7, sticky="ew")

                self.adlabel= ctk.CTkLabel(self.antebar,text='Dice', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.adlabel.grid(row=1, column=3, padx=self.rescale, sticky="ew", columnspan=4)

                self.adic = IntSpinbox(self.antebar,
                                    color=self.color, variable = self.ad[0])
                self.adic.grid(row=2, column=3)

                self.addlabel= ctk.CTkLabel(self.antebar, text='d', width=0, font=("Roboto", 12))
                self.addlabel.grid(row=2, column=4, padx=10/3)

                self.adic2 = IntSpinbox(self.antebar,
                                    color=self.color, variable = self.ad[1],
                                    from_ = 0)
                self.adic2.grid(row=2, column=5, padx=(0,self.rescale))

                self.adicbtt = ctk.CTkButton(self.antebar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda : self.antepaste(int(self.ad[0].get()), int(self.ad[1].get())))
                self.adicbtt.grid(row=2, column=6)

                self.interbar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.interbar.columnconfigure((2, 7), weight=1)
                self.interbar.grid(row=3, column=0, sticky="ew")

                self.interlabel= ctk.CTkLabel(self.interbar, text='Intermediate', fg_color="gray25", corner_radius=6, font=("Roboto", 14))
                self.interlabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=self.rescale, columnspan=11)

                self.iconlabel= ctk.CTkLabel(self.interbar,text='Constant', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.iconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), sticky="ew", columnspan=2)

                self.icon = IntSpinbox(self.interbar,
                                        color=self.color, variable = self.ic)
                self.icon.grid(row=2, column=0, padx=self.rescale, pady=self.rescale)

                self.iconbtt = ctk.CTkButton(self.interbar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.postpaste(int(self.ic.get()), 1, "c", "Inter"))

                self.iconbtt.grid(row=2, column=1)

                self.separator3= ctk.CTkLabel(self.interbar, text="")
                self.separator3.grid(row=2, column=2, sticky="ew")

                self.iadvlabel= ctk.CTkLabel(self.interbar,text='Advantage', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.iadvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), sticky="ew", columnspan=2)

                self.iadv = IntSpinbox(self.interbar,
                                        color=self.color, variable = self.ia)

                self.iadv.grid(row=2, column=8)

                self.iadvbtt = ctk.CTkButton(self.interbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.postpaste(int(self.ia.get()), 0, "adv", "Inter"))

                self.iadvbtt.grid(row=2, column=9, padx=self.rescale)

                self.separator4= ctk.CTkLabel(self.interbar, text="")
                self.separator4.grid(row=2, column=7, sticky="ew")

                self.idlabel= ctk.CTkLabel(self.interbar,text='Dice', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.idlabel.grid(row=1, column=3, padx=self.rescale, sticky="ew", columnspan=4)

                self.idic = IntSpinbox(self.interbar,
                                    color=self.color, variable = self.id[0])
                self.idic.grid(row=2, column=3)

                self.iddlabel= ctk.CTkLabel(self.interbar, text='d', width=0, font=("Roboto", 12))
                self.iddlabel.grid(row=2, column=4, padx=10/3)

                self.idic2 = IntSpinbox(self.interbar,
                                    color=self.color, variable = self.id[1],
                                    from_ = 0)
                self.idic2.grid(row=2, column=5, padx=(0,self.rescale))

                self.idicbtt = ctk.CTkButton(self.interbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.postpaste(int(self.id[0].get()), int(self.id[1].get()), "dice", "Inter"))
                self.idicbtt.grid(row=2, column=6)

                self.postbar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.postbar.columnconfigure((2, 7), weight=1)
                self.postbar.grid(row=4, column=0, sticky="ew", pady=self.rescale)

                self.postlabel= ctk.CTkLabel(self.postbar, text='Posterior', fg_color="gray25", corner_radius=6, font=("Roboto", 14))
                self.postlabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=self.rescale, columnspan=11)

                self.pconlabel= ctk.CTkLabel(self.postbar,text='Constant', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.pconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), sticky="ew", columnspan=2)

                self.pcon = IntSpinbox(self.postbar,
                                        color=self.color, variable = self.pc)
                self.pcon.grid(row=2, column=0, padx=self.rescale, pady=self.rescale)

                self.pconbtt = ctk.CTkButton(self.postbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.postpaste(int(self.pc.get()), 1, "c", "Post"))

                self.pconbtt.grid(row=2, column=1)

                self.separator5= ctk.CTkLabel(self.postbar, text="")
                self.separator5.grid(row=2, column=2, sticky="ew")

                self.padvlabel= ctk.CTkLabel(self.postbar,text='Advantage', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.padvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), sticky="ew", columnspan=2)

                self.padv = IntSpinbox(self.postbar,
                                        color=self.color, variable = self.pa)

                self.padv.grid(row=2, column=8)

                self.padvbtt = ctk.CTkButton(self.postbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.postpaste(int(self.pa.get()), 0, "adv", "Post"))

                self.padvbtt.grid(row=2, column=9, padx=self.rescale)

                self.separator6= ctk.CTkLabel(self.postbar, text="")
                self.separator6.grid(row=2, column=7, sticky="ew")

                self.pdlabel= ctk.CTkLabel(self.postbar,text='Dice', fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                self.pdlabel.grid(row=1, column=3, padx=self.rescale, sticky="ew", columnspan=4)

                self.pdic = IntSpinbox(self.postbar,
                                    color=self.color, variable = self.pd[0])
                self.pdic.grid(row=2, column=3)

                self.pddlabel= ctk.CTkLabel(self.postbar, text='d', width=0, font=("Roboto", 12))
                self.pddlabel.grid(row=2, column=4, padx=10/3)

                self.pdic2 = IntSpinbox(self.postbar,
                                    color=self.color, variable = self.pd[1],
                                    from_ = 0)
                self.pdic2.grid(row=2, column=5, padx=(0,self.rescale))

                self.pdicbtt = ctk.CTkButton(self.postbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.postpaste(int(self.pd[0].get()), int(self.pd[1].get()), "dice", "Post"))
                self.pdicbtt.grid(row=2, column=6)

                #------------------------
                self.hiddenres=ctk.CTkToplevel(fg_color="gray15")
                self.hiddenres.withdraw()
                self.hiddenres.title("Result (hidden)")
                self.hiddenres.resizable(width = False, height = False)
                self.hiddenres.geometry('300x100')
                self.hiddenres.protocol("WM_DELETE_WINDOW", self.hiddenres.withdraw)
                self.hiddenres.columnconfigure(0, weight=1)
                
                self.hidden_label=ctk.CTkLabel(self.hiddenres, text="", text_color=self.color, font=("Roboto", 25), fg_color="gray20", corner_radius=6)
                self.hidden_label.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale)

                self.dicewindow = ctk.CTkToplevel(fg_color="gray15")
                self.dicewindow.withdraw()
                self.dicewindow.title("Result (dice)")
                self.dicewindow.resizable(width = False, height = False)
                self.dicewindow.columnconfigure(0, weight=1)
                self.dicewindow.rowconfigure(0, weight=0)
                self.dicewindow.rowconfigure(1, weight=1)
                self.dicewindow.geometry('450x400')
                self.dicewindow.protocol("WM_DELETE_WINDOW", self.dicewindow.withdraw)

                self.progresswindow=ctk.CTkToplevel(fg_color="gray15")
                self.progresswindow.withdraw()
                self.progresswindow.title("Result (bar)")
                self.progresswindow.resizable(width = False, height = False)
                self.progresswindow.geometry('450x190') 
                self.progresswindow.columnconfigure(0, weight=1)
                self.progresswindow.rowconfigure(0, weight=0) # Pin info label to top
                self.progresswindow.rowconfigure(1, weight=1) # Let result frame expand
                self.progresswindow.protocol("WM_DELETE_WINDOW", self.progresswindow.withdraw)

                self.InfoLabel = ctk.CTkLabel(self.dicewindow, text="", fg_color="gray20", corner_radius=6, font=("Roboto", 14), pady=self.rescale)
                self.InfoLabel.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=(self.rescale, 0))
                self.ResultFrame=ctk.CTkFrame(self.dicewindow, fg_color="gray20")
                self.ResultFrame.columnconfigure(0, weight=1)
                self.ResultFrame.rowconfigure(0, weight=1)
                self.ResultFrame.grid(row=1, column=0, sticky="nsew", padx=self.rescale, pady=(self.rescale, self.rescale))
                
                self.ResultLabel=ctk.CTkLabel(self.ResultFrame, text="", text_color=self.color, font=("Roboto", 25), fg_color="gray20")
                self.ResultLabel.grid(row=0, column=0, pady=self.rescale)
                self.panel = ctk.CTkLabel(self.ResultFrame, text="", fg_color=self.color)
                self.panel.grid(row=1, column=0)

                # Pre-load dice images to prevent flickering
                self.dice_images_cache = {}
                for filename in os.listdir(DICE_IMAGES_DIR):
                    if filename.endswith(".png"):
                        img_path = os.path.join(DICE_IMAGES_DIR, filename)
                        img = Image.open(img_path).convert("RGBA")
                        self.dice_images_cache[filename] = ctk.CTkImage(img, size=(250,250))

                self.InfoLabel2 = ctk.CTkLabel(self.progresswindow, text="", fg_color="gray20", corner_radius=6, font=("Roboto", 14), pady=self.rescale)
                self.InfoLabel2.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=(self.rescale, 0))
                self.ResultFrame2 = ctk.CTkFrame(self.progresswindow, fg_color="gray20")
                self.ResultFrame2.columnconfigure(0, weight=1)
                self.ResultFrame2.rowconfigure((0, 1, 2), weight=1)
                self.ResultFrame2.grid(row=1, column=0, sticky="nsew", padx=self.rescale, pady=(self.rescale, self.rescale))

                self.ResultLabel2=ctk.CTkLabel(self.ResultFrame2, text="", text_color=self.color, font=("Roboto", 25, "bold"), fg_color="gray20")
                self.ResultLabel2.grid(row=0, column=0, pady=self.rescale)
                
                # Container for progress bar and zones
                self.BarContainer = ctk.CTkFrame(self.ResultFrame2, fg_color="transparent")
                self.BarContainer.grid(row=1, column=0, padx=self.rescale, pady=(0, self.rescale))
                
                # Zones background - Make it slightly taller than the bar so it's visible
                self.ZoneFrame = ctk.CTkFrame(self.BarContainer, fg_color="gray25", height=24, width=400, corner_radius=10)
                self.ZoneFrame.grid(row=0, column=0, sticky="ew")
                self.ZoneFrame.grid_propagate(False)
                
                self.CFZone = ctk.CTkFrame(self.ZoneFrame, fg_color="#4d4d4d", corner_radius=0) # gray30
                self.FailZone = ctk.CTkFrame(self.ZoneFrame, fg_color="#595959", corner_radius=0) # gray35
                self.SuccessZone = ctk.CTkFrame(self.ZoneFrame, fg_color="#666666", corner_radius=0) # gray40
                self.CritZone = ctk.CTkFrame(self.ZoneFrame, fg_color="#737373", corner_radius=0) # gray45
                
                # Precision markers (vertical lines)
                self.CFMarker = ctk.CTkFrame(self.BarContainer, fg_color="white", width=1, height=28)
                self.SMarker = ctk.CTkFrame(self.BarContainer, fg_color="white", width=1, height=28)
                self.CSMarker = ctk.CTkFrame(self.BarContainer, fg_color="white", width=1, height=28)

                self.progress = ctk.CTkProgressBar(self.BarContainer, width=400, height=12, fg_color="gray25", progress_color=self.color, corner_radius=0)
                self.progress.grid(row=0, column=0, padx=0, pady=0) # Overlay on zones
                
                # Labels for thresholds
                self.ThreshLabelsFrame = ctk.CTkFrame(self.BarContainer, fg_color="transparent", height=20, width=400)
                self.ThreshLabelsFrame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
                self.ThreshLabelsFrame.grid_propagate(False)
                
                self.CFThreshLabel = ctk.CTkLabel(self.ThreshLabelsFrame, text="CF", font=("Roboto", 10, "bold"), text_color="gray60")
                self.SuccessThreshLabel = ctk.CTkLabel(self.ThreshLabelsFrame, text="S", font=("Roboto", 10, "bold"), text_color="gray60")
                self.CritThreshLabel = ctk.CTkLabel(self.ThreshLabelsFrame, text="CS", font=("Roboto", 10, "bold"), text_color="gray60")

                # Wheel window setup
                self.wheelwindow=ctk.CTkToplevel(fg_color="gray15")
                self.wheelwindow.withdraw()
                self.wheelwindow.title("Result (wheel)")
                self.wheelwindow.geometry('450x530')
                self.wheelwindow.resizable(width = False, height = False)
                self.wheelwindow.columnconfigure(0, weight=1)
                self.wheelwindow.rowconfigure(0, weight=0)
                self.wheelwindow.rowconfigure(1, weight=1)
                self.wheelwindow.protocol("WM_DELETE_WINDOW", self.wheelwindow.withdraw)

                self.InfoLabel3 = ctk.CTkLabel(self.wheelwindow, text="", fg_color="gray20", corner_radius=6, font=("Roboto", 14), pady=self.rescale)
                self.InfoLabel3.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=(self.rescale, 0))
                self.ResultFrame3 = ctk.CTkFrame(self.wheelwindow, fg_color="gray20")
                self.ResultFrame3.columnconfigure(0, weight=1)
                self.ResultFrame3.rowconfigure(0, weight=1)
                self.ResultFrame3.grid(row=1, column=0, sticky="nsew", padx=self.rescale, pady=(self.rescale, self.rescale))

                self.ResultLabel3=ctk.CTkLabel(self.ResultFrame3, text="", text_color=self.color, font=("Roboto", 25), fg_color="gray20")
                self.ResultLabel3.grid(row=0, column=0, pady=self.rescale)
                
                # Create matplotlib figure for wheel
                self.wheel_fig = Figure(figsize=(4, 4), dpi=100, facecolor='#333333')
                self.wheel_ax = self.wheel_fig.add_subplot(111)
                self.wheel_ax.set_facecolor('#333333')
                self.wheel_ax.axis('equal')
                
                self.wheel_canvas = FigureCanvasTkAgg(self.wheel_fig, master=self.ResultFrame3)
                self.wheel_canvas.get_tk_widget().grid(row=1, column=0, padx=self.rescale, pady=(0,self.rescale))

                self.current_anim_id = 0


                # Pre-create rolldic window and canvas (like wheel display mode)
                self.possi = ctk.CTkToplevel(fg_color="gray15")
                self.possi.withdraw()
                self.possi.title("Dice roll")
                self.possi.geometry('820x630') # Shorter window to reduce bottom space
                self.possi.resizable(width=True, height=True)
                self.possi.protocol("WM_DELETE_WINDOW", self.possi.withdraw)
                
                self.possi_frame = ctk.CTkFrame(self.possi, fg_color="gray20")
                self.possi_frame.pack(fill=BOTH, expand=True, padx=self.rescale, pady=self.rescale)
                
                self.rolldic_res_label = ctk.CTkLabel(self.possi_frame, text="", font=("Roboto", 18, "bold"), text_color="white")
                self.rolldic_res_label.pack(side=TOP, pady=(15, 0))
                
                # Create the figure and canvas once
                self.possi_fig = Figure(figsize=(8, 5.7), dpi=100, facecolor='#333333')
                self.possi_ax = self.possi_fig.add_subplot(111)
                self.possi_ax.set_facecolor('#333333')
                self.possi_ax.set_axis_on()

                
                self.possi_canvas = FigureCanvasTkAgg(self.possi_fig, master=self.possi_frame)
                self.possi_canvas.get_tk_widget().pack(side=TOP, padx=0, pady=0)
                
                # Resize handler for auto-scaling
                def on_possi_resize(event):
                    if self.possi.winfo_viewable() and event.width > 10 and event.height > 10:
                        self.possi_fig.tight_layout(pad=2.2) # Tighter but safe padding
                        self.possi_canvas.draw()
                
                self.possi.bind("<Configure>", on_possi_resize)
                
                # Force initial layout calculation
                self.possi.deiconify()
                self.possi.update()
                self.possi_fig.tight_layout(pad=2.2)
                self.possi_canvas.draw()
                self.possi.withdraw()



                # self.hiddenres.withdraw()
                # self.progresswindow.withdraw()
                # self.dicewindow.withdraw()
                # self.wheelwindow.withdraw()

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
                # self.Window2.withdraw()

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
                self.deiconify()

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
                            if textlis[u].startswith(r'\j'):
                                textlis[u]=textlis[u].replace(r'\j','',1)
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
                            else:
                                line_content = textlis[u]
                                if textlis[u+1]!='' and not textlis[u+1].startswith(' '):
                                    line_content = justify(textlis[u], 42)
                                
                                # Parse for strikethrough tags \s ... \s
                                parts = re.split(r'(\\s)', line_content)
                                current_tags = []
                                for part in parts:
                                    if part == r'\s':
                                        if 'overstrike' in current_tags:
                                            current_tags.remove('overstrike')
                                        else:
                                            current_tags.append('overstrike')
                                    else:
                                        self.textCons.insert(END, part, tuple(current_tags))
                                self.textCons.insert(END, '\n')
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
                            self.selecLabel.configure(text='Remaining: '+str(message.num)+" rolls")
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
                            
                            
                            
                            aux_2=ctk.CTkLabel(possibs, text='Net advantage', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                            aux_2.grid(row=0, column=3, padx=(self.rescale, 0), pady=self.rescale)
                            aux_3=ctk.CTkLabel(possibs, text='Resources', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
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
                                aux_1=ctk.CTkLabel(possibs, text='% of f->s+', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
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
                                aux_12=ctk.CTkLabel(possibs, text='% of s->cs', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
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
                                aux_13=ctk.CTkLabel(possibs, text='% of cf->f+', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                                aux_13.grid(row=0, column=2, padx=(self.rescale, 0), pady=self.rescale)
                                aux_13_mor=ctk.CTkFrame(possibs, fg_color="gray20")
                                aux_13_mor.grid_columnconfigure(0, weight=1)
                                aux_13_mor.grid(row=1, column=2, padx=(self.rescale, 0), sticky="ew")
                                
                            for i in range(len(message)):
                                p, crit, r, resultStr=self.transl(message[i])
                                if aux1:
                                    aux_1=ctk.CTkLabel(aux_1_mor, text=probs[i], fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                    aux_1.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                if aux2:
                                    aux_12=ctk.CTkLabel(aux_12_mor, text=probs_crit[i], fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                    aux_12.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                if aux3:
                                    aux_13=ctk.CTkLabel(aux_13_mor, text=probs_fail[i], fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                    aux_13.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                                
                                aux_2=ctk.CTkLabel(aux_2_mor, text='+'*(message[i].adv>0)+str(message[i].adv), fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                aux_2.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")

                                text=message[i].mods[:-2]+'N/A'*(not message[i].mods[:-2])
                                resButton = ctk.CTkButton(aux_3_mor,
                                                text = text,
                                                fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                font=("Roboto", 12),
                                                command= lambda p=p, crit=crit, r=r, resultStr=resultStr, send_type=send_type: threading.Thread(target = self.displayres, args=[p, crit, r, resultStr, send_type, text]).start())
                                resButton.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                            
                            resButton = ctk.CTkButton(possibs,
                                                text = 'Show results',
                                                fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                font=("Roboto", 14),
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
            aux_1=ctk.CTkLabel(possibs, text='Result', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
            aux_1.grid(row=0, column=0, padx=self.rescale, pady=self.rescale, sticky="ew")
            aux_2=ctk.CTkLabel(possibs, text='Net advantage', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
            aux_2.grid(row=0, column=1, padx=(0, self.rescale), pady=self.rescale, sticky="ew")
            aux_3=ctk.CTkLabel(possibs, text='Resources', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
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
                    
                aux_1=ctk.CTkLabel(aux_1_mor, text=resultStr, fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                aux_2=ctk.CTkLabel(aux_2_mor, text='+'*(message[i].adv>=0)+str(message[i].adv), fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                aux_3=ctk.CTkLabel(aux_3_mor, text=message[i].mods[:-2]+'N/A'*(not message[i].mods[:-2]), fg_color="gray25", corner_radius=6, font=("Roboto", 12))

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
                        sides = dice_list[index][1]
                        
                        # Extract keep/drop info if present
                        k_type = dice_list[index][2] if len(dice_list[index]) > 2 else None
                        k_num = dice_list[index][3] if len(dice_list[index]) > 3 else number
                        
                        tt_aux=math.factorial(number)
                        for k in list(itertools.combinations_with_replacement([i for i in range(1, sides+1)], number)):
                            # Apply keep/drop logic to sorted combination k
                            if k_type == 'kh':
                                current_sum = sum(k[-k_num:]) if k_num > 0 else 0
                            elif k_type == 'kl':
                                current_sum = sum(k[:k_num]) if k_num > 0 else 0
                            elif k_type == 'dh':
                                current_sum = sum(k[:-k_num]) if k_num < number else 0
                            elif k_type == 'dl':
                                current_sum = sum(k[k_num:]) if k_num < number else 0
                            else:
                                current_sum = sum(k)
                                
                            tt=tt_aux
                            for i in range(1, sides+1):
                                tt/=math.factorial(k.count(i))
                            dic_aux=self.rec(tot+sgn*current_sum, num+tt, dice_list, index+1)
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
                        sides = dice_list[index][1]
                        
                        k_type = dice_list[index][2] if len(dice_list[index]) > 2 else None
                        k_num = dice_list[index][3] if len(dice_list[index]) > 3 else number
                        
                        tt_aux=math.factorial(number)
                        for k in list(itertools.combinations_with_replacement([i for i in range(1, sides+1)], number)):
                            if k_type == 'kh':
                                current_sum = sum(k[-k_num:]) if k_num > 0 else 0
                            elif k_type == 'kl':
                                current_sum = sum(k[:k_num]) if k_num > 0 else 0
                            elif k_type == 'dh':
                                current_sum = sum(k[:-k_num]) if k_num < number else 0
                            elif k_type == 'dl':
                                current_sum = sum(k[k_num:]) if k_num < number else 0
                            else:
                                current_sum = sum(k)
                                
                            aux=sgn*current_sum
                            tt=tt_aux
                            for i in range(1, sides+1):
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
                dice_match = re.search(r"'.*?'", stri)
                if not dice_match:
                    return
                dice_str = dice_match.group()
                stri=dice_str.replace("'","").replace(' ', '')
                # Find all parts (dice or constants) in order
                stri_con = re.findall(r'[+-]?[^+-]+', stri)
                dice_list=[]
                roll=0
                breakdown_parts = []
                for i in stri_con:
                    if 'd' in i:
                        m = re.match(r"([+-]?\d*)d(\d+)([kKdD][hHlL])?(\d+)?", i)
                        if m:
                            count_str, sides_str, k_type, k_num_str = m.groups()
                            
                            # Count
                            if count_str == '' or count_str == '+':
                                count = 1
                            elif count_str == '-':
                                count = -1
                            else:
                                count = int(count_str)
                                
                            # Sides
                            sides = int(sides_str)
                            
                            # Keep type/num
                            keep_type = k_type.lower() if k_type else None
                            # Default to 1 if kh/kl present but no number, else default to all dice
                            if keep_type:
                                keep_num = int(k_num_str) if k_num_str else 1
                            else:
                                keep_num = abs(count)
                            
                            # Simulation for initial result
                            sgn = np.sign(count)
                            num_dice = abs(count)
                            rolls_data = [random.randint(1, sides) for _ in range(num_dice)]
                            
                            # Individual rolls for breakdown
                            raw_rolls = rolls_data.copy()
                            
                            rolls_data.sort() # non-decreasing for keep/drop logic
                            
                            if keep_type == 'kh':
                                kept_values = rolls_data[-keep_num:] if keep_num > 0 else []
                            elif keep_type == 'kl':
                                kept_values = rolls_data[:keep_num] if keep_num > 0 else []
                            elif keep_type == 'dh':
                                kept_values = rolls_data[:-keep_num] if keep_num < num_dice else []
                            elif keep_type == 'dl':
                                kept_values = rolls_data[keep_num:] if keep_num < num_dice else []
                            else:
                                kept_values = rolls_data
                                
                            roll += sgn * sum(kept_values)
                            dice_list.append((count, sides, keep_type, keep_num))
                            
                            # Build breakdown with highlighting for dropped dice
                            temp_kept = kept_values.copy()
                            formatted_parts = []
                            for idx, r in enumerate(raw_rolls):
                                is_kept = False
                                if r in temp_kept:
                                    is_kept = True
                                    temp_kept.remove(r)
                                
                                if idx > 0 or sgn < 0:
                                    op = "+" if sgn > 0 else "-"
                                    if is_kept:
                                        formatted_parts.append(f"{op}{r}")
                                    else:
                                        formatted_parts.append(rf"\s{op}{r}\s")
                                else:
                                    if is_kept:
                                        formatted_parts.append(f"{r}")
                                    else:
                                        formatted_parts.append(rf"\s{r}\s")
                            
                            rolls_str = "".join(formatted_parts)
                            breakdown_parts.append(f"{i}({rolls_str})")
                    else:
                        # Constant
                        try:
                            val = int(i)
                            roll += val
                            dice_list.append((val, 1))
                            breakdown_parts.append(f"{i}")
                        except:
                            pass
                
                # Combine breakdown parts
                breakdown_full = "".join(breakdown_parts)
                # Cleanup: if it starts with "+", remove it
                if breakdown_full.startswith("+"):
                    breakdown_full = breakdown_full[1:]

                dice_list=sorted(dice_list, key=lambda tup: abs(tup[0]))

                # Send result notice to server
                result_msg = msg(['broadcast_roll_result'], f"{self.name} rolled {dice_str} -> {breakdown_full}={roll}.")
                message_sent = pickle.dumps(result_msg)
                message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(message_sent_header+message_sent)

                if self.rolldic_style.get() == "None":
                    return

                tot=0
                num=0
                mini=0
                maxi=0
                for i in dice_list:
                    multiplier = i[0]
                    sides = i[1]
                    k_type = i[2] if len(i) > 2 else None
                    k_num = i[3] if len(i) > 3 else abs(multiplier)
                    
                    num_dice = abs(multiplier)
                    sgn = np.sign(multiplier)
                    
                    if sides > 1:
                        # Effective count for bounds
                        if k_type in ['kh', 'kl']:
                            eff_count = k_num
                        elif k_type in ['dh', 'dl']:
                            eff_count = max(0, num_dice - k_num)
                        else:
                            eff_count = num_dice
                            
                        if sgn > 0:
                            mini += eff_count
                            maxi += eff_count * sides
                        else:
                            mini += eff_count * sides * sgn
                            maxi += eff_count * 1 * sgn
                    else:
                        # Constant
                        mini += multiplier
                        maxi += multiplier
                dic=OrderedDict(sorted(self.rec(tot, num, dice_list, 0).items(), reverse=True))
                total=sum(dic.values())
                
                # PMF (Probability Mass Function) - individual probability of each result
                pmf_values = [v/total for v in dic.values()]
                
                # Cumulative values (for the existing cumulative bar chart)
                cumulative_values=[x/total for x in dic.values()]
                tot_cum=0
                for i in range(len(cumulative_values)):
                    tot_cum+=cumulative_values[i]
                    cumulative_values[i]=tot_cum

                # Increment animation ID to stop previous loops
                self.current_anim_id += 1
                anim_id = self.current_anim_id

                # Reuse pre-created possi window and canvas (like wheel display mode)
                # Clear the axes and reset the label
                self.possi_ax.clear()
                self.possi_ax.set_facecolor('#333333')
                self.possi_ax.set_axis_on()
                self.possi_ax.set_aspect('auto')
                self.rolldic_res_label.configure(text='')

                
                style = self.rolldic_style.get()
                
                if style == 'Cumulative':
                    self.possi_ax.set_xlabel('r', fontsize=12, fontname='Roboto', color='white')
                    self.possi_ax.set_ylabel('p(x>=r)', fontsize=12, fontname='Roboto', color='white')
                    self.possi_ax.tick_params(axis='x', colors='white')
                    self.possi_ax.tick_params(axis='y', colors='white')
                    
                    # Solid bars with consistent gray base
                    bars = self.possi_ax.bar(dic.keys(), cumulative_values, color='#404040', edgecolor='none', alpha=1.0)
                    
                    # Set initial label text
                    self.rolldic_res_label.configure(text='Calculating roll results...')
                else:
                    # Wheel Style setup
                    self.possi_ax.axis('equal')
                    self.possi_ax.set_axis_off()
                    
                    # Set initial label text
                    self.rolldic_res_label.configure(text='Spinning the wheel...')
                    
                    # Calculate target angle for pointer landing
                    # Pie starts at startangle (default 90 is top), wedges go counter-clockwise
                    # Pointer is at top (90)
                    keys_list = list(dic.keys())
                    result_idx = keys_list.index(roll)
                    
                    # Cumulative probabilities up to the result
                    cumulative_before = sum(pmf_values[:result_idx])
                    target_wedge_prob = pmf_values[result_idx]
                    
                    # Target angle: cumulative rotation so pointer lands in wedge
                    # 3.6 because pmf is 0-1, 360 degrees
                    # target_angle should be -(cumulative_before + 0.5 * target_wedge_prob) * 360
                    target_angle = -(cumulative_before + 0.5 * target_wedge_prob) * 360
                    
                    full_rotations = random.randint(3, 5)
                    self.wheel_total_rotation = full_rotations * 360 + target_angle
                    self.wheel_current_rotation = 0
                    
                    # Initial draw (hidden/empty or first frame)
                    colors = ['#404040'] * len(pmf_values)
                    wedge_labels = [str(k) if len(pmf_values) < 30 else '' for k in dic.keys()]
                    
                    wedges, texts = self.possi_ax.pie(
                        pmf_values,
                        colors=colors,
                        startangle=90,
                        labeldistance=1.1,
                        wedgeprops={'linewidth': 1, 'edgecolor': '#333333'}
                    )
                    for text in texts:
                        text.set_color('white')
                        text.set_fontsize(8)
                        text.set_fontname('Roboto')
                    
                    # Pointer - adjust to be slightly smaller
                    self.possi_ax.fill([0, -0.04, 0.04], [1.02, 1.12, 1.12], color='white')
                
                self.possi_fig.tight_layout(pad=3.0)
                self.possi_canvas.draw()
                
                # Show the pre-created window
                if not self.possi.winfo_viewable():
                    self.possi.deiconify()
                self.possi.focus()
                
                if style == 'Cumulative':
                    rolls=[random.randint(mini, maxi)]

                    # More animation frames (15 to 25 rolls)
                    for i in range(random.randint(15, 25)):
                        c=random.randint(mini, maxi)
                        while c==rolls[-1]:
                            c=random.randint(mini, maxi)
                        rolls.append(c)
                    if rolls[-1]!=roll:
                        rolls.append(roll)
                    
                    # Setup animation state
                    self.anim_rolls = rolls
                    self.anim_index = 0
                    self.anim_bars = bars
                    self.anim_dic = dic
                    self.anim_total = total
                    self.anim_values = cumulative_values
                    self.anim_mini = mini
                    self.anim_roll = roll
                    self.anim_p = self.possi_ax
                    self.anim_canvas = self.possi_canvas
                    self.anim_f = self.possi_fig
                    self.run_animation_step(anim_id)

                else:

                    # Wheel animation setup
                    self.wheel_anim_step = 0
                    self.wheel_total_steps = 60
                    self.wheel_pmf = pmf_values
                    self.wheel_keys = list(dic.keys())
                    self.wheel_result = roll
                    self.wheel_total = total
                    self.wheel_dic = dic
                    self.wheel_p = self.possi_ax
                    self.wheel_canvas = self.possi_canvas
                    self.wheel_f = self.possi_fig
                    self.wheel_anim_id = anim_id
                    
                    self.run_wheel_rolldic_animation_step(anim_id)




            except Exception:
                print(traceback.format_exc())

        def run_animation_step(self, anim_id):
            try:
                # If window closed or a new animation started, stop
                if not self.possi.winfo_exists() or anim_id != self.current_anim_id:
                    return
                
                roll_val = self.anim_rolls[self.anim_index]

                # Reset all bars to white first (inefficient but safe) or just reset previous?
                # The original code re-drew the white bars every time.
                # Let's just update the specific bar color.
                
                # Map roll value to bar index. 
                # dic.keys() are x values. 
                # bars are in order of dic.keys()
                keys_list = list(self.anim_dic.keys())
                try:
                    bar_idx = keys_list.index(roll_val)
                    self.anim_bars[bar_idx].set_color(self.color)
                except ValueError:
                    pass # Should not happen if logic is correct
                
                self.anim_canvas.draw()
                
                if self.anim_index == len(self.anim_rolls) - 1:
                    # Final state
                    res_text = 'r='+str(self.anim_roll)+', p(r)='+"{:.1e}".format(self.anim_dic[self.anim_roll]/self.anim_total)+', p(x>=r)='+"{:.1e}".format(self.anim_values[self.anim_mini-self.anim_roll-1])
                    self.rolldic_res_label.configure(text=res_text)
                    self.anim_canvas.draw()
                    return

                # Schedule reset of this bar
                # Slowed down slightly: 200ms highlight
                self.possi.after(200, self.reset_animation_step, roll_val, anim_id)

            except Exception:
                print(traceback.format_exc())

        def reset_animation_step(self, roll_val, anim_id):
             try:
                if not self.possi.winfo_exists() or anim_id != self.current_anim_id:
                    return

                    
                keys_list = list(self.anim_dic.keys())
                try:
                    bar_idx = keys_list.index(roll_val)
                    self.anim_bars[bar_idx].set_color('#404040') # Reset to gray25
                except ValueError:
                    pass

                self.anim_canvas.draw()
                
                # Schedule next step
                self.anim_index += 1
                # Slowed down slightly: 100ms between rolls
                self.possi.after(100, self.run_animation_step, anim_id)

             except Exception:
                print(traceback.format_exc())

        def run_wheel_rolldic_animation_step(self, anim_id):
            try:
                if not self.possi.winfo_exists() or anim_id != self.current_anim_id:
                    return

                
                t = self.wheel_anim_step / self.wheel_total_steps
                # Ease-out cubic
                eased_t = 1 - pow(1 - t, 3)
                
                current_rotation = eased_t * self.wheel_total_rotation
                
                self.wheel_p.clear()
                self.wheel_p.axis('equal')
                self.wheel_p.set_axis_off()
                
                colors = ['#404040'] * len(self.wheel_pmf)
                if self.wheel_anim_step >= self.wheel_total_steps:
                    # Highlight the result wedge
                    try:
                        res_idx = self.wheel_keys.index(self.wheel_result)
                        colors[res_idx] = self.color
                    except ValueError:
                        pass
                
                wedge_labels = [str(k) if len(self.wheel_pmf) < 30 else '' for k in self.wheel_keys]
                
                wedges, texts = self.wheel_p.pie(
            self.wheel_pmf,
            labels=wedge_labels,
            colors=colors,
            startangle=90 + current_rotation,
            labeldistance=1.1,
            wedgeprops={'linewidth': 1, 'edgecolor': '#333333'}
        )
                for text in texts:
                    text.set_color('white')
                    text.set_fontsize(8)
                    text.set_fontname('Roboto')
                
                # Pointer - more precise tip
                self.wheel_p.fill([0, -0.04, 0.04], [1.02, 1.12, 1.12], color='white')
                
                if self.wheel_anim_step >= self.wheel_total_steps:
                     res_text = 'r='+str(self.wheel_result)+', p(r)='+"{:.1e}".format(self.wheel_dic[self.wheel_result]/self.wheel_total)
                     self.rolldic_res_label.configure(text=res_text)
                
                self.wheel_canvas.draw()
                
                if self.wheel_anim_step < self.wheel_total_steps:
                    self.wheel_anim_step += 1
                    delay = int(20 + 80 * t)
                    self.possi.after(delay, self.run_wheel_rolldic_animation_step, anim_id)

                
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
            self.rolldic(self.msg) 
            
# create a GUI class object
g = GUI()
g.mainloop()

