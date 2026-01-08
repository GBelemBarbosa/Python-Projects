import copy
import socket
import select
import pickle
import random
import re
import traceback
import itertools
import threading
import traceback
from datetime import datetime
from decimal import *
getcontext()
getcontext().prec=20

HEADER_LENGTH = 10

hostname = socket.gethostname()

IP = socket.gethostbyname(hostname)
PORT = 1234
class res:
    def __init__(self, p, crit, r, adv, hidden=False):
        self.p=p
        self.r=r
        self.crit=crit
        self.adv=adv
        # Visibility aware fields
        self.vis_adv_caller = adv
        self.vis_adv_receiver = adv
        self.mods=''
        self.mods_button=''
        self.mods_v_caller=''
        self.mods_v_receiver=''
        self.mods_button_v_caller=''
        self.mods_button_v_receiver=''
        self.hidden=hidden
        self.used_info = [] # List of (resName, subresObj) tuples used in this possibility
        # Attribution fields - track who contributed what (for chat display)
        # Each contains what that player added (with visibility filtering for viewer)
        self.caller_ante = ''        # Caller's anterior (full)
        self.caller_ante_v_caller = ''  # Caller's anterior visible to caller
        self.caller_ante_v_receiver = '' # Caller's anterior visible to receiver
        self.receiver_ante = ''
        self.receiver_ante_v_caller = ''
        self.receiver_ante_v_receiver = ''
        self.caller_inter = ''
        self.caller_inter_v_caller = ''
        self.caller_inter_v_receiver = ''
        self.receiver_inter = ''
        self.receiver_inter_v_caller = ''
        self.receiver_inter_v_receiver = ''
        self.caller_post = ''
        self.caller_post_v_caller = ''
        self.caller_post_v_receiver = ''
        self.receiver_post = ''
        self.receiver_post_v_caller = ''
        self.receiver_post_v_receiver = ''

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

def adv_mod(adv):
    return (adv>0)*350-(adv<0)*350

def transl(res_obj):
    """Translate result object to p, crit, r, resultStr for display."""
    p, crit, r = (2000-res_obj.p)/100, (2000-res_obj.crit)/100, (2000-res_obj.r)/100
    if (r >= p):
        if(r >= crit):
            resultStr = "Critical success"
        else:
            resultStr = "Success"
    else:
        if (r < p/2):
            resultStr = "Critical fail"
        else:
            resultStr = "Fail"
    return p, crit, r, resultStr

# Deduplicate tailored possibilities based on the button text the client will see
def deduplicate_tailored(tailored):
    seen = {}  # key -> res with highest p
    for p in tailored:
        if isinstance(p, res):
            key = p.mods_button.replace(r'\g', '').strip()
            if key not in seen or p.p > seen[key].p:
                seen[key] = p
    return list(seen.values())

# Consolidating tailor_possibilities
def tailor_possibilities(possib, is_caller):
    tailored = []
    for p in possib:
        if isinstance(p, res):
            new_p = copy.copy(p)
            new_p.adv = p.vis_adv_caller if is_caller else p.vis_adv_receiver
            new_p.mods = p.mods_v_caller if is_caller else p.mods_v_receiver
            new_p.mods_button = p.mods_button_v_caller if is_caller else p.mods_button_v_receiver
            tailored.append(new_p)
        else:
            tailored.append(p)
    # Deduplicate based on what client will see
    tailored = deduplicate_tailored(tailored)
    tailored.sort()
    return tailored
class roll:
    def __init__(self, receiver, who):
        self.receiver=receiver
        self.who=who

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
        self.subresName=timing+" Adv"*(typ=="adv")+" "+f"{num1:+}"+(typ=="dice")*("d"+str(num2)) + (" (H)" if hidden else "")
        self.hidden=hidden
        
class resourceSend:
    def __init__(self, qnt, resName, listSubres, hidden=False):
        self.qnt=qnt
        self.resName=resName + (" (H)" if hidden else "")
        self.listSubres=listSubres
        self.hidden=hidden

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

# Storage for pending posterior selections (waiting for both players)
# Format: {roll_id: {'caller': socket, 'receiver': socket, 'possib': list, 'caller_sel': None, 'receiver_sel': None, 'send_type': str, 'rolagem': dict}}
pending_posterior = {}
posterior_id_counter = 0

# Lock for synchronized roll processing
sync_lock = threading.Lock()

class posterior_selection:
    def __init__(self, roll_id, selection_index):
        self.roll_id = roll_id  # Unique ID for this roll's posterior selection
        self.selection_index = selection_index  # Index of chosen res option (-1 for N/A)
        
print(f'Listening for connections on {IP}:{PORT}...')

colore='#ffffff'

# Duplicate definitions removed

