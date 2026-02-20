# import all the required modules
# Set DPI awareness BEFORE any GUI imports
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import socket 
import threading
from tkinter import *
from tkinter import font, ttk, filedialog, messagebox, TclError
import customtkinter as ctk
import random
#import numpy as np
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
#import numpy as np
from PIL import ImageTk, Image
from math import exp
from math import floor, ceil
import os
import shutil
import traceback
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAST_CONFIGS_DIR = os.path.join(BASE_DIR, 'Past configs')
SAVED_CONFIGS_DIR = os.path.join(BASE_DIR, 'Saved configs')
DICE_IMAGES_DIR = os.path.join(BASE_DIR, 'Dice_Images')
from functools import partial
# --- MATPLOTLIB / NUMPY STUBS (Fixes crash on broken environment) ---
class Figure:
    def __init__(self, *args, **kwargs): pass
    def add_subplot(self, *args, **kwargs):
        class DummyAx:
            def set_facecolor(self, *args): pass
            def axis(self, *args): pass
            def set_axis_on(self, *args): pass
            def clear(self): pass
            def set_aspect(self, *args): pass
            def set_xlabel(self, *args, **kwargs): pass
            def set_ylabel(self, *args, **kwargs): pass
            def tick_params(self, *args, **kwargs): pass
            def plot(self, *args, **kwargs): pass
            def bar(self, *args, **kwargs): pass
            def text(self, *args, **kwargs): pass
            def set_title(self, *args, **kwargs): pass
            def set_ylim(self, *args, **kwargs): pass
            def set_xlim(self, *args, **kwargs): pass
            def legend(self, *args, **kwargs): pass
        return DummyAx()
    def tight_layout(self, *args, **kwargs): pass
    def clear(self): pass

class FigureCanvasTkAgg:
    def __init__(self, figure=None, master=None):
        self.master = master
    def get_tk_widget(self):
        return ctk.CTkFrame(self.master, width=1, height=1, fg_color="transparent")
    def draw(self): pass

class NavigationToolbar2Tk:
    def __init__(self, *args, **kwargs): pass
    def update(self): pass

class np_stub:
    @staticmethod
    def sign(x): return 1 if x >= 0 else (-1 if x < 0 else 0)
    @staticmethod
    def linspace(a, b, n): return [a + i*(b-a)/(n-1) for i in range(n)]
    @staticmethod
    def array(data): return data
    @staticmethod
    def exp(x): return math.exp(x)
    @staticmethod
    def abs(x): return abs(x)
    @staticmethod
    def mean(x): return sum(x)/len(x) if x else 0
    @staticmethod
    def std(x): return 0
    @staticmethod
    def sqrt(x): return math.sqrt(x)

np = np_stub()
plt = type('plt_stub', (), {'rcParams': {}, 'figure': lambda *a, **k: Figure()})()
fm = type('fm_stub', (), {'fontManager': type('fm_mgr', (), {'ttflist': [], 'addfont': lambda f: None})(), 'findSystemFonts': lambda *a, **k: []})()
# --- END STUBS ---

from collections import OrderedDict
import itertools
import math

# Set Matplotlib to use Roboto as the default font (stubbed)
#plt.rcParams['font.family'] = 'sans-serif'
#plt.rcParams['font.sans-serif'] = ['Roboto'] + plt.rcParams['font.sans-serif']

# DPI awareness already set at top of file

__all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']

_whitespace = '\t\n\x0b\x0c\r '

def justify(words, width):
    if len(words) >= width:
        return words
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
                    chunks.append(r'\j')
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
                        # Process ALL parts after split (handle multiple \g markers)
                        # Push in reverse so they maintain correct order when popped
                        for part in reversed(yob[1:]):
                            if part != '':
                                chunks.append(r'\j         '+part)
                        if not any(yob[1:]) and len(chunks)>1:
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

def wrap(text, width=1000, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)

def fill(text, width=1000, **kwargs):
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

    def destroy(self):
        """Safe destroy that processes pending events first and cleans up children."""
        # Note: Do NOT call update_idletasks() here. It forces redraws on dying widgets.
            
        # Explicitly destroy children with safety to stop their internal events
        for child in [self.add_button, self.subtract_button, self.entry]:
            try:
                if hasattr(child, 'winfo_exists') and child.winfo_exists():
                    child.destroy()
            except (TclError, Exception):
                pass
                
        try:
            super().destroy()
        except (TclError, Exception):
            pass

class AnteriorItem:
    def __init__(self, typ, val1, val2=0, hidden=False):
        self.typ=typ
        self.val1=val1
        self.val2=val2
        self.hidden=hidden

class premod:
    def __init__(self, adv, const, items=None):
        self.adv=adv
        self.const=const
        self.items = items if items is not None else []

class posmod:
    def __init__(self, typ, timing, num1, num2, hidden=False):
        self.typ=typ
        self.timing=timing
        self.value=num1*(num2+1)*25*(typ!="adv")+num1*(typ=="adv")
        h_marker = " (H)" if hidden else ""
        self.subresName=timing+" Advan"*(typ=="adv")+" "+"+"*(num1>0)+str(num1)+(typ=="dice")*("d"+str(num2))+h_marker
        self.hidden=hidden

class resource:
    def __init__(self, qnt, resName, hidden=False):
        self.qnt=qnt
        self.resName=resName
        self.hidden=hidden
        self.mainFrame=Frame()
        self.mainButton=Frame()
        self.listSubres=[]
        self.subButtons=[]
        self.qntLabel=Frame()
        self.deleteButton=Frame()

class resourceSend:
    def __init__(self, qnt, resName, listSubres, hidden=False):
        self.qnt=qnt
        self.resName=resName
        self.listSubres=listSubres
        self.hidden=hidden

class bloco:
    def __init__(self, premods, posmods, sn, crit, mini):
        self.premods=premods
        self.posmods=posmods
        self.sn=sn
        self.crit=crit
        self.min=mini
        self.aspect=None

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
    def __init__(self, p, crit, r, adv, hidden=False):
        self.p=p
        self.r=r
        self.crit=crit
        self.adv=adv
        self.mods=''
        self.hidden=hidden

    def __lt__(self, other):
         return self.p < other.p

class posterior_selection:
    def __init__(self, roll_id, selection_index):
        self.roll_id = roll_id  # Unique ID for this roll's posterior selection
        self.selection_index = selection_index  # Index of chosen res option (-1 for N/A)

