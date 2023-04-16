# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 16:51:15 2023

@author: Dell
"""

voterID_array=[
        'VOID001','VOID002','VOID003',
        'VOID004','VOID005','VOID006',
        'VOID007','VOID008','VOID009',
        'VOID010','VOID011','VOID012',
        'VOID013','VOID014','VOID015']

vote_see_chain=voterID_array.copy()
vote_check=voterID_array.copy()
minerID_array=['MOID001','MOID002','MOID003']

def add_voter_id(voter_id,voter_password):
    if(voter_id==voter_password):
        voterID_array.append(voter_id)
        return 1
    else:
        return 0 # on webpage,it should show a message that Invalid Voter ID or password
        
def remove_voter_id(voter_id,voter_password):
    if(voter_id not in voterID_array):
        return -1 # indicates that voterID is not currently registered in the system
    elif(voter_id!=voter_password):
        return 0;# indicates that invalid credentials have been entered 
    else:
        voterID_array.remove(voter_id)
        return 1; # indicates that voterID removed successfully from voerID array

def add_miner_id(miner_id,miner_password):
    if(miner_id==miner_password):
        minerID_array.append(miner_id)
        return 1
    else:
        return 0 # on webpage,it should show a message that Invalid Voter ID or password
        
def remove_miner_id(miner_id,miner_password):
    if(miner_id not in minerID_array):
        return -1 # indicates that voterID is not currently registered in the system
    elif(miner_id!=miner_password):
        return 0;# indicates that invalid credentials have been entered 
    else:
        minerID_array.remove(miner_id)
        return 1; # indicates that voterID removed successfully from voerID array

def show_current_voters():
    return voterID_array

def show_current_miners():
    return minerID_array