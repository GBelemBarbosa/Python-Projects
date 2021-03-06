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

class status:
    def __init__(self,num):
        self.num=num
class msg:
    def __init__(self,sender,content,cor):
        self.sender=sender
        self.content=content
        self.cor=cor

class roll:
    def __init__(self,receiver,who,crit):
        self.receiver=receiver
        self.who=who
        self.crit=crit

class bloco:
    def __init__(self,premod,posmod,sn):
        self.premod=premod
        self.posmod=posmod
        self.sn=sn

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

def send_rolagem(rolagem,r,crit):
    notifi="Rolagem entre "+clients[rolagem['receiver']]['data']+' e '+str(clients[rolagem['caller']]['data'])
    if rolagem['send_type']=='hidden':
        notifi=notifi+'\gNet Advantage: '+str(rolagem['advan'])
        notifi1=pickle.dumps(msg('Server',notifi,colore))
        send_new_message(notifi1,rolagem['caller'])
        opposite_message=(rolagem['hidden_message']=='n')*'Sim.'+(rolagem['hidden_message']=='s')*'N??o.'
        rolagem['hidden_message']=(rolagem['hidden_message']=='s')*'Sim.'+(rolagem['hidden_message']=='n')*'N??o.'
        notifi+='\gResposta: '+(r<=rolagem['p'])*rolagem['hidden_message']+(r>rolagem['p'])*opposite_message
        notifi=pickle.dumps(msg('Server',notifi,colore))
        send_new_message(notifi,rolagem['receiver'])
        print((r<=rolagem['p'])*rolagem['hidden_message']+(r>rolagem['p'])*opposite_message)
    else:
        if r<=crit:
            notifi+='\gCr??tico \g'
        elif r<=rolagem['p']:
            notifi+='\gSucesso \g'
        else:
            notifi+='\gFracasso \g'
        rolagem['p'],crit,r=2000-rolagem['p'],2000-crit,2000-r
        notifi+='Net Advantage: '+str(rolagem['advan'])+'\gInfo: '+str(r)+' de '+str(rolagem['p'])
        print(notifi)
        notifi=pickle.dumps(msg('Server',notifi,colore))
        notifi2=pickle.dumps(res(rolagem['p'],crit,r,rolagem['advan']))
        if rolagem['send_type']=='me':
            send_new_message(notifi,rolagem['caller'])
            send_new_message(notifi2,rolagem['caller'])
        elif rolagem['send_type']=='you':
            send_new_message(notifi,rolagem['receiver'])
            send_new_message(notifi2,rolagem['receiver'])
        elif rolagem['send_type']=='we':
            send_new_message(notifi,rolagem['caller'])
            send_new_message(notifi2,rolagem['caller'])
            send_new_message(notifi,rolagem['receiver'])
            send_new_message(notifi2,rolagem['receiver'])        

def apply_posmod_pre(receiver,fonte,rolagem):
    for mod in fonte['posmod']:
        #mod=(total de usos, [recurso 1, recurso 2, ...])
        if mod[0]!=0:
            for i in mod[1]:
                #intermediate ?? []
                if type(i)==list:
                    #advan intermediate ?? [n??mero de advan., 0]
                    if i[1]!=0:
                        #const. ?? c*d1 (i[0]=c, i[1]=1)
                        #dado ?? x*dy (i[0]=x, i[1]=y)
                        rolagem['p']+=i[0]*(i[1]+1)*25
                        if random.randint(1,80)<=i[0]*(i[1]+1):
                            mod[0]-=1
                            notifi='Usado o recurso '+str(i[0])+'d'+str(i[1])+' em '+str(mod[1])+' na rolagem entre '+clients[rolagem['caller']]['data']+' e '+clients[rolagem['receiver']]['data']+'. Restam '+str(mod[0])+' desse recurso.'
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,receiver)
                    else:
                        rolagem['p']+=adv_mod(rolagem['advan']+i[0])-adv_mod(rolagem['advan'])
                        rolagem['advan']+=i[0]
                        if random.randint(1,20)<=3*abs(i[0]):
                            mod[0]-=1
                            notifi='Usado o recurso '+str(i[0])+'*Advantage em '+str(mod[1])+' na rolagem entre '+clients[rolagem['caller']]['data']+' e '+clients[rolagem['receiver']]['data']+'. Restam '+str(mod[0])+' desse recurso.'
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,receiver)