# Character Sheet Window for D&D 5.5e
class CharacterSheetWindow(ctk.CTkToplevel):
    # Advantage values allowed by rules (Net Advantage: -3 to 3)
    ADV_VALUES = ["-3", "-2", "-1", "0", "1", "2", "3"]
    
    # Knowledge fields and their linked aspects
    KNOWLEDGE_ASPECTS = {
        "Arcana": "Investigation", "Alchemy": "Investigation", "Manufacturing": "Investigation",
        "Lore": "Investigation", "Occultism": "Investigation", "Society": "Investigation",
        "Animal handling": "Trustworthiness",
        "Medicine": "Awareness", "Nature": "Awareness", "Religion": "Awareness", "Artistry": "Awareness",
    }
    
    # Tool dropdown options (each linked to an aspect)
    TOOL_SET_OPTIONS = [
        "Alchemist's supplies", "Brewer's supplies", "Calligrapher's supplies",
        "Carpenter's tools", "Cartographer's tools", "Cobbler's tools",
        "Cook's utensils", "Glassblower's tools", "Jeweler's tools",
        "Leatherworker's tools", "Mason's tools", "Painter's supplies",
        "Potter's tools", "Smith's tools", "Tinker's tools",
        "Weaver's tools", "Woodcarver's tools", "Disguise kit",
        "Forgery kit", "Herbalism kit", "Navigator's tools",
        "Poisoner's kit", "Thieves' tools",
    ]
    INSTRUMENT_OPTIONS = [
        "Bagpipes", "Drum", "Dulcimer", "Flute", "Horn",
        "Lute", "Lyre", "Pan flute", "Shawm", "Viol",
    ]
    GAMING_SET_OPTIONS = [
        "Dice set", "Playing card set", "Dragonchess set", "Three-Dragon Ante set",
    ]
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Character Sheet")
        self.geometry("580x900")
        self.configure(fg_color="gray15")
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self._loaded_filepath = None
        
        # Styling
        self.color = getattr(parent, 'color', "#d63384")
        self.p = 8  # Standard client padding (matches self.rescale)
        
        if not os.path.exists("roll_configs"):
            os.makedirs("roll_configs")
        self.roll_configs_dir = "roll_configs" # Persistent roll configs in subfolder
        self.user_past_configs_dir = self.roll_configs_dir # Hook into existing cleanup logic
        
        # Data storage
        self.aspect_widgets = {}  # {name: (value_entry, prof_var, adv_var)}
        self.stat_entries = {}
        self.combat_entries = {}
        self.knowledge_widgets = {}  # {name: (prof_var, value_label, linked_aspect, adv_var)}
        self.tool_widgets = {}  # {name: (prof_var, value_label, linked_aspect, adv_var)}
        self.save_widgets = {} # {name: (prof_var, adv_var, total_lbl)}
        self.save_entries = {}  # {name: entry_field}
        self.weapon_widgets = {} # {id: (name_entry, aspect_menu, prof_var, bonus_lbl, as_lbl, row_frame)}
        self.shard_widgets = {}  # {id: (source_entry, source_type_var, shard_type_var, total_entry, max_output_entry, arcane_rest_var, rest_type_var, row_frame)}
        self.armor_settings = {
            "type": StringVar(value="None"),
            "aspect": StringVar(value="Resilience"),
            "shield": BooleanVar(value=False)
        }
        self.exhaustion_var = IntVar(value=0)
        self.feature_widgets = {} # {id: (name_ent, cur_ent, max_ent, reset_var, desc_data_list, row_frame)}
        # desc_data_list is a mutable list [text] to allow updates from popup
        self.spells = [] # List of dicts: {id, name, level, prepared, source, time, range, comp, dur, desc}
        self.spell_widgets = {} # {id: (row_frame, prep_var, name_ent, source_ent, qprep_lbl)}
        self.quick_prep_used = BooleanVar(value=False)
        self.hit_dice_vars = {die: [StringVar(value="0"), StringVar(value="0")] for die in ["d6", "d8", "d10", "d12"]}
        
        # Phase 2: New State Variables
        self.conditions_vars = {c: BooleanVar(value=False) for c in [
            "Blinded", "Charmed", "Deafened", "Frightened", "Grappled", 
            "Incapacitated", "Invisible", "Paralyzed", "Petrified", 
            "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious"
        ]}
        self.pet_widgets = {} # {id: (name_ent, type_ent, pcn_cur, pcn_max, aa_ent, spd_ent, desc_data, row_frame)}

        # Main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="gray15",
                                                  scrollbar_button_color="gray25",
                                                  scrollbar_button_hover_color="gray35")
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.main_frame.columnconfigure(0, weight=1)
        
        # State for delta updates
        self._prof_state = {} 
        
        self.create_header()
        self.create_stats_section()
        self.create_combat_section()
        self.create_conditions_section()
        self.create_rest_section()
        self.create_aspects_section()
        self.create_knowledge_section()
        self.create_tools_section()
        self.create_equipment_section()
        self.create_features_section()
        self.create_pets_section()
        self.create_shards_section()
        self.create_spells_section()
        self.create_footer()
        
        # Bind Combat Prof change to update everything
        if "Prof" in self.combat_entries:
            self.combat_entries["Prof"].bind("<KeyRelease>", self.on_global_prof_change)

    def create_bordered_frame(self, parent):
        """Section frame matching standard client style"""
        return ctk.CTkFrame(parent, fg_color="gray20", corner_radius=8)

    def create_section_header(self, parent, text, row=0, colspan=1, pack=True):
        """Section header in a lighter label (Packed)"""
        lbl = ctk.CTkLabel(parent, text=text, font=("Roboto", 12, "bold"),
                           fg_color="gray25", corner_radius=6, text_color="white",
                           anchor="w")
        if pack:
            lbl.pack(fill="x", padx=self.p, pady=(self.p, 2))
        return lbl

    def create_header(self):
        """Character info"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        # Content Frame (Grid)
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="x", padx=self.p)
        content.columnconfigure((1, 3), weight=1)
        
        fields = [("Name:", "name_entry", 0, 0), ("Class:", "class_entry", 0, 2),
                  ("Race:", "race_entry", 1, 0), ("Lvl:", "level_entry", 1, 2),
                  ("Bkg:", "background_entry", 2, 0), ("Lang:", "languages_entry", 2, 2)]
        for lbl, attr, r, c in fields:
            pad_y = (4, 4) if r == 0 else (2, self.p)
            ctk.CTkLabel(content, text=lbl, font=("Roboto", 12)).grid(row=r, column=c, padx=self.p, pady=pad_y, sticky="e")
            if lbl == "Lvl:":
                w = 50
            elif lbl == "Lang:":
                w = 140
            else:
                w = 140
            entry = ctk.CTkEntry(content, font=("Roboto", 12), fg_color="gray25", border_width=0, width=w)
            entry.grid(row=r, column=c+1, padx=self.p, pady=pad_y, sticky="ew" if lbl != "Lvl:" else "w")
            entry.bind("<FocusOut>", self.autosave_roll_configs)
            setattr(self, attr, entry)

    def create_stats_section(self):
        """MIND, SOUL, SENSES, BODY"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        # Content Frame
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="x", padx=self.p, pady=(0, self.p))
        content.columnconfigure((0, 1, 2, 3), weight=1)
        
        for i, stat in enumerate(["Mind", "Soul", "Senses", "Body"]):
            ctk.CTkLabel(content, text=stat, font=("Roboto", 12, "bold")).grid(row=0, column=i, padx=2, pady=(0, 2))
            entry = ctk.CTkEntry(content, font=("Roboto", 12), width=50, justify="center",
                                 fg_color="gray25", border_width=0)
            entry.grid(row=1, column=i, padx=self.p, pady=(0, 0))
            entry.bind("<FocusOut>", self.autosave_roll_configs)
            self.stat_entries[stat] = entry

    def create_combat_section(self):
        """PCN, AA, Spd, Prof, Vit & Saves"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        self.create_section_header(frame, "Combat & Saves", colspan=2)
        
        # Two main rows: Combat Stats (Top) and Horizontal Saves (Bottom)
        main_content = ctk.CTkFrame(frame, fg_color="transparent")
        main_content.pack(fill="x", padx=self.p, pady=self.p)
        
        # --- Top Row: Combat Stats ---
        stats_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 6))
        stats_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        combat_stats = [("PCN", "PCN"), ("AA", "AA"), ("Spd", "Spd"), ("Prof", "Prof"), ("Vit", "Vit")]
        for i, (lbl, key) in enumerate(combat_stats):
            sub = ctk.CTkFrame(stats_frame, fg_color="transparent")
            sub.grid(row=0, column=i, sticky="nsew", padx=2)
            sub.columnconfigure(0, weight=1)
            
            ctk.CTkLabel(sub, text=lbl, font=("Roboto", 11, "bold")).pack(pady=(0, 2))
            entry = ctk.CTkEntry(sub, font=("Roboto", 12), width=42, justify="center",
                                 fg_color="gray25", border_width=0)
            entry.pack(pady=(0, 4))
            entry.bind("<FocusOut>", self.autosave_roll_configs)
            self.combat_entries[key] = entry
            
            if key == "Spd":
                entry.bind("<FocusIn>", lambda e: setattr(self, '_base_speed_val', self.combat_entries["Spd"].get()))
                entry.bind("<FocusOut>", lambda e: setattr(self, '_base_speed_val', self.combat_entries["Spd"].get()))
        
        # Exhaustion (0-10)
        exh_sub = ctk.CTkFrame(stats_frame, fg_color="transparent")
        exh_sub.grid(row=0, column=5, sticky="nsew", padx=2)
        exh_sub.columnconfigure(0, weight=1)
        ctk.CTkLabel(exh_sub, text="Exh", font=("Roboto", 11, "bold")).pack(pady=(0, 2))
        exh_entry = ctk.CTkEntry(exh_sub, font=("Roboto", 12), width=42, justify="center",
                                  fg_color="gray25", border_width=0,
                                  textvariable=self.exhaustion_var)
        exh_entry.pack(pady=(0, 4))
        exh_entry.bind("<KeyRelease>", lambda e: self.update_net_adv())
        
        # Net Advantage (read-only)
        nadv_sub = ctk.CTkFrame(stats_frame, fg_color="transparent")
        nadv_sub.grid(row=0, column=6, sticky="nsew", padx=2)
        nadv_sub.columnconfigure(0, weight=1)
        ctk.CTkLabel(nadv_sub, text="Net Adv", font=("Roboto", 11, "bold")).pack(pady=(0, 2))
        self.net_adv_label = ctk.CTkLabel(nadv_sub, text="0", font=("Roboto", 12, "bold"),
                                           fg_color="gray25", corner_radius=4, width=42, height=28)
        self.net_adv_label.pack(pady=(0, 4))

        # --- Bottom Row: Horizontal Saves ---
        saves_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        saves_frame.pack(fill="x", pady=(4, 0))
        # 4 columns for 4 saves
        saves_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        for i, stat in enumerate(["Mind", "Soul", "Senses", "Body"]):
            # Create a vertical card for each save
            s_card = ctk.CTkFrame(saves_frame, fg_color="gray25", corner_radius=6)
            s_card.grid(row=0, column=i, sticky="nsew", padx=4, pady=0)
            s_card.columnconfigure(0, weight=1) # Center content
            
            # 1) Stat Name
            ctk.CTkLabel(s_card, text=stat, font=("Roboto", 11, "bold")).pack(pady=(4, 2))
            
            # 2) Base Entry
            base_frame = ctk.CTkFrame(s_card, fg_color="transparent")
            base_frame.pack(pady=2)
            ctk.CTkLabel(base_frame, text="Base:", font=("Roboto", 10), text_color="gray60").pack(side="left", padx=2)
            base_entry = ctk.CTkEntry(base_frame, font=("Roboto", 11), width=35, justify="center",
                                       fg_color="gray20", border_width=0)
            base_entry.pack(side="left", padx=2)
            base_entry.bind("<KeyRelease>", lambda _, s=stat: self.update_save_total(s))
            base_entry.bind("<FocusOut>", self.autosave_roll_configs)
            self.save_entries[stat] = base_entry
            
            # 3) Prof Buttons
            prof_var = StringVar(value="-")
            prof_seg = ctk.CTkSegmentedButton(s_card, values=["-", "½", "F", "E"], variable=prof_var,
                                               font=("Roboto", 10), width=80, height=20,
                                               fg_color="gray20", selected_color=self.color,
                                               selected_hover_color="gray30",
                                               command=lambda _, s=stat: self.update_save_total(s))
            prof_seg.pack(pady=4)
            
            # 4) Total (Big)
            total_lbl = ctk.CTkLabel(s_card, text="+0", font=("Roboto", 14, "bold"))
            total_lbl.pack(pady=2)
            
            # 5) Advantage
            adv_frame = ctk.CTkFrame(s_card, fg_color="transparent")
            adv_frame.pack(pady=(2, 6))
            ctk.CTkLabel(adv_frame, text="Adv:", font=("Roboto", 10), text_color="gray60").pack(side="left", padx=2)
            adv_var = StringVar(value="0")
            adv_menu = ctk.CTkOptionMenu(adv_frame, variable=adv_var, values=[str(v) for v in self.ADV_VALUES],
                                          font=("Roboto", 10), width=50, height=20,
                                          fg_color="gray20", button_color="gray30", button_hover_color="gray35")
            adv_menu.pack(side="left", padx=2)
            
            self.save_widgets[stat] = (prof_var, adv_var, total_lbl)

    def create_conditions_section(self):
        """Dedicated tracker for D&D Conditions"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        self.create_section_header(frame, "Conditions Tracker")
        
        main_content = ctk.CTkFrame(frame, fg_color="transparent")
        main_content.pack(fill="x", padx=self.p, pady=self.p)
        
        cond_frame = ctk.CTkFrame(main_content, fg_color="gray25", corner_radius=6)
        cond_frame.pack(fill="x", pady=(0, 4))
        # 3 or 4 columns to make it look full
        cond_frame.columnconfigure((0, 1, 2), weight=1)
        
        cond_list = sorted(list(self.conditions_vars.keys()))
        for i, cond in enumerate(cond_list):
            r, c = i // 3, i % 3
            cb = ctk.CTkCheckBox(cond_frame, text=cond, variable=self.conditions_vars[cond],
                                  font=("Roboto", 10), checkbox_width=16, checkbox_height=16,
                                  fg_color=self.color, border_color=self.color, hover_color=self.color,
                                  command=self.on_condition_change)
            cb.grid(row=r, column=c, padx=8, pady=4, sticky="w")

    def create_aspect_row(self, parent, aspect_name, row):
        """Aspect row: Name | Value | Prof(None/Half/Full) | Adv(spinbox)"""
        aspect_name = aspect_name.strip()
        
        # Revert to Card Style: separate frame for each row
        row_frame = ctk.CTkFrame(parent, fg_color="gray30", corner_radius=6)
        row_frame.grid(row=row, column=0, columnspan=5, sticky="ew", padx=self.p, pady=2)
        
        # Rigid Column Configuration to force alignment across separate frames
        row_frame.columnconfigure(0, weight=1, minsize=180) # Name: Fixed min width
        row_frame.columnconfigure(1, weight=0, minsize=45)  # Val
        row_frame.columnconfigure(2, weight=0, minsize=82)  # Prof (Reduced from 110)
        row_frame.columnconfigure(3, weight=0, minsize=45)  # Total
        row_frame.columnconfigure(4, weight=0, minsize=75)  # Adv

        ctk.CTkLabel(row_frame, text=aspect_name, font=("Roboto", 12), anchor="w").grid(
            row=0, column=0, padx=(self.p, 2), pady=4, sticky="w")
        
        # Base value entry
        val_entry = ctk.CTkEntry(row_frame, font=("Roboto", 12), width=45, justify="center",
                                  fg_color="gray20", border_width=0, corner_radius=4)
        val_entry.grid(row=0, column=1, padx=2, pady=4, sticky="ew")
        val_entry.bind("<KeyRelease>", lambda e: self.update_aspect_total(aspect_name))
        val_entry.bind("<FocusOut>", self.autosave_roll_configs)
        
        # Proficiency: segmented button (-, ½, F, E)
        prof_var = StringVar(value="-")
        # Offensive aspects don't have proficiency
        if aspect_name not in ["Concentration", "Meditation", "Precision", "Potency"]:
            prof_seg = ctk.CTkSegmentedButton(row_frame, values=["-", "½", "F", "E"], variable=prof_var,
                                               font=("Roboto", 11), width=80, height=24,
                                               fg_color="gray20", selected_color=self.color,
                                               selected_hover_color="gray40",
                                               command=lambda v, a=aspect_name: self.on_aspect_prof_change(a, v))
            prof_seg.grid(row=0, column=2, padx=2, pady=4, sticky="ew")
        else:
            # Spacer
            ctk.CTkLabel(row_frame, text="", width=84, height=24).grid(
                row=0, column=2, padx=2, pady=4, sticky="ew")

        # Total Label
        total_lbl = ctk.CTkLabel(row_frame, text="+0", font=("Roboto", 12, "bold"), width=45)
        total_lbl.grid(row=0, column=3, padx=2, pady=4, sticky="ew")
        
        # Advantage: option menu with valid values
        adv_var = StringVar(value="0")
        adv_menu = ctk.CTkOptionMenu(row_frame, variable=adv_var, values=[str(v) for v in self.ADV_VALUES],
                                      font=("Roboto", 11), width=75, height=24,
                                      fg_color="gray20", button_color="gray30", button_hover_color="gray35",
                                      dropdown_fg_color="gray20")
        adv_menu.grid(row=0, column=4, padx=(2, 4), pady=4, sticky="ew")
        
        self.aspect_widgets[aspect_name] = (val_entry, prof_var, adv_var, total_lbl)
        self._prof_state[aspect_name] = "-"


    def create_aspects_section(self):
        """All 16 aspects with proficiency and advantage (Card Layout)"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        # Single column for parent frame (it holds full-width row_frames)
        frame.columnconfigure(0, weight=1)
        
        self.create_section_header(frame, "Aspects")
        
        # Content Container to hold grid items
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=self.p, pady=(0, self.p))
        content_frame.columnconfigure(0, weight=1)
        
        # Column headers
        hdr_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=0)
        hdr_frame.grid(row=0, column=0, sticky="ew")
        
        # MATCHING Configuration to `create_aspect_row`
        hdr_frame.columnconfigure(0, weight=1, minsize=180) # Name match
        hdr_frame.columnconfigure(1, weight=0, minsize=45)  # Val match
        hdr_frame.columnconfigure(2, weight=0, minsize=82)  # Prof match
        hdr_frame.columnconfigure(3, weight=0, minsize=45)  # Total match
        hdr_frame.columnconfigure(4, weight=0, minsize=75)  # Adv match

        ctk.CTkLabel(hdr_frame, text="Aspect", font=("Roboto", 11, "bold"), anchor="w").grid(
            row=0, column=0, padx=(self.p, 2), pady=2, sticky="w")
        ctk.CTkLabel(hdr_frame, text="Val", font=("Roboto", 11, "bold"), width=45).grid(
            row=0, column=1, padx=2, pady=2, sticky="ew")
        ctk.CTkLabel(hdr_frame, text="Prof", font=("Roboto", 11, "bold"), width=82).grid(
            row=0, column=2, padx=2, pady=2, sticky="ew")
        ctk.CTkLabel(hdr_frame, text="Total", font=("Roboto", 11, "bold"), width=45).grid(
            row=0, column=3, padx=2, pady=2, sticky="ew")
        ctk.CTkLabel(hdr_frame, text="Adv", font=("Roboto", 11, "bold"), width=75).grid(
            row=0, column=4, padx=2, pady=2, sticky="ew")
        
        aspects_by_category = [
            ("Mind", ["Concentration", "Investigation", "Convincing", "Simulation"]),
            ("Soul", ["Meditation", "Awareness", "Performance", "Trustworthiness"]),
            ("Senses", ["Precision", "Mobility", "Acrobatics", "Dexterity"]),
            ("Body", ["Potency", "Resilience", "Athletics", "Constitution"]),
        ]
        
        row = 1
        for category, aspects in aspects_by_category:
            # Revert to standard divider look
            ctk.CTkLabel(content_frame, text=f"─ {category} ─", font=("Roboto", 9, "bold"), text_color="gray50").grid(
                row=row, column=0, padx=self.p, pady=(self.p//2, 2), sticky="ew")
            row += 1
            for aspect in aspects:
                self.create_aspect_row(content_frame, aspect, row)
                row += 1

    def create_knowledge_section(self):
        """Knowledge fields linked to aspects"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=0)
        frame.columnconfigure(3, weight=0)
        frame.columnconfigure(4, weight=0)
        
        self.create_section_header(frame, "Knowledge Fields (linked to Aspects)", colspan=5)
        
        # Content Container
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=self.p, pady=(0, 6))
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=0)
        content_frame.columnconfigure(2, weight=0)
        content_frame.columnconfigure(3, weight=0)
        content_frame.columnconfigure(4, weight=0)
        
        # Headers: Field | Prof | Linked | Value
        # Column headers — use same widths/padx as data row widgets for alignment
        hdr_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=0)
        hdr_frame.grid(row=0, column=0, columnspan=5, sticky="ew")
        hdr_frame.columnconfigure(0, weight=3)
        hdr_frame.columnconfigure(1, weight=0)
        hdr_frame.columnconfigure(2, weight=0)
        hdr_frame.columnconfigure(3, weight=0)
        hdr_frame.columnconfigure(4, weight=0)
        ctk.CTkLabel(hdr_frame, text="Field", font=("Roboto", 11, "bold"), anchor="w").grid(
            row=0, column=0, padx=(self.p, 2), pady=2, sticky="w")
        ctk.CTkLabel(hdr_frame, text="Prof", font=("Roboto", 11, "bold"), width=70).grid(
            row=0, column=1, padx=2, pady=2)
        ctk.CTkLabel(hdr_frame, text="Linked Aspect", font=("Roboto", 11, "bold"), width=120, anchor="w").grid(
            row=0, column=2, padx=self.p, pady=2, sticky="w")
        ctk.CTkLabel(hdr_frame, text="Total", font=("Roboto", 11, "bold"), width=30).grid(
            row=0, column=3, padx=2, pady=2)
        ctk.CTkLabel(hdr_frame, text="Adv", font=("Roboto", 11, "bold"), width=60).grid(
            row=0, column=4, padx=2, pady=2)
        
        for i, (field, linked_aspect) in enumerate(self.KNOWLEDGE_ASPECTS.items()):
            row = 1 + i
            # Container
            row_frame = ctk.CTkFrame(content_frame, fg_color="gray30", corner_radius=6)
            row_frame.grid(row=row, column=0, columnspan=5, sticky="ew", pady=2)
            row_frame.columnconfigure(0, weight=3)
            row_frame.columnconfigure(1, weight=0)
            row_frame.columnconfigure(2, weight=0)
            row_frame.columnconfigure(3, weight=0)
            row_frame.columnconfigure(4, weight=0)

            ctk.CTkLabel(row_frame, text=field, font=("Roboto", 12), anchor="w").grid(row=0, column=0, padx=(self.p, 2), pady=4, sticky="w")
            
            prof_var = StringVar(value="-")
            prof_seg = ctk.CTkSegmentedButton(row_frame, values=["-", "½", "F"], variable=prof_var,
                                               font=("Roboto", 11), width=70, height=20,
                                               fg_color="gray20", selected_color=self.color,
                                               selected_hover_color="gray40",
                                               command=lambda _, f=field: self.update_knowledge_fields())
            prof_seg.grid(row=0, column=1, padx=2, pady=4)
            
            ctk.CTkLabel(row_frame, text=f"→ {linked_aspect}", font=("Roboto", 11), text_color="gray50", width=120, anchor="w").grid(
                row=0, column=2, padx=self.p, pady=4, sticky="w")
            
            # Calculated Value Label
            val_lbl = ctk.CTkLabel(row_frame, text="-6", font=("Roboto", 12, "bold"), width=30)
            val_lbl.grid(row=0, column=3, padx=2, pady=4)
            
            # Advantage
            adv_var = StringVar(value="0")
            adv_menu = ctk.CTkOptionMenu(row_frame, variable=adv_var, values=[str(v) for v in self.ADV_VALUES],
                                          font=("Roboto", 11), width=60, height=24,
                                          fg_color="gray20", button_color="gray30", button_hover_color="gray35",
                                          dropdown_fg_color="gray20")
            adv_menu.grid(row=0, column=4, padx=(2, 4), pady=4)
            
            self.knowledge_widgets[field] = (prof_var, val_lbl, linked_aspect, adv_var)
        
        # Extra bottom padding on last row
        # Extra bottom padding on last row
        last_row = 1 + len(self.KNOWLEDGE_ASPECTS) - 1
        for w in content_frame.grid_slaves(row=last_row):
            w.grid_configure(pady=(2, self.p))

    def create_tools_section(self):
        """Tools linked to aspects - dynamic add/remove"""
        self.tools_frame = self.create_bordered_frame(self.main_frame)
        self.tools_frame.pack(fill="x", pady=(0, 6))
        
        self.create_section_header(self.tools_frame, "Tools (linked to Aspects)", colspan=1)
        
        # Content Container
        content_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=self.p, pady=(0, 6))
        content_frame.columnconfigure(0, weight=1)
        
        # Column headers
        hdr_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=0)
        hdr_frame.grid(row=0, column=0, sticky="ew")
        hdr_frame.columnconfigure(0, weight=3)
        hdr_frame.columnconfigure(1, weight=0)
        hdr_frame.columnconfigure(2, weight=0)
        hdr_frame.columnconfigure(3, weight=0)
        hdr_frame.columnconfigure(4, weight=0)
        hdr_frame.columnconfigure(5, weight=0)
        ctk.CTkLabel(hdr_frame, text="Tool", font=("Roboto", 11, "bold"), anchor="w").grid(
            row=0, column=0, padx=(self.p, 2), pady=2, sticky="w")
        ctk.CTkLabel(hdr_frame, text="Prof", font=("Roboto", 11, "bold"), width=70).grid(
            row=0, column=1, padx=2, pady=2)
        ctk.CTkLabel(hdr_frame, text="Linked Aspect", font=("Roboto", 11, "bold"), width=100, anchor="w").grid(
            row=0, column=2, padx=4, pady=2, sticky="w")
        ctk.CTkLabel(hdr_frame, text="Total", font=("Roboto", 11, "bold"), width=30).grid(
            row=0, column=3, padx=2, pady=2)
        ctk.CTkLabel(hdr_frame, text="Adv", font=("Roboto", 11, "bold"), width=60).grid(
            row=0, column=4, padx=2, pady=2)
        # Spacer for ✕ button column
        ctk.CTkLabel(hdr_frame, text="", width=28).grid(row=0, column=5, padx=(2, 4), pady=2)
        
        # Container for dynamic tool rows
        self.tools_container = ctk.CTkFrame(content_frame, fg_color="transparent", height=0)
        self.tools_container.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        
        # Add buttons footer (all on one row)
        add_footer = ctk.CTkFrame(content_frame, fg_color="transparent")
        add_footer.grid(row=2, column=0, sticky="ew", pady=(4, self.p))
        
        self._tool_set_var = StringVar(value="Add Tool Set...")
        ctk.CTkOptionMenu(add_footer, variable=self._tool_set_var,
                          values=self.TOOL_SET_OPTIONS,
                          font=("Roboto", 10), width=130, height=24,
                          fg_color="gray25", button_color="gray30",
                          button_hover_color="gray35", dropdown_fg_color="gray20",
                          command=lambda v: self._add_tool_item(v, "Dexterity", self._tool_set_var, "Add Tool Set...")).pack(side="left", padx=(0, 4))
        
        self._instrument_var = StringVar(value="Add Instrument...")
        ctk.CTkOptionMenu(add_footer, variable=self._instrument_var,
                          values=self.INSTRUMENT_OPTIONS,
                          font=("Roboto", 10), width=130, height=24,
                          fg_color="gray25", button_color="gray30",
                          button_hover_color="gray35", dropdown_fg_color="gray20",
                          command=lambda v: self._add_tool_item(v, "Performance", self._instrument_var, "Add Instrument...")).pack(side="left", padx=(0, 4))
        
        self._gaming_var = StringVar(value="Add Gaming Set...")
        ctk.CTkOptionMenu(add_footer, variable=self._gaming_var,
                          values=self.GAMING_SET_OPTIONS,
                          font=("Roboto", 10), width=130, height=24,
                          fg_color="gray25", button_color="gray30",
                          button_hover_color="gray35", dropdown_fg_color="gray20",
                          command=lambda v: self._add_tool_item(v, "Awareness", self._gaming_var, "Add Gaming Set...")).pack(side="left", padx=(0, 4))
        
        # Separator
        ctk.CTkLabel(add_footer, text="|", font=("Roboto", 11), text_color="gray40").pack(side="left", padx=(0, 4))
        
        # Custom tool: name entry + aspect dropdown + Add button
        aspect_names = ["Dexterity", "Performance", "Awareness", "Investigation",
                        "Convincing", "Simulation", "Meditation", "Trustworthiness",
                        "Acrobatics", "Athletics", "Constitution", "Concentration"]
        
        self._custom_tool_name = ctk.CTkEntry(add_footer, font=("Roboto", 10), width=120, height=24,
                                               fg_color="gray25", border_width=0,
                                               placeholder_text="Custom name...")
        self._custom_tool_name.pack(side="left", padx=(0, 4))
        
        self._custom_aspect_var = StringVar(value="Dexterity")
        ctk.CTkOptionMenu(add_footer, variable=self._custom_aspect_var,
                          values=aspect_names,
                          font=("Roboto", 10), width=110, height=24,
                          fg_color="gray25", button_color="gray30",
                          button_hover_color="gray35", dropdown_fg_color="gray20").pack(side="left", padx=(0, 4))
        
        ctk.CTkButton(add_footer, text="Add", font=("Roboto", 10), width=40, height=24,
                      fg_color="gray25", hover_color="gray35",
                      command=self._add_custom_tool).pack(side="left")

    def _add_tool_item(self, name, linked_aspect, reset_var=None, reset_text=None):
        """Add a dynamic tool row"""
        if reset_var and reset_text:
            reset_var.set(reset_text)
        if not name or name in self.tool_widgets:
            return  # No duplicates or empty names
        
        row_frame = ctk.CTkFrame(self.tools_container, fg_color="gray30", corner_radius=6)
        row_frame.pack(fill="x", padx=self.p, pady=2)
        row_frame.columnconfigure(0, weight=3)
        row_frame.columnconfigure(1, weight=0)
        row_frame.columnconfigure(2, weight=0)
        row_frame.columnconfigure(3, weight=0)
        row_frame.columnconfigure(4, weight=0)
        row_frame.columnconfigure(5, weight=0)
        
        ctk.CTkLabel(row_frame, text=name, font=("Roboto", 12), anchor="w").grid(
            row=0, column=0, padx=(self.p, 2), pady=4, sticky="w")
        
        # Proficiency: segmented button (-, ½, F)
        prof_var = StringVar(value="-")
        prof_seg = ctk.CTkSegmentedButton(row_frame, values=["-", "½", "F"], variable=prof_var,
                                           font=("Roboto", 11), width=70, height=20,
                                           fg_color="gray17", selected_color=self.color,
                                           selected_hover_color=self.color,
                                           command=lambda _: self.update_tool_fields())
        prof_seg.grid(row=0, column=1, padx=2, pady=4)
        
        ctk.CTkLabel(row_frame, text=f"→ {linked_aspect}", font=("Roboto", 11),
                     text_color="gray50", width=100, anchor="w").grid(
            row=0, column=2, padx=4, pady=4, sticky="w")
        
        val_lbl = ctk.CTkLabel(row_frame, text="-6", font=("Roboto", 12, "bold"), width=30)
        val_lbl.grid(row=0, column=3, padx=2, pady=4)
        
        adv_var = StringVar(value="0")
        adv_menu = ctk.CTkOptionMenu(row_frame, variable=adv_var, values=[str(v) for v in self.ADV_VALUES],
                                      font=("Roboto", 11), width=60, height=24,
                                      fg_color="gray17", button_color="gray25",
                                      button_hover_color=self.color, dropdown_hover_color=self.color,
                                      dropdown_fg_color="gray20")
        adv_menu.grid(row=0, column=4, padx=2, pady=4)
        
        del_btn = ctk.CTkButton(row_frame, text="✕", width=24, height=24,
                                fg_color="transparent", hover_color=self.color,
                                font=("Roboto", 11),
                                command=lambda n=name, f=row_frame: self._remove_tool_item(n, f))
        del_btn.grid(row=0, column=5, padx=(2, 4), pady=4)
        
        self.tool_widgets[name] = (prof_var, val_lbl, linked_aspect, adv_var)
        self.update_tool_fields()

    def _remove_tool_item(self, name, row_frame):
        """Remove a dynamic tool row"""
        row_frame.destroy()
        if name in self.tool_widgets:
            del self.tool_widgets[name]

    def _add_custom_tool(self):
        """Add a custom-named tool with user-chosen linked aspect"""
        name = self._custom_tool_name.get().strip()
        linked_aspect = self._custom_aspect_var.get()
        if name:
            self._add_tool_item(name, linked_aspect)
            self._custom_tool_name.delete(0, "end")

    def _guess_linked_aspect(self, name):
        """Guess the linked aspect for a tool name (backward compat)"""
        if name in self.TOOL_SET_OPTIONS:
            return "Dexterity"
        elif name in self.INSTRUMENT_OPTIONS:
            return "Performance"
        elif name in self.GAMING_SET_OPTIONS:
            return "Awareness"
        return "Dexterity"  # Default fallback


    def update_save_total(self, stat):
        """Update total bonus for a save (Base Value + Prof)"""
        if stat not in self.save_widgets or stat not in self.save_entries: return
        prof_var, _, total_lbl = self.save_widgets[stat]
        
        # Get base value from entry
        try:
            base_val = int(self.save_entries[stat].get() or 0)
        except ValueError:
            base_val = 0
        
        prof = prof_var.get()
        bonus = self.calculate_bonus(prof)
        total = base_val + bonus
        total_lbl.configure(text=f"{total:+}")
        self.autosave_roll_configs()

    def create_footer(self):
        """Centered Save/Load"""
        footer = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        footer.pack(pady=0)
        
        ctk.CTkButton(footer, text="Save", fg_color="gray25", hover_color="gray35",
                      border_color=self.color, border_width=2, font=("Roboto", 11), width=100,
                      command=self.save_character).pack(side="left", padx=15)
        ctk.CTkButton(footer, text="Load", fg_color="gray25", hover_color="gray35",
                      border_color=self.color, border_width=2, font=("Roboto", 11), width=100,
                      command=self.load_character).pack(side="left", padx=15)

    def get_prof_bonus(self):
        """Get proficiency bonus from combat entries"""
        try:
            return int(self.combat_entries["Prof"].get() or 0)
        except ValueError:
            return 0

    def calculate_bonus(self, prof_type):
        """Returns bonus for aspects: None=0, Half=floor(PB/2), Full=PB"""
        pb = self.get_prof_bonus()
        if prof_type == "½":
            return pb // 2
        elif prof_type == "F":
            return pb
        elif prof_type == "E":
            return pb * 2
        return 0

    def on_aspect_prof_change(self, aspect, new_prof):
        """Update total label based on proficiency"""
        self.update_aspect_total(aspect)
        self._prof_state[aspect] = new_prof
        # Trigger update of linked knowledge and tool fields
        self.update_knowledge_fields()
        self.update_tool_fields()

    def update_aspect_total(self, aspect):
        """Recalculate total for a single aspect"""
        if aspect not in self.aspect_widgets: return
        entry, prof_var, _, total_lbl = self.aspect_widgets[aspect]
        try:
            base_val = int(entry.get() or 0)
            prof = prof_var.get()
            bonus = self.calculate_bonus(prof)
            total = base_val + bonus
            total_lbl.configure(text=f"{total:+}")
        except ValueError:
            total_lbl.configure(text="err")
        
        # Trigger updates for linked fields
        self.update_knowledge_fields()
        self.update_tool_fields()
        self.autosave_roll_configs()

    def on_global_prof_change(self, event=None):
        """Called when user types in Prof input"""
        self.update_knowledge_fields()
        self.update_tool_fields()
        # Update saves too
        for stat in ["Mind", "Soul", "Senses", "Body"]:
            self.update_save_total(stat)
        self.update_aa()
        self.update_weapon_bonuses()

    def create_equipment_section(self):
        """Weapons, Armor, Spells, and Features"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        self.create_section_header(frame, "Equipment, Attacks & Items", colspan=2)
        
        # --- Armor Section ---
        # Container for vertical stacking
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=self.p, pady=(0, 4))
        
        armor_frame = ctk.CTkFrame(content_frame, fg_color="gray25", corner_radius=6)
        armor_frame.pack(fill="x", pady=(0, 4))
        
        # Header Label
        ctk.CTkLabel(armor_frame, text="Armor & AA", font=("Roboto", 11, "bold")).pack(anchor="w", padx=self.p, pady=(2, 0))
        
        # Centralized Controls Frame
        controls_frame = ctk.CTkFrame(armor_frame, fg_color="transparent")
        controls_frame.pack(pady=(0, 4))
        
        # Armor Type
        armor_types = ["None", "Padded", "Leather", "Studded leather", "Hide", "Chain shirt", "Scale mail", "Breastplate", "Half plate", "Ring mail", "Chain mail", "Splint", "Plate"]
        ctk.CTkLabel(controls_frame, text="Type:", font=("Roboto", 11)).pack(side="left", padx=(0, 4))
        armor_menu = ctk.CTkOptionMenu(controls_frame, values=armor_types, variable=self.armor_settings["type"],
                                        width=120, height=24, font=("Roboto", 11),
                                        fg_color="gray17", button_color="gray25",
                                        button_hover_color=self.color, dropdown_hover_color=self.color,
                                        command=lambda _: self.update_aa())
        armor_menu.pack(side="left", padx=(0, 10))
        
        # Aspect Selection
        ctk.CTkLabel(controls_frame, text="Aspect:", font=("Roboto", 11)).pack(side="left", padx=(0, 4))
        # Ensure Mobility is in the list and spelled correctly
        aspect_menu = ctk.CTkOptionMenu(controls_frame, values=["Resilience", "Mobility", "Dexterity", "Acrobatics"], variable=self.armor_settings["aspect"],
                                         width=100, height=24, font=("Roboto", 11),
                                         fg_color="gray17", button_color="gray25",
                                         button_hover_color=self.color, dropdown_hover_color=self.color,
                                         command=lambda _: self.update_aa())
        aspect_menu.pack(side="left", padx=(0, 10))
        
        # Armor Proficiency Toggle
        # Default keys for Settings should be initialized in __init__ if not already
        if "prof" not in self.armor_settings:
            self.armor_settings["prof"] = BooleanVar(value=True)
        if "shield_prof" not in self.armor_settings:
            self.armor_settings["shield_prof"] = BooleanVar(value=True)
            
        # Row 2: Checkboxes
        shield_cb = ctk.CTkCheckBox(controls_frame, text="Shield", variable=self.armor_settings["shield"],
                                     font=("Roboto", 11), checkbox_width=20, checkbox_height=20,
                                     hover_color=self.color, fg_color=self.color, border_color=self.color,
                                     command=self.update_aa)
        shield_cb.pack(side="left", padx=(0, 10))

        prof_cb = ctk.CTkCheckBox(controls_frame, text="Armor Prof", variable=self.armor_settings["prof"],
                                   font=("Roboto", 11), checkbox_width=20, checkbox_height=20,
                                   hover_color=self.color, fg_color=self.color, border_color=self.color,
                                   command=self.update_aa)
        prof_cb.pack(side="left", padx=(0, 10))
        
        sp_cb = ctk.CTkCheckBox(controls_frame, text="Shield Prof", variable=self.armor_settings["shield_prof"],
                                   font=("Roboto", 11), checkbox_width=20, checkbox_height=20,
                                   hover_color=self.color, fg_color=self.color, border_color=self.color,
                                   command=self.update_aa)
        sp_cb.pack(side="left", padx=(0, 4))
        
        # AA Extra Modifiers
        ctk.CTkLabel(controls_frame, text="+", font=("Roboto", 11), text_color="gray60").pack(side="left", padx=(4, 5))
        self.aa_extra_const = ctk.CTkEntry(controls_frame, font=("Roboto", 11), width=35, height=22, placeholder_text="",
                                           justify="center", fg_color="gray17", border_width=0)
        self.aa_extra_const.pack(side="left", padx=(0, 2))
        self.aa_extra_const.bind("<FocusOut>", self.autosave_roll_configs)
        self.aa_extra_const.insert(0, "") # Default empty
        
        # AA Extra Adv (Dropdown)
        ctk.CTkLabel(controls_frame, text="Adv", font=("Roboto", 11), text_color="gray60").pack(side="left", padx=(2, 6))
        
        adv_values = ["-3", "-2", "-1", "", "1", "2", "3"]
        self.aa_extra_adv_var = StringVar(value="")
        self.aa_extra_adv = ctk.CTkOptionMenu(controls_frame, values=adv_values, variable=self.aa_extra_adv_var,
                                              width=50, height=22, font=("Roboto", 11),
                                              fg_color="gray17", button_color="gray25",
                                              button_hover_color=self.color, dropdown_hover_color=self.color,
                                              command=lambda _: self.update_aa()) # Trigger update on change
        self.aa_extra_adv.pack(side="left", padx=(0, 2))
        
        # --- Weapons & Items Section ---
        # Column Headers for Weapons (Moved BEFORE items container)
        hdr_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=20)
        hdr_frame.pack(fill="x", pady=(4, 0))
        hdr_frame.columnconfigure(0, weight=1) # Name
        
        ctk.CTkLabel(hdr_frame, text="Name", font=("Roboto", 11, "bold"), anchor="w").grid(row=0, column=0, padx=4, sticky="ew")
        ctk.CTkLabel(hdr_frame, text="Aspect", font=("Roboto", 11, "bold"), width=100).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(hdr_frame, text="Prof", font=("Roboto", 11, "bold"), width=40).grid(row=0, column=2, padx=4)
        ctk.CTkLabel(hdr_frame, text="Type", font=("Roboto", 11, "bold"), width=60).grid(row=0, column=3, padx=2)
        ctk.CTkLabel(hdr_frame, text="+", font=("Roboto", 11, "bold"), width=35).grid(row=0, column=4, padx=2)
        ctk.CTkLabel(hdr_frame, text="Adv", font=("Roboto", 11, "bold"), width=50).grid(row=0, column=5, padx=2)
        ctk.CTkLabel(hdr_frame, text="Total", font=("Roboto", 11, "bold"), width=40).grid(row=0, column=6, padx=4)
        ctk.CTkLabel(hdr_frame, text="Desc", font=("Roboto", 11, "bold"), width=30).grid(row=0, column=7, padx=2)
        ctk.CTkLabel(hdr_frame, text="", width=28).grid(row=0, column=8, padx=(2,4))

        # Items List
        self.items_container = ctk.CTkFrame(content_frame, fg_color="transparent", height=0)
        self.items_container.pack(fill="x", pady=2)
        self.items_container.columnconfigure(0, weight=1)
        
        add_btn = ctk.CTkButton(content_frame, text="+ Add Weapon/Spell/Feature", font=("Roboto", 11),
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=self._add_weapon_row)
        add_btn.pack(pady=self.p)

    def _add_weapon_row(self, name="", linked_aspect="Precision", prof=False, roll_type="Atk", extra_const="", extra_adv="", desc=""):
        """Add a dynamic weapon/item row with Atk/AS toggle and extra modifiers"""
        # Unique ID generation
        if self.weapon_widgets:
            row_id = str(max([int(k) for k in self.weapon_widgets.keys()]) + 1)
        else:
            row_id = "0"
            
        row_frame = ctk.CTkFrame(self.items_container, fg_color="gray25", corner_radius=6)
        row_frame.pack(fill="x", padx=self.p, pady=2)
        row_frame.columnconfigure(0, weight=1) # Name
        
        # Name Entry
        name_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), height=22, placeholder_text="Name",
                                fg_color="gray17", border_width=1, border_color=self.color)
        name_ent.insert(0, name)
        name_ent.grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        name_ent.bind("<FocusOut>", self.autosave_roll_configs)
        
        # Aspect Menu
        aspects = sorted(list(self.aspect_widgets.keys()))
        asp_var = StringVar(value=linked_aspect)
        asp_menu = ctk.CTkOptionMenu(row_frame, values=aspects, variable=asp_var,
                                      width=100, height=22, font=("Roboto", 10),
                                      fg_color="gray17", button_color="gray25",
                                      button_hover_color=self.color, dropdown_hover_color=self.color,
                                      command=lambda _: self.update_weapon_bonuses())
        asp_menu.grid(row=0, column=1, padx=2, pady=4)
        
        # Prof toggle
        p_var = BooleanVar(value=prof)
        p_cb = ctk.CTkCheckBox(row_frame, text="", variable=p_var, font=("Roboto", 10),
                                checkbox_width=16, checkbox_height=16, width=16,
                                fg_color=self.color, hover_color="gray35",
                                command=self.update_weapon_bonuses)
        p_cb.grid(row=0, column=2, padx=14, pady=4) # Increased padding to center under "Prof" header (width 40 vs 16)
        
        # Type Menu (Atk / AS)
        type_var = StringVar(value=roll_type)
        type_menu = ctk.CTkOptionMenu(row_frame, values=["Atk", "AS"], variable=type_var,
                                       width=60, height=22, font=("Roboto", 10),
                                       fg_color="gray17", button_color="gray25",
                                       button_hover_color=self.color, dropdown_hover_color=self.color,
                                       command=lambda _: self.update_weapon_bonuses())
        type_menu.grid(row=0, column=3, padx=2, pady=4)

        # Extra Const
        extra_const_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=35, height=22, placeholder_text="+",
                                       justify="center", fg_color="gray17", border_width=0)
        extra_const_ent.insert(0, extra_const)
        extra_const_ent.grid(row=0, column=4, padx=2, pady=4)
        extra_const_ent.bind("<KeyRelease>", self.update_weapon_bonuses)
        extra_const_ent.bind("<FocusOut>", self.autosave_roll_configs)

        # Extra Adv (Dropdown)
        adv_values = ["-3", "-2", "-1", "", "1", "2", "3"]
        extra_adv_var = StringVar(value=extra_adv if extra_adv in adv_values else "") # Validate loaded value
        # If loaded value is "0" (str), convert to ""? Or keep?
        # Logic in standard Adv lists is usually "" for 0.
        
        extra_adv_menu = ctk.CTkOptionMenu(row_frame, values=adv_values, variable=extra_adv_var,
                                           width=50, height=22, font=("Roboto", 11),
                                           fg_color="gray17", button_color="gray25",
                                           button_hover_color=self.color, dropdown_hover_color=self.color,
                                           command=lambda _: self.update_weapon_bonuses())
        extra_adv_menu.grid(row=0, column=5, padx=2, pady=4)
        # Note: we store the Var in the widget list to get() it later
        
        # Total Label
        bonus_lbl = ctk.CTkLabel(row_frame, text="+0", font=("Roboto", 10, "bold"), width=40)
        bonus_lbl.grid(row=0, column=6, padx=4, pady=4)
        
        # Description button
        desc_data = [desc]
        desc_btn = ctk.CTkButton(row_frame, text="📝", width=30, height=22, fg_color="gray25", hover_color="gray35",
                                  border_color=self.color, border_width=2,
                                  command=lambda: self._open_feature_description(name_ent, desc_data))
        desc_btn.grid(row=0, column=7, padx=2, pady=4)
        
        # Remove button
        rem_btn = ctk.CTkButton(row_frame, text="×", width=22, height=22,
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=lambda: self._remove_weapon_row(row_id))
        rem_btn.grid(row=0, column=8, padx=(2, 4), pady=4)
        
        self.weapon_widgets[row_id] = (name_ent, asp_var, p_var, type_var, extra_const_ent, extra_adv_var, bonus_lbl, desc_data, row_frame)
        self.update_weapon_bonuses()

    def _remove_weapon_row(self, row_id):
        if row_id in self.weapon_widgets:
            widgets = self.weapon_widgets.pop(row_id)
            widgets[-1].destroy()

    def create_shards_section(self):
        """Shard tracking for spellcasting sources with dual arcane resonance (Normal/Pact)"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        self.create_section_header(frame, "Shards")
        
        # ── Caster Level Data ──
        # Level -> Total Shards
        self.CASTER_LEVEL_SHARDS = {
            1: 2, 2: 3, 3: 8, 4: 10, 5: 16, 6: 19, 7: 23, 8: 27, 9: 36, 10: 41,
            11: 47, 12: 47, 13: 54, 14: 54, 15: 62, 16: 62, 17: 71, 18: 76, 19: 82, 20: 89
        }
        # Level -> [Sat 1, Sat 2, ..., Sat 9]  (None means "-")
        self.CASTER_LEVEL_SATURATION = {
            1:  [2, None, None, None, None, None, None, None, None],
            2:  [3, None, None, None, None, None, None, None, None],
            3:  [4, 2, None, None, None, None, None, None, None],
            4:  [4, 3, None, None, None, None, None, None, None],
            5:  [4, 3, 2, None, None, None, None, None, None],
            6:  [4, 3, 3, None, None, None, None, None, None],
            7:  [4, 3, 3, 1, None, None, None, None, None],
            8:  [4, 3, 3, 2, None, None, None, None, None],
            9:  [4, 3, 3, 3, 1, None, None, None, None],
            10: [4, 3, 3, 3, 2, None, None, None, None],
            11: [4, 3, 3, 3, 2, 1, None, None, None],
            12: [4, 3, 3, 3, 2, 1, None, None, None],
            13: [4, 3, 3, 3, 2, 1, 1, None, None],
            14: [4, 3, 3, 3, 2, 1, 1, None, None],
            15: [4, 3, 3, 3, 2, 1, 1, 1, None],
            16: [4, 3, 3, 3, 2, 1, 1, 1, None],
            17: [4, 3, 3, 3, 2, 1, 1, 1, 1],
            18: [4, 3, 3, 3, 3, 1, 1, 1, 1],
            19: [4, 3, 3, 3, 3, 2, 1, 1, 1],
            20: [4, 3, 3, 3, 3, 2, 2, 1, 1]
        }
        
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=self.p, pady=(0, 6))
        content_frame.columnconfigure(0, weight=1)

        # ── Caster Level Dropdown ──
        cl_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        cl_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(cl_frame, text="Caster Level:", font=("Roboto", 11, "bold"), text_color="gray70").pack(side="left", padx=(0, 5))
        self.caster_level_var = StringVar(value="1")
        self.caster_level_dropdown = ctk.CTkOptionMenu(
            cl_frame, variable=self.caster_level_var,
            values=[str(i) for i in range(1, 21)],
            width=60, height=22, font=("Roboto", 11),
            fg_color="gray17", button_color="gray25",
            button_hover_color=self.color, dropdown_hover_color=self.color,
            command=self._update_shards_calculations
        )
        self.caster_level_dropdown.pack(side="left", padx=(0, 15))

        # Warlock Level Dropdown
        ctk.CTkLabel(cl_frame, text="Warlock Level:", font=("Roboto", 11, "bold"), text_color="gray70").pack(side="left", padx=(0, 5))
        self.warlock_level_var = StringVar(value="0")
        self.warlock_level_dropdown = ctk.CTkOptionMenu(
            cl_frame, variable=self.warlock_level_var,
            values=[str(i) for i in range(0, 21)],
            width=60, height=22, font=("Roboto", 11),
            fg_color="gray17", button_color="gray25",
            button_hover_color=self.color, dropdown_hover_color=self.color,
            command=self._update_shards_calculations
        )
        self.warlock_level_dropdown.pack(side="left")
        
        # ── Spellcasting Sources ──
        self.shards_container = ctk.CTkFrame(content_frame, fg_color="transparent", height=0)
        self.shards_container.pack(fill="x", pady=2)
        self.shards_container.columnconfigure(0, weight=1)
        
        add_btn = ctk.CTkButton(content_frame, text="+ Add Spellcasting Source", font=("Roboto", 11),
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=self._add_shard_row)
        add_btn.pack(pady=(self.p, 6))
        
        # ── Normal Arcane Resonance Grid ──
        res_header = ctk.CTkLabel(content_frame, text="Arcane Resonance (Normal)",
                                   font=("Roboto", 12, "bold"), text_color="white")
        res_header.pack(anchor="w", pady=(4, 2))
        
        self.normal_res_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.normal_res_frame.pack(fill="x", pady=2)
        self.resonance_saturation_entries = []
        self.resonance_count_entries = []
        self.normal_mult_labels = []
        self._create_resonance_grid(self.normal_res_frame, self.resonance_saturation_entries,
                                     self.resonance_count_entries, self.normal_mult_labels)

        # ── Pact Arcane Resonance Grid (Hidden by default) ──
        self.pact_res_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        # Pack this only when needed
        
        pact_header = ctk.CTkLabel(self.pact_res_container, text="Arcane Resonance (Pact)",
                                   font=("Roboto", 12, "bold"), text_color="white") # Changed to white
        pact_header.pack(anchor="w", pady=(8, 2))
        
        self.pact_res_frame = ctk.CTkFrame(self.pact_res_container, fg_color="transparent")
        self.pact_res_frame.pack(fill="x", pady=2)
        self.pact_saturation_entries = []
        self.pact_count_entries = []
        self.pact_mult_labels = []
        self._create_resonance_grid(self.pact_res_frame, self.pact_saturation_entries,
                                     self.pact_count_entries, self.pact_mult_labels, is_pact=True)
        
        # ── Rest & Recovery Buttons ──
        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(12, 4))
        
        ctk.CTkButton(btn_frame, text="Long Rest", font=("Roboto", 11, "bold"),
                       fg_color="gray25", hover_color="gray35", 
                       border_color=self.color, border_width=2,
                       width=90, height=28,
                       command=self._long_rest).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(btn_frame, text="Short Rest", font=("Roboto", 11, "bold"),
                       fg_color="gray25", hover_color="gray35", 
                       border_color=self.color, border_width=2,
                       width=90, height=28,
                       command=self._short_rest).pack(side="left", padx=(0, 15))
        
        # Arcane Recovery
        ctk.CTkButton(btn_frame, text="Arcane Recovery", font=("Roboto", 11, "bold"),
                       fg_color="gray25", hover_color="gray35", 
                       border_color=self.color, border_width=2,
                       width=120, height=28,
                       command=self._shard_arcane_recovery).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(btn_frame, text="Amt:", font=("Roboto", 10), text_color="gray60").pack(side="left", padx=(0, 4))
        self.arcane_recovery_entry = ctk.CTkEntry(btn_frame, font=("Roboto", 11), width=35, height=22,
                                                   justify="center", fg_color="gray17", border_width=0)
        self.arcane_recovery_entry.pack(side="left", padx=(0, 10))
        self.arcane_recovery_entry.insert(0, "0")
        
        def toggle_ar():
            if self.arcane_recovery_used_var.get():
                self.arcane_recovery_used_cb.configure(state="disabled", text_color="gray50")

        self.arcane_recovery_used_var = BooleanVar(value=False)
        self.arcane_recovery_used_cb = ctk.CTkCheckBox(btn_frame, text="Used (1/LR)", variable=self.arcane_recovery_used_var,
                                                        font=("Roboto", 10), checkbox_width=18, checkbox_height=18,
                                                        fg_color=self.color, hover_color=self.color,
                                                        border_color=self.color, text_color="gray60",
                                                        command=toggle_ar)
        if self.arcane_recovery_used_var.get():
            self.arcane_recovery_used_cb.configure(state="disabled", text_color="gray50")
        self.arcane_recovery_used_cb.pack(side="left")

    def _short_rest(self):
        """Global Short Rest: Reset SR features"""
        # Features
        for w in self.feature_widgets.values():
            # w = (name_ent, cur_ent, max_ent, reset_var, used_var, used_cb, desc_data, row_frame)
            if w[3].get() == "SR":
                m = w[2].get()
                if m:
                    try:
                        w[1].set(int(m))
                    except ValueError:
                        pass
                w[4].set(False)
                w[5].configure(state="normal")
        # Call Shard Short Rest
        self._shard_short_rest()
        
        # Trigger Hit Dice Spending Prompt
        self._prompt_hit_dice()

    def _restore_hit_dice(self):
        """Restore all hit dice to maximum"""
        for die, vars in self.hit_dice_vars.items():
            max_val = vars[1].get()
            if max_val and max_val != "0":
                vars[0].set(max_val)

    def _prompt_hit_dice(self):
        """Popup to select and roll hit dice to restore PCN"""
        available = {d: int(v[0].get() or 0) for d, v in self.hit_dice_vars.items() if (v[0].get() and v[0].get() != "0")}
        if not available:
            return
            
        popup = ctk.CTkToplevel(self)
        popup.title("Spend Hit Dice")
        popup.geometry("300x400")
        popup.configure(fg_color="gray20")
        popup.attributes("-topmost", True)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Spend Hit Dice", font=("Roboto", 14, "bold")).pack(pady=10)
        
        try:
            vit_mod = int(self.combat_entries["Vit"].get() or 0)
        except ValueError:
            vit_mod = 0
            
        ctk.CTkLabel(popup, text=f"Vitality Modifier: {vit_mod:+}", font=("Roboto", 12)).pack(pady=(0, 10))

        spend_vars = {}
        for die, count in available.items():
            frame = ctk.CTkFrame(popup, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(frame, text=f"{die} (Avail: {count}) " , font=("Roboto", 12)).pack(side="left")
            spend_vars[die] = IntVar(value=0)

            sub = ctk.CTkFrame(frame, fg_color="gray25", height=24)
            sub.pack(side="right")
            
            val_lbl = ctk.CTkLabel(sub, textvariable=spend_vars[die], width=30)
            
            def make_cmd(d, c, v_lbl, sp_var, diff):
                def cmd():
                    new_val = sp_var.get() + diff
                    if 0 <= new_val <= c:
                        sp_var.set(new_val)
                return cmd
                
            ctk.CTkButton(sub, text="-", width=20, height=24, fg_color="gray30", 
                          command=make_cmd(die, count, val_lbl, spend_vars[die], -1)).pack(side="left")
            val_lbl.pack(side="left", padx=5)
            ctk.CTkButton(sub, text="+", width=20, height=24, fg_color="gray30", 
                          command=make_cmd(die, count, val_lbl, spend_vars[die], 1)).pack(side="left")

        def roll_and_heal():
            total_healed = 0
            log_texts = []
            
            for die, var in spend_vars.items():
                num = var.get()
                if num > 0:
                    sides = int(die[1:])
                    for _ in range(num):
                        r = random.randint(1, sides)
                        total_healed += r + vit_mod
                        log_texts.append(f"1{die} ({r}) + {vit_mod}")
                    
                    # Deduct spent dice
                    current = int(self.hit_dice_vars[die][0].get())
                    self.hit_dice_vars[die][0].set(str(current - num))

            if total_healed > 0:
                try:
                    curr_pcn = int(self.combat_entries["PCN"].get() or 0)
                except ValueError:
                    curr_pcn = 0
                self.combat_entries["PCN"].delete(0, "end")
                self.combat_entries["PCN"].insert(0, str(curr_pcn + total_healed))
                
                log_str = " + ".join(log_texts)
                messagebox.showinfo("Hit Dice Rolled", f"Rolled: {log_str}\n\nTotal PCN Restored: {total_healed}", parent=popup)
                
            popup.destroy()

        ctk.CTkButton(popup, text="Roll & Heal", fg_color="gray25", border_width=2, 
                      border_color=self.color, hover_color="gray35",
                      command=roll_and_heal).pack(pady=20)


    def _long_rest(self):
        """Global Long Rest"""
        # Features
        for w in self.feature_widgets.values():
            if w[3].get() in ["SR", "LR"]:
                m = w[2].get()
                if m:
                    try:
                        w[1].set(int(m))
                    except ValueError:
                        pass
                w[4].set(False)
                w[5].configure(state="normal")
                
        # Hit Dice
        self._restore_hit_dice()
        
        # Shards & Saturation (Handles Arcane Recovery reset)
        self._shard_long_rest()
        
        # Quick Prep
        self.quick_prep_used.set(False)
        if hasattr(self, "qp_chk"):
            self.qp_chk.configure(state="normal")
        
        # Exhaustion
        try:
            exh = self.exhaustion_var.get()
            if exh > 0:
                self.exhaustion_var.set(exh - 1)
                self.update_net_adv()
        except:
            pass
            
    def _dawn_reset(self):
        for w in self.feature_widgets.values():
            if w[3].get() == "Dawn":
                m = w[2].get()
                if m: 
                    try:
                        w[1].set(int(m))
                    except ValueError:
                        pass
                w[4].set(False)
                w[5].configure(state="normal")
                
    def _dusk_reset(self):
        for w in self.feature_widgets.values():
            if w[3].get() == "Dusk":
                m = w[2].get()
                if m: 
                    try:
                        w[1].set(int(m))
                    except ValueError:
                        pass
                w[4].set(False)
                w[5].configure(state="normal")

    def create_rest_section(self):
        """Time & Rest Buttons"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        self.create_section_header(frame, "Time & Rest")
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="x", padx=self.p, pady=(0, self.p))
        content.columnconfigure((0, 1, 2, 3), weight=1)
        
        btns = [("Short Rest (SR)", self._short_rest), ("Long Rest (LR)", self._long_rest),
                ("Dawn", self._dawn_reset), ("Dusk", self._dusk_reset)]
        for i, (txt, cmd) in enumerate(btns):
            c = "gray25"
            ctk.CTkButton(content, text=txt, font=("Roboto", 11, "bold"),
                          fg_color=c, hover_color="gray35", border_color=self.color, border_width=2,
                          command=cmd).grid(row=0, column=i, padx=4, pady=(4,0), sticky="ew")

        # Hit Dice Sub-section
        hd_frame = ctk.CTkFrame(frame, fg_color="gray25", corner_radius=6)
        hd_frame.pack(fill="x", padx=self.p, pady=(4, self.p))
        
        lbl = ctk.CTkLabel(hd_frame, text="Hit Dice (Current / Max)", font=("Roboto", 11, "bold"))
        lbl.pack(pady=(4,2))
        
        hd_boxes = ctk.CTkFrame(hd_frame, fg_color="transparent")
        hd_boxes.pack(fill="x", pady=(0,4))
        hd_boxes.columnconfigure((0,1,2,3), weight=1)
        
        for i, die in enumerate(["d6", "d8", "d10", "d12"]):
            sub = ctk.CTkFrame(hd_boxes, fg_color="transparent")
            sub.grid(row=0, column=i, padx=4)
            ctk.CTkLabel(sub, text=f"{die}: ", font=("Roboto", 11, "bold")).pack(side="left")
            
            cur_entry = ctk.CTkEntry(sub, textvariable=self.hit_dice_vars[die][0], width=30, height=22, font=("Roboto", 11), justify="center", fg_color="gray17", border_width=0)
            cur_entry.pack(side="left", padx=2)
            
            ctk.CTkLabel(sub, text="/", font=("Roboto", 10)).pack(side="left")
            
            max_entry = ctk.CTkEntry(sub, textvariable=self.hit_dice_vars[die][1], width=30, height=22, font=("Roboto", 11), justify="center", fg_color="gray17", border_width=0)
            max_entry.pack(side="left", padx=2)

    def create_features_section(self):
        """Features & Limited Uses with Description and Auto-Reset"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        self.create_section_header(frame, "Features & Limited Uses")
        
        # Header Row (Hidden by default)
        self.features_header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        # Don't pack immediately
        self.features_header_frame.columnconfigure(0, weight=1) # Name
        
        ctk.CTkLabel(self.features_header_frame, text="Feature Name", font=("Roboto", 11, "bold"), anchor="w").grid(row=0, column=0, padx=4, sticky="ew")
        ctk.CTkLabel(self.features_header_frame, text="Uses", font=("Roboto", 11, "bold"), width=30).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(self.features_header_frame, text="/", font=("Roboto", 11, "bold"), width=10).grid(row=0, column=2, padx=0)
        ctk.CTkLabel(self.features_header_frame, text="Max", font=("Roboto", 11, "bold"), width=30).grid(row=0, column=3, padx=2)
        ctk.CTkLabel(self.features_header_frame, text="Reset", font=("Roboto", 11, "bold"), width=60).grid(row=0, column=4, padx=2)
        ctk.CTkLabel(self.features_header_frame, text="Use", font=("Roboto", 11, "bold"), width=28).grid(row=0, column=5, padx=2) # Used Checkbox
        ctk.CTkLabel(self.features_header_frame, text="Rst", font=("Roboto", 11, "bold"), width=28).grid(row=0, column=6, padx=2) # Header for manual reset
        ctk.CTkLabel(self.features_header_frame, text="Desc", font=("Roboto", 11, "bold"), width=30).grid(row=0, column=7, padx=2)
        ctk.CTkLabel(self.features_header_frame, text="", width=28).grid(row=0, column=8, padx=(2,4))
        
        # Features Container
        self.features_container = ctk.CTkFrame(frame, fg_color="transparent", height=0)
        self.features_container.pack(fill="x", padx=self.p, pady=(0, 2))
        self.features_container.columnconfigure(0, weight=1)
        
        add_btn = ctk.CTkButton(frame, text="+ Add Feature", font=("Roboto", 11),
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=self._add_feature_row)
        add_btn.pack(pady=(2, 6))

    def _add_feature_row(self, name="", current="", max_uses="", reset="LR", description="", used=False):
        """Add a feature row with Used checkbox and locking"""
        if not self.feature_widgets:
            # Show header if this is the first item
            self.features_header_frame.pack(fill="x", padx=self.p, pady=(0, 2), before=self.features_container)

        if self.feature_widgets:
            row_id = str(max([int(k) for k in self.feature_widgets.keys()]) + 1)
        else:
            row_id = "0"
            
        row_frame = ctk.CTkFrame(self.features_container, fg_color="gray25", corner_radius=6)
        row_frame.pack(fill="x", pady=2)
        row_frame.columnconfigure(0, weight=1)
        
        # Name
        name_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), height=22, placeholder_text="Name",
                                fg_color="gray17", border_width=1, border_color=self.color)
        name_ent.insert(0, name)
        name_ent.grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        name_ent.bind("<FocusOut>", self.autosave_roll_configs)
        
        # Uses (Current)
        cur_var = StringVar(value=str(current) if current else "0")
        cur_ent = IntSpinbox(row_frame, width=80, height=22, variable=cur_var,
                             color=self.color, from_=0, to_=999)
        cur_ent.grid(row=0, column=1, padx=2, pady=4)
        
        ctk.CTkLabel(row_frame, text="/", font=("Roboto", 11), width=10).grid(row=0, column=2, padx=0)
        
        # Max Uses
        max_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=30, height=22, justify="center",
                               fg_color="gray17", border_width=0)
        max_ent.insert(0, max_uses)
        max_ent.grid(row=0, column=3, padx=2, pady=4)
        max_ent.bind("<FocusOut>", self.autosave_roll_configs)
        
        # Reset Type
        reset_var = StringVar(value=reset)
        reset_menu = ctk.CTkOptionMenu(row_frame, values=["-", "SR", "LR", "Dawn", "Dusk"], variable=reset_var,
                                       width=60, height=22, font=("Roboto", 10),
                                       fg_color="gray17", button_color="gray25",
                                       button_hover_color=self.color, dropdown_hover_color=self.color)
        reset_menu.grid(row=0, column=4, padx=2, pady=4)

        def _enforce_limits(*args):
            try:
                m = int(max_ent.get())
                cur_ent.to_ = m
            except ValueError:
                cur_ent.to_ = 999
            
            r = reset_var.get()
            if r != "-":
                cur_ent.add_button.configure(state="disabled")
            else:
                cur_ent.add_button.configure(state="normal")
                
            try:
                c = int(cur_var.get())
                if c > cur_ent.to_ and r != "-":
                    cur_ent.set(cur_ent.to_)
            except ValueError:
                pass

        reset_var.trace_add("write", _enforce_limits)
        cur_var.trace_add("write", _enforce_limits)
        max_ent.bind("<KeyRelease>", lambda e: _enforce_limits())

        # Used Checkbox (Locking logic)
        used_var = BooleanVar(value=used)
        def toggle_used():
            if used_var.get():
                cur_ent.set(0)
                if reset_var.get() != "-":
                    used_cb.configure(state="disabled")
            
        used_cb = ctk.CTkCheckBox(row_frame, text="", variable=used_var, command=toggle_used,
                                   width=28, height=22, checkbox_width=18, checkbox_height=18,
                                   fg_color=self.color, border_color=self.color, hover_color=self.color)
        used_cb.grid(row=0, column=5, padx=2, pady=4)
        if used and reset != "-":
            used_cb.configure(state="disabled")

        # Manual Reset Button
        def _manual_reset():
            m = max_ent.get()
            if m:
                try:
                    m_int = int(m)
                    cur_ent.set(m_int)
                except ValueError:
                    pass
                used_var.set(False)
                used_cb.configure(state="normal")

        reset_btn = ctk.CTkButton(row_frame, text="↺", width=28, height=22,
                                   fg_color="gray25", hover_color="gray35",
                                   border_color=self.color, border_width=2,
                                   command=_manual_reset)
        reset_btn.grid(row=0, column=6, padx=2, pady=4)
        
        self.after(50, _enforce_limits)
        
        # Description Button
        desc_data = [description] 
        desc_btn = ctk.CTkButton(row_frame, text="📝", width=30, height=22,
                                  fg_color="gray25", hover_color="gray35",
                                  border_color=self.color, border_width=2,
                                  command=lambda: self._open_feature_description(name_ent, desc_data))
        desc_btn.grid(row=0, column=7, padx=2, pady=4)
        
        # Remove
        rem_btn = ctk.CTkButton(row_frame, text="×", width=22, height=22,
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=lambda: self._remove_feature_row(row_id))
        rem_btn.grid(row=0, column=8, padx=(2, 4), pady=4)
        
        self.feature_widgets[row_id] = (name_ent, cur_ent, max_ent, reset_var, used_var, used_cb, desc_data, row_frame)

    def _remove_feature_row(self, row_id):
        if row_id in self.feature_widgets:
            widgets = self.feature_widgets.pop(row_id)
            widgets[-1].destroy()
        
        if not self.feature_widgets:
             self.features_header_frame.pack_forget()

    def _open_feature_description(self, name_ent, desc_data):
        """Popup to edit description"""
        top = ctk.CTkToplevel(self)
        title_text = name_ent.get() if hasattr(name_ent, 'get') else name_ent
        top.title(f"Description: {title_text}")
        top.geometry("400x340")
        top.attributes("-topmost", True)
        
        txt = ctk.CTkTextbox(top, font=("Roboto", 12))
        txt.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        txt.insert("0.0", desc_data[0])
        
        def save_desc():
            desc_data[0] = txt.get("0.0", "end").strip()
            self.autosave_roll_configs()
            top.destroy()
            
        btn = ctk.CTkButton(top, text="Save Description", font=("Roboto", 12, "bold"),
                            fg_color=self.color, hover_color=self.color, command=save_desc)
        btn.pack(pady=(5, 10))
        
    # ---------------- SPELLS SECTION ----------------
    def create_spells_section(self):
        """Spell List with Levels, Prep, and Details"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        # Header
        self.create_section_header(frame, "Spells")
        
        # Column Headers Grid
        hdr = ctk.CTkFrame(frame, fg_color="transparent", height=20)
        hdr.pack(fill="x", padx=self.p, pady=(0, 2))
        # Cols: K(20), P(20), A(20), M(20), Name(exp), Src(30), Gear(24), X(24)
        hdr.columnconfigure(4, weight=1)
        
        labels = [("K", 0), ("P", 1), ("A", 2), ("R", 3)]
        for txt, col in labels:
            ctk.CTkLabel(hdr, text=txt, font=("Roboto", 10, "bold"), width=20, text_color="gray60").grid(row=0, column=col, padx=1)
        
        ctk.CTkLabel(hdr, text="Name", font=("Roboto", 10, "bold"), anchor="w").grid(row=0, column=4, padx=4, sticky="ew")
        
        # Container for Spell Levels (height=0 to collapse when empty)
        self.spells_container = ctk.CTkFrame(frame, fg_color="transparent", height=0)
        self.spells_container.pack(fill="x", padx=self.p, pady=(0, 2))
        
        # Footer (Add Button + Quick Prep)
        footer = ctk.CTkFrame(frame, fg_color="transparent")
        footer.pack(fill="x", padx=self.p, pady=(2, 6))
        
        # Grid layout for Footer: Button centered, QP right
        # Use uniform="b" on col 0 and 2 to force them to equal width, satisfying "Button centered"
        footer.columnconfigure(0, weight=1, uniform="b")
        footer.columnconfigure(1, weight=0) # Button (natural width)
        footer.columnconfigure(2, weight=1, uniform="b") # QP (same width as col 0, content sticky e)
        
        add_btn = ctk.CTkButton(footer, text="+ Add Spell", font=("Roboto", 11),
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=lambda: self._add_spell_row()) 
        add_btn.grid(row=0, column=1)
        
        def toggle_qp():
            if self.quick_prep_used.get():
                self.qp_chk.configure(state="disabled")

        self.qp_chk = ctk.CTkCheckBox(footer, text="Quick Prep (1/LR)", variable=self.quick_prep_used,
                                       font=("Roboto", 10), fg_color=self.color,
                                       checkbox_width=18, checkbox_height=18, hover_color=self.color,
                                       border_color=self.color, command=toggle_qp)
        if self.quick_prep_used.get():
            self.qp_chk.configure(state="disabled")
        self.qp_chk.grid(row=0, column=2, sticky="e", padx=(10, 0))
        
        # Initial Render
        self._update_spell_list()

    def _update_spell_list(self):
        """Rebuilds the spell list UI grouped by level"""
        # Clear existing widgets
        for w in self.spells_container.winfo_children():
            w.destroy()
        self.spell_widgets.clear()
        
        # Group spells by level
        grouped = {i: [] for i in range(10)} # 0-9
        for s in self.spells:
            try:
                lvl = int(s.get("level", 0))
            except:
                lvl = 0
            if 0 <= lvl <= 9:
                grouped[lvl].append(s)
            else:
                grouped[0].append(s) # Fallback
        
        # Render groups
        for lvl in range(10):
            spells = grouped[lvl]
            if not spells and lvl > 0: continue 
            if not spells and lvl == 0 and not self.spells: continue 

            # Sort spells within level: Always > Prepared > Known > Ritual > Name
            spells.sort(key=lambda s: (
                0 if s.get("always", False) else 1,
                0 if s.get("prepared", False) else 1,
                0 if s.get("known", True) else 1,
                0 if s.get("ritual", False) else 1,
                s.get("name", "").lower()
            ))
            
            # Level Header
            lbl_text = "Cantrips (0)" if lvl == 0 else f"Level {lvl}"
            ctk.CTkLabel(self.spells_container, text=lbl_text, font=("Roboto", 12, "bold"), 
                         text_color="gray70", anchor="w").pack(fill="x", pady=(4, 2))
            
            # Spells
            for spell in spells:
                self._render_spell_row(spell)

    def create_pets_section(self):
        """Companion tracking (João-com-braço, etc.)"""
        frame = self.create_bordered_frame(self.main_frame)
        frame.pack(fill="x", pady=(0, 6))
        
        self.create_section_header(frame, "Pets & Companions")
        
        # Header Row (Hidden by default)
        self.pets_header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        # Don't pack immediately
        self.pets_header_frame.columnconfigure(0, weight=1)
        
        # Match the widths and padding from _add_pet_row
        ctk.CTkLabel(self.pets_header_frame, text="Pet Name", font=("Roboto", 11, "bold"), anchor="w").grid(row=0, column=0, padx=4, sticky="ew")
        ctk.CTkLabel(self.pets_header_frame, text="Type", font=("Roboto", 11, "bold"), width=60, anchor="w").grid(row=0, column=1, padx=2)
        ctk.CTkLabel(self.pets_header_frame, text="PCN", font=("Roboto", 11, "bold"), width=40, anchor="center").grid(row=0, column=2, padx=2)
        ctk.CTkLabel(self.pets_header_frame, text="/", font=("Roboto", 11, "bold"), width=10, anchor="center").grid(row=0, column=3)
        ctk.CTkLabel(self.pets_header_frame, text="Max", font=("Roboto", 11, "bold"), width=40, anchor="center").grid(row=0, column=4, padx=2)
        ctk.CTkLabel(self.pets_header_frame, text="AA", font=("Roboto", 11, "bold"), width=30, anchor="center").grid(row=0, column=5, padx=2)
        ctk.CTkLabel(self.pets_header_frame, text="Spd", font=("Roboto", 11, "bold"), width=30, anchor="center").grid(row=0, column=6, padx=2)
        ctk.CTkLabel(self.pets_header_frame, text="Desc", font=("Roboto", 11, "bold"), width=30, anchor="center").grid(row=0, column=7, padx=2)
        ctk.CTkLabel(self.pets_header_frame, text="", width=28).grid(row=0, column=8, padx=(2,4))
        
        # Pets Container
        self.pets_container = ctk.CTkFrame(frame, fg_color="transparent", height=0)
        self.pets_container.pack(fill="x", padx=self.p, pady=(0, 2))
        self.pets_container.columnconfigure(0, weight=1)
        
        # Buttons Container (Add / Import side-by-side)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=(2, 6))
        
        add_btn = ctk.CTkButton(btn_frame, text="+ Add Companion", font=("Roboto", 11),
                                 fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=self._add_pet_row)
        add_btn.pack(side="left", padx=4)
        
        import_btn = ctk.CTkButton(btn_frame, text="📥 Import Monster", font=("Roboto", 11),
                                    fg_color="gray25", hover_color="gray35",
                                    border_color=self.color, border_width=2,
                                    command=self._import_monster_stat_block_popup)
        import_btn.pack(side="left", padx=4)

    def _add_pet_row(self, name="", type_="", cur_pcn="", max_pcn="", aa="", spd="", desc=""):
        if not self.pet_widgets:
            # Show header if this is the first item
            self.pets_header_frame.pack(fill="x", padx=self.p, pady=(0, 2), before=self.pets_container)
            
        row_id = str(uuid.uuid4())
        row_frame = ctk.CTkFrame(self.pets_container, fg_color="gray25", corner_radius=6)
        row_frame.pack(fill="x", pady=2)
        row_frame.columnconfigure(0, weight=1)
        
        name_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), height=22, fg_color="gray17", border_width=1, border_color=self.color)
        name_ent.insert(0, name); name_ent.grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        
        type_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=60, height=22, fg_color="gray17", border_width=0)
        type_ent.insert(0, type_); type_ent.grid(row=0, column=1, padx=2, pady=4)
        
        pcn_cur = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=40, height=22, justify="center", fg_color="gray17", border_width=0)
        pcn_cur.insert(0, cur_pcn); pcn_cur.grid(row=0, column=2, padx=2, pady=4)
        
        ctk.CTkLabel(row_frame, text="/", width=10).grid(row=0, column=3)
        
        pcn_max = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=40, height=22, justify="center", fg_color="gray17", border_width=0)
        pcn_max.insert(0, max_pcn); pcn_max.grid(row=0, column=4, padx=2, pady=4)
        
        aa_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=30, height=22, justify="center", fg_color="gray17", border_width=0)
        aa_ent.insert(0, aa); aa_ent.grid(row=0, column=5, padx=2, pady=4)
        
        spd_ent = ctk.CTkEntry(row_frame, font=("Roboto", 11), width=30, height=22, justify="center", fg_color="gray17", border_width=0)
        spd_ent.insert(0, spd); spd_ent.grid(row=0, column=6, padx=2, pady=4)
        
        # Bind all entries for autosave
        for e in [name_ent, type_ent, pcn_cur, pcn_max, aa_ent, spd_ent]:
            e.bind("<FocusOut>", self.autosave_roll_configs)
        
        desc_data = [desc]
        desc_btn = ctk.CTkButton(row_frame, text="📝", width=30, height=22, fg_color="gray25", hover_color="gray35",
                                  border_color=self.color, border_width=2,
                                  command=lambda: self._open_feature_description(name_ent, desc_data))
        desc_btn.grid(row=0, column=7, padx=2, pady=4)
        
        rem_btn = ctk.CTkButton(row_frame, text="×", width=22, height=22, fg_color="gray25", hover_color="gray35",
                                 border_color=self.color, border_width=2,
                                 command=lambda: self._remove_pet_row(row_id))
        rem_btn.grid(row=0, column=8, padx=(2, 4), pady=4)
        
        self.pet_widgets[row_id] = (name_ent, type_ent, pcn_cur, pcn_max, aa_ent, spd_ent, desc_data, row_frame)
        self.autosave_roll_configs()

    def _import_monster_stat_block_popup(self):
        """Popup to paste a monster stat block for automatic row creation"""
        top = ctk.CTkToplevel(self)
        top.title("Import Monster Stat Block")
        top.geometry("500x400")
        top.attributes("-topmost", True)
        
        ctk.CTkLabel(top, text="Paste D&D 5e Stat Block (e.g. from Wikidot/Roll20/PDF):",
                     font=("Roboto", 12, "bold")).pack(pady=10)
        
        txt = ctk.CTkTextbox(top, font=("Roboto", 11))
        txt.pack(fill="both", expand=True, padx=20, pady=10)
        
        def do_import():
            content = txt.get("0.0", "end")
            if content.strip():
                self._process_monster_import(content)
                top.destroy()
        
        ctk.CTkButton(top, text="Import", command=do_import,
                      fg_color=self.color, hover_color=self.color).pack(pady=20)

    def _process_monster_import(self, text):
        """Parse text for Name, AC, HP, Speed and add row"""
        # Translate the content using Monster Translator.py
        translated_text = text
        try:
            import importlib.util, os, sys
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Monster Translator.py")
            if os.path.exists(script_path):
                spec = importlib.util.spec_from_file_location("monster_translator", script_path)
                mt = importlib.util.module_from_spec(spec)
                sys.modules["monster_translator"] = mt
                spec.loader.exec_module(mt)
                translated_text = mt.translate_monster(text)
        except Exception as e:
            print(f"Monster translation error: {e}")
            
        # Clean text
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines: return
        
        name = lines[0] # Assume first line is name
        # Better name detection: skip if it looks like "Armor Class" or "Hit Points"
        for line in lines:
            if not any(x in line.lower() for x in ["armor class", "hit points", "speed", "size", "actions"]):
                name = line
                break
        
        # Regex extraction
        import re
        ac_match = re.search(r"Armor\s+Class\s+(\d+)", text, re.I)
        hp_match = re.search(r"Hit\s+Points\s+(\d+)", text, re.I)
        spd_match = re.search(r"Speed\s+(\d+)", text, re.I)
        
        ac = 10
        if ac_match: ac = int(ac_match.group(1))
        
        hp = ""
        if hp_match: hp = hp_match.group(1)
        
        spd = ""
        if spd_match: spd = spd_match.group(1)
        
        # G(r)ay AA logic: -(AC-10)*2
        aa = -(ac - 10) * 2
        
        # Determine type (Size/Type line usually follows name)
        m_type = ""
        for line in lines:
            if any(x in line.lower() for x in ["tiny", "small", "medium", "large", "huge", "gargantuan"]):
                m_type = line
                break
                
        self._add_pet_row(name=name, type_=m_type, cur_pcn=hp, max_pcn=hp, aa=str(aa), spd=spd, desc=translated_text)


    def _remove_pet_row(self, row_id):
        if row_id in self.pet_widgets:
            self.pet_widgets[row_id][-1].destroy()
            del self.pet_widgets[row_id]

    def _add_spell_row(self, spell_data=None):
        """Adds a new spell to data and refreshes UI"""
        if spell_data is None:
            # New empty spell
            spell_data = {
                "id": str(uuid.uuid4()),
                "name": "New Spell",
                "level": 0,
                "known": True,
                "prepared": False,
                "always": False,
                "ritual": False,
                "source": "Wizard",
                "time": "1 action",
                "range": "60 ft",
                "comp": "v, s",
                "dur": "Instantaneous",
                "desc": ""
            }
            self.spells.append(spell_data)
        
        # Refresh is inefficient for single add, but easiest for sorting/grouping
        self._update_spell_list()

    def _render_spell_row(self, spell):
        """Renders a single spell row with 4 columns (K, P, A, F)"""
        row = ctk.CTkFrame(self.spells_container, fg_color="gray25", corner_radius=6)
        row.pack(fill="x", pady=2)
        
        # Grid layout: K(0) P(1) A(2) M(3) Name(4) Src(5) Gear(6) Del(7)
        row.columnconfigure(4, weight=1) # Name entry expands
        
        def create_cb(col, key, default=False, visible=True):
            if not visible:
                # Placeholder
                ctk.CTkLabel(row, text="", width=20).grid(row=0, column=col, padx=1)
                return
            
            var = BooleanVar(value=spell.get(key, default))
            def toggle(s=spell, k=key, v=var):
                s[k] = v.get()
                self._update_spell_list() # Immediate re-sort and UI update
            
            cb = ctk.CTkCheckBox(row, text="", variable=var, command=toggle,
                                 checkbox_width=16, checkbox_height=16, width=20,
                                 fg_color=self.color, hover_color=self.color, border_color=self.color)
            cb.grid(row=0, column=col, padx=2, pady=2)
            return var
            
        lvl = int(spell.get("level", 0))
        is_leveled = lvl > 0
        
        # 1. Known (K) - Always vis
        create_cb(0, "known", True, True)
        
        # 2. Prepared (P) - Leveled only
        create_cb(1, "prepared", False, is_leveled)
        
        # 3. Always (A) - Leveled only
        create_cb(2, "always", False, is_leveled)
        
        # 4. Ritual (R) - Leveled only
        create_cb(3, "ritual", False, is_leveled)
        
        # Name Entry
        name_ent = ctk.CTkEntry(row, font=("Roboto", 12), height=24, border_width=1, fg_color="gray17", border_color="gray30")
        name_ent.insert(0, spell.get("name", ""))
        name_ent.grid(row=0, column=4, sticky="ew", padx=2)
        def _update_name(e=None):
            spell["name"] = name_ent.get()
            self.focus() # Unfocus
        name_ent.bind("<FocusOut>", lambda e: spell.update({"name": name_ent.get()}))
        name_ent.bind("<Return>", _update_name)
        
        # Source Label (Mini)
        src_lbl = ctk.CTkLabel(row, text=spell.get("source", "")[:3], font=("Roboto", 10), text_color="gray60", width=30)
        src_lbl.grid(row=0, column=5, padx=2)
        
        # Details Button
        edit_btn = ctk.CTkButton(row, text="⚙", width=24, height=24, fg_color="gray35", hover_color="gray45",
                                  font=("Arial", 12), command=lambda s=spell: self._open_spell_details(s))
        edit_btn.grid(row=0, column=6, padx=2)
        
        # Delete Button
        del_btn = ctk.CTkButton(row, text="×", width=24, height=24, fg_color="transparent", hover_color="#c0392b",
                                 text_color="gray60", command=lambda s=spell: self._delete_spell(s))
        del_btn.grid(row=0, column=7, padx=(2, 4))
        
        spell_id = spell.get("id", str(uuid.uuid4()))
        if "id" not in spell: spell["id"] = spell_id
        self.spell_widgets[spell_id] = (row, None, name_ent, src_lbl)

    def _delete_spell(self, spell):
        if spell in self.spells:
            self.spells.remove(spell)
            self._update_spell_list()

    def _open_spell_details(self, spell):
        """Popup to edit full spell details"""
        top = ctk.CTkToplevel(self)
        top.title(f"Edit: {spell['name']}")
        top.geometry("350x450")
        top.attributes("-topmost", True)
        
        # Helpers
        def add_field(parent, label, key, row):
            ctk.CTkLabel(parent, text=label, font=("Roboto", 11, "bold")).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            ent = ctk.CTkEntry(parent, font=("Roboto", 11))
            ent.insert(0, str(spell.get(key, "")))
            ent.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
            return ent
            
        f = ctk.CTkFrame(top, fg_color="transparent")
        f.pack(fill="x", padx=10, pady=10)
        f.columnconfigure(1, weight=1)
        
        # Fields
        lvl_ent = add_field(f, "Level (0-9):", "level", 0)
        src_ent = add_field(f, "Source:", "source", 1)
        time_ent = add_field(f, "Casting Time:", "time", 2)
        rng_ent = add_field(f, "Range:", "range", 3)
        cmp_ent = add_field(f, "Components:", "comp", 4)
        dur_ent = add_field(f, "Duration:", "dur", 5)
        
        # Description
        ctk.CTkLabel(top, text="Description:", font=("Roboto", 11, "bold")).pack(anchor="w", padx=15)
        desc_txt = ctk.CTkTextbox(top, font=("Roboto", 11), height=150)
        desc_txt.pack(fill="both", expand=True, padx=10, pady=5)
        desc_txt.insert("0.0", spell.get("desc", ""))
        
        def save():
            try:
                spell["level"] = int(lvl_ent.get())
            except:
                pass
            spell["source"] = src_ent.get()
            spell["time"] = time_ent.get()
            spell["range"] = rng_ent.get()
            spell["comp"] = cmp_ent.get()
            spell["dur"] = dur_ent.get()
            spell["desc"] = desc_txt.get("0.0", "end").strip()
            top.destroy()
            self._update_spell_list()
            
        ctk.CTkButton(top, text="Save & Close", command=save, fg_color=self.color).pack(pady=10)

    def _update_shards_calculations(self, _=None):
        # Parse Levels
        try:
            caster_lvl = int(self.caster_level_var.get())
        except ValueError:
            caster_lvl = 1
            
        try:
            warlock_lvl = int(self.warlock_level_var.get())
        except ValueError:
            warlock_lvl = 0
            
        # 1. Update Saturation Limits
        # Normal uses Caster Level
        sat_data_normal = self.CASTER_LEVEL_SATURATION.get(caster_lvl, [None]*9)
        for i, val in enumerate(sat_data_normal):
            ent = self.resonance_saturation_entries[i]
            ent.delete(0, "end")
            ent.insert(0, str(val) if val is not None else "–")
            self._update_res_h(i, self.resonance_count_entries, self.resonance_saturation_entries, self.normal_mult_labels)
            
        # Pact uses Warlock Level (if > 0)
        if warlock_lvl > 0:
            sat_data_pact = self.CASTER_LEVEL_SATURATION.get(warlock_lvl, [None]*9)
            for i, val in enumerate(sat_data_pact):
                ent = self.pact_saturation_entries[i]
                ent.delete(0, "end")
                ent.insert(0, str(val) if val is not None else "–")
                self._update_res_h(i, self.pact_count_entries, self.pact_saturation_entries, self.pact_mult_labels)
        else:
            # If Warlock 0, maybe clear or set safe defaults?
            pass

        # 2. Calculate Pact Shards and Mana Burn
        pact_base_shards = self.CASTER_LEVEL_SHARDS.get(warlock_lvl, 0)
        # Pact Shards = ceil(Base / 4)
        pact_count_total = math.ceil(pact_base_shards / 4) if warlock_lvl > 0 else 0
        
        # Pact Output Limit = floor(Warlock / 2 + 0.75), Max 5
        pact_max_out = min(5, math.floor(warlock_lvl / 2 + 0.75)) if warlock_lvl > 0 else 0
        
        # Mana Burn = Pact Shards * 4
        mana_burn = pact_count_total * 4
        
        # Normal Shards Base
        normal_base_shards = self.CASTER_LEVEL_SHARDS.get(caster_lvl, 0)
        
        # Final Normal Shards
        final_normal_shards = max(0, normal_base_shards - mana_burn)
        
        # 3. Update Shard Source Rows
        found_class = False
        found_pact = False
        
        for _, widgets in self.shard_widgets.items():
            # widgets = (source_ent, src_type_var, shard_type_var, current_ent, total_ent, max_out_ent, ...)
            s_type = widgets[1].get()
            sh_type = widgets[2].get()
            
            # Update First Normal Class Source
            if s_type == "Class" and sh_type == "Normal" and not found_class:
                widgets[4].delete(0, "end")
                widgets[4].insert(0, str(final_normal_shards))
                found_class = True
                
            # Update First Pact Source (Type doesn't strictly matter if Shard Type is Pact, but usually Class)
            if sh_type == "Pact" and not found_pact:
                widgets[4].delete(0, "end")
                widgets[4].insert(0, str(pact_count_total))
                widgets[5].delete(0, "end")
                widgets[5].insert(0, str(pact_max_out))
                found_pact = True
                
        # If user has Warlock levels but no Pact row, they might be confused, but we rely on them adding it.
        # Likewise for Class row.

    def _create_resonance_grid(self, parent, sat_list, count_list, mult_list, is_pact=False):
        """Helper to create a 9-column resonance grid with Cost Multiplier"""
        res_grid = ctk.CTkFrame(parent, fg_color="gray20", corner_radius=6)
        res_grid.pack(fill="x")
        for c in range(10):
            res_grid.columnconfigure(c, weight=1 if c > 0 else 0)
            
        color = "white" # Fixed to white as requested
            
        # Header (Outputs)
        ctk.CTkLabel(res_grid, text="Output", font=("Roboto", 9, "bold"),
                     text_color="gray50", width=55).grid(row=0, column=0, padx=2, pady=2)
        for i in range(1, 10):
            ctk.CTkLabel(res_grid, text=str(i), font=("Roboto", 10, "bold"),
                         text_color=color).grid(row=0, column=i, padx=1, pady=2)
        
        # Saturation
        ctk.CTkLabel(res_grid, text="Satur.", font=("Roboto", 9),
                     text_color="gray50", width=55).grid(row=1, column=0, padx=2, pady=1)
        for i in range(9):
            ent = ctk.CTkEntry(res_grid, font=("Roboto", 10), width=30, height=20, justify="center",
                               fg_color="gray17", border_width=0)
            ent.grid(row=1, column=i+1, padx=1, pady=1)
            ent.insert(0, "–")
            ent.bind("<KeyRelease>", lambda e, idx=i, cl=count_list, sl=sat_list, ml=mult_list: self._update_res_h(idx, cl, sl, ml))
            sat_list.append(ent)
            
        # Count
        ctk.CTkLabel(res_grid, text="Count", font=("Roboto", 9),
                     text_color="gray50", width=55).grid(row=2, column=0, padx=2, pady=1)
        for i in range(9):
            ent = ctk.CTkEntry(res_grid, font=("Roboto", 10), width=30, height=20, justify="center",
                               fg_color="gray17", border_width=0)
            ent.grid(row=2, column=i+1, padx=1, pady=(1, 2))
            ent.insert(0, "0")
            # Bind using separated method to avoid closure issues
            ent.bind("<KeyRelease>", lambda e, idx=i, cl=count_list, sl=sat_list, ml=mult_list: self._update_res_h(idx, cl, sl, ml))
            count_list.append(ent)
            
        # Cost Multiplier
        ctk.CTkLabel(res_grid, text="Cost Mult.", font=("Roboto", 9),
                     text_color="gray50", width=55).grid(row=3, column=0, padx=2, pady=(1, 4))
        for i in range(9):
            lbl = ctk.CTkLabel(res_grid, text="1x", font=("Roboto", 10, "bold"),
                               text_color="gray60")
            lbl.grid(row=3, column=i+1, padx=1, pady=(1, 4))
            mult_list.append(lbl)

    def _add_shard_row(self, source="", source_type="Class", shard_type="Normal",
                       current="", total="", max_output="", arcane_rest=False, rest_type="Long"):
        """Add a dynamic shard source row"""
        row_id = str(len(self.shard_widgets))
        row_frame = ctk.CTkFrame(self.shards_container, fg_color="gray21", corner_radius=6)
        row_frame.pack(fill="x", pady=3)
        
        # --- Top Row: Source, Type, Shard Type, Delete ---
        top = ctk.CTkFrame(row_frame, fg_color="transparent")
        top.pack(fill="x", padx=5, pady=(5, 2))
        
        # Source Name (Expand)
        ctk.CTkLabel(top, text="Source:", font=("Roboto", 11), text_color="gray60").pack(side="left", padx=(0, 5))
        source_ent = ctk.CTkEntry(top, font=("Roboto", 11), height=24, fg_color="gray17", border_width=0)
        source_ent.pack(side="left", fill="x", expand=True, padx=(0, 10))
        source_ent.insert(0, source)
        
        # Type
        type_var = StringVar(value=source_type)
        ctk.CTkOptionMenu(top, variable=type_var, values=["Class", "Feat", "Item", "Racial", "Other"],
                          font=("Roboto", 11), width=75, height=24,
                          fg_color="gray17", button_color="gray25",
                          button_hover_color=self.color, dropdown_hover_color=self.color).pack(side="left", padx=(0, 5))
                          
        # Shard Type
        shard_type_var = StringVar(value=shard_type)
        menu = ctk.CTkOptionMenu(top, variable=shard_type_var, values=["Normal", "Pact"],
                                  font=("Roboto", 11), width=75, height=24,
                                  fg_color="gray17", button_color="gray25",
                                  button_hover_color=self.color, dropdown_hover_color=self.color,
                                  command=lambda _: self._update_pact_visibility())
        menu.pack(side="left", padx=(0, 5))
        
        # Delete Button
        ctk.CTkButton(top, text="×", width=24, height=24,
                      fg_color="gray25", hover_color="#c44e4e",
                      border_color=self.color, border_width=0,
                      command=lambda: self._remove_shard_row(row_id)).pack(side="left")

        # --- Bottom Row: Current, Total, MaxOut, Arc.Rest, Rest Type ---
        bot = ctk.CTkFrame(row_frame, fg_color="transparent")
        bot.pack(fill="x", padx=5, pady=(0, 5))
        
        # Current / Total
        ctk.CTkLabel(bot, text="Curr:", font=("Roboto", 11), text_color="gray60").pack(side="left", padx=(0, 5))
        current_ent = ctk.CTkEntry(bot, font=("Roboto", 11, "bold"), width=40, height=24, justify="center",
                                    fg_color="gray17", border_width=1, border_color=self.color)
        current_ent.pack(side="left")
        current_ent.insert(0, current if current else total)
        
        ctk.CTkLabel(bot, text="/", font=("Roboto", 11), text_color="gray50").pack(side="left", padx=2)
        
        total_ent = ctk.CTkEntry(bot, font=("Roboto", 11), width=40, height=24, justify="center",
                                  fg_color="gray17", border_width=0)
        total_ent.pack(side="left", padx=(0, 15))
        total_ent.insert(0, total)
        
        # Max Output
        ctk.CTkLabel(bot, text="MaxOut:", font=("Roboto", 11), text_color="gray60").pack(side="left", padx=(0, 5))
        max_out_ent = ctk.CTkEntry(bot, font=("Roboto", 11), width=35, height=24, justify="center",
                                    fg_color="gray17", border_width=0)
        max_out_ent.pack(side="left", padx=(0, 15))
        max_out_ent.insert(0, max_output)
        
        # Arcane Rest
        arcane_var = BooleanVar(value=arcane_rest)
        ctk.CTkCheckBox(bot, text="Arc. Rest", variable=arcane_var,
                         font=("Roboto", 11), checkbox_width=18, checkbox_height=18,
                         hover_color=self.color, fg_color=self.color,
                         border_color=self.color).pack(side="left", padx=(0, 15))
        
        # Rest Type
        ctk.CTkLabel(bot, text="Rest:", font=("Roboto", 11), text_color="gray60").pack(side="left", padx=(0, 5))
        rest_var = StringVar(value=rest_type)
        ctk.CTkOptionMenu(bot, variable=rest_var, values=["Long", "Short"],
                           font=("Roboto", 11), width=70, height=24,
                           fg_color="gray17", button_color="gray25",
                           button_hover_color=self.color, dropdown_hover_color=self.color).pack(side="left")
        
        self.shard_widgets[row_id] = (source_ent, type_var, shard_type_var,
                                       current_ent, total_ent, max_out_ent,
                                       arcane_var, rest_var, row_frame)
        # Bind for autosave
        for e in [source_ent, current_ent, total_ent, max_out_ent]:
            e.bind("<FocusOut>", self.autosave_roll_configs)
        
        self._update_pact_visibility()

    def _remove_shard_row(self, row_id):
        if row_id in self.shard_widgets:
            self.shard_widgets[row_id][-1].destroy()
            del self.shard_widgets[row_id]
        self._update_pact_visibility()
        
    def _update_pact_visibility(self):
        """Show/Hide Pact Resonance section based on if any Pact source exists"""
        has_pact = False
        for _, widgets in self.shard_widgets.items():
            if widgets[2].get() == "Pact":
                has_pact = True
                break
        
        if has_pact:
            self.pact_res_container.pack(fill="x", pady=2, after=self.normal_res_frame)
        else:
            self.pact_res_container.pack_forget()

    def _update_res_h(self, idx, count_list, sat_list, mult_list):
        """Update highlighting and Cost Multiplier based on Saturation"""
        c_ent = count_list[idx]
        s_ent = sat_list[idx]
        m_lbl = mult_list[idx]
        
        try:
            count = int(c_ent.get())
        except ValueError:
            count = 0
            
        # Highlight count entry if active
        if count > 0:
            c_ent.configure(fg_color=self.color, text_color="white")
        else:
            c_ent.configure(fg_color="gray17", text_color="gray90")
            
        # Calculate Saturation Tier & Multiplier
        s_str = s_ent.get()
        sat_limit = 999999 # Default to infinite if "-" or empty
        if s_str.isdigit() and int(s_str) > 0:
            sat_limit = int(s_str)
            
        tier = count // sat_limit
        multiplier = 2 ** tier
        
        m_lbl.configure(text=f"{multiplier}x")
        
        # Color code multiplier
        if multiplier == 1:
            m_lbl.configure(text_color="gray60")
        elif multiplier == 2:
            m_lbl.configure(text_color="#e0e0e0") # White-ish
        elif multiplier == 4:
            m_lbl.configure(text_color=self.color) # User Accent Color
        else:
            m_lbl.configure(text_color="#ff5555") # Danger Red

    def _update_resonance_highlight(self, idx):
        # Legacy/Wrapper for manual calls (Normal Grid)
        self._update_res_h(idx, self.resonance_count_entries, self.resonance_saturation_entries, self.normal_mult_labels)

    def _shard_long_rest(self):
        """Long Rest: reset ALL slots, Shards, Resonance"""
        # (Features and Hit Dice are handled by _long_rest calling this)

        # Reset All Shards
        for _, widgets in self.shard_widgets.items():
            current_ent, total_ent = widgets[3], widgets[4]
            total_val = total_ent.get()
            current_ent.delete(0, "end")
            current_ent.insert(0, total_val)
            
        # Reset Normal resonance
        for i, ent in enumerate(self.resonance_count_entries):
            ent.delete(0, "end")
            ent.insert(0, "0")
            self._update_res_h(i, self.resonance_count_entries, self.resonance_saturation_entries, self.normal_mult_labels)
            
        # Reset Pact resonance
        for i, ent in enumerate(self.pact_count_entries):
            ent.delete(0, "end")
            ent.insert(0, "0")
            self._update_res_h(i, self.pact_count_entries, self.pact_saturation_entries, self.pact_mult_labels)
            
        self.arcane_recovery_used_var.set(False)
        self.arcane_recovery_used_cb.configure(state="normal", text_color="gray60")
        self.quick_prep_used.set(False)
        if hasattr(self, "qp_chk"):
            self.qp_chk.configure(state="normal")

    def _shard_short_rest(self):
        """Short Rest: reset Warlock Pact slots"""
        # (SR Features and Hit Dice are handled by _short_rest calling this)

        # Reset Pact Slots
        found_pact = False
        for _, widgets in self.shard_widgets.items():
            shard_type_var = widgets[2]
            if shard_type_var.get() == "Pact":
                current_ent, total_ent = widgets[3], widgets[4]
                total_val = total_ent.get()
                current_ent.delete(0, "end")
                current_ent.insert(0, total_val)
                found_pact = True

    def _shard_arcane_recovery(self):
        """Arcane Recovery: regain shards, once per long rest"""
        if self.arcane_recovery_used_var.get():
            return  # already used
        try:
            recovery = int(self.arcane_recovery_entry.get() or 0)
        except ValueError:
            return
        if recovery <= 0:
            return
        # Distribute recovered shards across sources that have arcane restoration
        remaining = recovery
        for _, widgets in self.shard_widgets.items():
            if remaining <= 0:
                break
            arcane_var = widgets[6]
            if not arcane_var.get():
                continue
            current_ent, total_ent = widgets[3], widgets[4]
            try:
                current = int(current_ent.get() or 0)
                total = int(total_ent.get() or 0)
            except ValueError:
                continue
            can_recover = min(remaining, total - current)
            if can_recover > 0:
                current_ent.delete(0, "end")
                current_ent.insert(0, str(current + can_recover))
                remaining -= can_recover
        self.arcane_recovery_used_var.set(True)
        self.arcane_recovery_used_cb.configure(state="disabled", text_color="gray50")

    def _guess_linked_aspect(self, name):
        """Helper for backward compatibility to guess aspect for tool"""
        name_lower = name.lower()
        if "instrument" in name_lower: return "Performance"
        if "gaming" in name_lower: return "Awareness"
        return "Dexterity"

    def update_aa(self, event=None):
        """Calculate and update AA field based on equipment"""
        typ = self.armor_settings["type"].get()
        aspect_name = self.armor_settings["aspect"].get()
        shield = self.armor_settings["shield"].get()
        
        armor_data = {
            "None": 0, "Padded": -2, "Leather": -3, "Studded leather": -4,
            "Hide": -4, "Chain shirt": -5, "Scale mail": -6, "Breastplate": -6, "Half plate": -7,
            "Ring mail": -6, "Chain mail": -7, "Splint": -8, "Plate": -10
        }
        
        armor_bonus = armor_data.get(typ, 0)
        shield_bonus = -4 if shield else 0
        
        print(f"DEBUG AA INPUTS: AspectName='{aspect_name}' ArmorType='{typ}' Shield={shield}", flush=True)
        aspect_val = 0
        if aspect_name in self.aspect_widgets:
            entry, _, _, _ = self.aspect_widgets[aspect_name]
            try:
                # Use raw base value (ignoring proficiency/expertise as requested)
                aspect_val = int(entry.get() or 0)
                print(f"DEBUG AA: Using Base Aspect Val={aspect_val}", flush=True)
            except Exception as e:
                print(f"DEBUG AA: Failed to get base value for '{aspect_name}': {e}", flush=True)
                aspect_val = 0
        else:
            print(f"DEBUG AA: Aspect '{aspect_name}' NOT FOUND in widgets. Available: {list(self.aspect_widgets.keys())}", flush=True)
                
        # Base AA calculation
        aa_base = -(aspect_val - 6) + armor_bonus
        
        if "AA" in self.combat_entries:
            self.combat_entries["AA"].delete(0, "end")
            
            # Mobility Shield Logic: Split AA if using Mobility + Shield
            if shield and aspect_name == "Mobility":
                # Melee gets shield bonus, Ranged does not
                aa_melee = aa_base + shield_bonus
                aa_ranged = aa_base
                self.combat_entries["AA"].delete(0, "end")
                self.combat_entries["AA"].insert(0, f"{aa_melee} / {aa_ranged}")
            else:
                aa_total = aa_base + shield_bonus
                self.combat_entries["AA"].delete(0, "end")
                self.combat_entries["AA"].insert(0, str(aa_total))
        
        # New: Update Speed based on conditions
        self.update_speed()
        
        # Re-generate configs to apply potential proficiency penalties
        self.autosave_roll_configs()
        self.update_net_adv()

    def update_net_adv(self, event=None):
        """Recalculate and display the net advantage from armor/shield/exhaustion penalties"""
        penalty = 0
        
        # Armor non-proficiency
        if self.armor_settings["type"].get() != "None" and not self.armor_settings["prof"].get():
            penalty -= 1
        
        # Shield non-proficiency
        if self.armor_settings["shield"].get() and not self.armor_settings["shield_prof"].get():
            penalty -= 1
        
        # Exhaustion
        try:
            exh = self.exhaustion_var.get()
            penalty -= max(0, min(10, exh))  # Clamp 0-10
        except (ValueError, TclError):
            pass

        # Conditions (General penalties)
        penalty += self.get_condition_modifiers('General')
        
        sign = "+" if penalty >= 0 else ""
        self.net_adv_label.configure(text=f"{sign}{penalty}")
        self.autosave_roll_configs()

    def on_condition_change(self):
        """Update everything that depends on conditions"""
        self.update_net_adv()
        self.update_speed()
        self.update_weapon_bonuses() 
        self.update_knowledge_fields()
        self.update_tool_fields()
        for stat in ["Mind", "Soul", "Senses", "Body"]:
            self.update_save_total(stat)
        self.update_aa() # This implicitly calls generate_roll_configs

    def update_speed(self):
        """Handle immobilizing conditions affecting Speed"""
        if "Spd" not in self.combat_entries: return
        
        active = {c for c, v in self.conditions_vars.items() if v.get()}
        immobilizers = ["Grappled", "Paralyzed", "Petrified", "Restrained", "Stunned", "Unconscious"]
        
        entry = self.combat_entries["Spd"]
        if any(c in active for c in immobilizers):
            # Capture current as base before zeroing if not already tracking
            # But only if it's NOT already 0 (to avoid capturing the penalty state as base)
            current = entry.get()
            if not hasattr(self, '_base_speed_val') or self._base_speed_val is None:
                if current != "0":
                    self._base_speed_val = current
            
            if entry.get() != "0":
                 entry.delete(0, "end")
                 entry.insert(0, "0")
            entry.configure(text_color="#ff4d4d") # Soft red
        else:
            # Restore base speed if we have one stored
            if hasattr(self, '_base_speed_val') and self._base_speed_val is not None:
                if entry.get() == "0":
                    entry.delete(0, "end")
                    entry.insert(0, self._base_speed_val)
                self._base_speed_val = None
            entry.configure(text_color="white")
        self.autosave_roll_configs()

    def get_condition_modifiers(self, roll_type, name=None):
        """
        Calculate total advantage/disadvantage modifier from active conditions.
        roll_type: 'Attack', 'Check', 'Save', 'AA', 'General'
        """
        mod = 0
        active = {c for c, v in self.conditions_vars.items() if v.get()}
        
        if roll_type == 'Attack':
            if "Blinded" in active: mod -= 1
            if "Frightened" in active: mod -= 1
            if "Invisible" in active: mod += 1
            if "Poisoned" in active: mod -= 1
            if "Prone" in active: mod -= 1
            if "Restrained" in active: mod -= 1
            
        elif roll_type == 'Check':
            if "Frightened" in active: mod -= 1
            if "Poisoned" in active: mod -= 1
            if name == "Awareness" and "Blinded" in active: mod -= 1
            if name in ["Mobility", "Acrobatics", "Dexterity"] and "Restrained" in active: mod -= 1
            
        elif roll_type == 'Save':
            # In this system, saves use stat categories (Senses=Dex, Body=Str/Con)
            if name == "Senses": # Dex
                if "Restrained" in active: mod -= 1
                if any(c in active for c in ["Paralyzed", "Petrified", "Stunned", "Unconscious"]): mod -= 1
            if name == "Body": # Str/Con
                if any(c in active for c in ["Paralyzed", "Petrified", "Stunned", "Unconscious"]): mod -= 1
        
        elif roll_type == 'AA':
            if "Invisible" in active: mod += 1
            if any(c in active for c in ["Blinded", "Paralyzed", "Petrified", "Restrained", "Stunned", "Unconscious"]): mod -= 1
            
        elif roll_type == 'General':
            if "Poisoned" in active: mod -= 1
            if "Frightened" in active: mod -= 1
            
        return mod

    def update_weapon_bonuses(self, event=None):
        """Update Atk/AS label for all items based on selection and extras"""
        pb = self.get_prof_bonus()
        for wid, (name_ent, asp_var, p_var, type_var, const_ent, adv_ent, bonus_lbl, _, _) in self.weapon_widgets.items():
            aspect_name = asp_var.get()
            is_prof = p_var.get()
            roll_type = type_var.get()
            
            # Get Aspect Value
            aspect_val = 0
            if aspect_name in self.aspect_widgets:
                _, _, _, total_lbl = self.aspect_widgets[aspect_name]
                try:
                    txt = total_lbl.cget("text")
                    if "Total:" in txt:
                        aspect_val = int(txt.split("Total:")[1].strip().replace("+", ""))
                    else:
                        aspect_val = int(txt.replace("+", ""))
                except:
                    aspect_val = 0
            
            # Get Extra Const
            try:
                extra = int(const_ent.get() or 0)
            except ValueError:
                extra = 0
            
            # Calculate Base Bonus
            base_bonus = aspect_val + (pb if is_prof else 0) + extra
            
            if roll_type == "Atk":
                bonus_lbl.configure(text=f"Atk: {base_bonus:+}")
            else: # AS
                # AS is usually 8 + Prof + Mod. 
                # Wait, original code was: as_bonus = -(atk_bonus - 4).
                # That logic: DC = 8 + Mod + Prof -> -(DC - 12) ? No.
                # Let's stick to standard DC = 8 + Mod + Prof + Extra
                # Or if it's "AS Roll" (roll d20 vs DC), then it mimics Atk?
                # The user context "Attack or AS" suggests Action Score (like Attack Roll).
                # Previous code: as_bonus = -(atk_bonus - 4). 
                # If Atk = +5 (Mod+3, Prof+2). AS = -(5 - 4) = -1. 
                # This implies AS is a "Penalty" applied to the target's roll? 
                # "Disadvantage against being attacked" user said.
                # Let's assume AS is another roll modifier.
                # If it's a "Save DC", it's usually 8+...
                # Given user request "Spell Attack and Spell AS", let's treat it as a number.
                # I'll use the same formula as Atk (Aspect + Prof + Extra) for now, 
                # unless the previous logic -(atk-4) meant something specific in this system.
                # ORIGINAL: as_bonus = -(atk_bonus - 4)  =>  - ( (Val + Prof) - 4 ) => 4 - Val - Prof.
                # This looks like "Defense vs Attack"? 10 + ...?
                # User said: "remove spell attack and spell as... let user supply input... such as disadvantage against being attack".
                # If I select "AS", maybe I just show the bonus derived from Aspect + Prof + Extra.
                # I will use standard additive logic for now. If AS needs that formula, I can revert.
                # Wait, "AS" in this system might be "Active Defense"?
                # Let's look at `load_local_roll` dynamic penalty logic... `-1` for armor non-prof.
                # The prompt mentions "AS: -14" in the screenshot! (Atk: +18, AS: -14).
                # +18 vs -14. 
                # If Atk was +18 (presumably very high level/stats).
                # AS = -(18 - 4) = -14. Correct.
                # So AS = 4 - (Aspect + Prof).
                # I will preserve this logic if type is "AS".
                
                as_val = 4 - base_bonus
                bonus_lbl.configure(text=f"AS: {as_val:+}")
        self.autosave_roll_configs()
        
    def autosave_roll_configs(self, event=None):
        """Silently generate roll configs periodically or on focus out"""
        if hasattr(self, '_autosave_after_id'):
            self.after_cancel(self._autosave_after_id)
        
        def _do_both():
            self.generate_roll_configs()
            self._silent_master_save()
            
        self._autosave_after_id = self.after(500, _do_both)
        
    def _silent_master_save(self):
        """Automatically saves the master character tracking object to the loaded filepath."""
        if getattr(self, '_loaded_filepath', None) and os.path.exists(self._loaded_filepath):
            try:
                with open(self._loaded_filepath, "wb") as f:
                    pickle.dump(self.gather_data(), f)
            except Exception as e:
                print(f"Master Sheet Autosave Error: {e}")

    def update_knowledge_fields(self):
        """Recalculate all knowledge field values based on linked aspects and prof"""
        pb = self.get_prof_bonus()
        print(f"DEBUG: Updating Knowledge Fields (PB={pb})")
        print(f"DEBUG: Aspect Keys: {list(self.aspect_widgets.keys())}")
        
        for field, (prof_var, val_lbl, linked_aspect, adv_var) in self.knowledge_widgets.items():
            # Get linked aspect's effective value (base + aspect's own prof bonus)
            if linked_aspect in self.aspect_widgets:
                entry, aspect_prof_var, _, _ = self.aspect_widgets[linked_aspect]
                try:
                    aspect_val = int(entry.get() or 0)
                except ValueError:
                    aspect_val = 0
                # Add the aspect's own proficiency contribution
                aspect_prof = aspect_prof_var.get()
                prof = prof_var.get()
                # Tool/Knowledge uses its own proficiency setting
                bonus = self.calculate_bonus(aspect_prof)
                if prof == "F" or prof == "E":
                    total = aspect_val + bonus
                elif prof == "-":
                    total = aspect_val + round(bonus/2 + 0.1) - 6
                else: # ½
                    total = aspect_val + bonus - 6
            else:
                total = 0
                print(f"DEBUG: Linked aspect '{linked_aspect}' not found for field '{field}'")
            
            val_lbl.configure(text=f"{total:+}")
            print(f"DEBUG: {field} -> Linked: {linked_aspect} ({aspect_val}) | Prof: {prof} | Aspect Prof: {aspect_prof} | Total: {total}")
        self.autosave_roll_configs()

    def update_tool_fields(self):
        """Recalculate all tool field values (same rules as knowledge fields)"""
        pb = self.get_prof_bonus()
        
        for tool, (prof_var, val_lbl, linked_aspect, adv_var) in self.tool_widgets.items():
            # Get linked aspect's effective value (base + aspect's own prof bonus)
            if linked_aspect in self.aspect_widgets:
                entry, aspect_prof_var, _, _ = self.aspect_widgets[linked_aspect]
                try:
                    aspect_val = int(entry.get() or 0)
                except ValueError:
                    aspect_val = 0
                aspect_prof = aspect_prof_var.get()
                prof = prof_var.get()
                # Tool/Knowledge uses its own proficiency setting
                bonus = self.calculate_bonus(aspect_prof)
                if prof == "F" or prof == "E":
                    total = aspect_val + bonus
                elif prof == "-":
                    total = aspect_val + round(bonus/2 + 0.1) - 6
                else: # ½
                    total = aspect_val + bonus - 6
            else:
                total = 0
                print(f"DEBUG: Linked aspect '{linked_aspect}' not found for tool '{tool}'")
            
            val_lbl.configure(text=f"{total:+}")
        self.autosave_roll_configs()

    def gather_data(self):
        return {
            "name": self.name_entry.get(),
            "class": self.class_entry.get(),
            "race": self.race_entry.get(),
            "caster_level": self.caster_level_var.get(),
            "warlock_level": self.warlock_level_var.get(),
            "level": self.level_entry.get(),
            "stats": {k: v.get() for k, v in self.stat_entries.items()},
            "combat": {k: v.get() for k, v in self.combat_entries.items()},
            "aspects": {k: (e.get(), p.get(), a.get()) for k, (e, p, a, _) in self.aspect_widgets.items()},
            "knowledge": {k: (pv.get(), av.get()) for k, (pv, _, _, av) in self.knowledge_widgets.items()},
            "tools": {k: (pv.get(), av.get(), la) for k, (pv, _, la, av) in self.tool_widgets.items()},
            "saves": {k: (pv.get(), av.get(), self.save_entries[k].get() if k in self.save_entries else "0") 
                      for k, (pv, av, _) in self.save_widgets.items()},
            "weapons": [(n.get(), a.get(), p.get(), t.get(), ec.get(), ea.get(), d[0]) 
                        for _, (n, a, p, t, ec, ea, _, d, _) in self.weapon_widgets.items()],
            "armor": {
                "type": self.armor_settings["type"].get(),
                "aspect": self.armor_settings["aspect"].get(),
                "shield": self.armor_settings["shield"].get(),
                "prof": self.armor_settings["prof"].get(),
                "shield_prof": self.armor_settings["shield_prof"].get(),
                "extra_const": self.aa_extra_const.get(),
                "extra_adv": self.aa_extra_adv.get()
            },
            "exhaustion": self.exhaustion_var.get(),
            "shards": [
                (src.get(), st.get(), sht.get(), cur.get(), tot.get(), mo.get(), ar.get(), rt.get())
                for _, (src, st, sht, cur, tot, mo, ar, rt, _) in self.shard_widgets.items()
            ],
            "resonance_saturation": [e.get() for e in self.resonance_saturation_entries],
            "resonance_counts": [e.get() for e in self.resonance_count_entries],
            "pact_resonance_saturation": [e.get() for e in self.pact_saturation_entries],
            "pact_resonance_counts": [e.get() for e in self.pact_count_entries],
            "arcane_recovery_amount": self.arcane_recovery_entry.get(),
            "arcane_recovery_used": self.arcane_recovery_used_var.get(),
            "features": [
                (w[0].get(), w[1].get(), w[2].get(), w[3].get(), w[6][0], w[4].get())
                for _, w in self.feature_widgets.items()
            ],
            "spells": self.spells,
            "quick_prep_used": self.quick_prep_used.get(),
            "hit_dice": {d: [v[0].get(), v[1].get()] for d, v in self.hit_dice_vars.items()},
            "background": self.background_entry.get(),
            "languages": self.languages_entry.get(),
            "conditions": {c: v.get() for c, v in self.conditions_vars.items()},
            "pets": [
                (w[0].get(), w[1].get(), w[2].get(), w[3].get(), w[4].get(), w[5].get(), w[6][0])
                for _, w in self.pet_widgets.items()
            ]
        }

    def load_data(self, data):
        for attr in ["name_entry", "class_entry", "race_entry", "level_entry", "background_entry", "languages_entry"]:
            if not hasattr(self, attr): continue
            entry = getattr(self, attr)
            entry.delete(0, "end")
            entry.insert(0, data.get(attr.replace("_entry", ""), ""))
            
        self.caster_level_var.set(data.get("caster_level", "1"))
        self.warlock_level_var.set(data.get("warlock_level", "0"))
        
        for k, v in data.get("stats", {}).items():
            if k in self.stat_entries:
                self.stat_entries[k].delete(0, "end")
                self.stat_entries[k].insert(0, v)
        
        for k, v in data.get("combat", {}).items():
            if k in self.combat_entries:
                self.combat_entries[k].delete(0, "end")
                self.combat_entries[k].insert(0, v)
        
        for k, (val, prof, adv) in data.get("aspects", {}).items():
            # Migration: Stealth -> Mobility
            if k == "Stealth":
                k = "Mobility"
            
            if k in self.aspect_widgets:
                e, p, a, _ = self.aspect_widgets[k]
                e.delete(0, "end")
                e.insert(0, val)
                p.set(prof)
                a.set(adv)
                self.update_aspect_total(k)
        
        for k, v in data.get("knowledge", {}).items():
            if k in self.knowledge_widgets:
                prof_var, _, _, adv_var = self.knowledge_widgets[k]
                if isinstance(v, tuple):
                    prof_var.set(v[0])
                    adv_var.set(v[1])
                else:
                    prof_var.set(v)  # backwards compat with old saves
        self.update_knowledge_fields()
        
        for k, v in data.get("tools", {}).items():
            if isinstance(v, tuple) and len(v) == 3:
                prof, adv, linked_aspect = v
                self._add_tool_item(k, linked_aspect)
                if k in self.tool_widgets:
                    pv, _, _, av = self.tool_widgets[k]
                    pv.set(prof)
                    av.set(adv)
            elif isinstance(v, tuple): # compat
                prof, adv, linked_aspect = v[0], v[1], self._guess_linked_aspect(k) # Guess linked aspect for old format
                self._add_tool_item(k, linked_aspect)
                if k in self.tool_widgets:
                    pv, _, _, av = self.tool_widgets[k]
                    pv.set(prof)
                    av.set(adv)
        self.update_tool_fields()
        
        # Load Spells
        self.spells = data.get("spells", [])
        self.quick_prep_used.set(data.get("quick_prep_used", False))
        self._update_spell_list()

        for k, v in data.get("saves", {}).items():
            if k in self.save_widgets:
                pv, av, _ = self.save_widgets[k]
                if isinstance(v, (list, tuple)):
                    pv.set(v[0])
                    av.set(v[1])
                    if len(v) > 2 and k in self.save_entries:
                        self.save_entries[k].delete(0, "end")
                        self.save_entries[k].insert(0, v[2])
                self.update_save_total(k)

        # Load Weapons
        self.weapon_widgets.clear()
        for child in self.items_container.winfo_children():
            child.destroy()
        
        for weapon_data in data.get("weapons", []):
            if len(weapon_data) >= 6:
                self._add_weapon_row(*weapon_data[:7])
            elif len(weapon_data) == 3: # Compat
                self._add_weapon_row(weapon_data[0], weapon_data[1], weapon_data[2])
            
        # Load Armor
        armor_data = data.get("armor", {})
        if armor_data:
            self.armor_settings["type"].set(armor_data.get("type", "None"))
            self.armor_settings["aspect"].set(armor_data.get("aspect", "Resilience"))
            self.armor_settings["shield"].set(armor_data.get("shield", False))
            self.armor_settings["prof"].set(armor_data.get("prof", False))
            self.armor_settings["shield_prof"].set(armor_data.get("shield_prof", False))
            self.aa_extra_const.delete(0, "end"); self.aa_extra_const.insert(0, armor_data.get("extra_const", ""))
            val = armor_data.get("extra_adv", "")
            self.aa_extra_adv.set(val if val in ["-3", "-2", "-1", "", "1", "2", "3"] else "")
        
        # Load Exhaustion
        self.exhaustion_var.set(data.get("exhaustion", 0))
        
        # Load Shards
        self.shard_widgets.clear()
        for child in self.shards_container.winfo_children():
            child.destroy()
        for shard_data in data.get("shards", []):
            if isinstance(shard_data, (list, tuple)):
                if len(shard_data) >= 8:
                    # New format: (source, src_type, shard_type, current, total, max_out, arcane, rest)
                    self._add_shard_row(*shard_data[:8])
                elif len(shard_data) >= 7:
                    # Old format without current: (source, src_type, shard_type, total, max_out, arcane, rest)
                    src, st, sht, tot, mo, ar, rt = shard_data[:7]
                    self._add_shard_row(src, st, sht, tot, tot, mo, ar, rt)

        # Load Features
        self.feature_widgets.clear()
        for child in self.features_container.winfo_children():
            child.destroy()
        for feat_data in data.get("features", []):
            # Format: (name, cur, max, reset, desc, used)
            if len(feat_data) >= 5:
                # _add_feature_row extracts name, cur, max, reset, desc, used from tuple
                self._add_feature_row(*feat_data[:6])
        
        # Load Resonance
        for i, val in enumerate(data.get("resonance_saturation", [])):
            if i < 9:
                self.resonance_saturation_entries[i].delete(0, "end")
                self.resonance_saturation_entries[i].insert(0, val)
        for i, val in enumerate(data.get("resonance_counts", [])):
            if i < 9:
                self.resonance_count_entries[i].delete(0, "end")
                self.resonance_count_entries[i].insert(0, val)
                self._update_resonance_highlight(i)
        
        # Load Pact Resonance
        for i, val in enumerate(data.get("pact_resonance_saturation", [])):
            if i < 9:
                self.pact_saturation_entries[i].delete(0, "end")
                self.pact_saturation_entries[i].insert(0, val)
        for i, val in enumerate(data.get("pact_resonance_counts", [])):
            if i < 9:
                self.pact_count_entries[i].delete(0, "end")
                self.pact_count_entries[i].insert(0, val)
                self._update_res_h(i, self.pact_count_entries, self.pact_saturation_entries, self.pact_mult_labels)
        
        # Ensure Pact visibility
        self._update_pact_visibility()
        
        # Load Arcane Recovery
        self.arcane_recovery_entry.delete(0, "end")
        self.arcane_recovery_entry.insert(0, data.get("arcane_recovery_amount", "0"))
        self.arcane_recovery_used_var.set(data.get("arcane_recovery_used", False))

        # Load Hit Dice
        for die, vals in data.get("hit_dice", {}).items():
            if die in self.hit_dice_vars and len(vals) == 2:
                self.hit_dice_vars[die][0].set(vals[0])
                self.hit_dice_vars[die][1].set(vals[1])

        # Load Conditions
        cond_data = data.get("conditions", {})
        for c, v in cond_data.items():
            if c in self.conditions_vars:
                self.conditions_vars[c].set(v)
                
        # Load Pets
        self.pet_widgets.clear()
        for child in self.pets_container.winfo_children():
            child.destroy()
        for pet_data in data.get("pets", []):
            if len(pet_data) == 7:
                self._add_pet_row(*pet_data)

        # Trigger regeneration of roll configs to ensure metadata (like aspect) is up to date
        self.generate_roll_configs()
        self.update_aa()
        self.update_net_adv()
        self.update_weapon_bonuses()

    def generate_roll_configs(self):
        """Generate/Update roll config files for all modifiers (Stats, Combat, Aspects, Tools) as bloco objects"""
        if not self.roll_configs_dir:
            return

        def process_mod(name, val_source, adv_val=0, aspect=None):
            # Sanitize filename
            safe_name = re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()
            if not safe_name: return
            
            # Extract value
            try:
                if isinstance(val_source, str):
                    val_str = val_source
                else:
                    val_str = str(val_source)
                
                # Handle "X / Y" split values (take the first/Melee value for now)
                if "/" in val_str:
                    val_str = val_str.split("/")[0].strip()
                    
                value = int(val_str.replace("+", "")) # Handle "+5"
            except (ValueError, TypeError):
                value = 0
            
            # Advantage: per-skill + armor/shield/exhaustion penalties
            final_adv = int(adv_val)
            
            # Add armor non-proficiency penalty
            if self.armor_settings["type"].get() != "None" and not self.armor_settings["prof"].get():
                final_adv -= 1
            # Add shield non-proficiency penalty
            if self.armor_settings["shield"].get() and not self.armor_settings["shield_prof"].get():
                final_adv -= 1
            # Add exhaustion penalty
            try:
                exh = self.exhaustion_var.get()
                if exh > 0:
                    final_adv -= max(0, min(10, exh))
            except (ValueError, TclError):
                pass
            
            # --- Condition Penalties ---
            c_p = 0
            if "save" in name.lower():
                c_p = self.get_condition_modifiers('Save', aspect)
            elif name in self.aspect_widgets or name in self.knowledge_widgets or name in self.tool_widgets:
                c_p = self.get_condition_modifiers('Check', name)
            elif "AA" in name:
                c_p = self.get_condition_modifiers('AA')
            else: # Usually weapons/features
                c_p = self.get_condition_modifiers('Attack')
            
            final_adv += c_p

            filepath = os.path.join(self.roll_configs_dir, f"{safe_name}.pkl")
            
            # Default: anterior type config with current value
            # Added AnteriorItem('c', value) to fix "no anterior mods" bug
            items = [AnteriorItem('c', value)]
            if final_adv != 0:
                items.append(AnteriorItem('adv', final_adv))
                
            pm = premod(adv=final_adv, const=value, items=items)
            config = bloco(premods=pm, posmods=[], sn=0, crit=0.2, mini=0)
            config.aspect = aspect
            
            # Preserve existing type/settings if possible
            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        old_config = pickle.load(f)
                    
                    # If it's a bloco object, we update the value and advantage but keep other settings
                    if hasattr(old_config, 'premods'):
                        old_config.premods.const = value
                        old_config.premods.adv = final_adv # Update advantage
                        old_config.aspect = aspect # Update aspect
                        
                        # Update Constant Item
                        c_item = next((x for x in old_config.premods.items if isinstance(x, AnteriorItem) and x.typ == 'c'), None)
                        if c_item:
                            c_item.val1 = value
                        else:
                            old_config.premods.items.insert(0, AnteriorItem('c', value))
                            
                        # Update Advantage Item
                        adv_item = next((x for x in old_config.premods.items if isinstance(x, AnteriorItem) and x.typ == 'adv'), None)
                        if final_adv != 0:
                            if adv_item:
                                adv_item.val1 = final_adv
                            else:
                                old_config.premods.items.append(AnteriorItem('adv', final_adv))
                        elif adv_item:
                            # Remove advantage item if it's now 0
                            old_config.premods.items.remove(adv_item)
                            
                        config = old_config
                except Exception:
                    pass
            
            # Save as pickled object
            try:
                with open(filepath, "wb") as f:
                    pickle.dump(config, f)
            except Exception as e:
                print(f"Error saving roll config for {name}: {e}")

        # List of uppercase stats to remove from directory
        stat_blocklist = ["Mind", "Soul", "Senses", "Body"]
        combat_blocklist = ["PCN", "Vit", "AA", "Prof", "Spd"]
        old_weapon_blocklist = ["Spell attack.pkl", "Spell AS.pkl", "Spell attack", "Spell AS"]
        offensive_attacks = ["Precision attack.pkl", "Concentration attack.pkl", "Meditation attack.pkl", "Potency attack.pkl"]
        
        # Cleanup old uppercase/combat files
        for b in stat_blocklist + combat_blocklist + old_weapon_blocklist + offensive_attacks:
            fp = os.path.join(self.roll_configs_dir, f"{b}.pkl")
            if os.path.exists(fp):
                try: os.remove(fp)
                except: pass
            # Also try without extension for the manual check if logic changed
            fp_no_ext = os.path.join(self.roll_configs_dir, f"{b}")
            if os.path.exists(fp_no_ext):
                try: os.remove(fp_no_ext)
                except: pass

        # 1. New Section: Saves
        for name, (pv, av, tl) in self.save_widgets.items():
            process_mod(f"{name} save", tl.cget("text"), av.get(), aspect=name)

        # 2. Aspects (Skills) only - no offensive specific attacks logic
        for name, (entry, _, adv_var, total_lbl) in self.aspect_widgets.items():
            process_mod(name, total_lbl.cget("text"), adv_var.get(), aspect=name)

        # 3. Knowledge Fields
        for name, (pv, tl, la, av) in self.knowledge_widgets.items():
            process_mod(name, tl.cget("text"), av.get(), aspect=la)

        # 4. Tools
        for name, (pv, tl, la, av) in self.tool_widgets.items():
            process_mod(name, tl.cget("text"), av.get(), aspect=la)

        # 5. Equipment (Weapons, Spells, Features)
        # 5. Equipment (Weapons, Spells, Features)
        for wid, widgets in self.weapon_widgets.items():
            try:
                # Robust unpacking to handle potential legacy/mixed widgets
                if len(widgets) == 8:
                    name_ent, asp_var, p_var, type_var, const_ent, adv_ent, bonus_lbl, _ = widgets
                    extra_const_val = 0 # Handled by bonus_lbl text
                elif len(widgets) == 6: # Legacy widget fallback
                    name_ent, asp_var, p_var, atk_lbl, as_lbl, _ = widgets
                    # Defaults for legacy
                    type_var, const_ent, adv_ent = None, None, None
                    bonus_lbl = atk_lbl # Default to Atk label
                else:
                    print(f"Skipping weapon {wid}: unexpected widget count {len(widgets)}")
                    continue

                name = name_ent.get().strip()
                if name:
                    # Use the calculated label value for const (includes aspect + prof + extra)
                    val_text = bonus_lbl.cget("text") # "Atk: +X" or "AS: +X"
                    # Extract number
                    try:
                        if ":" in val_text:
                            val = int(val_text.split(":")[1].strip().replace("+", ""))
                        else:
                            val = int(val_text.replace("+", ""))
                    except:
                        val = 0
                    
                    # Get extra advantage
                    try:
                         if adv_ent:
                            extra_adv = int(adv_ent.get() or 0)
                            final_atk_adv = extra_adv # Plus penalties if needed? Usually weapon adv is pure
                         else:
                            final_atk_adv = 0
                    except:
                        final_atk_adv = 0
                    
                    # Also include general penalties for weapon attacks? 
                    # Usually weapons are already calculated, but adv might be separate
                    try:
                        process_mod(name, val, final_atk_adv, aspect=asp_var.get())
                    except Exception as e:
                        print(f"DEBUG: Error processing weapon {name}: {e}")
            except Exception as e:
                print(f"Error generating config for weapon {wid}: {e}")
        
        print(f"DEBUG: generate_roll_configs completed. Generated {len(os.listdir(self.roll_configs_dir))} files.")

        # 6. Armor AA Roll
        if "AA" in self.combat_entries:
            val_str = self.combat_entries["AA"].get() 
            try:
                base_aa = int(val_str)
            except:
                base_aa = 0
                
            try:
                extra_const = int(self.aa_extra_const.get() or 0)
            except:
                extra_const = 0
                
            try:
                extra_adv = int(self.aa_extra_adv.get() or 0)
            except:
                extra_adv = 0
                
            total_aa = base_aa + extra_const
            
            # Ensure safe filename for AA
            aspect = self.armor_settings["aspect"].get()
            process_mod(f"{aspect} AA", total_aa, extra_adv)


    def save_character(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Character File", "*.pkl")])
        if filepath:
            self._loaded_filepath = filepath
            with open(filepath, "wb") as f:
                pickle.dump(self.gather_data(), f)
            
            # Update roll_configs_dir based on save name
            basename = os.path.basename(filepath)
            name_no_ext = os.path.splitext(basename)[0]
            
            # Strict path: ClientRPG/Roll configs/<name>
            roll_configs_root = os.path.join(BASE_DIR, "Roll configs")
            if not os.path.exists(roll_configs_root):
                try: os.makedirs(roll_configs_root)
                except: pass
            
            self.roll_configs_dir = os.path.join(roll_configs_root, name_no_ext)
            if not os.path.exists(self.roll_configs_dir):
                try: os.makedirs(self.roll_configs_dir)
                except: pass
                
            # Sync Main GUI silently
            if hasattr(self.parent, 'roll_configs_dir'):
                self.parent.roll_configs_dir = self.roll_configs_dir
                if hasattr(self.parent, 'populate_roll_list'):
                    self.parent.populate_roll_list()
                if hasattr(self.parent, 'menubar'):
                    try:
                        self.parent.menubar.delete(0, "end")
                        self.parent.openmenu.delete(0, "end")
                        self.parent.build_menu()
                    except: pass
            
            self.generate_roll_configs()
            self.lift()
            self.focus_force()

    def load_character(self):
        filepath = filedialog.askopenfilename(filetypes=[("Character File", "*.pkl")])
        if filepath:
            try:
                with open(filepath, "rb") as f:
                    data = pickle.load(f)
                if not isinstance(data, dict):
                    messagebox.showerror("Error", "Invalid file format.\nThis appears to be a Roll Config or other file.\nPlease select a Character Sheet file.")
                    return
                self.load_data(data)
                self._loaded_filepath = filepath
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load character:\n{e}")
                return
            
            # Silent update after load
            basename = os.path.basename(filepath)
            name_no_ext = os.path.splitext(basename)[0]
            
            roll_configs_root = os.path.join(BASE_DIR, "Roll configs")
            self.roll_configs_dir = os.path.join(roll_configs_root, name_no_ext)
            
            if not os.path.exists(roll_configs_root):
                try: os.makedirs(roll_configs_root)
                except: pass
            if not os.path.exists(self.roll_configs_dir):
                try: os.makedirs(self.roll_configs_dir)
                except: pass
                
            # Sync with main GUI silently
            if hasattr(self.parent, 'roll_configs_dir'):
                self.parent.roll_configs_dir = self.roll_configs_dir
                if hasattr(self.parent, 'populate_roll_list'):
                    self.parent.populate_roll_list()
                # Rebuild File menu to show new configs
                if hasattr(self.parent, 'menubar'):
                    try:
                        self.parent.menubar.delete(0, "end")
                        self.parent.openmenu.delete(0, "end")
                        self.parent.build_menu()
                    except Exception:
                        pass
            
            self.generate_roll_configs()
            # Focus back on the sheet window
            self.lift()
            self.focus_force()

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
                self.anterior_items = []
                self.players = []
                
                # chat window which is currently hidden
                self.configure(fg_color="gray15")
                self.withdraw()

                self.roll_configs_dir = None
                self.user_past_configs_dir = None
                self.protocol("WM_DELETE_WINDOW", self.on_closing)
                
                # login window 
                self.login = ctk.CTkToplevel(fg_color="gray15") 
                # set the title 
                self.login.title("Login") 
                self.center_window(self.login, 400, 125)
                self.login.grid_columnconfigure(0, weight=1)
                self.login.grid_rowconfigure(1, weight=1) # ONLY center row expands
                self.login.grid_rowconfigure((0, 2), weight=0) # Keep bars at edges
                self.login.resizable(width = False, height = False)
                self.login.protocol("WM_DELETE_WINDOW", self.on_closing)  

                # create a Label
                self.plsFrame=ctk.CTkFrame(self.login, fg_color="gray20")
                self.plsFrame.grid_columnconfigure(0, weight=1)
                self.plsFrame.grid(row=0, column=0, padx=self.rescale, pady=(self.rescale, 0), sticky="ew")
                
                self.pls = ctk.CTkLabel(self.plsFrame, text = "Please login to continue", font=("Roboto", 13)) 
                self.pls.grid(row=0, column=0, padx=2, pady=1)
                
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
                

        def center_window(self, window, width=None, height=None):
                """Center a window on the screen using its natural spawn as a reference."""
                if width and height:
                    window.geometry(f"{width}x{height}")
                
                window.update()
                
                # Get scaling factor (crucial for modern Windows high-DPI)
                scaling = window._get_window_scaling()

                # If width/height were not provided, get them from the rendered window
                # winfo_width/height returns physical pixels, so we convert to logical
                if width is None: width = window.winfo_width() / scaling
                if height is None: height = window.winfo_height() / scaling
                
                # Get dimensions of the virtual root (current monitor/desktop area)
                # These are usually in physical pixels, so we divide by scaling
                v_width = window.winfo_vrootwidth() / scaling
                v_height = window.winfo_vrootheight() / scaling
                v_x = window.winfo_vrootx() / scaling
                v_y = window.winfo_vrooty() / scaling

                # Fallback if vroot is not reporting properly (sometimes returns 0 or 1)
                if v_width <= 1:
                    v_width = window.winfo_screenwidth() / scaling
                    v_height = window.winfo_screenheight() / scaling
                    v_x = 0
                    v_y = 0

                # Formula: offset + (total_area - window_size) // 2
                x = int(v_x + (v_width - width) / 2)
                y = int(v_y + (v_height - height) / 2) - 20 # Slight upward bias for taskbar
                
                print(f"DEBUG Centering: {window.title()} | scaling={scaling:.2f} | vroot: {v_width}x{v_height}+{v_x}+{v_y} | target: {width}x{height} | final: +{x}+{y}")
                window.geometry(f"+{x}+{y}")

        def goAhead3(self, name):
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
            self.my_name = name
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

                # Setup user-specific past configs folder
                self.user_past_configs_dir = os.path.join(PAST_CONFIGS_DIR, name)
                os.makedirs(self.user_past_configs_dir, exist_ok=True)
                for filename in os.listdir(self.user_past_configs_dir):
                    os.remove(os.path.join(self.user_past_configs_dir, filename))

                self.goAhead3(name)
            else:
                self.pls.configure(text=server_message)

        def onPlayerClick(self, c):
            try:
                if self.players[c]['selected']:
                    self.playerBtts[c].configure(fg_color="gray25")
                else:
                    self.playerBtts[c].configure(fg_color="gray35")
                self.players[c]['selected'] = not self.players[c]['selected']
            except IndexError:
                pass

        def onPlayerSelec(self, c):
            try:
                player_name = self.players[c]['name']
                player_color = self.players[c]['color']
                self.roll_list.append(player_name)  # Add player to roll list
                tempLabel = ctk.CTkButton(self.label,
                                                        fg_color="gray25",
                                                        hover=False,
                                                        border_color=player_color,
                                                        border_width=2,
                                                        text = player_name,
                                                        font=("Roboto", 12))
                self.playerSelected.append(tempLabel)
                self.playerSelected[-1].grid(row=len(self.playerSelected)-1, column=0, pady=(0,self.rescale), sticky="ew")
            except IndexError:
                pass

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
                

        def displayres(self, p, crit, r, resultStr, send_type, resources, caller_name=None, is_hidden=False):
            try:
                # Thread-safe window closing
                def close_windows():
                    try:
                        if hasattr(self, 'wheelwindow') and self.wheelwindow.winfo_exists():
                            self.wheelwindow.withdraw()
                        if hasattr(self, 'possi') and self.possi.winfo_exists():
                            self.possi.withdraw()
                    except (TclError, Exception):
                        pass
                self.after(0, close_windows)
                    
                destiny=[]
                
                # Limits message construction
                limits_msg = r"\n Limits: \gCF: "+str(round(p/2))+r"; \gS: "+str(p)+r"; \gCS: "+str(crit)+r"; \gRolled: "+str(int(r))
                
                if is_hidden or send_type == 'hidden':
                    # Mystery Mode or Hidden Roll: No limits, no rolled value.
                    prefix = "Hidden roll result: " if send_type == 'hidden' else "Roll result: "
                    message = prefix+resultStr+r". \n"+resources
                else:
                    message = r"Roll result: "+resultStr+r". \n"+resources + limits_msg
                
                # Signal hidden resources to the user who used them
                if is_hidden and not send_type == 'hidden':
                    message += r"\n (Some resources were hidden from your opponent)"

                # Send result message to server for broadcast
                # If it's a synchronized roll (caller_name set), server handles the broadcast
                # If it's a solo roll or button click, broadcast normally
                should_broadcast = caller_name is None  # Only broadcast for non-two-player rolls
                
                if should_broadcast:
                    message_sent = pickle.dumps(msg(destiny, message))
                    message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                    client.send(message_sent_header+message_sent)
                
                # Animation Handling
                # Disable animations if hidden resources are used
                if is_hidden or send_type == 'hidden':
                    return

                info_limits = f"Limits:\nCF: <{p/2:.1f}; F: <{p:.1f}; S: <{crit:.1f}; CS: >={crit:.1f}"
                info_header_initial = info_limits + "\n "
                
                if self.displaymode.get() == 'bar':
                    def setup_bar_gui():
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
                        self.CSMarker.place(relx=crit_norm + 0.0025, rely=0.5, anchor="center")
                        
                        # Place threshold labels
                        self.CFThreshLabel.place(relx=cf_norm, anchor="n")
                        self.SuccessThreshLabel.place(relx=p_norm, anchor="n")
                        self.CritThreshLabel.place(relx=crit_norm, anchor="n")

                        if not self.progresswindow.winfo_viewable():
                            self.progresswindow.update()
                            self.progresswindow.deiconify()
                        self.progresswindow.focus()
                    
                    self.after(0, setup_bar_gui)
                    
                    p_norm = p/20
                    crit_norm = crit/20
                    cf_norm = p_norm / 2
                    x=0
                    n=random.randint(2, 15)
                    r_bar = r/20
                    
                    for i in range(100):
                        sleep(0.02)
                        x+=0.01
                        y=r_bar*n*x/(1+(n-1)*x)
                        
                        def update_bar(y=y):
                            if y < cf_norm:
                                self.progress.configure(progress_color="#4d4d4d")
                            elif y < p_norm:
                                self.progress.configure(progress_color="#595959")
                            elif y < crit_norm:
                                self.progress.configure(progress_color="#666666")
                            else:
                                self.progress.configure(progress_color="#737373")
                            self.progress.set(value=y)
                        self.after(0, update_bar)
                    
                    def finalize_bar():
                        self.progress.configure(progress_color=self.color)
                        self.progress.set(value=r_bar)
                        self.ResultLabel2.configure(text = resultStr)
                        self.InfoLabel2.configure(text = info_limits + f"\nRolled: {r:.1f}")
                    self.after(0, finalize_bar)

                elif self.displaymode.get() == 'dice':
                    def setup_dice_gui():
                        self.InfoLabel.configure(text = info_header_initial)
                        self.ResultLabel.configure(text = "")

                        if not self.dicewindow.winfo_viewable():
                            self.dicewindow.update()
                            self.dicewindow.deiconify()
                        self.dicewindow.focus()
                        
                        self.panel.configure(fg_color="gray70")
                        self.ResultFrame.configure(fg_color="gray20")
                        self.ResultLabel.configure(fg_color="gray20")
                    self.after(0, setup_dice_gui)

                    sleepTime = random.randint(self.minST,self.maxST)/100
                    maxSleepTime = random.randint(self.minMST,self.maxMST)/100
                    
                    currentRoll = random.randint(0, 20)
                    while maxSleepTime-sleepTime > 0.1 and maxSleepTime > sleepTime:
                        rolagem = random.randint(0, 20)
                        while rolagem == currentRoll:
                            rolagem = random.randint(0, 20)
                        currentRoll = rolagem
                        
                        self.after(0, lambda r=rolagem: self.panel.configure(image = self.dice_images_cache[str(r)+".png"]))
                        
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

                    def finalize_dice(img=img_name):
                        self.panel.configure(image = self.dice_images_cache[img], fg_color=self.color)
                        self.ResultFrame.configure(fg_color="gray20")
                        self.ResultLabel.configure(fg_color="gray20")
                        self.ResultLabel.configure(text = resultStr)
                        self.InfoLabel.configure(text = info_limits + f"\nRolled: {r:.1f}")
                    self.after(0, finalize_dice)
                elif self.displaymode.get() == 'wheel':
                    def setup_wheel_gui():
                        self.InfoLabel3.configure(text = info_header_initial)
                        self.ResultLabel3.configure(text = "")

                        if not self.wheelwindow.winfo_viewable():
                            self.wheelwindow.update()
                            self.wheelwindow.deiconify()
                        self.wheelwindow.focus()
                    self.after(0, setup_wheel_gui)

                    # Sizes calculation (from previous code)
                    sizes = [p/2, p/2, crit-p, 20-crit]
                    # Map to result index
                    if r < p/2: result_index = 0
                    elif r < p: result_index = 1
                    elif r < crit: result_index = 2
                    else: result_index = 3
                    
                    labels = ["CF", "F", "S", "CS"]
                    base_colors = ["#4d4d4d", "#595959", "#666666", "#737373"]
                    
                    self.wheel_sizes = sizes
                    self.wheel_labels = labels
                    self.wheel_base_colors = base_colors
                    self.wheel_result_index = result_index
                    self.wheel_resultStr = resultStr
                    self.wheel_p = p
                    self.wheel_crit = crit
                    self.wheel_r = r
                    self.wheel_info_limits = info_limits
                    
                    cumulative = 0
                    for i in range(result_index):
                        cumulative += sizes[i]
                    
                    if result_index == 0: rel_pos = (r - 0) / (p / 2)
                    elif result_index == 1: rel_pos = (r - p/2) / (p/2)
                    elif result_index == 2: rel_pos = (r - p) / (crit - p)
                    else: rel_pos = (r - crit) / (20 - crit)
                    
                    target_angle = cumulative + rel_pos * sizes[result_index]
                    full_rotations = random.randint(3, 5)
                    self.wheel_total_rotation = full_rotations * 360 - target_angle * 18
                    self.wheel_current_rotation = 0
                    self.wheel_animation_step = 0
                    self.wheel_total_steps = 60
                    
                    self.after(0, self.animate_wheel)
                elif self.displaymode.get() == 'none':
                    pass
            except Exception:
                print(traceback.format_exc())

        def nextSleepTime(self, currentTime, limitTime): # 3 opcoes de incremento de tempo
            # return currentTime + currentTime**2 / 2
            # return currentTime + incrementFraction*currentTime
            return currentTime+limitTime*(1-exp(-currentTime*self.incrementFraction))

        def animate_wheel(self):
            try:
                # Ensure window exists and is visible before drawing
                if not self.wheelwindow.winfo_exists() or not self.wheelwindow.winfo_viewable():
                    return
                
                # Update idle tasks to ensure state is consistent
                try:
                    self.wheelwindow.update_idletasks()
                except:
                    pass

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
            except (TclError, Exception):
                # Silence GUI errors during teardown
                pass

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
            if self.user_past_configs_dir and os.path.exists(self.user_past_configs_dir):
                shutil.rmtree(self.user_past_configs_dir, ignore_errors=True)
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

        def sheetswitch(self):
            if not self.SheetWindow.winfo_viewable():
                self.SheetWindow.deiconify()
                self.sheetbtt.configure(text='►')
            else:
                self.SheetWindow.withdraw()
                self.sheetbtt.configure(text='◄')

        ##-----------------------------------------------
        def build_menu(self):
            self.menubar.add_cascade(label="File", menu=self.openmenu)
            self.openmenu.add_command(label="Open new...", command=lambda: self.openfile(0))
            self.openmenu.add_command(label="Save", command=self.savefile)
            self.openmenu.add_command(label="Save as..", command=self.savefileas)
            
            # Roll Configs dropdown
            rc_dir = getattr(self, 'roll_configs_dir', None)
            if rc_dir and os.path.isdir(rc_dir):
                self.openmenu.add_separator()
                
                # Main Categories
                saves_menu = Menu(self.openmenu, tearoff=0)
                aspects_menu = Menu(self.openmenu, tearoff=0)
                knowledge_menu = Menu(self.openmenu, tearoff=0)
                tools_menu = Menu(self.openmenu, tearoff=0)
                equip_menu = Menu(self.openmenu, tearoff=0)
                custom_menu = Menu(self.openmenu, tearoff=0)
                
                self.openmenu.add_cascade(label="Saves and AA", menu=saves_menu)
                self.openmenu.add_cascade(label="Aspects", menu=aspects_menu)
                self.openmenu.add_cascade(label="Knowledge Fields", menu=knowledge_menu)
                self.openmenu.add_cascade(label="Tools", menu=tools_menu)
                self.openmenu.add_cascade(label="Equipment / Spells / Features", menu=equip_menu)
                self.openmenu.add_cascade(label="Custom", menu=custom_menu)

                # Nested Aspect Submenus (Stats) - Use UPPERCASE for labels to match UI
                stat_menus = {
                    "Mind": Menu(aspects_menu, tearoff=0),
                    "Soul": Menu(aspects_menu, tearoff=0),
                    "Senses": Menu(aspects_menu, tearoff=0),
                    "Body": Menu(aspects_menu, tearoff=0)
                }
                for stat, m in stat_menus.items():
                    aspects_menu.add_cascade(label=stat, menu=m)

                # Track Aspect Submenus for other categories
                knowledge_aspect_menus = {}
                tools_aspect_menus = {}
                equip_aspect_menus = {}

                # Mappings (Lowercase keys for robust matching)
                aspects_by_stat = {
                    "Mind": [a.lower() for a in ["Concentration", "Investigation", "Convincing", "Simulation"]],
                    "Soul": [a.lower() for a in ["Meditation", "Awareness", "Performance", "Trustworthiness"]],
                    "Senses": [a.lower() for a in ["Precision", "Mobility", "Acrobatics", "Dexterity"]],
                    "Body": [a.lower() for a in ["Potency", "Resilience", "Athletics", "Constitution"]]
                }
                save_names = [s.lower() for s in ["Body save", "Mind save", "Soul save", "Senses save"]]
                equip_keywords = ["spell", "attack", "as", "dagger", "sword", "bow", "switchblade", "crossbow", "hammer", "axe", "whip"]

                try:
                    files = sorted([f for f in os.listdir(rc_dir) if f.endswith(".pkl")])
                    for filename in files:
                        name_orig = os.path.splitext(filename)[0]
                        name = name_orig.lower()
                        filepath = os.path.join(rc_dir, filename)
                        cmd = lambda f=filepath: self.openfile(f)
                        
                        # Load config to check for aspect metadata
                        config_aspect = None
                        try:
                            with open(filepath, "rb") as f:
                                cfg = pickle.load(f)
                                config_aspect = getattr(cfg, 'aspect', None)
                        except: pass

                        # 1. Saves and AA
                        if name in save_names or "aa" in name:
                            saves_menu.add_command(label=name_orig, command=cmd)
                            continue

                        # 2. Aspects
                        placed = False
                        for stat, asp_list in aspects_by_stat.items():
                            if name in asp_list:
                                stat_menus[stat].add_command(label=name_orig, command=cmd)
                                placed = True
                                break
                        if placed: continue

                        # 3. Categorize by metadata or name matching
                        target_menu = None
                        aspect_tracking_dict = None
                        
                        # Use CharacterSheetWindow for lookup (case-insensitive keys)
                        known_fields_lower = {k.lower(): v for k, v in CharacterSheetWindow.KNOWLEDGE_ASPECTS.items()}
                        
                        if name in known_fields_lower:
                            target_menu = knowledge_menu
                            aspect_tracking_dict = knowledge_aspect_menus
                            if not config_aspect: config_aspect = known_fields_lower[name]
                        elif any(k.lower() in name for k in CharacterSheetWindow.TOOL_SET_OPTIONS + CharacterSheetWindow.INSTRUMENT_OPTIONS + CharacterSheetWindow.GAMING_SET_OPTIONS) or "tools" in name:
                            target_menu = tools_menu
                            aspect_tracking_dict = tools_aspect_menus
                            if not config_aspect: config_aspect = self.SheetWindow._guess_linked_aspect(name_orig)
                        elif config_aspect: # Metadata exists but not a known Knowledge/Tool
                            target_menu = equip_menu
                            aspect_tracking_dict = equip_aspect_menus
                        elif any(k in name for k in equip_keywords):
                            target_menu = equip_menu
                            aspect_tracking_dict = equip_aspect_menus
                        
                        if target_menu is not None:
                            asp_name = config_aspect if config_aspect else "Other"
                            if asp_name not in aspect_tracking_dict:
                                aspect_tracking_dict[asp_name] = Menu(target_menu, tearoff=0)
                                target_menu.add_cascade(label=asp_name, menu=aspect_tracking_dict[asp_name])
                            aspect_tracking_dict[asp_name].add_command(label=name_orig, command=cmd)
                        else:
                            custom_menu.add_command(label=name_orig, command=cmd)
                except Exception as e:
                    print(f"DEBUG: Error building roll menu: {e}")
                
        def modify(self, a, b, c):
            self.modified=1           

        def build_resor(self):
            # Only create aFrame if there are anterior items
            if self.anterior_items:
                self.aFrame=ctk.CTkFrame(self.terFrame, fg_color="gray25")
                self.aFrame.columnconfigure((0,1), weight=1, uniform="anterior")
                self.aFrame.grid(row=0, column=0, sticky="ew", pady=(0,self.rescale))

                self.anteriorLabel=ctk.CTkLabel(self.aFrame, text="Anterior", fg_color="gray30", corner_radius=6, font=("Roboto", 14))
                self.anteriorLabel.grid(row=0, column=0, sticky="ew", padx=self.rescale, pady=self.rescale, columnspan=2)

                # List Anterior Items
                self.ante_buttons = []
                for i, item in enumerate(self.anterior_items):
                    text_label = ""
                    if item.typ == 'c':
                        text_label = f"Const: {item.val1:+}"
                    elif item.typ == 'adv':
                        text_label = f"Adv: {'+' if item.val1 > 0 else ''}{item.val1}"
                    elif item.typ == 'dice':
                        text_label = f"Dice: {item.val1}d{item.val2}"
                    
                    if item.hidden:
                        text_label += " (H)"
                    
                    btn = ctk.CTkButton(self.aFrame, 
                                        text=text_label, 
                                        border_color=self.color,
                                        border_width=2,
                                        fg_color="gray30", hover_color="gray40", 
                                        font=("Roboto", 11), 
                                        command=lambda idx=i: self.destroy_ante(idx))
                    btn.grid(row=1+i, column=0, columnspan=2, sticky="ew", padx=self.rescale, pady=(0, self.rescale))
                    btn.bind("<Button-3>", lambda event, idx=i: self.toggle_hidden_ante(idx))
                    self.ante_buttons.append(btn)
                
                start_row = 1
            else:
                start_row = 0


            for i in range(len(self.resor)):
                aux=("Resource #"+str(i+1))*(self.resor[i].resName.replace(" ", "")=="")+self.resor[i].resName*(self.resor[i].resName.replace(" ", "")!="")
                self.resor[i].mainFrame=ctk.CTkFrame(self.terFrame, fg_color="gray25")
                self.resor[i].mainFrame.columnconfigure((0,1) , weight=1)
                self.resor[i].mainFrame.grid(row=start_row+i, column=0, sticky="ew", pady=(0,self.rescale))
                
                hidden_mark = " (H)" if self.resor[i].hidden else ""

                self.resor[i].mainButton=ctk.CTkRadioButton(self.resor[i].mainFrame, 
                                                                        variable = self.selectRes, 
                                                                        value = i+1,
                                                                        text = aux + hidden_mark, fg_color=self.color, bg_color="gray25", border_color="gray30", hover_color=self.color, font=("Roboto", 12))
                self.resor[i].mainButton.grid(row=0, column=0, sticky="w", padx=self.rescale, pady=self.rescale)
                self.resor[i].mainButton.bind("<Button-3>", lambda event, idx=i: self.toggle_hidden_res(idx))

                self.resor[i].qntLabel=ctk.CTkLabel(self.resor[i].mainFrame, text=self.resor[i].qnt, fg_color="gray30", corner_radius=6, font=("Roboto", 12))
                self.resor[i].qntLabel.grid(row=0, column=1, sticky="e", padx=(0,self.rescale), pady=self.rescale)
    
                self.resor[i].subButtons=[]
                for j in range(len(self.resor[i].listSubres)):
                    text = self.resor[i].listSubres[j].subresName
                    if self.resor[i].hidden and " (H)" not in text:
                         text += " (H)"
                    elif getattr(self.resor[i].listSubres[j], 'hidden', False) and " (H)" not in text:
                         text += " (H)"

                    self.resor[i].subButtons.append(ctk.CTkButton(self.resor[i].mainFrame, 
                                                                    text = text, 
                                                                    fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                                    font=("Roboto", 12),
                                                                    command = lambda c=(i, j): self.destroy_subres(c)))
                    self.resor[i].subButtons[-1].grid(row=j+1, column=0, padx=self.rescale, pady=(0,self.rescale), columnspan=2, sticky="ew")
                    self.resor[i].subButtons[-1].bind("<Button-3>", lambda event, idx=(i, j): self.toggle_hidden_subres(idx))

                self.resor[i].delButton=ctk.CTkButton(self.resor[i].mainFrame, 
                                                                    text = "Delete resource", 
                                                                    fg_color=self.color, hover_color="gray35", font=("Roboto", 14), command = lambda idx=i: self.destroy_res(idx), border_width=2)
                self.resor[i].delButton.grid(row=len(self.resor[i].listSubres)+1, column=0, padx=self.rescale, pady=self.rescale, columnspan=2, sticky="ew")

        def destroy_all(self):
            """Safely destroy resources and anterior frames without individual widget destruction
               which causes race conditions and TclErrors in CustomTkinter."""
            try:
                if hasattr(self, 'Window2') and self.Window2.winfo_exists():
                    self.Window2.update_idletasks()
            except:
                pass

            # Destroy anterior items frame
            if hasattr(self, 'aFrame') and self.aFrame.winfo_exists():
                try:
                    self.aFrame.destroy()
                except (TclError, Exception):
                    pass
            
            # Destroy all resource frames
            if hasattr(self, 'resor'):
                for r in self.resor:
                    if hasattr(r, 'mainFrame') and r.mainFrame.winfo_exists():
                        try:
                            # Destroying parent Frame is sufficient and safer
                            r.mainFrame.destroy()
                        except (TclError, Exception):
                            pass

        def destroy_subres(self, pos):
            self.resor[pos[0]].listSubres.pop(pos[1])
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

        def load_local_roll(self, filepath):
            """Load a local roll config into the roll window fields"""
            try:
                with open(filepath, "rb") as f:
                    config = pickle.load(f)
                
                # Reset fields (clears inputs)
                self.ac.set(0); self.aa.set(0); self.ad[0].set(0); self.ad[1].set(0)
                self.ic.set(0); self.ia.set(0); self.id[0].set(0); self.id[1].set(0)
                self.pc.set(0); self.pa.set(0); self.pd[0].set(0); self.pd[1].set(0)
                
                # Clear existing resources
                self.resor = []
                self.destroy_all() # Clears UI list
                
                # Load Anterior Inputs
                if hasattr(config, 'premods') and config.premods:
                    self.ac.set(config.premods.const)
                    self.aa.set(config.premods.adv)
                    # Load dice if present
                    dice_item = next((x for x in config.premods.items if x.typ == 'dice'), None)
                    if dice_item:
                        self.ad[0].set(dice_item.val1)
                        self.ad[1].set(dice_item.val2)

                    # Add Main Resource
                    config_name = os.path.basename(filepath).replace(".pkl", "")
                    main_res = resource(1, config_name)
                    
                    # Convert AnteriorItems to posmod (sub-resources)
                    # Note: posmod architecture is: typ, timing(name), num1, num2
                    for item in config.premods.items:
                        p_mod = None
                        if item.typ == 'c':
                            # Use "Base" or "Const" as name
                            p_mod = posmod('const', 'Base', item.val1, 0, hidden=item.hidden)
                        elif item.typ == 'adv':
                            p_mod = posmod('adv', 'Base', item.val1, 0, hidden=item.hidden)
                        elif item.typ == 'dice':
                            p_mod = posmod('dice', 'Base', item.val1, item.val2, hidden=item.hidden)
                        
                        if p_mod:
                            main_res.listSubres.append(p_mod)
                            
                    self.resor.append(main_res)
                    
                self.destroy_all()
                self.build_resor()
                self.modified=1 
                self.hiddenAnte.set(False)
                self.hiddenRes.set(False)
                self.hiddenInter.set(False)
                self.hiddenPost.set(False)
                
            except Exception as e:
                print(f"Error loading local roll: {e}")
                print(traceback.format_exc())

        def destroy_res(self, index):
            self.destroy_all()
            self.resor.pop(index)
            self.build_resor()
            self.selectRes.set(0)
            self.modified=1

        def destroy_ante(self, index):
            self.anterior_items.pop(index)
            self.destroy_all()
            self.build_resor()
            self.modified=1

        def toggle_hidden_ante(self, index):
            self.anterior_items[index].hidden = not self.anterior_items[index].hidden
            self.destroy_all()
            self.build_resor()
            self.modified=1

        def toggle_hidden_res(self, index):
            self.resor[index].hidden = not self.resor[index].hidden
            self.destroy_all()
            self.build_resor()
            self.modified=1

        def toggle_hidden_subres(self, pos):
            i, j = pos
            self.resor[i].listSubres[j].hidden = not self.resor[i].listSubres[j].hidden
            self.destroy_all()
            self.build_resor()
            self.modified=1

        def resourcepaste(self, num, name):
            if int(num):
                self.destroy_all()
                self.resor.append(resource(num, name, hidden=False))
                self.build_resor()
                self.selectRes.set(len(self.resor))
                self.modified=1
            
        def anteadvpaste(self, num):
            try:
                if num:
                    self.anterior_items.append(AnteriorItem('adv', num, hidden=False))
                    self.destroy_all()
                    self.build_resor()                
                    self.modified=1
            except:
                pass
        
        def antepaste(self, num1, num2):
            try:
                if num1 and num2:
                    typ = 'c' if num2 == 1 else 'dice'
                    self.anterior_items.append(AnteriorItem(typ, num1, num2, hidden=False))
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
                parent = self.resor[self.selectRes.get()-1]
                hid = parent.hidden
                parent.listSubres.append(posmod(typ, timing, num1, num2, hidden=hid))
                self.destroy_all()
                self.build_resor()
                self.modified=1

        def conversao(self): 
            try:
                c_sum = 0
                a_sum = 0
                for item in self.anterior_items:
                    if item.typ == 'c':
                        c_sum += item.val1
                    elif item.typ == 'adv':
                        a_sum += item.val1
                    elif item.typ == 'dice':
                        c_sum += int(item.val1 * (item.val2 + 1) / 2)
                
                # premod constructor: adv, const, items
                pm = premod(a_sum, c_sum, self.anterior_items)
                return bloco(pm, self.clean_resor(), self.sn.get(), int(self.crit.get())/100, int(self.mini.get()))
            except:
                print(traceback.format_exc())
                messagebox.showerror(parent=self.Window2, title="Conversion error", message="Something went wrong, please check your submission.")
                return

        def clean_resor(self):
            posmods=[]
            for i in range(len(self.resor)):
                aux=("Resource #"+str(i+1))*(self.resor[i].resName.replace(" ", "")=="")+self.resor[i].resName*(self.resor[i].resName.replace(" ", "")!="")
                if self.resor[i].listSubres:
                    posmods.append(resourceSend(int(self.resor[i].qnt), aux, self.resor[i].listSubres, hidden=self.resor[i].hidden))
            return posmods

        def send_block(self):
            message_sent = self.conversao()
            if message_sent:
                try:
                    with open(os.path.join(self.user_past_configs_dir, str(self.past_index_max)+'.txt'), 'xb') as file:
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
                # Restore hidden status for the resource
                if hasattr(i, 'hidden'):
                    self.resor[-1].hidden = i.hidden
            
            # Restore anterior items from premods
            if hasattr(self.premod, 'items') and self.premod.items:
                self.anterior_items = self.premod.items
            else:
                self.anterior_items = []
        
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
                # Default to roll configs folder if available
                rc_dir = getattr(self, 'roll_configs_dir', None)
                initial_dir = rc_dir if rc_dir and os.path.isdir(rc_dir) else None
                
                self.path = filedialog.asksaveasfilename(
                    parent=self.Window2,
                    initialdir=initial_dir,
                    defaultextension=".pkl",
                    filetypes=[("Roll Configs", "*.pkl"), ("Text files", "*.txt"), ("All files", "*.*")]
                )
                if not self.path:
                    return
                    
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
                        self.path = filedialog.askopenfile(parent=self.Window2, filetypes = [("Roll Configs", "*.pkl"), ("Text files", "*.txt"), ("All files", "*.*")]).name                              
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
                            self.path=os.path.join(self.user_past_configs_dir, str(self.past_index)+'.txt')
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
                    self.path=os.path.join(self.user_past_configs_dir, str(self.past_index)+'.txt')
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
                self.SheetWindow = CharacterSheetWindow(self)
                self.SheetWindow.withdraw()
                
                # to show chat window 
                # self.deiconify() - moved to end of layout to prevent jank
                self.title("Chatroom") 
                self.resizable(width = False, height = False) 
                self.center_window(self, 800, 504)
                self.columnconfigure(2 , weight=1)
                self.rowconfigure(1, weight=1)

                self.sidebarLabel=ctk.CTkLabel(self, text="Players online", fg_color="gray20", corner_radius=6, font=("Roboto", 14))
                self.sidebarLabel.grid(row=0, column=1, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.sidebar=ctk.CTkScrollableFrame(self,
                                                    fg_color="gray20",
                                                    scrollbar_button_color="gray25",
                                                    scrollbar_button_hover_color="gray35")
                self.sidebar.columnconfigure(0 , weight=1)
                self.sidebar.grid(row=1, column=1, padx=self.rescale, sticky="ns")

                self.allButton = ctk.CTkButton(self,
                                    text="Select all",
                                    border_color=self.color,
                                    border_width=2,
                                    fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.AllClick())
                self.allButton.grid(row=2, column=1, padx=self.rescale, pady=self.rescale, sticky="ew")

                self.blocbtt= ctk.CTkButton(self, 
                                                    text = '►',
                                                    width=26,                      
                                                    border_color=self.color,
                                                    border_width=2,
                                                    fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.blocswitch())
                self.blocbtt.grid(row=0, column=4, padx=self.rescale, pady=self.rescale, sticky="ns", rowspan=3)
                
                self.sheetbtt= ctk.CTkButton(self, 
                                                    text = '◄',
                                                    width=26,                      
                                                    border_color=self.color,
                                                    border_width=2,
                                                    fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda: self.sheetswitch())
                self.sheetbtt.grid(row=0, column=0, padx=(self.rescale, 0), pady=self.rescale, sticky="ns", rowspan=3)
                                
                self.entryMsg = ctk.CTkEntry(self, fg_color="gray20", border_width=0, placeholder_text_color="gray30", placeholder_text="Write a message", font=("Roboto", 12)) 
                self.entryMsg.grid(row=2, column=2, padx=(0,self.rescale), pady=self.rescale, sticky="ew")
                #self.entryMsg.after(20, self.entryMsg.focus)
                
                self.buttonMsg = ctk.CTkButton(self, 
                                                            text = "Send",
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray20", hover_color="gray30", font=("Roboto", 12), command = lambda : self.sendButton(self.entryMsg.get())) 
                self.buttonMsg.grid(row=2, column=3, pady=self.rescale, sticky="ew")
                
                self.textCons=ctk.CTkTextbox(self, fg_color="gray20", font=("Roboto", 12))
                self.textCons.grid(row=0, column=2, pady=(self.rescale,0), sticky="nsew", rowspan=2, columnspan=2)
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
                self.center_window(self.Window2, 1350, 524)
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

                self.reslabel = ctk.CTkEntry(self.resourcebar2, fg_color="gray25", border_width=0, placeholder_text_color="gray35", placeholder_text="Resource name", font=("Roboto", 12), justify="center")
                self.reslabel.grid(row=0, column=1, columnspan=3, padx=self.rescale, pady=(self.rescale, 0), sticky="ew")

                self.resbtt2 = ctk.CTkButton(self.resourcebar2, 
                                                            text = '◄', 
                                                            width=26,
                                                            border_color=self.color,
                                                            border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12), command = lambda: self.callbackRes(self.reslabel.get())) 
                self.resbtt2.grid(row=1, column=1, padx=(self.rescale, self.rescale), pady=(self.rescale, self.rescale), sticky="e")
                
                self.resbox = IntSpinbox(self.resourcebar2,
                                    color=self.color, variable = self.res,
                                    from_ = 0)
                self.resbox.grid(row=1, column=2, padx=(0, self.rescale), pady=(self.rescale, self.rescale), sticky="ew")

                self.resbtt = ctk.CTkButton(self.resourcebar2, 
                                                            text = "+", 
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 14, "bold"), command = lambda: self.resourcepaste(self.res.get(), self.reslabel.get())) 
                self.resbtt.grid(row=1, column=3, padx=(0, self.rescale), pady=(self.rescale, self.rescale), sticky="w")
                


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
                self.antebar.columnconfigure(10, weight=0) # Space for hidden check
                self.antebar.grid(row=1, column=0, sticky="ew", pady=(0, self.rescale))

                self.antelabel= ctk.CTkLabel(self.antebar, text='Anterior', fg_color="gray25", corner_radius=6, font=("Roboto", 14))           
                self.antelabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=(self.rescale, 0), columnspan=10)

                self.aconlabel= ctk.CTkLabel(self.antebar,text='Constant', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.aconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), pady=(self.rescale, 0), sticky="ew", columnspan=2)
                

                self.acon = IntSpinbox(self.antebar,
                                        color=self.color, variable = self.ac)
                self.acon.grid(row=2, column=0, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.aconbtt = ctk.CTkButton(self.antebar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda : self.antepaste(int(self.ac.get()), 1))
                self.aconbtt.grid(row=2, column=1, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.separator1= ctk.CTkLabel(self.antebar, text="")
                self.separator1.grid(row=2, column=2, sticky="ew")

                self.aadvlabel= ctk.CTkLabel(self.antebar,text='Advantage', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.aadvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), pady=(self.rescale, 0), sticky="ew", columnspan=2)

                self.aadv = IntSpinbox(self.antebar,
                                        color=self.color, variable = self.aa)
                self.aadv.grid(row=2, column=8, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.aadvbtt = ctk.CTkButton(self.antebar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda : self.anteadvpaste(int(self.aa.get())))

                self.aadvbtt.grid(row=2, column=9, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.separator2= ctk.CTkLabel(self.antebar, text="")
                self.separator2.grid(row=2, column=7, sticky="ew")

                self.adlabel= ctk.CTkLabel(self.antebar,text='Dice', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.adlabel.grid(row=1, column=3, padx=self.rescale, pady=(self.rescale, 0), sticky="ew", columnspan=4)

                self.adic = IntSpinbox(self.antebar,
                                    color=self.color, variable = self.ad[0])
                self.adic.grid(row=2, column=3, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.addlabel= ctk.CTkLabel(self.antebar, text='d', width=0, font=("Roboto", 12))
                self.addlabel.grid(row=2, column=4, padx=10/3, pady=(self.rescale, self.rescale))

                self.adic2 = IntSpinbox(self.antebar,
                                    color=self.color, variable = self.ad[1],
                                    from_ = 0)
                self.adic2.grid(row=2, column=5, padx=0, pady=(self.rescale, self.rescale))

                self.adicbtt = ctk.CTkButton(self.antebar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda : self.antepaste(int(self.ad[0].get()), int(self.ad[1].get())))
                self.adicbtt.grid(row=2, column=6, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.interbar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.interbar.columnconfigure((2, 7), weight=1)
                self.interbar.grid(row=3, column=0, sticky="ew", pady=(0, self.rescale))

                self.interLabel= ctk.CTkLabel(self.interbar, text='Intermediate', fg_color="gray25", corner_radius=6, font=("Roboto", 14))
                self.interLabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=(self.rescale, 0), columnspan=10)

                self.iconlabel= ctk.CTkLabel(self.interbar,text='Constant', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.iconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), pady=(self.rescale, 0), sticky="ew", columnspan=2)

                self.icon = IntSpinbox(self.interbar,
                                        color=self.color, variable = self.ic)
                self.icon.grid(row=2, column=0, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.iconbtt = ctk.CTkButton(self.interbar,
                                                            text = "+",
                                                            width=26,
                                                            border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda: self.postpaste(int(self.ic.get()), 1, "c", "Inter"))

                self.iconbtt.grid(row=2, column=1, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.separator3= ctk.CTkLabel(self.interbar, text="")
                self.separator3.grid(row=2, column=2, sticky="ew")

                self.iadvlabel= ctk.CTkLabel(self.interbar,text='Advantage', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.iadvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), pady=(self.rescale, 0), sticky="ew", columnspan=2)

                self.iadv = IntSpinbox(self.interbar,
                                        color=self.color, variable = self.ia)

                self.iadv.grid(row=2, column=8, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.iadvbtt = ctk.CTkButton(self.interbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda: self.postpaste(int(self.ia.get()), 0, "adv", "Inter"))

                self.iadvbtt.grid(row=2, column=9, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.separator4= ctk.CTkLabel(self.interbar, text="")
                self.separator4.grid(row=2, column=7, sticky="ew")

                self.idlabel= ctk.CTkLabel(self.interbar,text='Dice', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.idlabel.grid(row=1, column=3, padx=self.rescale, pady=(self.rescale, 0), sticky="ew", columnspan=4)

                self.idic = IntSpinbox(self.interbar,
                                    color=self.color, variable = self.id[0])
                self.idic.grid(row=2, column=3, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.iddlabel= ctk.CTkLabel(self.interbar, text='d', width=0, font=("Roboto", 12))
                self.iddlabel.grid(row=2, column=4, padx=10/3, pady=(self.rescale, self.rescale))

                self.idic2 = IntSpinbox(self.interbar,
                                    color=self.color, variable = self.id[1],
                                    from_ = 0)
                self.idic2.grid(row=2, column=5, padx=0, pady=(self.rescale, self.rescale))

                self.idicbtt = ctk.CTkButton(self.interbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda: self.postpaste(int(self.id[0].get()), int(self.id[1].get()), "dice", "Inter"))
                self.idicbtt.grid(row=2, column=6, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.postbar=ctk.CTkFrame(self.secFrame, fg_color="gray20")
                self.postbar.columnconfigure((2, 7), weight=1)
                self.postbar.grid(row=4, column=0, sticky="ew", pady=(0, self.rescale))

                self.postLabel= ctk.CTkLabel(self.postbar, text='Posterior', fg_color="gray25", corner_radius=6, font=("Roboto", 14))
                self.postLabel.grid(row=0, column=0, padx=self.rescale, sticky="ew", pady=(self.rescale, 0), columnspan=10)

                self.pconlabel= ctk.CTkLabel(self.postbar,text='Constant', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.pconlabel.grid(row=1, column=0, padx=(2*self.rescale,self.rescale), pady=(self.rescale, 0), sticky="ew", columnspan=2)

                self.pcon = IntSpinbox(self.postbar,
                                        color=self.color, variable = self.pc)
                self.pcon.grid(row=2, column=0, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.pconbtt = ctk.CTkButton(self.postbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda: self.postpaste(int(self.pc.get()), 1, "c", "Post"))

                self.pconbtt.grid(row=2, column=1, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.separator5= ctk.CTkLabel(self.postbar, text="")
                self.separator5.grid(row=2, column=2, sticky="ew")

                self.padvlabel= ctk.CTkLabel(self.postbar,text='Advantage', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.padvlabel.grid(row=1, column=8, padx=(self.rescale,2*self.rescale), pady=(self.rescale, 0), sticky="ew", columnspan=2)

                self.padv = IntSpinbox(self.postbar,
                                        color=self.color, variable = self.pa)

                self.padv.grid(row=2, column=8, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.padvbtt = ctk.CTkButton(self.postbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda: self.postpaste(int(self.pa.get()), 0, "adv", "Post"))

                self.padvbtt.grid(row=2, column=9, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                self.separator6= ctk.CTkLabel(self.postbar, text="")
                self.separator6.grid(row=2, column=7, sticky="ew")

                self.pdlabel= ctk.CTkLabel(self.postbar,text='Dice', fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                self.pdlabel.grid(row=1, column=3, padx=self.rescale, pady=(self.rescale, 0), sticky="ew", columnspan=4)

                self.pdic = IntSpinbox(self.postbar,
                                    color=self.color, variable = self.pd[0])
                self.pdic.grid(row=2, column=3, padx=(self.rescale, 0), pady=(self.rescale, self.rescale))

                self.pddlabel= ctk.CTkLabel(self.postbar, text='d', width=0, font=("Roboto", 12))
                self.pddlabel.grid(row=2, column=4, padx=10/3, pady=(self.rescale, self.rescale))

                self.pdic2 = IntSpinbox(self.postbar,
                                    color=self.color, variable = self.pd[1],
                                    from_ = 0)
                self.pdic2.grid(row=2, column=5, padx=0, pady=(self.rescale, self.rescale))

                self.pdicbtt = ctk.CTkButton(self.postbar,
                                                            text = "+",
                                                            width=26, border_color=self.color, border_width=2,
                                                            fg_color="gray25", hover_color="gray35", font=("Roboto", 12, "bold"), command = lambda: self.postpaste(int(self.pd[0].get()), int(self.pd[1].get()), "dice", "Post"))
                self.pdicbtt.grid(row=2, column=6, padx=(10/3, self.rescale), pady=(self.rescale, self.rescale))

                #------------------------
                self.hiddenres=ctk.CTkToplevel(fg_color="gray15")
                self.hiddenres.withdraw()
                self.hiddenres.title("Result (hidden)")
                self.hiddenres.resizable(width = False, height = False)
                self.center_window(self.hiddenres, 300, 100)
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
                self.center_window(self.dicewindow, 450, 400)
                self.dicewindow.protocol("WM_DELETE_WINDOW", self.dicewindow.withdraw)

                self.progresswindow=ctk.CTkToplevel(fg_color="gray15")
                self.progresswindow.withdraw()
                self.progresswindow.title("Result (bar)")
                self.progresswindow.resizable(width = False, height = False)
                self.center_window(self.progresswindow, 450, 190)
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
                self.center_window(self.wheelwindow, 450, 530)
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
                self.center_window(self.possi, 820, 630)
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
                self.SheetWindow.protocol("WM_DELETE_WINDOW", self.sheetswitch)
                
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
                        SYNC_WIDTH = 150
                        textlis=wrap(message.content, width=SYNC_WIDTH)
                        for u in range(len(textlis)):
                            # Filter hidden resources if present and I'm not the sender
                            # (Sender checking logic handled later? No, better to strip content before display if needed)
                            
                            if "(H)" in message.content:
                                 # Checking logic: if I am not the sender.
                                 # message.sender is the sender NAME.
                                 if message.sender != self.my_name and message.sender != "Server":
                                     # Strip hidden parts
                                     # Regex to remove substring ending in (H)
                                     # Assuming default server formatting: \gName: Sub (H), Sub2.
                                     # Sub (H) might be at end of line.
                                     # Remove: [anything] (H)[comma?]
                                     
                                     filtered_content = message.content
                                     # Pattern: (non-g chars) (H) (, )?
                                     filtered_content = re.sub(r'[^\\,:]+? \(H\)(?:, )?', '', filtered_content)
                                     
                                     # Clean up empty resource entries "Res: ," or "Res: ."
                                     filtered_content = re.sub(r'(?<=\: )\,+', '', filtered_content) # Leading commas
                                     filtered_content = re.sub(r'\,\.', '.', filtered_content) # Comma before dot
                                     filtered_content = re.sub(r'(?<=\: )\.', '.', filtered_content) # Empty entry
                                     
                                     message.content = filtered_content
                                     
                                     # Update textlis with new content
                                     textlis=wrap(message.content, width=SYNC_WIDTH)

                            if textlis[u].startswith(r'\j'):
                                textlis[u]=textlis[u].replace(r'\j','',1)
                                textlis[u]=textlis[u].rstrip()
                            else:
                                textlis[u]=textlis[u].rstrip()
                        textlis.append('')
                        def display_message(message=message, textlis=textlis):
                            self.textCons.configure(state=NORMAL)
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
                                    # Don't justify headers, short lines, or indented lines
                                    is_header = line_content.strip().endswith(':') or "result:" in line_content.lower() or len(line_content.strip()) < 30
                                    is_indented = line_content.startswith(' ')
                                    if textlis[u+1]!='' and not textlis[u+1].startswith(' ') and not is_header and not is_indented:
                                        line_content = justify(textlis[u], SYNC_WIDTH)
                                    
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
                        self.after(0, display_message)
                    elif type(message).__name__=='dict':
                        def update_players(message=message):
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
                        self.after(0, update_players)
                    elif type(message).__name__=='status':
                        def show_roll_window(message=message):
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
                                # Populate valid rolls from config files
                                self.populate_roll_list()
                                
                        self.after(0, show_roll_window)
                    elif type(message).__name__=='tuple' and message[0]=='final_result':
                        # Handle final result from server after both players selected
                        final_possib = message[1]
                        caller_name = message[2] if len(message) > 2 else None
                        final_res = final_possib[0]
                        send_type = final_possib[1]
                        p, crit, r, resultStr = self.transl(final_res)
                        text = final_res.mods.strip() or 'N/A'
                        threading.Thread(target=self.displayres, args=[p, crit, r, resultStr, send_type, text, caller_name, final_res.hidden]).start()
                    else:
                        if not message or type(message[0]).__name__!='res':
                            def sync_players(message=message):
                                self.players = []
                                for dics in message:
                                    dics['selected'] = False
                                    self.players.append(dics)
                                self.createSidebarButtons()
                            self.after(0, sync_players)
                        else:
                            def show_possibs(message=message):
                                # Check if this is a two-player roll (has roll_id as last element)
                                is_two_player = False
                                roll_id = None
                                send_type = ""
                                
                                # Standard format: [res..., [send_type], [roll_id]]
                                # We work on a copy to avoid modifying the original message list if it's shared
                                msg_list = message.copy()
                                
                                # We check from the end of the list
                                if len(msg_list) >= 1:
                                    last = msg_list[-1]
                                    if isinstance(last, int):
                                        # It's a roll_id
                                        is_two_player = True
                                        roll_id = msg_list.pop(-1)
                                        if len(msg_list) >= 1 and isinstance(msg_list[-1], str):
                                            send_type = msg_list.pop(-1)
                                    elif isinstance(last, str):
                                        # It's a send_type (solo roll or non-sync roll)
                                        send_type = msg_list.pop(-1)
                                
                                # Safety check: if msg_list is now empty, we have a problem
                                if not msg_list:
                                    print("CRITICAL: Received empty possibilities list after parsing tags.")
                                    return
                                
                                possibs=ctk.CTkToplevel(self, fg_color="gray15")
                                possibs.title('Possibilities')
                                possibs.resizable(width = False, height = False)
                                
                                main_frame = ctk.CTkFrame(possibs, fg_color="transparent")
                                main_frame.grid(padx=4, pady=4)
                                
                                aux_2=ctk.CTkLabel(main_frame, text='Net advantage', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                                aux_2.grid(row=0, column=3, padx=4, pady=4)
                                aux_3=ctk.CTkLabel(main_frame, text='Resources', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                                aux_3.grid(row=0, column=4, padx=4, pady=4, sticky="ew")
                                
                                aux_2_mor=ctk.CTkFrame(main_frame, fg_color="gray20")
                                aux_2_mor.grid_columnconfigure(0, weight=1)
                                aux_2_mor.grid(row=1, column=3, padx=4, pady=4, sticky="ew")
                                aux_3_mor=ctk.CTkFrame(main_frame, fg_color="gray20")
                                aux_3_mor.grid_columnconfigure(0, weight=1)
                                aux_3_mor.grid(row=1, column=4, padx=4, pady=4, sticky="ew")

                                diff=[]
                                diff_crit=[]
                                diff_fail=[]
                                border=[]
                                border_crit=[]
                                border_fail=[]
                                p, crit, r, resultStr=self.transl(msg_list[0])
                                for i in msg_list:
                                    p_old, crit_old=p, crit
                                    p, crit, r, resultStr=self.transl(i)
                                    diff.append(p_old-p)
                                    diff_crit.append(crit_old-crit)
                                    diff_fail.append((p_old-p)/2)
                                    border.append(p)
                                    border_crit.append(crit)
                                    border_fail.append(p/2)
                                probs=["0%"*(diff[i]!=0)+"-"*(diff[i]==0) for i in range(len(msg_list))]
                                probs_crit=["0%"*(diff_crit[i]!=0)+"-"*(diff_crit[i]==0) for i in range(len(msg_list))]
                                probs_fail=["0%"*(diff_fail[i]!=0)+"-"*(diff_fail[i]==0) for i in range(len(msg_list))]
                                
                                percent=min(0.5, max(np.random.normal(0.25, 0.1), 0))
                                aux1=[i for i in range(1, len(diff)) if (r<border[i-1] and r>=border[i]-percent*diff[i])]
                                if aux1:
                                    ind=random.choice(aux1)
                                    probs[ind:]=["-" for i in range(ind, len(msg_list))]
                                    probs[ind]="{:.1%}".format(1-percent)
                                    aux_1=ctk.CTkLabel(main_frame, text='% of f->s+', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                                    aux_1.grid(row=0, column=0, padx=4, pady=4)
                                    aux_1_mor=ctk.CTkFrame(main_frame, fg_color="gray20")
                                    aux_1_mor.grid_columnconfigure(0, weight=1)
                                    aux_1_mor.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

                                percent=min(0.5, max(np.random.normal(0.25, 0.1), 0))
                                aux2=[i for i in range(1, len(diff_crit)) if (r<border_crit[i-1] and r>=border_crit[i]-percent*diff_crit[i])]
                                if aux2:
                                    ind=random.choice(aux2)
                                    probs_crit[ind:]=["-" for i in range(ind, len(msg_list))]
                                    probs_crit[ind]="{:.1%}".format(1-percent)
                                    aux_12=ctk.CTkLabel(main_frame, text='% of s->cs', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                                    aux_12.grid(row=0, column=1, padx=4, pady=4)
                                    aux_12_mor=ctk.CTkFrame(main_frame, fg_color="gray20")
                                    aux_12_mor.grid_columnconfigure(0, weight=1)
                                    aux_12_mor.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
                                    
                                percent=min(0.5, max(np.random.normal(0.25, 0.1), 0))
                                aux3=[i for i in range(1, len(diff_fail)) if (r<border_fail[i-1] and r>=border_fail[i]-percent*diff_fail[i])]
                                if aux3:
                                    ind=random.choice(aux3)
                                    probs_fail[ind:]=["-" for i in range(ind, len(msg_list))]
                                    probs_fail[ind]="{:.1%}".format(1-percent)
                                    aux_13=ctk.CTkLabel(main_frame, text='% of cf->f+', fg_color="gray20", corner_radius=6, font=("Roboto", 12))
                                    aux_13.grid(row=0, column=2, padx=4, pady=4)
                                    aux_13_mor=ctk.CTkFrame(main_frame, fg_color="gray20")
                                    aux_13_mor.grid_columnconfigure(0, weight=1)
                                    aux_13_mor.grid(row=1, column=2, padx=4, pady=4, sticky="ew")
                                    
                                for i in range(len(msg_list)):
                                    p, crit, r, resultStr=self.transl(msg_list[i])
                                    if aux1:
                                        aux_1=ctk.CTkLabel(aux_1_mor, text=probs[i], fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                        aux_1.grid(row=i, column=0, padx=8, pady=8, sticky="ew")
                                    if aux2:
                                        aux_12=ctk.CTkLabel(aux_12_mor, text=probs_crit[i], fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                        aux_12.grid(row=i, column=0, padx=8, pady=8, sticky="ew")
                                    if aux3:
                                        aux_13=ctk.CTkLabel(aux_13_mor, text=probs_fail[i], fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                        aux_13.grid(row=i, column=0, padx=8, pady=8, sticky="ew")
                                                    
                                    aux_2_text = '+'*(msg_list[i].adv>0)+str(msg_list[i].adv)
                                    aux_2=ctk.CTkLabel(aux_2_mor, text=aux_2_text, fg_color="gray25", corner_radius=6, font=("Roboto", 12))
                                    aux_2.grid(row=i, column=0, padx=8, pady=8, sticky="ew")

                                    text=msg_list[i].mods_button.replace(r'\g', '').strip()
                                    if not text:
                                        text = 'N/A'
                                    full_text = msg_list[i].mods # Keep full text for chat
                                    if is_two_player:
                                        # Two-player roll: send selection to server
                                        resButton = ctk.CTkButton(aux_3_mor,
                                                        text = text,
                                                        fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                        font=("Roboto", 12),
                                                        command=lambda idx=i, rid=roll_id, win=possibs: self.send_posterior_selection(rid, idx, win))
                                        resButton.grid(row=i, column=0, padx=8, pady=8, sticky="ew")
                                    else:
                                        # Single player or receiver: show button to display result
                                        # Pass msg_list[i].hidden to displayres
                                        is_hidden = msg_list[i].hidden
                                        resButton = ctk.CTkButton(aux_3_mor,
                                                        text = text,
                                                        fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                        font=("Roboto", 12),
                                                        command=lambda p=p, crit=crit, r=r, resStr=resultStr, st=send_type, txt=full_text, hid=is_hidden: threading.Thread(target = self.displayres, args=[p, crit, r, resStr, st, txt, None, hid]).start())
                                        resButton.grid(row=i, column=0, padx=8, pady=8, sticky="ew")
                                
                                if not is_two_player:
                                    resButton = ctk.CTkButton(main_frame,
                                                        text = 'Show results',
                                                        fg_color="gray25", hover_color="gray35", border_color=self.color, border_width=2,
                                                        font=("Roboto", 14),
                                                        command=partial(self.show_res, msg_list, send_type))
                                    resButton.grid(row=2, column=0, columnspan=5, padx=4, pady=4, sticky="ew")

                                possibs.focus()
                                self.center_window(possibs)
                            self.after(0, show_possibs)
                except Exception:
                    print(traceback.format_exc())
                    if self.not_closing:
                        self.on_closing()
                    else:
                        break

        def send_posterior_selection(self, roll_id, selection_index, window):
            """Send posterior selection to server for synchronized two-player rolls."""
            try:
                selection = posterior_selection(roll_id, selection_index)
                message_sent = pickle.dumps(selection)
                message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(message_sent_header + message_sent)
                window.destroy()  # Close the possibilities window
            except Exception as e:
                print(f"Error sending posterior selection: {e}")

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
                aux_3=ctk.CTkLabel(aux_3_mor, text=(message[i].mods.strip() or 'N/A'), fg_color="gray25", corner_radius=6, font=("Roboto", 12))

                aux_1.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                                    
                aux_2.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
                
                aux_3.grid(row=i, column=0, padx=self.rescale, pady=((i==0)*self.rescale, self.rescale), sticky="ew")
            possibs.focus()
            self.center_window(possibs)
            
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
                if not self.possi.winfo_exists() or not self.possi.winfo_viewable() or anim_id != self.current_anim_id:
                    return
                
                # Update idle tasks to ensure state is consistent
                try:
                    self.possi.update_idletasks()
                except:
                    pass
                
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

            except (TclError, Exception):
                pass

        def reset_animation_step(self, roll_val, anim_id):
             try:
                if not self.possi.winfo_exists() or not self.possi.winfo_viewable() or anim_id != self.current_anim_id:
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

             except (TclError, Exception):
                pass

        def run_wheel_rolldic_animation_step(self, anim_id):
            try:
                if not self.possi.winfo_exists() or not self.possi.winfo_viewable() or anim_id != self.current_anim_id:
                    return

                # Update idle tasks to ensure state is consistent
                try:
                    self.possi.update_idletasks()
                except:
                    pass

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

                
            except (TclError, Exception):
                pass
                
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
try:
    g.mainloop()
except (KeyboardInterrupt, SystemExit):
    # Handle force close (Ctrl+C)
    if hasattr(g, 'user_past_configs_dir') and g.user_past_configs_dir and os.path.exists(g.user_past_configs_dir):
        try:
            shutil.rmtree(g.user_past_configs_dir, ignore_errors=True)
        except:
            pass
    print("Program closed.")
except Exception:
    traceback.print_exc()
finally:
    # Ensure cleanup always runs if not already done
    if hasattr(g, 'user_past_configs_dir') and g.user_past_configs_dir and os.path.exists(g.user_past_configs_dir):
        try:
            shutil.rmtree(g.user_past_configs_dir, ignore_errors=True)
        except:
            pass

