import re

dic_skill={
    'acrobatics': [3, 1, 'acrobatics'],
    'animal handling': [9, 4, 'animal handling'],
    'arcana': [7, 4, 'arcana'],
    'athletics': [1, 0, 'athletics'],
    'deception': [11, 2, 'simulation'],
    'history': [7, 4, 'lore'],
    'insight': [9, 3, 'awareness'],
    'intimidation': [11, 3, 'trustworthiness'],
    'investigation': [7, 2, 'investigation'],
    'medicine': [9, 4, 'medicine'],
    'nature': [7, 4, 'survival'],
    'perception': [9, 3, 'awareness'],
    'performance': [11, 3, 'performance'],
    'persuasion': [11, 2, 'convincing'],
    'religion': [7, 4, 'religion'],
    'sleight of hand': [3, 1, 'dexterity'],
    'stealth': [3, 1, 'stealth'],
    'survival': [9, 4, 'survival']
}

dic_save={
    'strength': 'body',
    'dexterity': 'senses',
    'constitution': 'body',
    'intelligence': 'mind',
    'charisma': 'soul/mind',
    'wisdom': 'soul/mind'
}

def signe(a):
    return "+"*(a>=0)

def skill_swap(m, entry, i, scores, scores2):
    m=m.group()
    aux=re.search("-?\d+", m).group()
    bonus=2*(int(aux)-scores[entry[0]])+scores2[entry[1]]
    m=m.replace("+", "")
    m=m.replace(aux, signe(bonus)+str(bonus))
    m=m.replace(i, entry[2])
    return m

def AC_swap(m, entry, i):
    m=m.group()
    aux=re.search("-?\d+", m).group()
    bonus=-(int(aux)-10)*2
    m=m.replace(i, entry)
    m=m.replace("+", "")
    m=m.replace(aux, signe(bonus)+str(bonus))
    m=m[:2].replace("dc", "AC")+m[2:]
    return m

def AS_swap(m, entry, i):
    m=m.group()
    aux=re.search("-?\d+", m).group()
    bonus=-(int(aux)-10)*2
    m=m.replace(i, entry)
    m=m.replace("+", "")
    m=m.replace(aux, signe(bonus)+str(bonus))
    m=m[:2].replace("dc", "AS")+m[2:]
    return m

linha=input()
stat=linha
while (linha!=''):
    linha=input()
    stat+="\n"+linha
stat=stat.lower()
stat=stat.replace("armor class", "AA")
stat=re.sub("AA -?\d+", lambda m: "AA "+str(-(int(re.search("-?\d+", m.group()).group())-10)*2), stat)
aux=re.search("\nstr \d.+?cha.+?\)", stat, re.DOTALL)
if aux:
    aux2=re.search("\nstr.+?cha?.*?\n(\d|\(|\)| |\+|-)+", stat, re.DOTALL)
    if aux2:
        if len(aux2.group())>len(aux.group()):
            aux=aux2
else:
    aux=re.search("\nstr.+?cha?.*?\n(\d|\(|\)| |\+|-)+", stat, re.DOTALL)
print(aux.group())
scores=[int(x) for x in re.findall("-?\d+", aux.group())]
scores2=[int((scores[0]+scores[4]+1)/2)-10, scores[2]-10, int((scores[6]+scores[10]+1)/2)-10, int((scores[8]+scores[10]+1)/2)-10,0]
bloqueto=str(int((scores[0]+scores[4]+1)/2))+' ('+str(scores2[0])+") "+str(scores[2])+' ('+str(scores2[1])+") "+str(int((scores[6]+scores[10]+1)/2))+' ('+str(scores2[2])+") "+str(int((scores[8]+scores[10]+1)/2))+' ('+str(scores2[3])+") "+str(scores[5])
stat=stat[:stat.find("\nstr")]+"\nBody Senses Mind Soul Vitality\n"+bloqueto+stat[aux.end():]
aux=re.search("passive perception.+?\n", stat)
auxau=aux.group()
auxau=re.sub("perception.+?\d+\D", lambda m: skill_swap(string(int(m)-10), dic_skill["perception"], "perception", scores, scores2), auxau)
stat=stat[:aux.start()]+auxau+stat[aux.end():]
if "skills" in stat:
    aux=re.search("skills.+?\n", stat)
    auxau=aux.group()
    for i in dic_skill:
        auxau=re.sub(i+".+?\d+\D", lambda m: skill_swap(m, dic_skill[i], i, scores, scores2), auxau)
    stat=stat[:aux.start()]+auxau+stat[aux.end():]
for i in dic_skill:
    stat=re.sub("dc.+?\d+?.+?"+i+".+?check", lambda m: AC_swap(m, dic_skill[i][2], i), stat, re.DOTALL)
def chain_gang_chec(g, dic, stat):
    aux=re.findall(", "+dic[g][2]+" and|, "+dic[g][2]+" or|, "+dic[g][2]+",", stat)
    print(aux)
    if not aux:
        return stat
    for u in aux:
        for p in dic:
            stat=re.sub(p+u, dic[p][2]+u, stat)
            if dic[p][2]+u in stat:
                stat=chain_gang_chec(p, dic, stat)
    return stat
def chain_gang_sav(g, dic, stat):
    aux=re.findall(", "+dic[g]+" and|, "+dic[g]+" or|, "+dic[g]+",", stat)
    print(aux)
    if not aux:
        return stat
    for u in aux:
        for p in dic:
            stat=re.sub(p+u, dic[p]+u, stat)
            if dic[p]+u in stat:
                stat=chain_gang_sav(p, dic, stat)
    return stat
for i in dic_skill:
        stat=re.sub(i+" check", dic_skill[i][2]+" check", stat)
        aux=re.findall(" and "+dic_skill[i][2]+" check| or "+dic_skill[i][2]+" check", stat)
        for j in aux:
            for p in dic_skill:
                stat=re.sub(p+j, dic_skill[p][2]+j, stat)
                if dic_skill[p][2]+j in stat:
                    stat=chain_gang_chec(p, dic_skill, stat)
for i in dic_save:
    stat=re.sub("dc.+?\d+?.+?"+i+".+?sav", lambda m: AS_swap(m, dic_save[i], i), stat, re.DOTALL)
    stat=re.sub(i+" \n?\(.+?\)", lambda m: m.group().replace(i+" ", '').replace("(",'').replace(")",""), stat, re.DOTALL)
for i in dic_save:
        stat=re.sub(i+" sav", dic_save[i]+" sav", stat)
        aux=re.findall(" and "+dic_save[i]+" sav| or "+dic_save[i]+" sav", stat)
        for j in aux:
            for p in dic_save:
                stat=re.sub(p+j, dic_save[p]+j, stat)
                if dic_save[p]+j in stat:
                    stat=chain_gang_sav(p, dic_save, stat)
stat=re.sub(":.+?to hit", lambda m: ": "+"+"*("+" in m.group())+str(int(re.search("-?\d+", m.group()).group())*2)+" to hit", stat, re.DOTALL)
stat=stat.replace("hit points", "pcn")
stat=stat.replace("hit point", "pcn")
print(stat)