def send_rolagem(rolagem, possib):
    global posterior_id_counter
    try:
        aux=r" Info: \gCrit chance: "+str(round(rolagem['crit']*100))+r"%; \gMinimum roll: "+str(rolagem['min'])+" out of 2000."
        
        if rolagem['send_type']=='single':
            # Solo roll - Caller is Receiver.
            notifi="Solo roll finalized!"+aux
            notifi=pickle.dumps(msg('Server', notifi, colore))
            send_new_message(notifi, rolagem['receiver'])
            
            roll_id = posterior_id_counter
            posterior_id_counter += 1
            
            pending_posterior[roll_id] = {
                'caller': rolagem['receiver'],
                'caller_name': clients[rolagem['receiver']]['data'],
                'receiver': None,
                'possib': possib.copy(), # Keep untailored version for combine_selections
                'caller_sel': None,
                'receiver_sel': None,
                'send_type': 'single',
                'rolagem': rolagem
            }
            
            # Use Caller view (True) for solo rolls so user sees their own hidden mods with (H)
            tailored = tailor_possibilities(possib, True)
            tailored.append("") # send_type
            tailored.append(roll_id)
            notifi=pickle.dumps(tailored)
            send_new_message(notifi, rolagem['receiver'])
        else:
            # Two-player roll
            notifi="Roll between "+clients[rolagem['receiver']]['data']+' and '+clients[rolagem['caller']]['data']+" finalized! Select your posterior option. "+aux
            notifi=pickle.dumps(msg('Server', notifi, colore))
            send_new_message(notifi, rolagem['caller'])
            send_new_message(notifi, rolagem['receiver'])
            
            roll_id = posterior_id_counter
            posterior_id_counter += 1
            
            pending_posterior[roll_id] = {
                'caller': rolagem['caller'],
                'caller_name': clients[rolagem['caller']]['data'],
                'receiver': rolagem['receiver'],
                'possib': possib.copy(), # Keep untailored version for combine_selections
                'caller_sel': None,
                'receiver_sel': None,
                'send_type': rolagem['send_type'],
                'rolagem': rolagem
            }
            
            if rolagem['send_type']=='hidden':
                possib_caller = tailor_possibilities(possib, True)
                possib_caller.append((rolagem['hidden_message']=='s')*'Yes'+(rolagem['hidden_message']=='n')*'No')
                possib_caller.append(roll_id)
                send_new_message(pickle.dumps(possib_caller), rolagem['caller'])
                
                possib_receiver = tailor_possibilities(possib, False)
                possib_receiver.append("")
                possib_receiver.append(roll_id)
                send_new_message(pickle.dumps(possib_receiver), rolagem['receiver'])
            else:
                if rolagem['send_type']=='we':
                    possib_caller = tailor_possibilities(possib, True)
                    possib_caller.append("")
                    possib_caller.append(roll_id)
                    send_new_message(pickle.dumps(possib_caller), rolagem['caller'])

                    possib_receiver = tailor_possibilities(possib, False)
                    possib_receiver.append("")
                    possib_receiver.append(roll_id)
                    send_new_message(pickle.dumps(possib_receiver), rolagem['receiver'])
                else:
                    # 'me' or 'you' - only one player selects
                    if rolagem['send_type']=='me':
                        # Only caller selects, auto-set receiver to N/A (index 0)
                        pending_posterior[roll_id]['receiver_sel'] = 0
                        tailored = tailor_possibilities(possib, True)
                        tailored.append("")
                        tailored.append(roll_id)
                        send_new_message(pickle.dumps(tailored), rolagem['caller'])
                    elif rolagem['send_type']=='you':
                        # Only receiver selects, auto-set caller to N/A (index 0)
                        pending_posterior[roll_id]['caller_sel'] = 0
                        tailored = tailor_possibilities(possib, False)
                        tailored.append("")
                        tailored.append(roll_id)
                        send_new_message(pickle.dumps(tailored), rolagem['receiver'])
    except Exception as e:
        print(f"ERROR in send_rolagem: {e}")
        print(traceback.format_exc())

def combine_selections(pending):
    """Combine two players' selections to find union of resources used."""
    caller_idx = pending['caller_sel']
    
    # For single rolls, just return the caller's selection
    if pending['send_type'] == 'single':
        return caller_idx if caller_idx != -1 else 0
        
    receiver_idx = pending['receiver_sel']
    possib = pending['possib']
    
    # Get mods strings from both selections (-1 means N/A = empty mods)
    caller_mods = "" if caller_idx == -1 else possib[caller_idx].mods
    receiver_mods = "" if receiver_idx == -1 else possib[receiver_idx].mods
    
    # Parse mods into sets of resource usages
    # Format: "\gResourceName: SubresName, SubresName \gResourceName: SubresName"
    caller_set = set(caller_mods.split(r"\g")) - {"", " "}
    receiver_set = set(receiver_mods.split(r"\g")) - {"", " "}
    
    # Find union
    common = caller_set | receiver_set
    
    # Find the possibility that best matches the common resources
    # If common is empty, use base result (index 0, N/A)
    if not common:
        return 0  # Base result with no posterior mods
    
    # Find possibility with matching mods
    # Ensure leading \gis preserved
    for i, p in enumerate(possib):
        p_mods = getattr(p, 'mods', '') if p else ''
        if set(p_mods.split(r"\g")) - {"", " "} == common:
            return i
    
    # Fallback to base if no exact match
    return 0

def tailor_final_result(res_obj, is_caller):
    new_res = copy.copy(res_obj)
    new_res.adv = res_obj.vis_adv_caller if is_caller else res_obj.vis_adv_receiver
    new_res.mods = res_obj.mods_v_caller if is_caller else res_obj.mods_v_receiver
    return new_res