def apply_posmod_pos(receiver,fonte,rolagem,r):
    for mod in fonte['posmod']:
        if mod[0]!=0:
            for i in mod[1]:
                #posterior ?? []
                if type(i)==tuple:
                    c=False
                    #advan intermediate ?? (n??mero de advan., 0)
                    if i[1]!=0:
                        #const. ?? c*d1 (i[0]=c, i[1]=1)
                        #dado ?? x*dy (i[0]=x, i[1]=y)
                        if r<=rolagem['p'] and i[0]<0:
                            if r-(rolagem['alin']+1)*i[0]*(i[1]+1)*25+50*rolagem['alin']*i[0]>rolagem['p']:
                                c=True
                        elif r>rolagem['p'] and i[0]>0:
                            if r-(rolagem['alin']+1)*i[0]*(i[1]+1)*25+50*rolagem['alin']*i[0]<=rolagem['p']:
                                c=True
                        if c:
                            mod[0]-=1
                            rolagem['p']+=50*i[0]*random.randint(1, i[1])
                            notifi='Usado o recurso '+str(i)+' em '+mod[1]+' na rolagem entre '+clients[rolagem['caller']]['data']+' e '+clients[rolagem['receiver']]['data']+'. Restam '+str(mod[0])+' desse recurso.'
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,receiver)
                            rolagem['p']+=i*50
                    else:
                        check=adv_mod(rolagem['advan'])
                        check2=adv_mod(rolagem['advan']+i[0])
                        if r<=rolagem['p'] and i[0]<0:
                            if rolagem['p']-check+check2<r:
                                c=True
                            else:
                                rolagem['ready']+=i[0]
                                i[0]=abs(i[0])*'-'
                        elif r>rolagem['p'] and i[0]>0:
                            if rolagem['p']-check+check2>=r:
                                c=True
                            else:
                                rolagem['ready']+=i[0]
                                i[0]=i[0]*'+'
                        if c:
                            rolagem['p']+=(check2-check)
                            mod[0]-=1
                            notifi='Usado o recurso '+str(i[0])+'*Advantage em '+str(mod[1])+' na rolagem entre '+clients[rolagem['caller']]['data']+' e '+clients[rolagem['receiver']]['data']+'. Restam '+str(mod[0])+' desse recurso.'
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,receiver)
                    if mod[0]==0:
                        for i in mod[1]:
                            if type(i[0])==str:
                                rolagem['ready']-=i[0].count("+")-i[0].count("-")
                                i[0]=i[0].count("+")-i[0].count("-")

def backNforth(fonte1, fonte2, r):
    if (fonte1['p']-adv_mod(fonte1['advan'])+adv_mod(fonte1['ready'])>=r)!=(fonte1['p']>=r):
        fonte1+=(adv_mod(fonte1['ready'])-adv_mod(fonte1['advan']))
        fonte1['advan']=fonte1['ready']
    else:
        return
    for fonte in [fonte1, fonte2]:
        for mod in fonte:
            if mod[0]:
                for i in mod[1]:
                    if type(i[0])==str:
                        if mod[0]:
                            if (fonte1['p']+adv_mod(fonte1['advan']-i[0].count("+")+i[0].count("-"))-adv_mod(fonte1['advan'])>=r)==(fonte1['p']>=r):
                                fonte1+=(adv_mod(fonte1['advan']-i[0].count("+")+i[0].count("-"))-adv_mod(fonte1['advan']))
                                fonte1['advan']-=i[0].count("+")-i[0].count("-")
                            else:    
                                mod[0]-=1
                        else:
                            fonte1+=(adv_mod(fonte1['advan']-i[0].count("+")+i[0].count("-"))-adv_mod(fonte1['advan']))
                            fonte1['advan']-=i[0].count("+")-i[0].count("-")

