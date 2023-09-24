import hashlib
import time


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = self.build_tree(transactions)

    def build_tree(self, transactions):
        if len(transactions) % 2 == 1:
            transactions.append(transactions[-1])

        tree = [hashlib.sha256((transactions[i] + transactions[i + 1]).encode()).hexdigest() for i in range(0, len(transactions), 2)]

        if len(tree) > 1:
            return self.build_tree(tree)
        else:
            return tree[0]

    def get_root(self):
        return self.tree


class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.merkle_tree = MerkleTree(transactions)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()


def create_genesis_block():
    return Block(0, "0", int(time.time()), ["Genesis Transaction"])


class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


my_blockchain = Blockchain()
my_blockchain.add_block(Block(1, "", int(time.time()), ["Transaction Data 1", "Transaction Data 2"]))
my_blockchain.add_block(Block(2, "", int(time.time()), ["Transaction Data 3"]))

for block in my_blockchain.chain:
    print(f"Block {block.index}:")
    print(f"Timestamp: {block.timestamp}")
    print(f"Transactions: {block.transactions}")
    print(f"Merkle Tree Root: {block.merkle_tree.get_root()}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print()