def send_final_result(roll_id):
    """Process combined selections and send final result to both players."""
    pending = pending_posterior[roll_id]
    possib = pending['possib']
    send_type = pending['send_type']
    rolagem = pending['rolagem']
    
    try:
        # Combine selections
        final_idx = combine_selections(pending)
        final_res = possib[final_idx]
        
        # Create final result message for display
        # Format: [single res object, send_type, roll_id]
        final_possib = [final_res]
        
        # Notify about used posterior resources
        for res_name, subres in final_res.used_info:
            # Find parent resource to decrement qnt
            for res_obj in rolagem['posmod']:
                if res_obj.resName == res_name:
                    res_obj.qnt -= 1
                    
                    sub_name = subres.subresName + (" (H)" if subres.hidden and " (H)" not in subres.subresName else "")
                    par_name = res_name + (" (H)" if res_obj.hidden and " (H)" not in res_name else "")
                    notifi = 'The possible resource ' + sub_name + ' out of ' + par_name + ' was used in the '
                    if send_type == 'single':
                        notifi += 'solo roll.'
                    else:
                        notifi += 'roll between ' + clients[pending['receiver']]['data'] + ' and ' + clients[pending['caller']]['data'] + '. ' + str(res_obj.qnt) + ' of this resource left.'
                    
                    notifi_pickle = pickle.dumps(msg('Server', notifi, colore))
                    
                    # Broadcast or Notify owner
                    if not subres.hidden:
                        for client_id, client_info in clients.items():
                            send_new_message(notifi_pickle, client_id)
                    else:
                        # Find owner socket (caller if it was their resource, else receiver)
                        # The pending dict has 'caller' and 'receiver'.
                        # We need to know who added this resource.
                        # Wait, is_caller was passed to apply_posmod_pos.
                        # I should probably store that too.
                        # For now, let's just notify the player who selected it if we can't be sure, 
                        # but usually posterior resources are added by the caller or receiver in their own steps.
                        # Since it's hidden, only the owner should see it anyway.
                        # We'll send to both players involved if we can't distinguish, 
                        # but better to find the socket.
                        send_new_message(notifi_pickle, pending['caller'])
                        if send_type != 'single':
                             send_new_message(notifi_pickle, pending['receiver'])
        
        if send_type == 'hidden':
            # Caller gets Yes/No, receiver gets empty
            res_c = tailor_final_result(final_res, True)
            final_possib_caller = [res_c, (rolagem['hidden_message']=='s')*'Yes'+(rolagem['hidden_message']=='n')*'No']
            notifi_caller = pickle.dumps(('final_result', final_possib_caller, pending['caller_name']))
            send_new_message(notifi_caller, pending['caller'])
            
            res_r = tailor_final_result(final_res, False)
            final_possib_receiver = [res_r, "hidden"]
            notifi_receiver = pickle.dumps(('final_result', final_possib_receiver, pending['caller_name']))
            send_new_message(notifi_receiver, pending['receiver'])
        else:
            if send_type == 'me':
                res_c = tailor_final_result(final_res, True)
                notifi = pickle.dumps(('final_result', [res_c, ""], pending['caller_name']))
                send_new_message(notifi, pending['caller'])
            elif send_type == 'you':
                res_r = tailor_final_result(final_res, False)
                notifi = pickle.dumps(('final_result', [res_r, ""], pending['caller_name']))
                send_new_message(notifi, pending['receiver'])
            elif send_type == 'we':
                res_c = tailor_final_result(final_res, True)
                notifi_c = pickle.dumps(('final_result', [res_c, ""], pending['caller_name']))
                send_new_message(notifi_c, pending['caller'])
                
                res_r = tailor_final_result(final_res, False)
                notifi_r = pickle.dumps(('final_result', [res_r, ""], pending['caller_name']))
                send_new_message(notifi_r, pending['receiver'])
            elif send_type == 'single':
                # Solo roll - notify caller (who is the only player)
                res_c = tailor_final_result(final_res, True)
                notifi = pickle.dumps(('final_result', [res_c, ""], pending['caller_name']))
                send_new_message(notifi, pending['caller'])
        
        # Broadcast personalized chat messages to all clients
        # Get the result values
        p, crit, r, resultStr = transl(final_res)
        limits_msg = r" \nLimits: \gCF: "+str(round(p/2))+r"; \gS: "+str(int(p))+r"; \gCS: "+str(int(crit))+r"; \gRolled: "+str(int(r))
        
        # Tailor messages for caller, receiver, and other clients
        res_c = tailor_final_result(final_res, True)
        res_r = tailor_final_result(final_res, False)
        
        caller_name = pending['caller_name']
        receiver_name = clients[pending['receiver']]['data'] if pending['receiver'] and pending['receiver'] in clients else 'Unknown'
        
        # Check if any hidden resources were used
        caller_has_hidden = final_res.mods != res_r.mods  # Receiver can't see all of caller's mods
        receiver_has_hidden = final_res.mods != res_c.mods  # Caller can't see all of receiver's mods
        
        if send_type == 'hidden':
            prefix = f"[{caller_name}] Hidden roll result: "
            base_msg = prefix + resultStr + r"."
        elif send_type == 'single':
            prefix = f"[{caller_name}] Roll result: "
            base_msg = prefix + resultStr + r"."
        else:
            prefix = f"[{caller_name} vs {receiver_name}] Roll result: "
            base_msg = prefix + resultStr + r"."
        
        for client_socket in clients:
            # Build attributed resource string for this viewer
            attributed_resources = ""
            hidden_note = ""
            
            # Solo roll - simpler format without attribution brackets
            if send_type == 'single':
                if client_socket == pending['caller']:
                    if final_res.caller_ante_v_caller:
                        attributed_resources += r" \nAnterior: " + final_res.caller_ante_v_caller
                    if final_res.caller_inter_v_caller:
                        attributed_resources += r" \nIntermediate: " + final_res.caller_inter_v_caller
                    if final_res.caller_post_v_caller:
                        attributed_resources += r" \nPosterior: " + final_res.caller_post_v_caller
                    # Solo player can see if they had hidden resources
                    if final_res.hidden:
                        hidden_note = r" \n(Contains hidden resources)"
                else:
                    # Other clients watching solo roll
                    if final_res.caller_ante_v_receiver:
                        attributed_resources += r" \nAnterior: " + final_res.caller_ante_v_receiver
                    if final_res.caller_inter_v_receiver:
                        attributed_resources += r" \nIntermediate: " + final_res.caller_inter_v_receiver
                    if final_res.caller_post_v_receiver:
                        attributed_resources += r" \nPosterior: " + final_res.caller_post_v_receiver
                    if final_res.hidden:
                        hidden_note = r" \n(Some resources were hidden)"
            elif client_socket == pending['caller']:
                # Caller sees: their own ante/inter/post (with H), receiver's non-hidden
                if final_res.caller_ante_v_caller:
                    attributed_resources += rf" \n[{caller_name}'s] Anterior: " + final_res.caller_ante_v_caller
                if final_res.receiver_ante_v_caller:
                    attributed_resources += rf" \n[{receiver_name}'s] Anterior: " + final_res.receiver_ante_v_caller
                if final_res.caller_inter_v_caller:
                    attributed_resources += rf" \n[{caller_name}'s] Intermediate: " + final_res.caller_inter_v_caller
                if final_res.receiver_inter_v_caller:
                    attributed_resources += rf" \n[{receiver_name}'s] Intermediate: " + final_res.receiver_inter_v_caller
                if final_res.caller_post_v_caller:
                    attributed_resources += rf" \n[{caller_name}'s] Posterior: " + final_res.caller_post_v_caller
                if final_res.receiver_post_v_caller:
                    attributed_resources += rf" \n[{receiver_name}'s] Posterior: " + final_res.receiver_post_v_caller
                hidden_note = r" \n(Some resources were hidden from your opponent)" if receiver_has_hidden else ""
                
            elif client_socket == pending['receiver']:
                # Receiver sees: their own ante/inter/post (with H), caller's non-hidden
                if final_res.caller_ante_v_receiver:
                    attributed_resources += rf" \n[{caller_name}'s] Anterior: " + final_res.caller_ante_v_receiver
                if final_res.receiver_ante_v_receiver:
                    attributed_resources += rf" \n[{receiver_name}'s] Anterior: " + final_res.receiver_ante_v_receiver
                if final_res.caller_inter_v_receiver:
                    attributed_resources += rf" \n[{caller_name}'s] Intermediate: " + final_res.caller_inter_v_receiver
                if final_res.receiver_inter_v_receiver:
                    attributed_resources += rf" \n[{receiver_name}'s] Intermediate: " + final_res.receiver_inter_v_receiver
                if final_res.caller_post_v_receiver:
                    attributed_resources += rf" \n[{caller_name}'s] Posterior: " + final_res.caller_post_v_receiver
                if final_res.receiver_post_v_receiver:
                    attributed_resources += rf" \n[{receiver_name}'s] Posterior: " + final_res.receiver_post_v_receiver
                hidden_note = r" \n(Some resources were hidden from your opponent)" if caller_has_hidden else ""
            else:
                # Other clients see only non-hidden from both
                if final_res.caller_ante_v_receiver:  # Use receiver's view as public
                    attributed_resources += rf" \n[{caller_name}'s] Anterior: " + final_res.caller_ante_v_receiver
                if final_res.receiver_ante_v_caller:
                    attributed_resources += rf" \n[{receiver_name}'s] Anterior: " + final_res.receiver_ante_v_caller
                if final_res.caller_inter_v_receiver:
                    attributed_resources += rf" \n[{caller_name}'s] Intermediate: " + final_res.caller_inter_v_receiver
                if final_res.receiver_inter_v_caller:
                    attributed_resources += rf" \n[{receiver_name}'s] Intermediate: " + final_res.receiver_inter_v_caller
                if final_res.caller_post_v_receiver:
                    attributed_resources += rf" \n[{caller_name}'s] Posterior: " + final_res.caller_post_v_receiver
                if final_res.receiver_post_v_caller:
                    attributed_resources += rf" \n[{receiver_name}'s] Posterior: " + final_res.receiver_post_v_caller
                hidden_note = r" \n(Some resources were hidden)" if (caller_has_hidden or receiver_has_hidden) else ""
            
            if not attributed_resources:
                attributed_resources = r" \nNo resources used."
            
            if send_type == 'hidden' or final_res.hidden:
                chat_msg = base_msg + attributed_resources + hidden_note
            else:
                chat_msg = base_msg + attributed_resources + limits_msg + hidden_note
            
            broadcast_msg = pickle.dumps(msg('Server', chat_msg, colore))
            send_new_message(broadcast_msg, client_socket)
        
        # Clean up
        if roll_id in pending_posterior:
            del pending_posterior[roll_id]
    except Exception:
        print(f"ERROR in send_final_result ({roll_id}):")
        print(traceback.format_exc())

