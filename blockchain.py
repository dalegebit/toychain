import hashlib
import datetime
import json

class Transaction:
    def __init__(self, **kargs):
        self.from_addr = kargs['from_addr']
        self.to_addr = kargs['to_addr']
        self.amount = kargs['amount']

    def __repr__(self):
        return str(self.__dict__)


class Block:
    def __init__(self, **kargs):
        self.timestamp = kargs.get('timestamp', str(datetime.datetime.now()))
        self.transactions = kargs['transactions']
        self.nouce = kargs.get('nouce', 0)
        self.prev_hash = kargs.get('prev_hash', '')
        self.hash = self.calc_hash()

    def calc_hash(self):
        str_obj = (str(self.timestamp) + str(self.transactions) 
                    + str(self.prev_hash) + str(self.nouce))
        return hashlib.sha256(str_obj.encode()).hexdigest()
    
    def link_prev(self, prev_block):
        self.prev_hash = prev_block.hash
        self.calc_hash()
    
    def __repr__(self):
        return str(self.__dict__)

    def to_dict(self):
        d = self.__dict__
        d['transactions'] = [trans.__dict__ for trans in self.transactions]
        return d
    
    def jsonify(self):
        return json.dumps(self.to_dict())


class BlockChain:
    def __init__(self, chain=[], difficulty=2):
        self.chain = chain
        self.difficulty = difficulty
        self.transactions = []
        if len(self.chain) == 0:
            self.add_gensis()
    
    @property
    def last_block(self):
        return self.chain[-1]

    def add_gensis(self):
        self.chain.append(Block(transactions=[], prev_hash='0'))

    def add_trans(self, transaction):
        self.transactions.append(transaction)

    def mine_block(self, block):
        block.link_prev(self.last_block)
        while block.hash[:self.difficulty] != '0' * self.difficulty:
            block.nouce += 1
            block.hash = block.calc_hash()
        self.chain.append(block)

    def mine_trans(self):
        block = Block(transactions=self.transactions)
        self.mine_block(block)

    def get_balance(self, address):
        balance = 0
        for block in self.chain[1:]:
            for transaction in block.transactions:
                if address == transaction.to_addr:
                    balance += transaction.amount
                if address == transaction.from_addr:
                    balance -= transaction.amount
        return balance

    def is_chain_valid(self):
        for prev_block, block in zip(self.chain[:-1], self.chain[1:]):
            if block.hash != block.calc_hash():
                return False
            if block.prev_hash != prev_block.hash:
                return False
        return True
    
    def is_trans_valid(self, transaction):
        from_balance = self.get_balance(transaction.from_addr)
        if from_balance > transaction.amount:
            return True
        return False
    
    def jsonify(self):
        d = self.__dict__
        d['chain'] = [block.to_dict() for block in self.chain]
        return json.dumps(d)


bc = BlockChain()
t1 = Transaction(from_addr='f_addr', to_addr='t_addr', amount=10)
print("This transaction {} is valid? {}".format(str(t1), bc.is_trans_valid(t1)))
bc.mine_trans()
print([block for block in bc.chain])
print("The balance of 'f_addr' is", bc.get_balance('f_addr'))
print(bc.jsonify())