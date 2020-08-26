# Iroha-CLI

Command Line Interface written in Python for use with Iroha Distributed Ledger.

**Use at own risk**

It is highly recommended that you first test & familiarize yourself with this CLi & Tools using a test network before transacting withh a live network.

**Hyperledger Iroha is a DLT / Blockchain.**

The below is just a set of practices I follow that might be of use to other users. 
This is not a **Best Practices List** nor **advisory information**. 

*   All transactions(commands) are irreversable.
*   **Private Keys** should be stored in a secure manner (Generated & Encrypted by user / client-side).
*   Node keys are required to have file extentions .priv & .pub respectively. If your using multiple node setup, ensure that unique keypairs are  generated for each node & that their are distributed accordingly. This will differ for each type of deployment e.g. manually starting nodes vs kubernetes deployment
*   By default - User account & transactional information (inclusive of block level information) is **not** encrypted. 
    If your use case / project falls under GDPR or similar privacy laws, carefully design the processes and ensure that only the relevant parties have access to the senstive information.
    This could be done in a few ways including:

    *   assigning supervisory / administrative accounts & corrosponding roles with allocated permisions where multiple users could be added as multiple signatories with a required quorom
    
    or 
    
    *   with multiple user accounts with s

## Usage Requirements

* Python 3.8 ( Tested - Should work with 3.6+ )
* Poetry (Manages Virtual Environments & Setup)

## CLi Commands

Command line interface tool for users & network administrators.

**Please Note:  This is not the official CLI**

This tool was developed for a cross-platform cli alternative to the official cli included in Iroha releases. 

Currently supports the following list of V1.2+ commands & queries.

Users / accounts must have **valid permissions** assigned to the account.

### Iroha Commands:

- [x] CreateAccount
- [ ] SetAccountDetail
- [ ] SetAccountDetail
- [ ] SetAccountDetail

### Iroha Queries:

- [x] ViewAccount
- [ ] ViewAccountDetail
- [ ] GetBlocks


### Iroha V1 Genesis Block Generator

Simple Hyperledger Iroha genesis block generator.
Uses **valid JSON** style template ( genesis_block.json)

### Features