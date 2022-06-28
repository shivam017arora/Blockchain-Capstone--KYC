from scripts import helper
from scripts.deploy import add_bank, add_customer_to_bank
from brownie import KYC, exceptions
import pytest
from web3 import Web3

def test_can_add_bank_to_blockchain():
    account = helper.get_account()
    contract = KYC.deploy({'from': account})
    print("Contract address:", contract.address)

    bank1 = helper.get_account(index=3)
    print("Adding bank to contract")
    add_bank(contract, account, "ICICI", bank1.address)

    assert contract.banks(bank1.address)['bankName'] == "ICICI"
    with pytest.raises(exceptions.VirtualMachineError):
        add_bank(contract, bank1, "ICICI", bank1.address)

def test_can_block_bank_from_adding_user():
    account = helper.get_account()
    contract = KYC.deploy({'from': account})
    print("Contract address:", contract.address)

    bank1 = helper.get_account(index=3)
    print("Adding bank to contract")
    add_bank(contract, account, "ICICI", bank1.address)

    print("Blocking bank from adding user")
    tx = contract.blockBankFromAddingUser(bank1.address, {'from': account})
    tx.wait(1)

    assert contract.banks(bank1.address)['canAddUser'] == False

def test_can_block_bank_from_kyc_priviledge():
    account = helper.get_account()
    contract = KYC.deploy({'from': account})
    print("Contract address:", contract.address)

    bank1 = helper.get_account(index=3)
    print("Adding bank to contract")
    add_bank(contract, account, "ICICI", bank1.address)

    print("Blocking bank from adding user")
    tx = contract.blockBankFromKyc(bank1.address, {'from': account})
    tx.wait(1)

    assert contract.banks(bank1.address)['kycPrivilege'] == False

def test_can_add_customer_to_bank():
    account = helper.get_account()
    contract = KYC.deploy({'from': account})
    print("Contract address:", contract.address)

    bank1 = helper.get_account(index=3)
    print("Adding bank to contract")
    add_bank(contract, account, "ICICI", bank1.address)

    print("Adding customer to bank")
    add_customer_to_bank(contract, bank1, "John", "John's Data", bank1.address)

    assert contract.customers("John")['customerName'] == "John"
    with pytest.raises(exceptions.VirtualMachineError):
        add_customer_to_bank(contract, account, "Bob", "Bob's Data", bank1.address)
    with pytest.raises(exceptions.VirtualMachineError):
        tx = contract.blockBankFromAddingUser(bank1.address, {'from': account})
        tx.wait(1)
        add_customer_to_bank(contract, bank1, "Tag", "Tag's Data", bank1.address)

def test_perform_kyc():
    account = helper.get_account()
    contract = KYC.deploy({'from': account})
    print("Contract address:", contract.address)

    bank1 = helper.get_account(index=3)
    print("Adding bank to contract")
    add_bank(contract, account, "ICICI", bank1.address)

    print("Adding customer to bank")
    add_customer_to_bank(contract, bank1, "John", "John's Data", bank1.address)
    
    print("KYC status of John:", contract.checkKycStatusOfCustomer("John", {'from': bank1}))
    
    print("Performing KYC of John on bank1")
    tx = contract.performKycOfCustomer("John", {'from': bank1})
    tx.wait(1)
    
    assert contract.checkKycStatusOfCustomer("John", {'from': bank1}) == True
    with pytest.raises(exceptions.VirtualMachineError):
        tx = contract.performKycOfCustomer("John", {'from': account})
        tx.wait(1)
