from brownie import accounts, network

FLC = ['mainnet-fork']
LCBE = ['development', 'ganache-local']

def get_account(index=None, id=None):
    if(index and network.show_active() in LCBE):
        return accounts[index]
    if(id):
        return accounts.load(id);
        
    if(network.show_active() in LCBE or network.show_active() in FLC):
        return accounts[0]
    else:
        return accounts.load('shivam')