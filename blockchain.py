import time
import json
from hashlib import sha256
import requests

class Blockchain(object):
    def __init__(self):
        self.listTransactions = []
        self.blockchain = []
        self.nodes = set()

        self.createBlock(previousHash='1',proof = 100)
    
    def createBlock (self, proof, previousHash):
        block = {
            "index": len (self.blockchain) + 1,
            "timestap": time.time(),
            "transaction": self.listTransactions,
            "proof": proof,
            "previousHash": previousHash or hash(self.blockchain[-1])
        }
        self.listTransactions = []
        self.blockchain.append(block)
        return block

    def addTransactions (self, sender, reciver, amount):
        self.listTransactions.append({
            "sender": sender,
            "reciver": reciver,
            "amount": amount
        })
        return self.lastBlock['index'] + 1

    @property
    def lastBlock (self):
        return self.blockchain[-1]

    @staticmethod
    def hash (block):
        blockHash = json.dumps(block, sort_keys = True).encode()
        return sha256(blockHash).hexdigest()
    
    def proofOfWrork (self,lastBlock):
        lastProof = lastBlock['proof']
        proof = 0
        while self.validProof(lastProof,proof) is False:
            proof += 1
        return proof

    @staticmethod             
    def validProof (previousproof,proof):
        guess = f'{previousproof*proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def newNodes (self, url):
        self.nodes.add(url)

    def resolveConflicts(self):
        newChain = None
        actualLength = len(self.blockchain)

        for i in self.nodes:
            response = requests.get(str(i)+'/chain')

            length = response.json()['lenght']
            chain = response.json()['blockchain']

            if length > actualLength and self.valid_chain(chain): 
                actualLength = length
                newChain = chain
    
        if newChain:
            self.blockchain = newChain
            return True

        return False

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previousHash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.validProof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True


