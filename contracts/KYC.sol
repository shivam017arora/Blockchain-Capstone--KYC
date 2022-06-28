//SPDX-Licence-Identifier: MIT

/*
Problem Proposed:
KYC (Know Your Customer) is a service provided by financial institutions such as banks. 
There are both public and private sector banks managed by a central bank. 
These banks are banned by the central bank from adding any new customer and do any more customer KYCs as they see suspicious activities that need to be sorted out first. 
Despite this, the banks add new customers and do the KYC in the background.

Solution Proposed:
An immutable solution is needed where the central bank maintains a list of all the banks 
and tracks which banks are allowed to add new customers and perform KYC. 
It can also track which customer KYC is completed or pending along with customer details.

Banks can also add the new customer if allowed and do the KYC of the customers.

*/

pragma solidity 0.6.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract KYC is Ownable {
    // given Bank will have these properties
    struct Bank {
        string bankName;
        address bankAddress;
        uint256 kycCount;
        bool canAddUser;
        bool kycPrivilege;
    }
    // given Customer will have these properties
    struct Customer {
        string customerName;
        string customerData;
        address customerBank;
        bool kycStatus;
    }

    // bank address => bank type
    mapping(address => Bank) public banks;
    // customer address => customer type
    mapping(string => Customer) public customers;

    function addNewBankToBlockchain(
        string memory _bankName,
        address _bankAddress
    ) public onlyOwner {
        /*
        Add a new bank to the blockchain. This function can be called by admin only.
        Args: 
            _bankName: name of the bank
            _bankAddress: unique eth address of the bank
        */
        Bank memory bank = Bank({
            bankName: _bankName,
            bankAddress: _bankAddress,
            kycCount: 0,
            canAddUser: true,
            kycPrivilege: true
        });
        banks[_bankAddress] = bank;
    }

    function blockBankFromKyc(address _bankAddress) public onlyOwner {
        /*
        Block a bank from adding new customers and performing KYC. This function can be called by admin only.
        Args: 
            _bankAddress: unique eth address of the bank
        */
        Bank memory bank = banks[_bankAddress];
        bank.kycPrivilege = false;
        banks[_bankAddress] = bank;
    }

    function blockBankFromAddingUser(address _bankAddress) public onlyOwner {
        /*
        Block a bank from adding new customers. This function can be called by admin only.
        Args: 
            _bankAddress: unique eth address of the bank
        */
        Bank memory bank = banks[_bankAddress];
        bank.canAddUser = false;
        banks[_bankAddress] = bank;
    }

    function allowBankFromKyc(address _bankAddress) public onlyOwner {
        /*
        Allow a bank to add new customers and perform KYC. This function can be called by admin only.
        Args: 
            _bankAddress: unique eth address of the bank
        */
        Bank memory bank = banks[_bankAddress];
        bank.kycPrivilege = true;
        banks[_bankAddress] = bank;
    }

    function allowBankFromAddingUser(address _bankAddress) public onlyOwner {
        /*
        Allow a bank to add new customers. This function can be called by admin only.
        Args: 
            _bankAddress: unique eth address of the bank
        */
        Bank memory bank = banks[_bankAddress];
        bank.canAddUser = true;
        banks[_bankAddress] = bank;
    }

    function addNewCustomerToBank(
        string memory _custName,
        string memory _custData,
        address _bankAddress
    ) public {
        /*
        Add a new customer to a bank. This can only be called by the bank itself.
        Args: 
            _custName: name of the customer
            _custData: data of the customer
            _bankAddress: unique eth address of the bank
        */
        Bank memory bank = banks[_bankAddress];

        require(msg.sender == _bankAddress);
        require(bank.canAddUser == true);

        if (bank.canAddUser) {
            Customer memory customer = Customer({
                customerName: _custName,
                customerData: _custData,
                customerBank: _bankAddress,
                kycStatus: false
            });
            customers[_custName] = customer;
            bank.kycCount++;
            banks[_bankAddress] = bank;
        }
    }

    function checkKycStatusOfCustomer(string memory _custName)
        public
        view
        returns (bool)
    {
        /*
        Check if the KYC of the customer is true or false. This can only be called by the bank itself.
        Args: 
            _custName: name of the customer
        */
        require(msg.sender == customers[_custName].customerBank);
        Customer memory customer = customers[_custName];
        return customer.kycStatus;
    }

    function performKycOfCustomer(string memory _custName) public {
        /*
        Perform the KYC of the customer. This can only be called by the bank itself.
        Args: 
            _custName: name of the customer
        */
        require(msg.sender == customers[_custName].customerBank);
        if (banks[msg.sender].kycPrivilege) {
            Customer memory customer = customers[_custName];
            customer.kycStatus = true;
            customers[_custName] = customer;
        }
    }

    function viewCustomerData(string memory _custName)
        public
        view
        returns (string memory)
    {
        /*
        View the data of the customer.
        Args: 
            _custName: name of the customer
        */
        Customer memory customer = customers[_custName];
        return customer.customerData;
    }
}
