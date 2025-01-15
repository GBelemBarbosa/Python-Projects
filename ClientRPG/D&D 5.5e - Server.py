import socket
import select
import pickle
import random
import re
import itertools
from decimal import *
getcontext()
getcontext().prec=20

HEADER_LENGTH = 10

hostname = socket.gethostname()

IP = socket.gethostbyname(hostname)
PORT = 1234
class res:
    def __init__(self, p, crit, r, adv):
        self.p=p
        self.r=r
        self.crit=crit
        self.adv=adv
        self.mods=''

    def __lt__(self, other):
         return self.p < other.p

class status:
    def __init__(self, num):
        self.num=num

class msg:
    def __init__(self, sender, content, cor):
        self.sender=sender
        self.content=content
        self.cor=cor

class roll:
    def __init__(self, receiver, who):
        self.receiver=receiver
        self.who=who

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

# Create a socket
# socket.AF_INET - address family, IPv4, some other possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

espera_de_cor={}

rolls={}
        
print(f'Listening for connections on {IP}:{PORT}...')

colore='#ffffff'

def adv_mod(adv):
    return (adv>0)*300-(adv<0)*300

def send_new_message(notifi,client_socket):
    notifi_header = f"{len(notifi):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(notifi_header+notifi)

def send_rolagem(rolagem,possib):
    aux=" Info: \gCrit chance: "+str(round(rolagem['crit']*100))+"%;\gMinimum roll: "+str(rolagem['min'])+" out of 2000."
    if rolagem['send_type']=='single':
        notifi="Solo roll finalized!"+aux
        notifi=pickle.dumps(msg('Server', notifi, colore))
    else:
        notifi="Roll between "+clients[rolagem['receiver']]['data']+' and '+clients[rolagem['caller']]['data']+" finalized!"+aux
        notifi=pickle.dumps(msg('Server', notifi, colore))
        send_new_message(notifi, rolagem['caller'])
    send_new_message(notifi, rolagem['receiver'])
    
    if rolagem['send_type']=='hidden':
        possib.append((rolagem['hidden_message']=='s')*'Yes'+(rolagem['hidden_message']=='n')*'No')
        notifi=pickle.dumps(possib)
        send_new_message(notifi, rolagem['caller'])
        send_new_message(notifi, rolagem['receiver'])
    else:
        possib.append("")
        notifi=pickle.dumps(possib)
        if rolagem['send_type']=='me':
            send_new_message(notifi, rolagem['caller'])
        elif rolagem['send_type']=='you' or rolagem['send_type']=='single':
            send_new_message(notifi, rolagem['receiver'])
        elif rolagem['send_type']=='we':
            send_new_message(notifi, rolagem['caller'])
            send_new_message(notifi, rolagem['receiver'])

def apply_posmod_pre(receiver,fonte,rolagem):
    for res in fonte['posmod']:
        if res.qnt>0:
            for i in res.listSubres:                
                if i.timing=="Inter":
                    usado=0
                    if i.typ!="adv":
                        rolagem['p']+=i.value
                        if random.randint(1,2000)<=i.value:
                            usado=1
                    else:
                        rolagem['p']+=adv_mod(rolagem['advan']+i.value)-adv_mod(rolagem['advan'])
                        rolagem['advan']+=i.value
                        if random.randint(1,20)<=3*abs(i.value):
                            usado=1
                    if usado:
                        res.qnt-=1
                        notifi='The possible resource '+i.subresName+' out of '+res.resName+' was used in the '
                        if rolagem['send_type']=='single':
                            notifi+='solo roll.'
                        else:
                            notifi+='roll between '+clients[rolagem['caller']]['data']+' and '+clients[rolagem['receiver']]['data']+'. '+str(mod[0])+' of this resource left.'
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,receiver)

def apply(listSubres, who, mods):
    const=0
    adv=0
    for i in who:
        if i:
            i-=1
            mods+=listSubres[i].subresName+', '
            if listSubres[i].typ!="adv":
                const+=listSubres[i].value
            #advan posterior é (número de advan., 0)
            else:
                adv+=listSubres[i].value
    mods=mods[:-2]+" | "
    return const, adv, mods