def apply_posmod_pre(receiver,fonte,rolagem, is_caller_adding):
    full_list = []
    v_c_list = []
    v_r_list = []
    h_adv = 0
    for res in fonte['posmod']:
        if res.qnt>0:
            for i in res.listSubres:                
                if i.timing=="Inter":
                    usado=0
                    if i.typ=="dice":
                        rolagem['p']+=i.value 
                        if random.randint(1,2000)<=i.value:
                            usado=1
                    elif i.typ!="adv":
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
                        
                        m_text = res.resName + ": " + i.subresName
                        full_list.append(m_text)
                        
                        if not i.hidden or is_caller_adding:
                            v_c_list.append(m_text)
                        if not i.hidden or not is_caller_adding:
                            v_r_list.append(m_text)
                            
                        if i.typ == 'adv' and i.hidden:
                            h_adv += i.value

                        sub_name = i.subresName + (" (H)" if i.hidden and " (H)" not in i.subresName else "")
                        par_name = res.resName + (" (H)" if res.hidden and " (H)" not in res.resName else "")
                        notifi='The possible resource ' + sub_name + ' out of ' + par_name + ' was used in the '
                        if rolagem['send_type']=='single':
                            notifi+='solo roll.'
                        else:
                            notifi+='roll between '+clients[rolagem['receiver']]['data']+' and '+clients[rolagem['caller']]['data']+'. '+str(res.qnt)+' of this resource left.'
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                    
                        # Broadcast to ALL connected clients if resource is NOT hidden
                        if not i.hidden:
                            for client_id, client_info in clients.items():
                                send_new_message(notifi, client_id)
                        else:
                            # If hidden, notify owner only
                            owner_socket = rolagem['caller'] if is_caller_adding else receiver
                            send_new_message(notifi, owner_socket)
    return full_list, v_c_list, v_r_list, h_adv
def apply(listSubres, res_name, res_hidden, who, is_caller_adding):
    const=0
    adv=0
    
    # Calculate visible advantage for both players
    v_adv_caller = 0
    v_adv_receiver = 0
    
    # Calculate visible mods for both players
    m_base = r"\g" + res_name + ": "
    m_v1 = m_base if (not res_hidden or is_caller_adding) else ""
    m_v2 = m_base if (not res_hidden or not is_caller_adding) else ""
    
    actual_mods = m_base
    
    used_res_info = []
    for i in who:
        if i:
            i-=1
            sub = listSubres[i]
            used_res_info.append((res_name, sub))
            
            # Dynamically ensure (H) marker is correct based on current hidden status
            # Strip potential existing (H) to avoid double marking or stale marker
            base_name = sub.subresName.replace(" (H)", "")
            sub_name = base_name + (" (H)" if sub.hidden else "")
            
            actual_mods += sub_name + ', '
            
            if m_v1:
                # Mod owner sees their hidden subres; others only see non-hidden
                if not sub.hidden or is_caller_adding:
                    m_v1 += sub_name + ', '
            if m_v2:
                if not sub.hidden or not is_caller_adding:
                    m_v2 += sub_name + ', '
                    
            if sub.typ != "adv":
                const += sub.value
            else:
                adv += sub.value
                if not sub.hidden or is_caller_adding:
                    v_adv_caller += sub.value
                if not sub.hidden or not is_caller_adding:
                    v_adv_receiver += sub.value

    # Clean up trailing separators
    if m_v1.endswith(', '): m_v1 = m_v1[:-2]
    elif m_v1 == m_base: m_v1 = ""
    
    if m_v2.endswith(', '): m_v2 = m_v2[:-2]
    elif m_v2 == m_base: m_v2 = ""
    
    return const, adv, actual_mods[:-2], v_adv_caller, v_adv_receiver, m_v1, m_v2, used_res_info

