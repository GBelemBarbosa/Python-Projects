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

def translate_monster(stat):
    stat=stat.lower()
    stat=stat.replace("armor class", "AA")
    stat=re.sub("AA -?\d+", lambda m: "AA "+str(-(int(re.search("-?\d+", m.group()).group())-10)*2), stat)
    # Consume preceding whitespace so we don't double up \n when replacing
    aux = re.search(r'\s*\bstr\b(?:.*?\d+\s*\([+-]?\d+\)){6}', stat, re.DOTALL)
    
    if aux:
        scores=[int(x) for x in re.findall("-?\d+", aux.group())]
        scores2=[int((scores[0]+scores[4]+1)/2)-10, scores[2]-10, int((scores[6]+scores[10]+1)/2)-10, int((scores[8]+scores[10]+1)/2)-10,0]
        bloqueto=str(int((scores[0]+scores[4]+1)/2))+' ('+str(scores2[0])+") "+str(scores[2])+' ('+str(scores2[1])+") "+str(int((scores[6]+scores[10]+1)/2))+' ('+str(scores2[2])+") "+str(int((scores[8]+scores[10]+1)/2))+' ('+str(scores2[3])+") "+str(scores[5])
        
        # Determine if we need a trailing newline based on what follows
        trailing = "\n" if aux.end() < len(stat) and stat[aux.end()] != '\n' else ""
        
        stat=stat[:aux.start()]+"\nBody Senses Mind Soul Vitality\n"+bloqueto+trailing+stat[aux.end():]
        
        aux_perc=re.search("passive perception.+?\n", stat)
        if aux_perc:
            auxau=aux_perc.group()
            # Careful: the original lambda used m.group() indirectly or produced an error. This keeps the logic safe.
            try:
                auxau=re.sub("perception.+?\d+\D", lambda m: skill_swap(m, dic_skill["perception"], "perception", scores, scores2), auxau)
            except: pass
            stat=stat[:aux_perc.start()]+auxau+stat[aux_perc.end():]
            
        if "skills" in stat:
            aux_sk=re.search("skills.+?\n", stat)
            if aux_sk:
                auxau=aux_sk.group()
                for i in dic_skill:
                    auxau=re.sub(i+".+?\d+\D", lambda m: skill_swap(m, dic_skill[i], i, scores, scores2), auxau)
                stat=stat[:aux_sk.start()]+auxau+stat[aux_sk.end():]
                
        # Handle "saving throws" line specifically
        aux_save_line=re.search("saving throws.+?\n", stat)
        if aux_save_line:
            auxau=aux_save_line.group()
            # Find and replace all saves in format "str +5" or "dex -1"
            shorthand_save_map = {'str': 'body', 'dex': 'senses', 'con': 'body', 'int': 'mind', 'wis': 'soul/mind', 'cha': 'soul/mind'}
            scores_idx_map = {'str': (0,1), 'dex': (2,3), 'con': (4,5), 'int': (6,7), 'wis': (8,9), 'cha': (10,11)}
            scores2_idx_map = {'body':0, 'senses':1, 'mind':2, 'soul/mind':3, 'soul':3}
            
            for k, v in shorthand_save_map.items():
                idx_score, idx_mod = scores_idx_map[k]
                g_stat_idx = scores2_idx_map[v]
                
                def save_line_swap(m, k=k, v=v, idx_mod=idx_mod, g_stat_idx=g_stat_idx):
                    match_str = m.group()
                    raw_bonus_str = re.search("-?\d+", match_str).group()
                    dnd_prof_bonus = int(raw_bonus_str) - scores[idx_mod]
                    gray_bonus = (dnd_prof_bonus * 2) + scores2[g_stat_idx]
                    return match_str.replace(k, v).replace(raw_bonus_str, signe(gray_bonus)+str(gray_bonus)).replace("+", "")
                    
                # Matches 'dex +6' or 'con -1' allowing punctuation
                auxau=re.sub(r'\b'+k+r'\s+-?\+?\d+\b', save_line_swap, auxau)
            
            # Reconstruct string
            stat=stat[:aux_save_line.start()]+auxau+stat[aux_save_line.end():]
                
    for i in dic_skill:
        stat=re.sub("dc.+?\d+?.+?"+i+".+?check", lambda m: AC_swap(m, dic_skill[i][2], i), stat, re.DOTALL)
        
    for i in dic_skill:
        stat=re.sub(i+" check", dic_skill[i][2]+" check", stat)
        aux_check=re.findall(" and "+dic_skill[i][2]+" check| or "+dic_skill[i][2]+" check", stat)
        for j in aux_check:
            for p in dic_skill:
                stat=re.sub(p+j, dic_skill[p][2]+j, stat)
                if dic_skill[p][2]+j in stat:
                    stat=chain_gang_chec(p, dic_skill, stat)
                    
    for i in dic_save:
        stat=re.sub("dc.+?\d+?.+?"+i+".+?sav", lambda m: AS_swap(m, dic_save[i], i), stat, re.DOTALL)
        stat=re.sub(i+" \n?\(.+?\)", lambda m: m.group().replace(i+" ", '').replace("(",'').replace(")",""), stat, re.DOTALL)
        
    for i in dic_save:
        stat=re.sub(i+" sav", dic_save[i]+" sav", stat)
        aux_sav=re.findall(" and "+dic_save[i]+" sav| or "+dic_save[i]+" sav", stat)
        for j in aux_sav:
            for p in dic_save:
                stat=re.sub(p+j, dic_save[p]+j, stat)
                if dic_save[p]+j in stat:
                    stat=chain_gang_sav(p, dic_save, stat)
                    
    stat=re.sub(":.+?to hit", lambda m: ": "+"+"*("+" in m.group())+str(int(re.search("-?\d+", m.group()).group())*2)+" to hit", stat, re.DOTALL)
    stat=re.sub("hit points", "pcn", stat, flags=re.IGNORECASE)
    stat=re.sub("hit point", "pcn", stat, flags=re.IGNORECASE)
    return stat

if __name__ == "__main__":
    linha=input()
    stat=linha
    while (linha!=''):
        linha=input()
        stat+="\n"+linha
    print(translate_monster(stat))