def apply_posmod_pos(fonte, rolagem, possib):
    for resource in fonte['posmod']:
        if resource.qnt>0:
            index=[]
            modsAux=resource.resName+": "
            for i in range(len(resource.listSubres)):
                if resource.listSubres[i].timing=="Post":
                    index.append(i+1)
            possib_aux=[]
            whos=set(itertools.combinations(index+[0 for i in range(resource.qnt)], resource.qnt))
            while whos:
                who=whos.pop()
                if any(who):
                    const, adv, mods=apply(resource.listSubres, who, modsAux)
                    for j in possib:
                        dif=adv_mod(j.adv+adv)-adv_mod(j.adv)
                        poss=res(j.p+const+dif, 0, j.r, j.adv+adv)
                        poss.mods=j.mods+mods
                        poss.crit=calc_crit(rolagem['crit'], poss.p)
                        possib_aux.append(poss)
            possib=possib+possib_aux
    return possib
                    
def rola(rolagem):
    global rolls
    if rolagem['ready']!=2:
        return
    recibru=rolagem['receiver']
    rolagem['p']+=adv_mod(rolagem['advan'])
    r=min(random.randint(0, 1999), 2000-rolagem['min'])
    apply_posmod_pre(recibru, rolagem, rolagem)
    if rolagem['send_type']!='single':
        rolls[recibru].pop()
        caller=rolagem['caller']
        apply_posmod_pre(caller, rolls[caller], rolagem)
        possib=[res(rolagem['p'], calc_crit(rolagem['crit'], rolagem['p']), r, rolagem['advan'])]
        possib=apply_posmod_pos(rolagem, rolagem, possib)
        caller_rolls=rolls[caller]
        possib=apply_posmod_pos(caller_rolls, rolagem, possib)
    else:
        possib=[res(rolagem['p'], calc_crit(rolagem['crit'], rolagem['p']), r, rolagem['advan'])]
        possib=apply_posmod_pos(rolagem, rolagem, possib)
    possib.sort()
    send_rolagem(rolagem, possib)

def calc_crit(crit_chance, p):
    return round(p*crit_chance+max(0, 2*(p-2000)/5))

