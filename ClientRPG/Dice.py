from tkinter import *
from PIL import ImageTk, Image
from time import sleep
import random
from math import exp
from math import floor, ceil

class res:
    def __init__(self,p,crit,r,advan):
        self.p=p
        self.r=r
        self.crit=crit
        self.advan=advan

testRes = res(1000, 1900, 2000, 0)

def diceRollingWindow(roll):

    window = Tk()

    minRollLabel = Label(window, text='', font=('Courier', 12))
    minRollLabel.pack()
    critRollLabel = Label(window, text='', font=('Courier', 12))
    critRollLabel.pack()
    realRollLabel = Label(window, text='', font=('Courier', 12))
    realRollLabel.pack()

    ResultLabel = Label(window, text='', font=('Courier', 25), fg='#f00')
    ResultLabel.pack()

    panel = Label(window)
    panel.pack()

    #Assumindo os significados em res:
    # res.p = o minimo necessario na rolagem para passar
    # res.r = o valor rolado
    # res.crit = o minimo necessario na rolagem para critar

    #Valores em linguagem d20:
    # realRoll = roll.r/100
    # minRoll = roll.p/100
    # critRoll = roll.crit/100

    minRollLabel.config(text = "Precisa: "+str(roll.p/100))
    critRollLabel.config(text = "Crítico a partir de: "+str(roll.crit/100))

    ##### CONSTANTES PARA ADEQUACAO DOS TEMPOS DE ROLAGEM (EM 10^-2s)
    minST = 1               #ST = sleepTime
    maxST = 10
    minMST = 60             #MST = maxSleepTime
    maxMST = 100    
    incrementFraction = 1/10    #sometimes not used


    sleepTime = random.randint(minST,maxST)/100
    maxSleepTime = random.randint(minMST,maxMST)/100
    
    def nextSleepTime(currentTime, limitTime): # 3 opcoes de incremento de tempo
        # return currentTime + currentTime**2 / 2
        # return currentTime + incrementFraction*currentTime
        return currentTime + limitTime * (1-exp(-currentTime * incrementFraction))


    currentRoll = random.randint(1, 20)
    img = False
    while maxSleepTime-sleepTime > 0.1 and maxSleepTime > sleepTime:
        rolagem = random.randint(1, 20)
        while rolagem == currentRoll:
            rolagem = random.randint(1, 20)

        currentRoll = rolagem

        del img

        img = Image.open("Dice_Images/"+str(rolagem)+".png")
        img = img.resize((250,250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.config(image = img)

        window.update_idletasks()
        window.update()
        
        sleep(sleepTime)
        sleepTime = nextSleepTime(sleepTime, maxSleepTime)

    sleep(maxMST/100 - maxSleepTime)

    resultStr = "FALHA"
    roundedRealDiceRoll = floor(roll.r/100)
    if(roll.r >= roll.p):
        roundedRealDiceRoll = ceil(roll.r/100)
        if(roll.r >= roll.crit):
            resultStr = "SUCESSO CRÍTICO"
        else:
            resultStr = "SUCESSO"

    img = Image.open("Dice_Images/"+str(roundedRealDiceRoll)+".png")
    img = img.resize((250,250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.config(image = img)


    realRollLabel.config(text = "Rolou: "+str(roll.r/100))

    ResultLabel.config(text = resultStr)

    window.focus()

    window.mainloop()


diceRollingWindow(testRes)
