from . import helper
from brownie import KYC, network, config

def deploy():
    account = helper.get_account()
    contract = KYC.deploy({'from': account})
    print("Contract address:", contract.address)

    bank1 = helper.get_account(index=3)
    print("Adding bank to contract")
    add_bank(contract, account, "ICICI", bank1.address)

    bank2 = helper.get_account(index=4)
    print("Adding bank to contract")
    add_bank(contract, account, "HDFC", bank2.address)

    print("Adding customer to bank")
    add_customer_to_bank(contract, bank1, "John", "John's Data", bank1.address)

    print("Adding customer to bank")
    add_customer_to_bank(contract, bank2, "Bob", "Bob's Data", bank2.address)

    print("KYC status of John:", contract.checkKycStatusOfCustomer("John", {'from': bank1}))
    print("KYC status of Bob:", contract.checkKycStatusOfCustomer("Bob", {'from': bank2}))

    print("Performing KYC of John on bank1")
    contract.performKycOfCustomer("John", {'from': bank1})
    print("KYC status of John:", contract.checkKycStatusOfCustomer("John", {'from': bank1}))

    print("Performing KYC of Bob on bank2")
    contract.performKycOfCustomer("Bob", {'from': bank2})
    print("KYC status of Bob:", contract.checkKycStatusOfCustomer("Bob", {'from': bank2}))

def main():
    deploy()

def add_customer_to_bank(contract, account, _custName, _custData, _bankAddress):
    tx = contract.addNewCustomerToBank(_custName, _custData, _bankAddress, {'from': account})
    tx.wait(1)
    print(f"Customer {_custName} added to bank: {_bankAddress}")

def add_bank(contract, account, _bankName, _bankAddress):
    tx = contract.addNewBankToBlockchain(_bankName, _bankAddress, {'from': account})
    tx.wait(1)
    print("Bank added to contract")