# Handles message receiving
def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)

        # Else existing socket is sending a message
        else:
            if notified_socket in clients:
                # Receive message
                message = receive_message(notified_socket)

                # If False, client disconnected, cleanup
                if message is False:
                        
                    print('Closed connection from: {}.'.format(clients[notified_socket]['data']))
                    for client_socket in clients[notified_socket]['calling']:
                        notifi=clients[notified_socket]['data']+" disconnected while calling you. You're not rolling anymore."
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,client_socket)
                        notifi=pickle.dumps(status(0))
                        send_new_message(notifi,client_socket)
                        clients[client_socket]['rolling']=0
                    try:
                        clients[rolls[notified_socket][0]['caller']]['calling'].remove(notified_socket)
                        if clients[rolls[notified_socket][0]['caller']]['calling']==[]:
                            notifi=clients[notified_socket]['data']+" disconnected and they were your only call. You're not rolling anymore."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                            notifi=pickle.dumps(status(0))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                            clients[rolls[notified_socket][0]['caller']]['rolling']=0
                        else:
                            notifi=clients[notified_socket]['data']+" disconnected but you still have calls. You keep rolling with them."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                    except:
                        pass
                    
                    # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                    newuser=pickle.dumps({'name': clients[notified_socket]['data']})
                    newuser_header=f"{len(newuser):<{HEADER_LENGTH}}".encode('utf-8')
                    
                    # Remove from our list of users
                    del clients[notified_socket]

                    for client_socket in clients:
                        client_socket.send(newuser_header+newuser)

                    continue

                # Get user by notified socket, so we will know who sent the message
                user = clients[notified_socket]
                messagepf=pickle.loads(message["data"])
                
                if type(messagepf).__name__=='msg':
                    messagepf.cor=user['cor']
                    if not messagepf.destiny:
                        messagepf.sender=user['data']
                        message['data']=pickle.dumps(messagepf)
                        message["header"]=f"{len(message['data']):<{HEADER_LENGTH}}".encode('utf-8')
                        for client_socket in clients:
                            client_socket.send(message["header"] + message['data'])
                    else:
                        messagepf.sender=user['data']+" (private)"
                        message['data']=pickle.dumps(messagepf)
                        message["header"]=f"{len(message['data']):<{HEADER_LENGTH}}".encode('utf-8')
                        for client_socket in clients:
                            if clients[client_socket]['data'] in messagepf.destiny:
                                client_socket.send(message["header"] + message['data'])
                        notified_socket.send(message["header"] + message['data'])

                elif type(messagepf).__name__=='roll':
                    if not user["rolling"]:
                        if messagepf.who=='hidden':
                            notifi=pickle.dumps(msg('Server', "Check what you expect to send to the opponent in case of their success (Yes or No). Repeat the roll if necessary.",colore))
                            send_new_message(notifi,notified_socket)
                        for client_socket in clients:
                            check=clients[client_socket]['data']
                            roladas=messagepf.receiver.count(check)
                            if roladas:
                                if not clients[client_socket]['rolling']:
                                    clients[client_socket]['rolling']+=roladas
                                    user['calling'].append(client_socket)
                                    notifi=pickle.dumps(msg('Server', check+" is available.",colore))
                                    send_new_message(notifi, notified_socket)
                                    notifi=user['data']+" started "+str(roladas)+" roll(s) with you with the tag "+messagepf.who+'.'+(roladas>1)*" \gIt is recommended to read the previous result before inserting the next block to avoid repeating resources."
                                    notifi=pickle.dumps(msg('Server',notifi,colore))
                                    send_new_message(notifi, client_socket)
                                    notifi=pickle.dumps(status(roladas))
                                    send_new_message(notifi,client_socket)
                                    dic={'advan': 0, 'receiver': client_socket, 'caller': notified_socket, 'ready': 0, 'p':1000, 'send_type': messagepf.who, 'crit': 0.1, 'min': 0}
                                    rolls[client_socket]=[dic]
                                    for i in range(roladas-1):
                                        dic={'advan': 0, 'receiver': client_socket, 'caller': notified_socket, 'ready': 0, 'p':1000, 'send_type': messagepf.who, 'crit': 0.1, 'min': 0}
                                        rolls[client_socket].append(dic)
                                else:
                                    notifi=check+" is unavailable as it is already rolling."
                                    notifi=pickle.dumps(msg('Server', notifi, colore))
                                    send_new_message(notifi, notified_socket)
                        if user['calling']:
                            user['rolling']=1
                            rolls[notified_socket]={'send_type':messagepf.who}
                            notifi=pickle.dumps(status(1))
                            send_new_message(notifi,notified_socket)
                        else:
                            notifi="Nobody accepted."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,notified_socket)
                    else:
                        notifi="You are already rolling, so you cannot start new rolls."
                        notifi=pickle.dumps(msg('Server', notifi, colore))
                        send_new_message(notifi, notified_socket)
                
                elif type(messagepf).__name__=='bloco':
                    converted_pos=''
                    for i in messagepf.posmods:
                        converted_pos+=i.resName+": "
                        for j in i.listSubres:
                            converted_pos+=j.subresName+', '
                        converted_pos=converted_pos[:-2]+".\g          "
                    converted_pos=converted_pos[:-12]
                    b=(converted_pos.replace(" ", "")!="")
                    notifi='Block received! Block info:\gValue: '+(messagepf.premods.const>0)*"+"+str(messagepf.premods.const)+";\gAdvantage: "+(messagepf.premods.adv>0)*"+"+str(messagepf.premods.adv)+"."*(not b)+(";\gResources: \g          "+converted_pos)*b
                    
                    if user['rolling']:
                        notifi+=" \gAnother "+str(user['rolling'])+' rolls to go.'
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,notified_socket)

                        user['rolling']-=1
                        notifi=pickle.dumps(status(user['rolling']))
                        send_new_message(notifi,notified_socket)
                        if not user['calling']:
                            rolls[notified_socket][-1]['posmod']=messagepf.posmods
                            rolls[notified_socket][-1]['p']+=50*messagepf.premods.const
                            rolls[notified_socket][-1]['advan']+=messagepf.premods.adv
                            rolls[notified_socket][-1]['ready']+=1
                            rolls[notified_socket][-1]['crit']=max(rolls[notified_socket][-1]['crit'], messagepf.crit)
                            rolls[notified_socket][-1]['min']=max(rolls[notified_socket][-1]['min'], messagepf.min)
                            rola(rolls[notified_socket][-1]) 
                        else:
                            rolls[notified_socket]['posmod']=messagepf.posmods
                            if rolls[notified_socket]['send_type']=='hidden':
                                for called_socket in user['calling']:
                                    for i in range(len(rolls[called_socket])):
                                        rolls[called_socket][i]['hidden_message']=messagepf.sn
                            for called_socket in user['calling']:
                                for i in range(len(rolls[called_socket])):
                                    rolls[called_socket][i]['p']+=50*messagepf.premods.const
                                    rolls[called_socket][i]['advan']+=messagepf.premods.adv
                                    rolls[called_socket][i]['ready']+=1
                                    rolls[called_socket][i]['crit']=max(rolls[called_socket][i]['crit'], messagepf.crit)
                                    rolls[called_socket][i]['min']=max(rolls[called_socket][i]['min'], messagepf.min)
                                    rola(rolls[called_socket][i]) 
                        user['calling']=[]
                    else:
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,notified_socket)
                        rola({'advan': messagepf.premods.adv, 'receiver': notified_socket, 'crit': messagepf.crit, 'ready': 2, 'p': 1000+50*messagepf.premods.const, 'posmod': messagepf.posmods, 'send_type': 'single', 'min': messagepf.min}) 
                            
            elif notified_socket in espera_de_cor:
                cor=receive_message(notified_socket)
                if cor is False:
                        sockets_list.remove(notified_socket)
                else:
                    cordec=cor['data'].decode('utf-8')
                    newuser=pickle.dumps({'name': espera_de_cor[notified_socket]['data'], 'color': cordec})
                    newuser_header=f"{len(newuser):<{HEADER_LENGTH}}".encode('utf-8')
                    alreadyuser=[]
                    for client_socket in clients:
                        alreadyuser.append({'name': clients[client_socket]['data'], 'color': clients[client_socket]['cor']})
                        client_socket.send(newuser_header+newuser)
                    # print(alreadyuser)
                    alreadyuser=pickle.dumps(alreadyuser)
                    auser_header=f"{len(alreadyuser):<{HEADER_LENGTH}}".encode('utf-8')
                    notified_socket.send(auser_header+alreadyuser)
                    # Save username and username header                        
                    clients[notified_socket] = espera_de_cor[notified_socket]
                    clients[notified_socket]['calling'] = []
                    clients[notified_socket]['rolling'] = 0
                    clients[notified_socket]['cor']=cordec
                    print('Accepted new connection from user: {}.'.format(clients[notified_socket]['data']))
                del espera_de_cor[notified_socket]
            else:
                    # Client should send his name right away, receive it
                    user = receive_message(notified_socket)

                    # If False - client disconnected before he sent his name
                    if user is False:
                            
                            sockets_list.remove(notified_socket)

                    else:
                        
                        login_message='ok'
                        user['data']=user['data'].decode('utf-8').replace(' ','_')

                        if len(sockets_list)>=10:
                            sockets_list.remove(notified_socket)
                            login_message='Servidor lotado'

                        if login_message=='ok':
                            for socket in clients:
                                if clients[socket]['data']==user['data']:
                                    login_message='Username já em uso, tente outro'

                        if login_message=='ok':
                            if user['data']=='Server' or user['data']=='':
                                login_message='Username não pode ser \'Server\' ou ser em branco, tente outro'

                        if login_message=='ok':
                            if '\\' in user['data']:
                                login_message='Retire caracteres \ do username'

                        if login_message=='ok':
                            if len(user['data'])>12:
                                login_message='Username pode conter até 12 caracteres, tente outro'
                            else:
                                espera_de_cor[notified_socket]=user
            
                        login_message=login_message.encode('utf-8')
                        login_message_header=f"{len(login_message):<{HEADER_LENGTH}}".encode('utf-8')
                        notified_socket.send(login_message_header+login_message)

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]

            


