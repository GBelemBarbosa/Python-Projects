import re
import numpy
import matplotlib.pyplot as plt
from collections import OrderedDict
import random

#, (-1, 4), (-4, 1)
stri='-1d6-2d8+4+1d6'
stri=stri.replace(' ', '')
stri_con=re.findall('-.*?(?=-|\+|$)', stri)+re.findall('(?=^|\+)(?!-).*?(?=-|\+|$)', stri)
print(stri_con)
dice_list=[]
roll=0
for i in stri_con:
    dice=re.split('d', i)
    if dice[0]:
        dice[0]=int(dice[0])
        if len(dice)>1:
            dice[1]=int(dice[1])
            roll+=dice[0]*random.randint(1, dice[1])
            sgn=numpy.sign(dice[0])
            for j in range(abs(dice[0])):
                dice_list.append((sgn, dice[1]))
        else:
            roll+=dice[0]
            dice_list.append((dice[0], 1))
print(dice_list, roll)
tot=0
num=0
mini=0
for i in dice_list:
    if i[0]>0:
        mini+=max(1, i[0])
        print(max(1, i[0]))
    else:
        mini+=min(-i[1], i[0])
        print(min(-i[1], i[0]))
print(mini)
def rec(tot, num, dice_list, index):
    if index!=len(dice_list)-1:
        if dice_list[index][1]>1:
            dic={}
            if dice_list.index(dice_list[index])==index:
                rep=dice_list.count(dice_list[index])
            else:
                rep=1
            for k in range(1, dice_list[index][1]+1):
                dic_aux=rec(tot+dice_list[index][0]*k, num+1, dice_list, index+1)
                for i in dic_aux.keys():
                    if i in dic.keys():
                        dic[i]+=dic_aux[i]/rep
                    else:
                        dic[i]=dic_aux[i]/rep
            return dic
        else:
            return rec(tot+dice_list[index][0], num, dice_list, index+1)
    else:
        if dice_list[index][1]>1:
            dic={}
            for k in range(1, dice_list[index][1]+1):
                dic[int(tot+dice_list[index][0]*k)]=num+1
            return dic
        else:
            return {tot+dice_list[index][0]: num}
dic=OrderedDict(sorted(rec(tot, num, dice_list, 0).items(), reverse=True))
total=sum(dic.values())
values=[x/total for x in dic.values()]
tot=0
for i in range(len(values)):
    tot+=values[i]
    values[i]=tot
plt.bar(dic.keys(), values, color='g')
plt.bar(roll, values[mini-roll-1], color='r')
plt.show()
        
        