def rola(rolagem):
    global rolls
    if rolagem['ready']!=2:
        return
    caller=rolagem['caller']
    recibru=rolagem['receiver']
    rolls[recibru].pop()
    apply_posmod_pre(recibru,rolagem,rolagem)
    apply_posmod_pre(caller,rolls[caller],rolagem)
    rolagem['p']+=adv_mod(rolagem['advan'])
    r=random.randint(1,2000)
    while True:
        rolagem['ready']=rolagem['advan']
        confere=rolagem['p']
        apply_posmod_pos(recibru,rolagem,rolagem,r)
        apply_posmod_pos(caller,rolls[caller],rolagem,r)
        backNforth(rolagem, rolls[caller], r)
        if confere==rolagem['p']:
            break
    crit=rolagem['p']*rolagem['crit']+(rolagem['p']>2000)*(rolagem['p']-2000)
    send_rolagem(rolagem,r,crit)
            
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
                        notifi=clients[notified_socket]['data']+" desconectou enquanto chamava voc??. Voc?? n??o est?? mais rolando."
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,client_socket)
                        notifi=pickle.dumps(status(0))
                        send_new_message(notifi,client_socket)
                        clients[client_socket]['rolling']=0
                    try:
                        clients[rolls[notified_socket][0]['caller']]['calling'].remove(notified_socket)
                        if clients[rolls[notified_socket][0]['caller']]['calling']==[]:
                            notifi=clients[notified_socket]['data']+" desconectou e era sua ??nica chamada. Voc?? n??o est?? mais rolando."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                            notifi=pickle.dumps(status(0))
                            send_new_message(notifi,rolls[notified_socket][0]['caller'])
                            clients[rolls[notified_socket][0]['caller']]['rolling']=0
                        else:
                            notifi=clients[notified_socket]['data']+" desconectou por??m voc?? ainda tem chamadas. Voc?? continua rolando."
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
                            notifi=pickle.dumps(msg('Server',"Confira o que voc?? espera enviar ao oponente em caso de sucesso dele (Sim ou N??o). Repita a rolagem se necess??rio.",colore))
                            send_new_message(notifi,notified_socket)
                        for client_socket in clients:
                            check=clients[client_socket]['data']
                            roladas=messagepf.receiver.count(check)
                            if roladas:
                                if not clients[client_socket]['rolling']:
                                    clients[client_socket]['rolling']+=roladas
                                    user['calling'].append(client_socket)
                                    notifi=pickle.dumps(msg('Server', check+" encontra-se dispon??vel.",colore))
                                    send_new_message(notifi, notified_socket)
                                    notifi=user['data']+" iniciou "+str(roladas)+" rolagem(ns) com voc?? com a tag "+messagepf.who+(roladas>1)*"\gRecomenda-se ler o resultado anterior para inserir o pr??ximo bloco para evitar repeti????o de recursos."
                                    notifi=pickle.dumps(msg('Server', notifi,colore))
                                    send_new_message(notifi, client_socket)
                                    notifi=pickle.dumps(status(roladas))
                                    send_new_message(notifi,client_socket)
                                    dic={'advan': 0,'receiver': client_socket, 'crit': messagepf.crit, 'caller': notified_socket,'ready':0,'p':1000,'send_type': messagepf.who}
                                    rolls[client_socket]=[dic]
                                    for i in range(roladas-1):
                                        dic={'advan': 0,'receiver': client_socket, 'crit': messagepf.crit, 'caller': notified_socket,'ready':0,'p':1000,'send_type': messagepf.who}
                                        rolls[client_socket].append(dic)
                                else:
                                    notifi=check+" encontra-se indispon??vel."
                                    notifi=pickle.dumps(msg('Server',notifi,colore))
                                    send_new_message(notifi,notified_socket)
                        if user['calling']:
                            user['rolling']=1
                            rolls[notified_socket]={'send_type':messagepf.who}
                            notifi=pickle.dumps(status(1))
                            send_new_message(notifi,notified_socket)
                        else:
                            notifi="Ningu??m aceitou."
                            notifi=pickle.dumps(msg('Server',notifi,colore))
                            send_new_message(notifi,notified_socket)
                
                elif type(messagepf).__name__=='bloco':
                    if user['rolling']:
                        user['rolling']-=1
                        notifi=pickle.dumps(status(user['rolling']))
                        send_new_message(notifi,notified_socket)
                        notifi='Bloco: '+str(messagepf.premod)+str(messagepf.posmod)+"\gFinalizado! Mais "+str(user['rolling'])+' rolagens.'
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
                                    rola(rolls[called_socket][i]) 
                        
                        user['calling']=[]
                    else:
                        notifi="Voc?? n??o se encontra rolando no momento."
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,notified_socket)
                            
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
                                    login_message='Username j?? em uso, tente outro'

                        if login_message=='ok':
                            if user['data']=='Server' or user['data']=='':
                                login_message='Username n??o pode ser Server ou ser em branco, tente outro'

                        if login_message=='ok':
                            if '\\' in user['data']:
                                login_message='Retire caracteres \ do username'

                        if login_message=='ok':
                            if len(user['data'])>12:
                                login_message='Username pode conter at?? 12 caracteres, tente outro'
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

            


