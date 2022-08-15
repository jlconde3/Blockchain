from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.lastBlock
    proof = blockchain.proofOfWrork(last_block)

    blockchain.addTransactions(
        sender="0",
        reciver= "yo",
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.createBlock(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transaction': block['transaction'],
        'proof': block['proof'],
        'previousHash': block['previousHash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'reciver', 'amount']
    if not all (k in values for k in required):
        return 'Missin values', 400

    index = blockchain.addTransactions(values['sender'], values['reciver'], values['amount'])
    response  = {'message': f'Transaction will be added to Block {index}'}
    return jsonify (response), 201

@app.route('/chain', methods = ['GET'])
def chain ():
    response = {
        'blockchain': blockchain.blockchain,
        'lenght': len(blockchain.blockchain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods = ['POST'])
def registerNodes():
    values = request.get_json()
    nodes = values['nodes']

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.newNodes(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/list', methods = ['GET'])
def listingNodes():
    response = {
        'message': 'Nodes',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response)

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolveConflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.blockchain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.blockchain
        }

    return jsonify(response), 200



if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5002)