def apply_posmod_pos(fonte, rolagem, possib, is_caller=True):
    # Check for hidden anterior resources (if stored in rolagem)
    hidden_anterior = False
    if 'premods' in rolagem:
         for item in rolagem['premods'].items:
             if item.hidden:
                 hidden_anterior = True
                 break

    for resource in fonte['posmod']:
        if resource.qnt>0:
            index=[]
            for i in range(len(resource.listSubres)):
                if resource.listSubres[i].timing=="Post":
                    index.append(i+1)
            possib_aux=[]
            whos=set(itertools.combinations(index+[0 for i in range(resource.qnt)], resource.qnt))
            while whos:
                who=whos.pop()
                if any(who):
                    hidden_res = False
                    for idx in who:
                        if idx > 0 and resource.listSubres[idx-1].hidden:
                            hidden_res = True
                            break
                    
                    const, adv, mods, v_adv_c, v_adv_r, m_v_c, m_v_r, used_res_info = apply(resource.listSubres, resource.resName, resource.hidden, who, is_caller)
                    for j in possib:
                        dif=adv_mod(j.adv+adv)-adv_mod(j.adv)
                        # Inherit hidden status
                        is_hidden = j.hidden or hidden_res or hidden_anterior
                        poss=res(j.p+const+dif, 0, j.r, j.adv+adv, hidden=is_hidden)
                        # Store used resource info for later notification
                        poss.used_info = j.used_info + used_res_info
                        
                        # Set visibility fields
                        poss.vis_adv_caller = j.vis_adv_caller + v_adv_c
                        poss.vis_adv_receiver = j.vis_adv_receiver + v_adv_r
                        
                        # Handle mod strings (accumulate visible parts with headers)
                        pos_header = r" \nPosterior resources: "
                        
                        poss.mods = (j.mods.strip() + pos_header + mods.strip()).strip()
                        poss.mods_v_caller = (j.mods_v_caller.strip() + (pos_header if m_v_c.strip() else "") + m_v_c.strip()).strip()
                        poss.mods_v_receiver = (j.mods_v_receiver.strip() + (pos_header if m_v_r.strip() else "") + m_v_r.strip()).strip()
                        
                        poss.mods_button = (j.mods_button.strip() + ", " + mods.strip()).strip(', ')
                        poss.mods_button_v_caller = (j.mods_button_v_caller.strip() + ", " + m_v_c.strip()).strip(', ')
                        poss.mods_button_v_receiver = (j.mods_button_v_receiver.strip() + ", " + m_v_r.strip()).strip(', ')
                        
                        # Copy attribution fields from parent
                        poss.receiver_ante = j.receiver_ante
                        poss.receiver_ante_v_caller = j.receiver_ante_v_caller
                        poss.receiver_ante_v_receiver = j.receiver_ante_v_receiver
                        poss.caller_ante = j.caller_ante
                        poss.caller_ante_v_caller = j.caller_ante_v_caller
                        poss.caller_ante_v_receiver = j.caller_ante_v_receiver
                        poss.receiver_inter = j.receiver_inter
                        poss.receiver_inter_v_caller = j.receiver_inter_v_caller
                        poss.receiver_inter_v_receiver = j.receiver_inter_v_receiver
                        poss.caller_inter = j.caller_inter
                        poss.caller_inter_v_caller = j.caller_inter_v_caller
                        poss.caller_inter_v_receiver = j.caller_inter_v_receiver
                        
                        # Accumulate posterior attribution based on who is adding
                        if is_caller:
                            poss.caller_post = (j.caller_post.strip() + " " + mods.strip()).strip()
                            poss.caller_post_v_caller = (j.caller_post_v_caller.strip() + " " + m_v_c.strip()).strip()
                            poss.caller_post_v_receiver = (j.caller_post_v_receiver.strip() + " " + m_v_r.strip()).strip()
                            poss.receiver_post = j.receiver_post
                            poss.receiver_post_v_caller = j.receiver_post_v_caller
                            poss.receiver_post_v_receiver = j.receiver_post_v_receiver
                        else:
                            poss.receiver_post = (j.receiver_post.strip() + " " + mods.strip()).strip()
                            poss.receiver_post_v_caller = (j.receiver_post_v_caller.strip() + " " + m_v_c.strip()).strip()
                            poss.receiver_post_v_receiver = (j.receiver_post_v_receiver.strip() + " " + m_v_r.strip()).strip()
                            poss.caller_post = j.caller_post
                            poss.caller_post_v_caller = j.caller_post_v_caller
                            poss.caller_post_v_receiver = j.caller_post_v_receiver

                        poss.crit=calc_crit(rolagem['crit'], poss.p)
                        possib_aux.append(poss)
            possib=possib+possib_aux
    
    # Clean up empty spaces and normalize mod strings
    for p in possib:
        p.mods = p.mods.strip()
        p.mods_v_caller = p.mods_v_caller.strip()
        p.mods_v_receiver = p.mods_v_receiver.strip()

    return possib
                    
