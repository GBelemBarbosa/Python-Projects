import socket
import select
import pickle
import random
import re
from decimal import *
getcontext()
getcontext().prec=20

HEADER_LENGTH = 10

hostname = socket.gethostname()

IP = socket.gethostbyname(hostname)
PORT = 1234
class res:
    def __init__(self,p,crit,r,advan):
        self.p=p
        self.r=r
        self.crit=crit
        self.advan=advan
        self.mods=''

    def __lt__(self, other):
         return self.p < other.p

class status:
    def __init__(self,num):
        self.num=num

class msg:
    def __init__(self,sender,content,cor):
        self.sender=sender
        self.content=content
        self.cor=cor

class roll:
    def __init__(self,receiver,who):
        self.receiver=receiver
        self.who=who

class bloco:
    def __init__(self,premod,posmod,sn,crit):
        self.premod=premod
        self.posmod=posmod
        self.sn=sn
        self.crit=crit

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
    if rolagem['send_type']=='single':
        notifi="Rolagem solo finalizada!"
    else:
        notifi="Rolagem entre "+clients[rolagem['receiver']]['data']+' e '+clients[rolagem['caller']]['data']+" finalizada!"
    if rolagem['send_type']=='hidden':
        notifi1=pickle.dumps(msg('Server',notifi,colore))
        send_new_message(notifi1,rolagem['caller'])
        opposite_message=(rolagem['hidden_message']=='n')*'Sim.'+(rolagem['hidden_message']=='s')*'Não.'
        rolagem['hidden_message']=(rolagem['hidden_message']=='s')*'Sim.'+(rolagem['hidden_message']=='n')*'Não.'
        notifi+='\gResposta: '+(r<=rolagem['p'])*rolagem['hidden_message']+(r>rolagem['p'])*opposite_message
        notifi=pickle.dumps(msg('Server',notifi,colore))
        send_new_message(notifi,rolagem['receiver'])
        print((r<=rolagem['p'])*rolagem['hidden_message']+(r>rolagem['p'])*opposite_message)
        notifi=pickle.dumps(possib)
        send_new_message(notifi,rolagem['caller'])
        send_new_message(notifi,rolagem['receiver'])
    else:
        notifi=pickle.dumps(possib)
        if rolagem['send_type']=='me':
            send_new_message(notifi,rolagem['caller'])
        elif rolagem['send_type']=='you' or rolagem['send_type']=='single':
            send_new_message(notifi,rolagem['receiver'])
        elif rolagem['send_type']=='we':
            send_new_message(notifi,rolagem['caller'])
            send_new_message(notifi,rolagem['receiver'])

def apply_posmod_pre(receiver,fonte,rolagem):
    res_index=0
    for mod in fonte['posmod']:
        #mod=(total de usos, [recurso 1, recurso 2, ...])
        res_index+=1
        pos_res_index=0
        if mod[0]!=0:
            for i in mod[1]:                
                pos_res_index+=1
                #intermediate é []
                if type(i)==list:
                    #advan intermediate é [número de advan., 0]
                    usado=0
                    if i[1]!=0:
                        #const. é c*d1 (i[0]=c, i[1]=1)
                        #dado é x*dy (i[0]=x, i[1]=y)
                        rolagem['p']+=i[0]*(i[1]+1)*25
                        if random.randint(1,80)<=i[0]*(i[1]+1):
                            usado=1
                    else:
                        rolagem['p']+=adv_mod(rolagem['advan']+i[0])-adv_mod(rolagem['advan'])
                        rolagem['advan']+=i[0]
                        if random.randint(1,20)<=3*abs(i[0]):
                            usado=1
                    if usado:
                        mod[0]-=1
                        if rolagem['send_type']=='single':
                            notifi='Usado o #'+str(pos_res_index)+' possível recurso ('+str(i[0])+'d'+str(i[1])+' intermediate) do #'+str(res_index)+' recurso na rolagem solo.'
                        else:
                            notifi='Usado o #'+str(pos_res_index)+' possível recurso ('+str(i[0])+'d'+str(i[1])+' intermediate) do #'+str(res_index)+' recurso na rolagem entre '+clients[rolagem['caller']]['data']+' e '+clients[rolagem['receiver']]['data']+'. Restam '+str(mod[0])+' desse recurso.'
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,receiver)
                        

