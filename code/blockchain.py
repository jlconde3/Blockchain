from hashlib import sha256
import time 
import json
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.listTransactions = []
        self.blockchain = []
        #primer bloque de la cadena
        self.createBlock(1,100)
        #conjunto que contiene el total de nodos asociados a la red
        self.nodes = set()

    
    #registrar nuevos nodos en la red
    def newNodes (self, url):
        parsedUrl = urlparse(url)
        self.nodes.add(parsedUrl)


    #Crea un bloque que contiene una lista con las transacciones
    def createBlock (self, proof, previousHash):
        block = {
            "index": len (self.blockchain) + 1,
            "timestap": time.time(),
            "transaction": self.listTransactions,
            "proof": proof,
            "previousHash": previousHash or hash(self.blockchain[-1]) #se genera el hash del bloque anterior al que se crea
        }
        self.blockchain.append(block)
        self.listTransactions = []
        return block

    #Añadir transacciones a la lista de transacciones de un bloque
    def addTransactions (self, sender, reciver, amount):
        self.listTransactions.append({
            "sender": sender,
            "reciver": reciver,
            "amount": amount
        })

        return len (self.blockchain)

    @staticmethod #Método estático, que no afecta ni a la clase ni al método
    def hash (block):
        blockHash = json.dumps(block, sort_keys = True).encode()
        return sha256(blockHash).hexdigest()
    
    #Cuando se mina o crea el bloque se tiene obtener el "proof" que resuelva el problema. Una vez obtenido se inserta el bloque. 
    #El algoritmo a resolver usa el valor del "proof" del último bloque y la variable "proof". 
    
    def proofOfWrork (self,previousproof):
        proof = 0
        while sha256((f"{previousproof * proof}").encode()).hexdigest()[:4] != "0000":
            proof +=1
        return proof
                    