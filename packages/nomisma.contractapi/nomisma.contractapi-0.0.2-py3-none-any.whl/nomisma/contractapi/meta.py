class ContractMetaData:
    def __init__(self, web3, asyncexec, address, abi, caller_account=None):
        self.web3 = web3
        self.asyncexec = asyncexec
        self.address = address
        self.abi = abi
        self.caller_account = caller_account