def apply_posmod_pos(fonte,rolagem,r,possib):
    l=len(possib)
    print(l)
    for mod in fonte['posmod']:
        if mod[0]>0:
            for i in mod[1]:
                print(i)
                print(mod[1])
                #posterior é []
                if type(i)==tuple:
                    #advan posterior é (número de advan., 0)
                    if i[1]!=0:
                        #const. é c*d1 (i[0]=c, i[1]=1)
                        #dado é x*dy (i[0]=x, i[1]=y)
                        possib_aux=[]
                        for j in possib:
                            poss=res(j.p+i[0]*(1+i[1])*25, 0, j.r, j.advan)
                            poss.mods=j.mods+str(i).replace('(','{').replace(')','}')+', '
                            poss.crit=calc_crit(rolagem['crit'], poss.p)
                            possib_aux.append(poss)
                    else:
                        dif=adv_mod(rolagem['advan']+i[0])-adv_mod(rolagem['advan'])
                        possib_aux=[]
                        for j in possib:
                            poss=res(j.p+dif, 0, j.r, j.advan+i[0])
                            poss.mods=j.mods+str(i).replace('(','{').replace(')','}')+', '
                            poss.crit=calc_crit(rolagem['crit'], poss.p)
                            possib_aux.append(poss)
                    possib+=possib_aux
                    mod[1].remove(i)
                    mod[1].append(1)
                    if len(mod[1])>1:
                        if any(isinstance(x, tuple) for x in mod[1]):
                            possib=possib+apply_posmod_pos(fonte,rolagem,r,possib[:l])
                            print(possib)
                        elif 1 in mod[1]:
                            return possib[1:]
                    mod[0]-=1
    if l==1:
        return possib
    else:
        possib[l:]
                    
def rola(rolagem):
    global rolls
    if rolagem['ready']!=2:
        return
    recibru=rolagem['receiver']
    rolagem['p']+=adv_mod(rolagem['advan'])
    r=random.randint(1,2000)
    apply_posmod_pre(recibru,rolagem,rolagem)
    if rolagem['send_type']!='single':
        rolls[recibru].pop()
        caller=rolagem['caller']
        apply_posmod_pre(caller,rolls[caller],rolagem)
        possib=[res(rolagem['p'], calc_crit(rolagem['crit'], rolagem['p']), r, rolagem['advan'])]
        possib=apply_posmod_pos(rolagem,rolagem,r,possib)
        possib=apply_posmod_pos(rolls[caller],rolagem,r,possib)
    else:
        possib=[res(rolagem['p'], calc_crit(rolagem['crit'], rolagem['p']), r, rolagem['advan'])]
        possib=apply_posmod_pos(rolagem,rolagem,r,possib)
    possib.sort()
    send_rolagem(rolagem,possib)

