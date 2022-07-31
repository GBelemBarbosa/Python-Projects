# import all the required modules 
import socket 
import threading 
from tkinter import *
from tkinter import font 
from tkinter import ttk 
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

red=Color('#ff0000')
violet=Color('#ff00ff')
colors = list(red.range_to(violet,50))
colors=colors+list(violet.range_to(red,50))
rollBg = ('#3ec2fd', '#0c6495')

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
                        if yob[1]!='':
                            chunks.append(yob[1])
                        elif len(chunks)>1:
                            z=chunks.pop()
                            chunks[-1]='\j'+z+chunks[-1]
                        else:
                            chunks.append('\j')
                        chunks.append(' '*50)
                        if yob[0]!='':
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
    def __init__(self,premod,posmod,sn):
        self.premod=premod
        self.posmod=posmod
        self.sn=sn

class status:
    def __init__(self,num):
        self.num=num
class msg:
    def __init__(self,destiny,content):
        self.destiny=destiny
        self.content=content

class roll:
    def __init__(self,receiver,who,crit):
        self.receiver=receiver
        self.who=who
        self.crit=crit

class res:
    def __init__(self,p,crit,r,advan):
        self.p=p
        self.r=r
        self.crit=crit
        self.advan=advan

# GUI class for the chat 
class GUI: 

        # constructor method 
        def __init__(self): 
                
                # chat window which is currently hidden 
                self.Window = Tk() 
                self.Window.withdraw() 
                
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
                                        font = "Courier 14 bold") 
                
                self.pls.place(relheight = 0.15, 
                                        relx = 0.5, 
                                        rely = 0.09,
                                        anchor=CENTER)
                
                # create a Label 
                self.labelName = Label(self.login, 
                                                        text = "Username: ",
                                                        font = "Courier 14") 
                
                self.labelName.place(relheight = 0.2, 
                                                        relx = 0.25, 
                                                        rely = 0.16) 
                
                # create a entry box for 
                # typing the message 
                self.entryName = Entry(self.login, 
                                                        font = "Courier 14") 
                
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
                                                font = "Courier 14 bold", 
                                                command = lambda: self.goAhead(self.entryName.get())) 

                self.entryName.bind('<Return>',(lambda event: self.goAhead(self.entryName.get())))
                self.login.protocol("WM_DELETE_WINDOW", self.on_closing)  
                self.go.place(relx = 0.4, 
                                        rely = 0.55) 
                self.Window.mainloop() 

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
            message_sent = pickle.dumps(roll(self.roll_list,self.who.get(),float(int(self.crit.get())/100)))
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
                                                font = "Courier 14 bold",
                                                command=lambda c=i: self.onPlayerClick(c))
                self.playerBtts.append(tempButton)
                self.playerBtts[-1].place(relwidth=1, relheight=0.1, rely = 0.1*(len(self.playerBtts)-1))

                tempButton = Button(self.sidebaroll,
                                                    fg = self.players[i]['color'],
                                                    bg = 'black', text = self.players[i]['name'],
                                                    font = "Courier 14 bold",
                                                    command=lambda c=i: self.onPlayerSelec(c))
                self.playerBtts2.append(tempButton)
                self.playerBtts2[-1].place(relwidth=1, relheight=0.1, rely = 0.1*(len(self.playerBtts2)-1))

                
        def displayres(self,res):
            if self.displaymode.get()=='bar':
                self.progress['value']=0
                self.minRollLabel2.config(text = "Precisa: "+str(res.p/100))
                self.critRollLabel2.config(text = "Crítico a partir de: "+str(res.crit/100))
                self.realRollLabel2.config(text = "")
                self.ResultLabel2.config(text = "")
                
                if (res.r > res.p):
                    roundedRealDiceRoll = ceil(res.r/100)
                    if(res.r > res.crit):
                        resultStr = "SUCESSO CRÍTICO"
                    else:
                        resultStr = "SUCESSO"
                else:
                    roundedRealDiceRoll = max(floor(res.r/100),1)
                    if (res.r<=(2000-res.p)/10):
                        resultStr = "FALHA CRÍTICA"
                    else:
                        resultStr = "FRACASSO"
                RealDiceRoll=str(res.r/100)        
                res.p=res.p//5
                res.r=(res.r+19)//20
                res.crit=res.crit//5

                if not self.progresswindow.winfo_viewable():
                    self.progresswindow.deiconify()
                if self.dicewindow.winfo_viewable():
                    self.dicewindow.withdraw()
                self.progresswindow.focus()
                
                self.barracrit1.place(relwidth=0.0025,x=res.crit-1)
                self.barrap1.place(relwidth=0.0025,x=res.p-1)
                self.barracrit2.place(relwidth=0.0025,x=res.crit+1)
                self.barrap2.place(relwidth=0.0025,x=res.p+1)

                x=0;
                n=random.randint(2,15)
                for i in range(159):
                    sleep(0.01)
                    x+=0.00625
                    y=int(res.r*n*x/(1+(n-1)*x))
                    self.progress['value']=y
                
                self.ResultLabel2.config(text = resultStr)
                self.realRollLabel2.config(text = "Rolou: "+RealDiceRoll)
            else:
                self.minRollLabel.config(text = "Precisa: "+str(res.p/100))
                self.critRollLabel.config(text = "Crítico a partir de: "+str(res.crit/100))
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
                
                currentRoll = random.randint(1, 20)
                while maxSleepTime-sleepTime > 0.1 and maxSleepTime > sleepTime:
                    rolagem = random.randint(1, 20)
                    while rolagem == currentRoll:
                        rolagem = random.randint(1, 20)

                    currentRoll = rolagem

                    img = Image.open("Dice_Images/"+str(rolagem)+".png")
                    img = img.resize((250,250), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(img)
                    self.panel.config(image = self.img)
                    
                    sleep(sleepTime)
                    sleepTime = self.nextSleepTime(sleepTime, maxSleepTime)

                sleep(self.maxMST/100 - maxSleepTime)

                if (res.r > res.p):
                    roundedRealDiceRoll = ceil(res.r/100)
                    if(res.r > res.crit):
                        resultStr = "SUCESSO CRÍTICO"
                    else:
                        resultStr = "SUCESSO"
                else:
                    roundedRealDiceRoll = max(floor(res.r/100),1)
                    if (res.r<=(2000-res.p)/10):
                        resultStr = "FALHA CRÍTICA"
                    else:
                        resultStr = "FALHA"
                img = Image.open("Dice_Images/"+str(roundedRealDiceRoll)+".png")
                img = img.resize((250,250), Image.ANTIALIAS)
                self.img = ImageTk.PhotoImage(img)
                self.panel.config(image = self.img)

                self.realRollLabel.config(text = "Rolou: "+str(res.r/100))
                self.ResultLabel.config(text = resultStr)

        def nextSleepTime(self, currentTime, limitTime): # 3 opcoes de incremento de tempo
                # return currentTime + currentTime**2 / 2
                # return currentTime + incrementFraction*currentTime
                return currentTime+limitTime*(1-exp(-currentTime*self.incrementFraction))

        def on_closing(self):
                client.close()
                sys.exit()
        
        def blocswitch(self):
            if not self.Window2.winfo_viewable():
                self.Window2.deiconify()
                self.block_entry.focus()
                self.blocbtt.config(text='<')
            else:
                self.Window2.withdraw()
                self.blocbtt.config(text='>')            

        def resourcepaste(self, num):
            index=len(self.block_entry.get())
            self.block_entry.focus()
            self.block_entry.icursor(index)
            self.block_entry.insert(index, "("+num.get()+", []), ")           
            self.block_entry.icursor(self.block_entry.index(INSERT)-4)

        def anteadvpaste(self, num):
            bloco_text=self.advan_entry.get()
            
            bloco_text=bloco_text.replace(" ", "")
            if not bloco_text:
                bloco_text=0
            try:
                bloco_text=str(int(bloco_text)+int(num.get()))
                self.advan_entry.delete(0, END)
                self.advan_entry.insert(END, bloco_text)
                self.advan_entry.icursor(self.advan_entry.index(INSERT))
            except:
                pass
            self.advan_entry.focus()
        
        def antepaste(self, num1, num2):
            if type(num2)!=str:
                num2=num2.get()
            bloco_text=self.value_entry.get()
            
            bloco_text=bloco_text.replace(" ", "")
            if not bloco_text:
                bloco_text=0
            try:
                bloco_text=str(int(bloco_text)+int(int(num1.get())*(int(num2)+1)/2))
                self.value_entry.delete(0, END)
                self.value_entry.insert(END, bloco_text)
                self.value_entry.icursor(self.value_entry.index(INSERT))
            except:
                pass
            self.value_entry.focus()

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
                        rcv = threading.Thread(target=self.receive) 
                        rcv.start()
                        clr = threading.Thread(target=self.colorloop)
                        clr.start()
                else:
                        self.pls.config(text=server_message)

        # The main layout of the chat 
        def layout(self,name): 

                self.who=StringVar(value='we')
                self.crit=StringVar(value='10')
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
                self.Window.deiconify() 
                self.Window.title("CHATROOM") 
                self.Window.resizable(width = False, height = False) 
                self.Window.configure(width = 800, height = 500, bg = 'black')

                self.sidebar = Frame(self.Window, bg = 'black', width=200, height=500)
                self.sidebar.pack(expand = False, fill = 'both', side = 'left')

                
                self.sep = Label(self.Window, bg = self.color)
                self.sep.pack(expand = False, fill = 'both', side = 'left')

                self.mainFrame = Frame(self.Window, width=562, height=500)
                self.mainFrame.pack(expand=False, side='left')

                self.sep2 = Label(self.Window, bg=self.color)
                self.sep2.pack(expand = False, fill = 'both', side = 'left')

                self.bttframe = Frame(self.Window, width=30, height=500)
                self.bttframe.pack(expand=False, side='left')
                self.blocbtt= Button(self.bttframe, 
                                                    text = ">", 
                                                    font = "Courier 12 bold", 
                                                    fg = self.color,
                                                    bg='black',
                                                    command = lambda : self.blocswitch())
                self.blocbtt.place(relheight=1,relwidth=1)
                
                self.Window2=Toplevel()
                self.Window2.title("ROLL") 
                self.Window2.resizable(width = False, height = False)
                self.Window2.configure(width = 775, height = 500, bg = 'black')
                self.Window2.pack_propagate(0)

                self.label = Label(self.Window2,
                                                text='Select the players to roll',
                                                bg = 'black',
                                                fg='white',
                                                width=30,
                                                font = "Courier 14 bold",
                                                pady=5) 
                self.label.pack(expand=True, fill="y", side="top")
                
                self.sidebaroll = Frame(self.Window2, bg = 'black', width=200, height=500)
                self.sidebaroll.pack(expand = False, fill = 'both', side = 'left')
                
                self.sep3 = Label(self.Window2, bg = self.color)
                self.sep3.pack(expand = False, fill = 'both', side = 'left')
        
                self.secFrame = Frame(self.Window2, width=562, height=500, bg='black')
                self.secFrame.pack(expand=True, fill = 'both', side='left')

                self.labelBottom2 = Label(self.secFrame, bg = 'black', height = 79, width = 562)     
                self.labelBottom2.place(y=385) 
                
                self.block_entry = Entry(self.labelBottom2, bg = 'black', fg="white", font = "Courier 12", insertbackground = "white") 
                self.block_entry.place(width = 417, 
                                                height = 65, 
                                                y = 5, 
                                                x = 5) 
                
                self.button_block = Button(self.labelBottom2, 
                                                            text = "Send", 
                                                            font = "Courier 12 bold", 
                                                            width = 10, 
                                                            bg = 'black',
                                                            fg=self.color,
                                                            command = lambda : self.conversao(self.block_entry.get())) 
                
                self.button_block.place(x = 428, 
                                            y = 5, 
                                            height = 66, 
                                            width = 126) 
                
                self.line3 = Label(self.secFrame, bg=self.color)                 
                self.line3.place(relwidth=1,relheight=0.012,y=379)

                self.line4 = Label(self.Window2, bg=self.color)
                self.line4.place(relwidth=1,relheight=0.012,y=36)

                self.stypebar= Label(self.secFrame, bg = 'black')
                self.stypebar.place(relwidth=1,relheight=0.05,y=1)

                self.sep4 = Label(self.Window2, bg = self.color)
                self.sep4.pack(expand = False, fill = 'both', side = 'left')

                self.antebar= Label(self.secFrame, bg = 'black')
                self.antebar.place(relwidth=1,relheight=0.14,rely=0.05)

                self.antebar2= Label(self.secFrame, bg = 'black')
                self.antebar2.place(relwidth=1,relheight=0.09,rely=0.19)

                self.line8 = Label(self.secFrame, bg=self.color)                 
                self.line8.place(relwidth=1,relheight=0.012,rely=0.05)

                self.interbar= Label(self.secFrame, bg = 'black')
                self.interbar.place(relwidth=1,relheight=0.17,rely=0.286)

                self.line5 = Label(self.secFrame, bg=self.color)                 
                self.line5.place(relwidth=1,relheight=0.012,rely=0.286)

                self.postbar= Label(self.secFrame, bg = 'black')
                self.postbar.place(relwidth=1,relheight=0.17,rely=0.456)

                self.line6 = Label(self.secFrame, bg=self.color)                 
                self.line6.place(relwidth=1,relheight=0.012,rely=0.456)
                
                self.resourcebar= Label(self.secFrame, bg = 'black')
                self.resourcebar.place(relwidth=1,relheight=0.19,rely=0.626)

                self.line7 = Label(self.secFrame, bg=self.color)                 
                self.line7.place(relwidth=1,relheight=0.012,rely=0.626)

                self.progresswindow=Toplevel(bg='black')
                self.progresswindow.title("RESULT")
                self.progresswindow.protocol("WM_DELETE_WINDOW", self.progresswindow.withdraw)

                self.dicewindow = Toplevel(bg='black')
                self.dicewindow.title("RESULT")
                self.dicewindow.protocol("WM_DELETE_WINDOW", self.dicewindow.withdraw)

                self.minRollLabel = Label(self.dicewindow, text='', fg='white', bg='black', font=('Courier', 12))
                self.minRollLabel.pack()
                self.critRollLabel = Label(self.dicewindow, text='', fg='white', bg='black', font=('Courier', 12))
                self.critRollLabel.pack()
                self.realRollLabel = Label(self.dicewindow, text='', fg='white', bg='black', font=('Courier', 12))
                self.realRollLabel.pack()
                self.ResultLabel = Label(self.dicewindow, text='', bg='black', font=('Courier', 25), fg=self.color)
                self.ResultLabel.pack()

                self.panel = Label(self.dicewindow, bg='black')
                self.panel.pack()

                self.minRollLabel2 = Label(self.progresswindow, text='', fg='white', bg='black', font=('Courier', 12))
                self.minRollLabel2.pack()
                self.critRollLabel2 = Label(self.progresswindow, text='', fg='white', bg='black', font=('Courier', 12))
                self.critRollLabel2.pack()
                self.realRollLabel2 = Label(self.progresswindow, text='', fg='white', bg='black', font=('Courier', 12))
                self.realRollLabel2.pack()
                self.ResultLabel2 = Label(self.progresswindow, text='', bg='black', font=('Courier', 25), fg=self.color)
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
                                                                        font = 'Courier 10 bold')
                
                self.hiddenBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'hidden',
                                                                        text = 'Hidden', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')
                self.weBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'we',
                                                                        text = 'We', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')

                self.youBtt=Radiobutton(self.stypebar, 
                                                                        variable = self.who, 
                                                                        value = 'you',
                                                                        text = 'You', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')

                self.sbtt=Radiobutton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 's',
                                                                        text = 'Sim', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')

                self.nbtt=Radiobutton(self.stypebar, 
                                                                        variable = self.sn, 
                                                                        value = 'n',
                                                                        text = 'Não', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')

                self.sdtypelabel= Label(self.stypebar,fg="white",text='Send type: ',bg='black', width=11, font = 'Courier 10 bold')
                self.messagelabel= Label(self.stypebar,fg="white",text='Message: ',bg='black', width=9, font = 'Courier 10 bold')
                self.sdtypelabel.pack(side='left')
                self.weBtt.pack(side='left')
                self.meBtt.pack(side='left')
                self.youBtt.pack(side='left')
                self.hiddenBtt.pack(side='left')
                self.nbtt.pack(side='right')
                self.sbtt.pack(side='right')
                self.messagelabel.pack(side='right')

                self.antelabel= Label(self.antebar,fg="white",text='Anterior',bg='black', width=8, font = 'Courier 12 bold')           
                self.antelabel.pack(side='top')

                #----------------------------------------

                self.valuelabel= Label(self.antebar2,fg="white",text='            Total value: ',bg= 'black', width=25, font = 'Courier 10 bold')           
                self.valuelabel.pack(side='left')

                self.value_entry = Entry(self.antebar2, bg = 'black', fg="white", font = "Courier 12", width = 4, insertbackground = "white") 
                self.value_entry.pack(side='left')

                self.value_entry.insert(END, '0')

                self.advanlabel= Label(self.antebar2,fg="white",text='  Total advantage: ',bg= 'black', width=19, font = 'Courier 10 bold')           
                self.advanlabel.pack(side='left')

                self.advan_entry = Entry(self.antebar2, bg = 'black', fg="white", font = "Courier 12", width = 4, insertbackground = "white") 
                self.advan_entry.pack(side='left')

                self.advan_entry.insert(END, '0')

                #----------------------------------------

                self.aconlabel= Label(self.antebar,fg="white",text='Constant: ',bg= 'black', width=10, font = 'Courier 10 bold')           
                self.aconlabel.pack(side='left')
                
                self.acon = Spinbox(self.antebar,
                                    textvariable = self.ac,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.acon.pack(side='left')

                self.aconbtt = Button(self.antebar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.antepaste(self.ac, "1")) 
                
                self.aconbtt.pack(side='left')

                self.aadvlabel= Label(self.antebar,fg="white",text='  Advantage: ',bg='black', width=13, font = 'Courier 10 bold')           
                self.aadvlabel.pack(side='left')

                self.aadv = Spinbox(self.antebar,
                                    textvariable = self.aa,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.aadv.pack(side='left')

                self.aadvbtt = Button(self.antebar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.anteadvpaste(self.aa)) 
                
                self.aadvbtt.pack(side='left')

                self.adlabel= Label(self.antebar,fg="white",text='  Dice: ',bg='black', width=8, font = 'Courier 10 bold')           
                self.adlabel.pack(side='left')

                self.adic = Spinbox(self.antebar,
                                    textvariable = self.ad[0],
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.adic.pack(side='left')

                self.addlabel= Label(self.antebar,fg="white",text='d',bg='black', width=1, font = 'Courier 10 bold')           
                self.addlabel.pack(side='left')

                self.adic2 = Spinbox(self.antebar,
                                    textvariable = self.ad[1],
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = 0,
                                    to = 100)

                self.adic2.pack(side='left')

                self.adicbtt = Button(self.antebar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.antepaste(self.ad[0], self.ad[1])) 
                
                self.adicbtt.pack(side='left')
                
                self.interlabel= Label(self.interbar,fg="white",text='Intermediate',bg='black', width=12, font = 'Courier 12 bold')
                self.interlabel.pack(side='top')

                self.iconlabel= Label(self.interbar,fg="white",text='Constant: ',bg='black', width=10, font = 'Courier 10 bold')
                self.iconlabel.pack(side='left')

                self.icon = Spinbox(self.interbar,
                                    textvariable = self.ic,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.icon.pack(side='left')

                self.iconbtt = Button(self.interbar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.interpaste(self.ic, "1")) 
                
                self.iconbtt.pack(side='left')

                self.iadvlabel= Label(self.interbar,fg="white",text='  Advantage: ',bg='black', width=13, font = 'Courier 10 bold')           
                self.iadvlabel.pack(side='left')

                self.iadv = Spinbox(self.interbar,
                                    textvariable = self.ia,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.iadv.pack(side='left')

                self.iadvbtt = Button(self.interbar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.interpaste(self.ia, "0")) 
                
                self.iadvbtt.pack(side='left')

                self.idlabel= Label(self.interbar,fg="white",text='  Dice: ',bg='black', width=8, font = 'Courier 10 bold')           
                self.idlabel.pack(side='left')

                self.idic = Spinbox(self.interbar,
                                    textvariable = self.id[0],
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.idic.pack(side='left')

                self.iddlabel= Label(self.interbar,fg="white",text='d',bg='black', width=1, font = 'Courier 10 bold')           
                self.iddlabel.pack(side='left')

                self.idic2 = Spinbox(self.interbar,
                                    textvariable = self.id[1],
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = 0,
                                    to = 100)

                self.idic2.pack(side='left')

                self.idicbtt = Button(self.interbar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.interpaste(self.id[0], self.id[1])) 
                
                self.idicbtt.pack(side='left')

                self.postlabel= Label(self.postbar,fg="white",text='Posterior',bg='black', width=9, font = 'Courier 12 bold')
                self.postlabel.pack(side='top')

                self.pconlabel= Label(self.postbar,fg="white",text='Constant: ',bg='black', width=10, font = 'Courier 10 bold')
                self.pconlabel.pack(side='left')

                self.pcon = Spinbox(self.postbar,
                                    textvariable = self.pc,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.pcon.pack(side='left')

                self.pconbtt = Button(self.postbar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.postpaste(self.pc, "1")) 

                self.pconbtt.pack(side='left')

                self.padvlabel= Label(self.postbar,fg="white",text='  Advantage: ',bg='black', width=13, font = 'Courier 10 bold')           
                self.padvlabel.pack(side='left')

                self.padv = Spinbox(self.postbar,
                                    textvariable = self.pa,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.padv.pack(side='left')

                self.padvbtt = Button(self.postbar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.postpaste(self.pa, "0")) 

                self.padvbtt.pack(side='left')

                self.pdlabel= Label(self.postbar,fg="white",text='  Dice: ',bg='black', width=8, font = 'Courier 10 bold')           
                self.pdlabel.pack(side='left')

                self.pdic = Spinbox(self.postbar,
                                    textvariable = self.pd[0],
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = -100,
                                    to = 100)

                self.pdic.pack(side='left')

                self.pddlabel= Label(self.postbar,fg="white",text='d',bg='black', width=1, font = 'Courier 10 bold')           
                self.pddlabel.pack(side='left')

                self.pdic2 = Spinbox(self.postbar,
                                    textvariable = self.pd[1],
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = 0,
                                    to = 100)

                self.pdic2.pack(side='left')

                self.pdicbtt = Button(self.postbar, 
                                                            text = "+", 
                                                            font = "Courier 10 bold", 
                                                            width = 1, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.postpaste(self.pd[0], self.pd[1])) 

                self.pdicbtt.pack(side='left')

                self.resourcebar1= Label(self.resourcebar, bg='black')
                self.resourcebar1.pack(side='left')

                self.sep5= Label(self.resourcebar, bg=self.color)
                self.sep5.pack(expand = False, fill = 'both', side = 'left')

                self.resourcebar2= Label(self.resourcebar, bg='black')
                self.resourcebar2.pack(side='left', expand=True, fill="both")

                self.sep6= Label(self.resourcebar, bg=self.color)
                self.sep6.pack(expand = False, fill = 'both', side = 'left')

                self.resourcebar3= Label(self.resourcebar, bg='black')
                self.resourcebar3.pack(side='left')

                self.reslabel= Label(self.resourcebar2,fg="white",text='Resource quantity:',bg='black', width=18, font = 'Courier 12 bold')
                self.reslabel.pack()

                self.resbox = Spinbox(self.resourcebar2,
                                    textvariable = self.res,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = 0,
                                    to = 100)

                self.resbox.pack(pady=2)

                self.resbtt = Button(self.resourcebar2, 
                                                            text = "Add resource", 
                                                            font = "Courier 10 bold", 
                                                            width = 12, 
                                                            bg = 'black',
                                                            fg="white",
                                                            command = lambda : self.resourcepaste(self.res)) 
                
                self.resbtt.pack(side='bottom')

                self.critlabel= Label(self.resourcebar1,fg="white",text='Crit chance: ',bg='black', width=13, font = 'Courier 12 bold')
                self.critlabel.pack(side='left')

                self.critbox = Spinbox(self.resourcebar1,
                                    textvariable = self.crit,
                                    bg="black",
                                    fg='white',
                                    font='Courier 10',
                                    width = 4,
                                    from_ = 0,
                                    to = 100,
                                    increment = 10)

                self.critbox.pack(side='left')

                self.percelabel= Label(self.resourcebar1,fg="white",text='%',bg='black', width=1, font = 'Courier 12 bold')
                self.percelabel.pack(side='left')

                self.dicebar= Label(self.resourcebar3,fg="white",text='Display mode:',bg='black', width=13, font = 'Courier 12 bold')
                self.dicebar.pack()

                self.barbtt=Radiobutton(self.resourcebar3, 
                                                                        variable = self.displaymode, 
                                                                        value = 'bar',
                                                                        text = 'Bar', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')
                
                self.barbtt.pack()

                self.dicebtt=Radiobutton(self.resourcebar3, 
                                                                        variable = self.displaymode, 
                                                                        value = 'dice',
                                                                        text = 'Dice', 
                                                                        fg="white", 
                                                                        bg='black', 
                                                                        selectcolor='black', 
                                                                        font = 'Courier 10 bold')
                
                self.dicebtt.pack()

                self.Window2.protocol("WM_DELETE_WINDOW", self.blocswitch)
                self.Window2.withdraw()

                self.playerBtts = []
                self.playerBtts2 = []
                self.roll_list=[]
                self.createSidebarButtons()

                self.labelHead = Label(self.mainFrame, bg = 'black', text = self.name, font = "Courier 14 bold", pady=5) 
                self.labelHead.place(relwidth=1)

                self.line = Label(self.mainFrame)                 
                self.line.place(relwidth=1,relheight=0.012,y=36)
                
                self.textCons = Text(self.mainFrame, 
                                                        width = 20, 
                                                        height = 2, 
                                                        bg = 'black',  
                                                        font = "Courier 14", 
                                                        padx = 5, 
                                                        pady = 5) 
                self.textCons.place(y=42, relheight = 0.745, relwidth = 1)

                self.line2 = Label(self.mainFrame)                 
                self.line2.place(relwidth=1,relheight=0.012,y=415)
                
                self.labelBottom = Label(self.mainFrame, bg = 'black', height = 79)     
                self.labelBottom.place(relwidth=1,y=421) 
                
                self.entryMsg = Entry(self.labelBottom, bg = 'black', font = "Courier 12", insertbackground = "white") 
                self.entryMsg.place(width = 417, 
                                                height = 65, 
                                                y = 5, 
                                                x = 5) 
                self.entryMsg.focus() 
                
                self.buttonMsg = Button(self.labelBottom, 
                                                            text = "Send", 
                                                            font = "Courier 12 bold", 
                                                            width = 10, 
                                                            bg = 'black',
                                                            command = lambda : self.sendButton(self.entryMsg.get())) 
                self.buttonMsg.place(x = 428, 
                                            y = 5, 
                                            height = 66, 
                                            width = 126) 
                
                self.rollBtt = Button(self.sidebaroll, 
                                                        text = "Roll", 
                                                        font = "Courier 14 bold", 
                                                        bg = 'black', fg=self.color,
                                                        command = lambda : self.rollerrola()) 
                self.rollBtt.place(relwidth=1, relheight=0.1,rely=0.9)
    
                self.allButton = Button(self.sidebar,
                                    fg = self.color,
                                    bg = 'black', text = 'Select all',
                                    font = "Courier 14 bold",
                                    command=lambda: self.AllClick())
                self.allButton.place(relwidth=1, relheight=0.1,rely=0.9)

                self.textCons.config(cursor = "arrow") 
                self.textCons.config(state = DISABLED) 

                self.Window.bind_all("<MouseWheel>", self.on_mousewheel)
                self.Window.bind('<Return>',(lambda event: self.sendButton(self.entryMsg.get())))
                self.Window.bind("<Up>",self.up_down)
                self.Window.bind("<Down>",self.up_down)
                self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)

                self.Window2.bind('<Return>',(lambda event: self.conversao(self.block_entry.get())))

                self.s = ttk.Style()
                self.s.theme_use('alt')
                self.s.configure("black.Horizontal.TProgressbar", foreground='black', background='black')

        def on_mousewheel(self, event):
            self.textCons.yview_scroll(-1*int(event.delta/120), "units")

        def up_down(self,event):
                if event.keysym == 'Up':
                        self.textCons.yview_scroll(-1,'units')
                if event.keysym == 'Down':
                        self.textCons.yview_scroll(1,'units')

        def colorloop(self):
            global colors
            try:
                while True:
                    for i in range(len(colors)):
                        self.changecolor(i)
                        sleep(0.5)
            except:
                self.on_closing()

        def changecolor(self,i):
            global colors
            self.buttonMsg.config(fg=colors[(i-10)%100])
            self.allButton.config(fg=colors[(i-12)%100])
            self.entryMsg.config(fg=colors[(i-10)%100])
            self.labelHead.config(fg=colors[i])
            self.line.config(bg=colors[(i-2)%100])
            self.line2.config(bg=colors[(i-7)%100])
        
        # function to basically start the thread for sending messages 
        def sendButton(self, msg):
                self.msg=msg 
                self.entryMsg.delete(0, END) 
                snd= threading.Thread(target = self.sendMessage) 
                snd.start() 

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
                                    textlis=wrap(message_final,width=50)
                                    for u in range(len(textlis)):
                                        if textlis[u].startswith('\j'):
                                            textlis[u]=textlis[u].replace('\j','',1)
                                            textlis[u]=textlis[u].rstrip()
                                        else:
                                            textlis[u]=textlis[u].strip()
                                    textlis.append('')
                                    for u in range(len(textlis)-1):
                                        if textlis[u]=='':
                                            self.textCons.insert(END,'\n')
                                        elif textlis[u+1]!='' and not textlis[u+1].startswith(' '):
                                            linha=justify(textlis[u],50)
                                            self.textCons.insert(END, linha+'\n',message.cor)
                                        else:
                                            self.textCons.insert(END, textlis[u]+'\n',message.cor)
                                    self.textCons.insert(END,'\n')
                                    self.textCons.see(END)
                                    self.textCons.config(state = DISABLED)
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
                                elif type(message).__name__=='res':
                                    self.displayres(message)
                                elif type(message).__name__=='status':                                    
                                    if not self.Window2.winfo_viewable():
                                        self.Window2.deiconify()
                                        self.blocbtt.config(text='<')
                                        self.block_entry.focus() 
                                    else:
                                        self.Window2.deiconify()
                                    self.roll_list=[]
                                    if message.num!=0:
                                        self.label.config(text='Restam '+str(message.num)+" rolagens")
                                    else:
                                        self.label.config(text='Select the players to roll')
                                else:
                                    self.players = []
                                    for dics in message:
                                        dics['selected'] = False
                                        self.players.append(dics)
                                    break
                        except:   
                            self.on_closing()
        
        def rolldic(self, dice):
            try:
                dice=dice.replace(" ","")
                dice=dice.replace("-","+-")
                parts=re.findall("(?:(?<=\+)|(?<=^))(-?\d+)d?(\d*)", dice)
                dice=0
                for i in parts:
                    pred=int(i[0])
                    if i[1]:
                        posd=int(i[1])
                        for u in range(abs(pred)):
                            dice+=np.sign(pred)*random.randint(1, posd)
                    else:
                        dice+=pred
                return str(parts)+" = "+str(dice)
            except:
                return "FORMAT ERROR"
                
        # function to send messages 
        def sendMessage(self):
                destinatários = []
                self.msg=re.sub("'.+?'", lambda x: self.rolldic(x.group().replace("'","")), self.msg)
                for player in self.players:
                    if player['selected']:
                        destinatários.append(player['name'])
                message_sent = pickle.dumps(msg(destinatários,self.msg))
                message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(message_sent_header+message_sent)    
        
        def conversao(self, bloco_text):
            self.block_entry.delete(0, END) 
            try:
                bloco_text=bloco_text.replace(" ", "").replace(">,",">").replace("),",")").replace("},","}")

                rec=bloco((int(self.value_entry.get()),int(self.advan_entry.get())),[],self.sn.get())

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
                message_sent = pickle.dumps(rec)
                message_sent_header = f"{len(message_sent):<{HEADER_LENGTH}}".encode(FORMAT)
                client.send(message_sent_header+message_sent)
            except:
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, 'Client > Algo deu errado, confira seu envio.\n\n','#ffffff')
                self.textCons.see(END)
                self.textCons.config(state = DISABLED)
# create a GUI class object
g = GUI()

