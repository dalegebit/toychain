import hashlib
import datetime

class Transaction:
    def __init__(self, from_addr, to_addr, amount):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount

    def __repr__(self):
        return str(self.__dict__)


class Block:
    def __init__(self, data, prev_hash=''):
        self._timestamp = datetime.datetime.now()
        self._data = data
        self.nouce = 0
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        str_obj = (str(self._timestamp) + str(self._data) 
                    + str(self.prev_hash) + str(self.nouce))
        return hashlib.sha256(str_obj.encode()).hexdigest()
    
    def link_prev(self, prev_block):
        self.prev_hash = prev_block.hash
        self.calc_hash()


class BlockChain:
    def __init__(self, chain=[], difficulty=2):
        self.chain = chain
        self.difficulty = difficulty
        self.transactions = []
        if len(self.chain) == 0:
            self.add_gensis()
    
    def add_gensis(self):
        self.chain.append(Block('Genesis', '0'))

    def add_trans(self, transaction):
        self.transactions.append(transaction)

    def mine_block(self, block):
        block.link_prev(self.chain[-1])
        while block.hash[:self.difficulty] != '0' * self.difficulty:
            block.nouce += 1
            block.hash = block.calc_hash()
        self.chain.append(block)

    def mine_trans(self):
        block = Block(self.transactions)
        self.mine_block(block)

    def is_valid(self):
        for prev_block, block in zip(self.chain[:-1], self.chain[1:]):
            if block.hash != block.calc_hash():
                return False
            if block.prev_hash != prev_block.hash:
                return False
        return True
