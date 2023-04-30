'''backend file which takes care of the working of the blockchain'''
import hashlib
from time import time
from uuid import uuid4
import json
import requests

class Blockchain:
    '''creating a class for the blockchain'''
    def __init__(self):
        '''init function'''
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Creation of genesis block
        self.create_block(previous_hash=1, proof=100)

    def is_chain_valid(self, chain):
        '''function to check if the given chain is valid'''
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check whether HASH of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.verify_chain(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        '''consesus algorithm'''
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain', timeout= 5000)
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    new_chain = chain
        if new_chain is None:
            return True
        return False

    def create_block(self, proof, previous_hash=None):
        '''function to create a new block'''
        node_identifier = str(uuid4()).replace('-', '')
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'session_key': node_identifier,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def append_transaction(self, party_a , party_b):
        '''function to append a transaction to current node'''
        self.current_transactions.append({
            'Party_A': hash(party_a),   #Voter
            'Party_B': party_b,         #Party
            'Votes': 1
            })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        '''function to return the last block of the chain'''
        return self.chain[-1]

    @staticmethod
    def hash(block):
        '''function to create a SHA-256 hash of a string'''
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        '''proof of work'''
        proof = 0
        while self.verify_chain(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def verify_chain(last_proof, proof):
        '''function to verify the integrity of the chain'''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