def rola(rolagem, caller_mods_source=None):
    global rolls
    if rolagem['ready']!=2:
        return
    recibru=rolagem['receiver']
    # Use local variable instead of modifying rolagem['p'] in place
    roll_p = rolagem['p'] + adv_mod(rolagem['advan'])
    r=min(random.randint(0, 1999), 2000-rolagem['min'])
    # Build anterior mods strings for visibility
    ante_mods_v_caller = ""
    ante_mods_v_receiver = ""
    full_ante_mods = ""
    
    # Track hidden advantage contributions separately
    receiver_hidden_adv = 0
    caller_hidden_adv = 0    
    
    # 1. Intermediate resources (Receiver/Participant)
    rec_inter_full, rec_inter_v_c, rec_inter_v_r, rec_h_adv = apply_posmod_pre(recibru, rolagem, rolagem, False)
    receiver_hidden_adv += rec_h_adv

    hidden_anterior = False
    
    # Attribution tracking - receiver's anterior
    receiver_ante_full = ""
    receiver_ante_v_c = ""  # What caller can see of receiver's ante
    receiver_ante_v_r = ""  # What receiver can see (their own ante)
    
    # 2. Process receiver's premods (Anterior)
    if 'premods' in rolagem and rolagem['premods'].items:
        v_caller = []
        v_receiver = []
        full = []
        for item in rolagem['premods'].items:
            # rolagem['premods'] contains Receiver's anterior items
            m_text = r""
            if item.typ == 'c': m_text = f"{item.val1:+}"
            elif item.typ == 'adv': m_text = f"Adv: {item.val1:+}"
            elif item.typ == 'dice': m_text = f"{item.val1}d{item.val2}"
            
            if item.hidden:
                hidden_anterior = True
                full.append(m_text + " (H)")
                v_receiver.append(m_text + " (H)") # Owner sees it with (H) marker
                if item.typ == 'adv':
                    receiver_hidden_adv += item.val1
            else:
                full.append(m_text)
                v_receiver.append(m_text)
                v_caller.append(m_text) # Others see non-hidden
            
            # Broadcast usage notification for each sub-resource used
            notifi_text = 'The possible resource ' + (m_text + (" (H)" if item.hidden else "")) + ' was used in the '
            if rolagem['send_type'] == 'single':
                notifi_text += 'solo roll.'
            else:
                notifi_text += 'roll between ' + clients[rolagem['receiver']]['data'] + ' and ' + clients[rolagem['caller']]['data'] + '.'
            
            notifi_pickle = pickle.dumps(msg('Server', notifi_text, colore))
            if not item.hidden:
                for client_id, client_info in clients.items():
                    send_new_message(notifi_pickle, client_id)
            else:
                # Notify receiver (owner of these premods)
                send_new_message(notifi_pickle, rolagem['receiver'])
        
        # Build attributed strings for receiver's anterior
        if full: 
            full_ante_mods = r" \nAnterior: \g" + r" \g".join(full)
            receiver_ante_full = r" \g" + r" \g".join(full)
        if v_caller: 
            ante_mods_v_caller = r" \nAnterior: \g" + r" \g".join(v_caller)
            receiver_ante_v_c = r" \g" + r" \g".join(v_caller)
        if v_receiver: 
            ante_mods_v_receiver = r" \nAnterior: \g" + r" \g".join(v_receiver)
            receiver_ante_v_r = r" \g" + r" \g".join(v_receiver)

    # 3. Process caller's premods if available (Anterior)
    # Attribution tracking - caller's anterior
    caller_ante_full = ""
    caller_ante_v_c = ""
    caller_ante_v_r = ""
    
    if caller_mods_source and 'premods' in caller_mods_source and caller_mods_source['premods'].items:
        c_full = []
        c_v_caller = []
        c_v_receiver = []
        for item in caller_mods_source['premods'].items:
            # caller_mods_source['premods'] contains Caller's anterior items
            m_text = ""
            if item.typ == 'c': m_text = f"{item.val1:+}"
            elif item.typ == 'adv': m_text = f"Adv: {item.val1:+}"
            elif item.typ == 'dice': m_text = f"{item.val1}d{item.val2}"
            
            if item.hidden:
                hidden_anterior = True
                c_full.append(m_text + " (H)")
                c_v_caller.append(m_text + " (H)") # Caller sees it with (H) marker
                if item.typ == 'adv':
                    caller_hidden_adv += item.val1
            else:
                c_full.append(m_text)
                c_v_caller.append(m_text)
                c_v_receiver.append(m_text) # Receiver sees non-hidden
            
            # Broadcast usage notification for each sub-resource used
            notifi_text = 'The possible resource ' + (m_text + (" (H)" if item.hidden else "")) + ' was used in the '
            if rolagem['send_type'] == 'single':
                notifi_text += 'solo roll.'
            else:
                notifi_text += 'roll between ' + clients[rolagem['receiver']]['data'] + ' and ' + clients[rolagem['caller']]['data'] + '.'
            
            notifi_pickle = pickle.dumps(msg('Server', notifi_text, colore))
            if not item.hidden:
                for client_id, client_info in clients.items():
                    send_new_message(notifi_pickle, client_id)
            else:
                # Notify caller (owner of these premods)
                send_new_message(notifi_pickle, rolagem['caller'])
        
        # Build attributed strings for caller's anterior
        if c_full:
            caller_ante_full = r" \g" + r" \g".join(c_full)
            if full_ante_mods:
                full_ante_mods += r" \g" + r" \g".join(c_full)
            else:
                full_ante_mods = r" \gAnterior resources: \g" + r" \g".join(c_full)
        if c_v_caller:
            caller_ante_v_c = r" \g" + r" \g".join(c_v_caller)
            if ante_mods_v_caller:
                ante_mods_v_caller += r" \g" + r" \g".join(c_v_caller)
            else:
                ante_mods_v_caller = r" \gAnterior resources: \g" + r" \g".join(c_v_caller)
        if c_v_receiver:
            caller_ante_v_r = r" \g" + r" \g".join(c_v_receiver)
            if ante_mods_v_receiver:
                ante_mods_v_receiver += r" \g" + r" \g".join(c_v_receiver)
            else:
                ante_mods_v_receiver = r" \gAnterior resources: \g" + r" \g".join(c_v_receiver)

    # 4. Intermediate resources (Caller)
    call_inter_full, call_inter_v_c, call_inter_v_r, call_h_adv = [], [], [], 0
    if rolagem['send_type']!='single':
        caller=rolagem['caller']
        call_inter_full, call_inter_v_c, call_inter_v_r, call_h_adv = apply_posmod_pre(caller, rolls[caller], rolagem, True)
    
    caller_hidden_adv += call_h_adv

    # Capture final Anterior+Intermediate total BEFORE posterior mods are calculated
    actual_ante_adv = rolagem['advan']

    initial_res = res(roll_p, calc_crit(rolagem['crit'], roll_p), r, actual_ante_adv, hidden=hidden_anterior)
    
    # Construct Detail strings (Full vs Visible)
    initial_res.mods = full_ante_mods
    initial_res.mods_v_caller = ante_mods_v_caller
    initial_res.mods_v_receiver = ante_mods_v_receiver
    
    # Set attribution fields for anterior
    initial_res.receiver_ante = receiver_ante_full
    initial_res.receiver_ante_v_caller = receiver_ante_v_c
    initial_res.receiver_ante_v_receiver = receiver_ante_v_r
    initial_res.caller_ante = caller_ante_full
    initial_res.caller_ante_v_caller = caller_ante_v_c
    initial_res.caller_ante_v_receiver = caller_ante_v_r
    
    # Set attribution fields for intermediate
    if rec_inter_full:
        initial_res.receiver_inter = r" \g" + r" \g".join(rec_inter_full)
    if rec_inter_v_c:
        initial_res.receiver_inter_v_caller = r" \g" + r" \g".join(rec_inter_v_c)
    if rec_inter_v_r:
        initial_res.receiver_inter_v_receiver = r" \g" + r" \g".join(rec_inter_v_r)
    if call_inter_full:
        initial_res.caller_inter = r" \g" + r" \g".join(call_inter_full)
    if call_inter_v_c:
        initial_res.caller_inter_v_caller = r" \g" + r" \g".join(call_inter_v_c)
    if call_inter_v_r:
        initial_res.caller_inter_v_receiver = r" \g" + r" \g".join(call_inter_v_r)
    
    if rec_inter_full or call_inter_full:
        inter_f = r" \nIntermediate resources: \g" + r" \g".join(rec_inter_full + call_inter_full)
        inter_v_c = r" \nIntermediate resources: \g" + r" \g".join(rec_inter_v_c + call_inter_v_c) if (rec_inter_v_c or call_inter_v_c) else ""
        inter_v_r = r" \nIntermediate resources: \g" + r" \g".join(rec_inter_v_r + call_inter_v_r) if (rec_inter_v_r or call_inter_v_r) else ""
        
        initial_res.mods += inter_f
        initial_res.mods_v_caller += inter_v_c
        initial_res.mods_v_receiver += inter_v_r

    # mods_button gets NOTHING for Anterior/Intermediate (clean button)
    initial_res.mods_button = ""
    initial_res.mods_button_v_caller = ""
    initial_res.mods_button_v_receiver = ""
    
    # vis_adv shows the player's Visible Total Advantage
    # (Actual Total - What they can't see)
    initial_res.vis_adv_caller = actual_ante_adv - receiver_hidden_adv
    initial_res.vis_adv_receiver = actual_ante_adv - caller_hidden_adv
    
    if rolagem['send_type']!='single':
        rolls[recibru].pop()
        possib = [initial_res]
        # Receiver's posterior mods (is_caller=False)
        possib=apply_posmod_pos(rolagem, rolagem, possib, is_caller=False)
        # Caller's posterior mods (is_caller=True)
        caller_rolls=rolls[caller]
        possib=apply_posmod_pos(caller_rolls, rolagem, possib, is_caller=True)
    else:
        possib = [initial_res]
        # Solo roll: Caller is Receiver
        possib=apply_posmod_pos(rolagem, rolagem, possib, is_caller=True)
    
    # Deduplicate possibilities based on button text
    # If two options show the same button text, they're duplicates (keep highest p)
    seen = {}  # key -> res with highest p for that key
    print(f"DEBUG DEDUP: Total before: {len(possib)}", flush=True)
    for i, p in enumerate(possib):
        # Use the button text that will be displayed (stripped of \g formatting)
        # This matches how the client displays: mods_button.replace(r'\g', '').strip()
        key = p.mods_button.replace(r'\g', '').strip()
        
        print(f"  [{i}] p={p.p}, key='{key}'", flush=True)
        
        if key not in seen:
            seen[key] = p
        else:
            # Keep the one with higher p (better outcome)
            if p.p > seen[key].p:
                print(f"    -> REPLACING previous (higher p)", flush=True)
                seen[key] = p
            else:
                print(f"    -> DROPPED (duplicate, lower or equal p)", flush=True)
    
    possib = list(seen.values())
    print(f"DEBUG DEDUP: Total after: {len(possib)}", flush=True)
    
    possib.sort()
    send_rolagem(rolagem, possib)

