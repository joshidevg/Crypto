import numpy as np

voterID_array = {'VOID001': 1, 'VOID002': 1, 'VOID003': 1,
                 'VOID004': 1, 'VOID005': 1, 'VOID006': 1,
                 'VOID007': 1, 'VOID008': 1, 'VOID009': 1}

minerID_array=['MOID001','MOID002','MOID003']

# print(voterID_array['VOID010'])

def add_voter_id(voter_id,voter_password):
    if(voter_id != voter_password):
        return -1 # on webpage,it should show a message that Invalid Voter ID or password
    else:
        if voter_id not in voterID_array:
            voterID_array[voter_id] = 1
            return 1 #on webpage, it should show success
        else:
            return 0 #on webpage, it should show that the voterID already exists

def remove_voter_id(voter_id,voter_password):
    if(voter_id not in voterID_array):
        return -1 # indicates that voterID is not currently registered in the system
    elif(voter_id!=voter_password):
        return 0; # indicates that invalid credentials have been entered 
    else:
        del(voterID_array[voter_id])
        return 1; # indicates that voterID removed successfully from voterID array

def find_voter_id(voter_id):
    if(voter_id not in voterID_array):
        return -1 # indicates that voterID is not currently registered in the system
    else:
        return voterID_array[voter_id]  # 0 = voted, 1 = not yet voted

def show_current_voters():
    return voterID_array

def show_current_miners():
    return minerID_array