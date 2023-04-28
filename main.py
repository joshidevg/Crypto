'''Blockchain Based Voting'''
import json
from flask import Flask, request, render_template, redirect, url_for
from backend import Blockchain

#Web App named app
app = Flask(__name__)

# Initializing class here
blockchain = Blockchain()

voterID_array = {'VOID001': 1, 'VOID002': 1, 'VOID003': 1,
                 'VOID004': 1, 'VOID005': 1, 'VOID006': 1,
                 'VOID007': 1, 'VOID008': 1, 'VOID009': 1}

minerID_array=['MOID001','MOID002','MOID003']

def add_voter_id(voter_id,voter_password):
    '''function to add voter id'''
    if voter_id != voter_password:
        return -1 # on webpage,it should show a message that Invalid Voter ID or password
    else:
        if voter_id not in voterID_array:
            voterID_array[voter_id] = 1
            return 1 #on webpage, it should show success
        else:
            return 0 #on webpage, it should show that the voterID already exists

def remove_voter_id(voter_id,voter_password):
    '''function to remove voter id (not used)'''
    if voter_id not in voterID_array:
        return -1 # indicates that voterID is not currently registered in the system
    elif voter_id!=voter_password:
        return 0 # indicates that invalid credentials have been entered
    else:
        del voterID_array[voter_id]
        return 1 # indicates that voterID removed successfully from voterID array

def find_voter_id(voter_id):
    '''function to get the status of voter'''
    if voter_id not in voterID_array:
        return -1 # indicates that voterID is not currently registered in the system
    else:
        return voterID_array[voter_id]  # 0 = voted, 1 = not yet voted

def show_current_voters():
    '''returns voter dictionary'''
    return voterID_array

def show_current_miners():
    '''returns the tupple containing all miners'''
    return minerID_array

@app.route('/',methods=['GET','POST'])
def start():
    '''function to call home page'''
    if request.method=='POST':
        print(request.form["submit"])
        if request.form["submit"] == "vote":
            return redirect(url_for('initial'))
        if request.form["submit"] == "mine":
            return redirect(url_for('get_miner'))
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/voter',methods=['POST','GET'])
def initial():
    '''login page for voter'''
    if request.method=='POST':
        user=request.form["voterID"]
        idstat = find_voter_id(user)
        if (idstat == 1) and request.form["submit"]=='new_vote' \
            and request.form["confirm"] == "Confirm":
            return redirect(url_for("put_vote",name=user))
        else:
            return redirect(url_for("control",User="Voter",ID=user))
    else:
        return render_template('initial.html')


@app.route('/<User>_failure/<ID>')
def control(user,id1):
    '''function to renger the failure page'''
    reason = "Unknown Error"
    idstat = find_voter_id(id1)
    if idstat == -1 and id1 not in minerID_array:
        # print("")
        reason = "This "+user+"ID does not exist"
    elif idstat == 0 or (id1 not in minerID_array):
        reason = "You have already voted once"
    return render_template("failure.html",User=user,ID=id1, reason=reason)

@app.route('/put_vote/<name>',methods=['POST','GET'])
def put_vote(name):
    '''function to add vote to the block'''
    idstat = find_voter_id(name)
    if request.method=='POST'and (idstat == 1):
        voterID_array[name] = 0
        option=request.form['vote']
        print(blockchain.chain)
        index = blockchain.new_transaction(name, option)
        print(index)
        return redirect(url_for("vote_done", name = name))
    else:
        return render_template("fillup.html")

@app.route('/put_vote/<name>/success', methods=['GET','POST'])
def vote_done(name):
    '''function to call the success page'''
    if request.method=='POST':
        if request.args.get("Success", False) == "OK":
            # render_template('index.html')
            redirect_url = request.referrer or '/'
            return redirect(redirect_url)
    else:
        return render_template("success.html", UserID = name)

@app.route('/mine/', methods=['GET', 'POST'])
def mine():
    '''function to mine the block'''
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    block = blockchain.new_block(proof)
    data = {
        'message': "New Block Mined",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    response = app.response_class(
        response =json.dumps(data,indent=2),
        status = 200,
        mimetype = 'application/json'
    )
    return response


@app.route('/miner_login/', methods=['GET', 'POST'])
def get_miner():
    '''miner login page'''
    if request.method=='POST':
        user=request.form["MinerID"]
        # print("user = "+str(user))
        # print(user in minerID_array)
        if user in minerID_array and request.form["submit"]=='newMine' \
            and request.form["confirm"]=="Confirm":
            # print(user)
            # print(user in minerID_array)
            return redirect(url_for("mine"))
        else:
            # print(user in minerID_array)
            return redirect(url_for("control",User="Miner",ID=user))
    else:
        return render_template('mine.html')

@app.route('/chain/', methods=['GET'])
def full_chain():
    '''function to see the full chain'''
    # Displays the whole block chain
    data = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        }
    response = app.response_class(
        response = json.dumps(data,indent=2),
        status = 200,
        mimetype = 'application/json'
    )
    return response

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    '''function to render the admin page'''
    if request.method=='POST':
        print(request.form["submit"])
        if request.form["submit"] == "newVoter":
            return redirect(url_for("newvoter"))
        if request.form["submit"] == "result":
            return redirect(url_for('full_chain'))
        else:
            return render_template('admin.html')
    else:
        return render_template('admin.html')

@app.route('/newvoter', methods = ['GET', 'POST'])
def newvoter():
    '''function to add voter to backend'''
    if request.method=='POST':
        user=request.form["voterId"]
        print(user)
        idstat = add_voter_id(user, user)
        print(idstat)
        if idstat != 1:
            print("Already Exists")
            return render_template("failure.html",User="voter",ID=user, reason="ID already exists")
        else:
            print("Added successfuly")
            return render_template("success.html", UserID=user)
    else:
        return render_template('newVoter.html')


if __name__ == '__main__':
    # App starts
    app.run(host='localhost', port=5500, debug=True)