def calc_crit(crit_chance, p):
    return round(p*crit_chance+max(0, 2*(p-2000)/5))

def send_new_message(message_data, socket_dest):
    message_header = f"{len(message_data):<{HEADER_LENGTH}}".encode('utf-8')
    socket_dest.send(message_header + message_data)

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
                    if messagepf.destiny == ['broadcast_roll_result']:
                        messagepf.sender='Server'
                        messagepf.cor=colore
                        message['data']=pickle.dumps(messagepf)
                        message["header"]=f"{len(message['data']):<{HEADER_LENGTH}}".encode('utf-8')
                        for client_socket in clients:
                            client_socket.send(message["header"] + message['data'])
                    else:
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
                            if client_socket == notified_socket:
                                continue # Caller doesn't need to be notified as a receiver
                            check=clients[client_socket]['data']
                            roladas=messagepf.receiver.count(check)
                            if roladas:
                                if not clients[client_socket]['rolling']:
                                    clients[client_socket]['rolling']+=roladas
                                    user['calling'].append(client_socket)
                                    notifi=pickle.dumps(msg('Server', check+" is available.",colore))
                                    send_new_message(notifi, notified_socket)
                                    notifi=user['data']+" started "+str(roladas)+" roll(s) with you with the tag "+messagepf.who+'.'+(roladas>1)*r" \gIt is recommended to read the previous result before inserting the next block to avoid repeating resources."
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
                        # Owner sees ALL their resources, including hidden ones with (H) marker
                        visible_subres = []
                        for j in i.listSubres:
                            # subresName already has (H) appended if j.hidden from posmod.__init__
                            visible_subres.append(j.subresName)
                        if visible_subres:
                            # Add (H) marker to parent resource name if hidden
                            res_h_marker = " (H)" if (i.hidden if hasattr(i, 'hidden') else False) else ""
                            converted_pos+=i.resName + res_h_marker + ": " + r', '.join(visible_subres) + r"; \g"

                    b=(converted_pos.replace(" ", "")!="")
                    if b:
                        # Remove trailing "; \g" and replace with "."
                        converted_pos = converted_pos[:-4] + "."
                    
                    # Build anterior text - each item on its own line for proper \gparsing
                    visible_ante = []
                    if messagepf.premods.items:
                        for item in messagepf.premods.items:
                            # Owner sees ALL their items, hidden ones get (H) marker
                            h_marker = " (H)" if item.hidden else ""
                            if item.typ == 'c': visible_ante.append(rf"{item.val1:+}{h_marker}")
                            elif item.typ == 'adv': visible_ante.append(rf"Adv: {item.val1:+}{h_marker}")
                            elif item.typ == 'dice': visible_ante.append(rf"{item.val1}d{item.val2}{h_marker}")
                    
                    # Use \gseparator so each item gets proper green formatting
                    ante_text = (r" \nAnterior: \g" + r"; \g".join(visible_ante)) if visible_ante else ""
                    notifi=r'Block received!'+ante_text+"."*(not b)+(r". \nResources: \g"+converted_pos)*b
                    
                    if user['rolling']:
                        user['rolling']-=1
                        notifi+=r" \nAnother "+str(user['rolling'])+' roll(s) to go.'
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi, notified_socket)
                        notifi=pickle.dumps(status(user['rolling']))
                        send_new_message(notifi,notified_socket)
                        if not user['calling']:
                            rolls[notified_socket][-1]['posmod']=messagepf.posmods
                            rolls[notified_socket][-1]['premods']=messagepf.premods
                            rolls[notified_socket][-1]['p']+=50*messagepf.premods.const
                            rolls[notified_socket][-1]['advan']+=messagepf.premods.adv
                            rolls[notified_socket][-1]['ready']+=1
                            rolls[notified_socket][-1]['crit']=max(rolls[notified_socket][-1]['crit'], messagepf.crit)
                            rolls[notified_socket][-1]['min']=max(rolls[notified_socket][-1]['min'], messagepf.min)
                            # Get caller mods from rolls if they exists
                            caller_socket = rolls[notified_socket][-1]['caller']
                            caller_mods = rolls[caller_socket] if (caller_socket in rolls and 'premods' in rolls[caller_socket]) else None
                            rola(rolls[notified_socket][-1], caller_mods) 
                        else:
                            rolls[notified_socket]['posmod']=messagepf.posmods
                            rolls[notified_socket]['premods']=messagepf.premods
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
                                    rola(rolls[called_socket][i], rolls[notified_socket]) 
                        user['calling']=[]
                    else:
                        notifi=pickle.dumps(msg('Server',notifi,colore))
                        send_new_message(notifi,notified_socket)
                        rola({'advan': messagepf.premods.adv, 'receiver': notified_socket, 'crit': messagepf.crit, 'ready': 2, 'p': 1000+50*messagepf.premods.const, 'posmod': messagepf.posmods, 'send_type': 'single', 'min': messagepf.min, 'premods': messagepf.premods}, None) 
                
                elif type(messagepf).__name__=='posterior_selection':
                    try:
                        # Handle posterior selection from player
                        roll_id = messagepf.roll_id
                        selection_idx = messagepf.selection_index
                        
                        if roll_id in pending_posterior:
                            with sync_lock:
                                # Re-check inside lock to handle concurrent processing
                                if roll_id in pending_posterior:
                                    pending = pending_posterior[roll_id]
                                    
                                    # Determine if this is caller or receiver
                                    if notified_socket == pending['caller']:
                                        pending['caller_sel'] = selection_idx
                                        
                                        if pending['send_type'] == 'single':
                                            send_final_result(roll_id)
                                        else:
                                            notifi = pickle.dumps(msg('Server', "Selection received. Waiting for opponent...", colore))
                                            send_new_message(notifi, notified_socket)
                                            
                                    elif notified_socket == pending['receiver']:
                                        pending['receiver_sel'] = selection_idx
                                        notifi = pickle.dumps(msg('Server', "Selection received. Waiting for opponent...", colore))
                                        send_new_message(notifi, notified_socket)
                                    
                                    # Check if both have selected (only if entry still exists)
                                    if roll_id in pending_posterior and pending['caller_sel'] is not None and pending['receiver_sel'] is not None:
                                        # Both selected - send final result
                                        send_final_result(roll_id)
                        else:
                            notifi = pickle.dumps(msg('Server', "Error: Roll not found.", colore))
                            send_new_message(notifi, notified_socket)
                    except Exception:
                        print(f"ERROR in posterior_selection handler:")
                        print(traceback.format_exc())
                            
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
                            login_message='Server full'

                        if login_message=='ok':
                            for socket in clients:
                                if clients[socket]['data']==user['data']:
                                    login_message='Username already in use, try another'

                        if login_message=='ok':
                            if user['data']=='Server' or user['data']=='':
                                login_message='Username cannot be \'Server\' or blank, try another'

                        if login_message=='ok':
                            if '\\' in user['data']:
                                login_message=r'Remove \ characters from username'

                        if login_message=='ok':
                            if len(user['data'])>12:
                                login_message='Username can contain up to 12 characters, try another'
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

            