def calc_crit(crit_chance, p):
    return p*crit_chance+(p>2000)*(p-2000)

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
                        notifi=clients[notified_socket]['data']+" desconectou enquanto chamava você. Você não está mais rolando."
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,client_socket)
                        notifi=pickle.dumps(status(0))
                        send_new_message(notifi,client_socket)
                        clients[client_socket]['rolling']=0
                    try:
                        clients[rolls[notified_socket][0]['caller']]['calling'].remove(notified_socket)
                        if clients[rolls[notified_socket][0]['caller']]['calling']==[]:
                            notifi=clients[notified_socket]['data']+" desconectou e era sua única chamada. Você não está mais rolando."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                            notifi=pickle.dumps(status(0))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                            clients[rolls[notified_socket][0]['caller']]['rolling']=0
                        else:
                            notifi=clients[notified_socket]['data']+" desconectou porém você ainda tem chamadas. Você continua rolando."
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
                        messagepf.sender='Privado > '+user['data']
                        message['data']=pickle.dumps(messagepf)
                        message["header"]=f"{len(message['data']):<{HEADER_LENGTH}}".encode('utf-8')
                        for client_socket in clients:
                            if clients[client_socket]['data'] in messagepf.destiny:
                                client_socket.send(message["header"] + message['data'])
                        notified_socket.send(message["header"] + message['data'])

                elif type(messagepf).__name__=='roll' and not user["rolling"]:                       
                        if messagepf.who=='hidden':
                            notifi=pickle.dumps(msg('Server',"Confira o que você espera enviar ao oponente em caso de sucesso dele (Sim ou Não). Repita a rolagem se necessário.",colore))
                            send_new_message(notifi,notified_socket)
                        for client_socket in clients:
                            check=clients[client_socket]['data']
                            roladas=messagepf.receiver.count(check)
                            if roladas:
                                if not clients[client_socket]['rolling']:
                                    clients[client_socket]['rolling']+=roladas
                                    user['calling'].append(client_socket)
                                    notifi=pickle.dumps(msg('Server', check+" encontra-se disponível.",colore))
                                    send_new_message(notifi, notified_socket)
                                    notifi=user['data']+" iniciou "+str(roladas)+" rolagem(ns) com você com a tag "+messagepf.who+'.'+(roladas>1)*"\gRecomenda-se ler o resultado anterior antes de inserir o próximo bloco para evitar repetição de recursos."
                                    notifi=pickle.dumps(msg('Server', notifi,colore))
                                    send_new_message(notifi, client_socket)
                                    notifi=pickle.dumps(status(roladas))
                                    send_new_message(notifi,client_socket)
                                    dic={'advan': 0, 'receiver': client_socket, 'caller': notified_socket, 'ready': 0, 'p':1000, 'send_type': messagepf.who}
                                    rolls[client_socket]=[dic]
                                    for i in range(roladas-1):
                                        dic={'advan': 0, 'receiver': client_socket, 'caller': notified_socket, 'ready': 0, 'p':1000, 'send_type': messagepf.who}
                                        rolls[client_socket].append(dic)
                                else:
                                    notifi=check+" encontra-se indisponível."
                                    notifi=pickle.dumps(msg('Server',notifi,colore))
                                    send_new_message(notifi,notified_socket)
                        if user['calling']:
                            user['rolling']=1
                            rolls[notified_socket]={'send_type':messagepf.who}
                            notifi=pickle.dumps(status(1))
                            send_new_message(notifi,notified_socket)
                        else:
                            notifi="Ninguém aceitou."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,notified_socket)
                
                elif type(messagepf).__name__=='bloco':
                    if user['rolling']:
                        user['rolling']-=1
                        notifi=pickle.dumps(status(user['rolling']))
                        send_new_message(notifi,notified_socket)
                        
                        converted_pos=''
                        for i in messagepf.posmod:
                            converted_pos+="("+str(i[0])+", ["
                            for j in i[1]:
                                if type(j)==list:
                                    converted_pos+="<"+str(j[0])+", "+str(j[1])+">, "
                                else:
                                    converted_pos+="{"+str(j[0])+", "+str(j[1])+"}, "
                            converted_pos=converted_pos[:-2]+"]), "
                        converted_pos=converted_pos[:-2]
                        
                        notifi='Info:\gValue: '+str(messagepf.premod[0])+".\gAdvantage: "+str(messagepf.premod[1])+".\gResources: "+converted_pos+".\gFinalizado! Mais "+str(user['rolling'])+' rolagens.'
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,notified_socket)
                        if not user['calling']:
                            rolls[notified_socket][-1]['posmod']=messagepf.posmod
                            rolls[notified_socket][-1]['p']+=50*messagepf.premod[0]
                            rolls[notified_socket][-1]['advan']+=messagepf.premod[1]
                            rolls[notified_socket][-1]['ready']+=1
                            rola(rolls[notified_socket][-1]) 
                        else:
                            rolls[notified_socket]['posmod']=messagepf.posmod
                            if rolls[notified_socket]['send_type']=='hidden':
                                for called_socket in user['calling']:
                                    for i in range(len(rolls[called_socket])):
                                        rolls[called_socket][i]['hidden_message']=messagepf.sn
                            for called_socket in user['calling']:
                                for i in range(len(rolls[called_socket])):
                                    rolls[called_socket][i]['p']+=50*messagepf.premod[0]
                                    rolls[called_socket][i]['advan']+=messagepf.premod[1]
                                    rolls[called_socket][i]['ready']+=1
                                    rolls[called_socket][i]['crit']=messagepf.crit
                                    rola(rolls[called_socket][i]) 
                        
                        user['calling']=[]
                    else:
                        rola({'advan': messagepf.premod[1], 'receiver': notified_socket, 'crit': messagepf.crit, 'ready': 2, 'p': 1000+50*messagepf.premod[0], 'posmod': messagepf.posmod, 'send_type': 'single'}) 
                            
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
                                    login_message='Username já em uso, tente outro.'

                        if login_message=='ok':
                            if user['data']=='Server' or user['data']=='':
                                login_message='Username não pode ser \'Server\' ou ser em branco, tente outro.'

                        if login_message=='ok':
                            if '\\' in user['data']:
                                login_message='Retire caracteres \ do username.'

                        if login_message=='ok':
                            if len(user['data'])>12:
                                login_message='Username pode conter até 12 caracteres, tente outro.'
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

            


