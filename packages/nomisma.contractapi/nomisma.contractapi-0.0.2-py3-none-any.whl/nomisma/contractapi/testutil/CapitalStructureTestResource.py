from datetime import date
import time
import nomisma.contractapi.testutil.TruffleContract
import nomisma.contractapi.util
import web3._utils.abi
from web3 import Web3

from nomisma.contractapi.BankRegistryAbstract import BankRegistryAbstract
from nomisma.contractapi.asyncexec import AsyncExec
from nomisma.contractapi.testutil.FullERC20MockAbstract import FullERC20MockAbstract

delegate_contracts = ['BankInvest.json', 'BankStateGetters.json', 'BankRedeem.json',
                      'BankInitialise.json', 'BankBorrow.json', 'TokenManager.json']

DAY_IN_SECONDS = 24 * 3600

RATE_PRECISION_MULTIPLIER = 10 ** 4


def from_abi(web3, name):
    return ContractForTest(web3, nomisma.contractapi.testutil.TruffleContract.from_abi(name))


def from_mock_abi(web3, name):
    return ContractForTest(web3, nomisma.contractapi.testutil.TruffleContract.from_mock_abi(name))


class CapitalStructureTestResource:
    def __init__(self,
                 web3=None,
                 deployment_account=None,
                 governor_address=None,
                 commission_beneficiary_address=None,
                 date_keeper_data=None,
                 min_equity_balance=1,
                 commission_percentage=0.1):
        if web3 is None:
            self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        else:
            self.web3 = web3
        self.asyncexec = AsyncExec(10, poll_interval=0.1)
        if deployment_account is None:
            self.deployment_account = self.web3.eth.accounts[0]
        else:
            self.deployment_account = deployment_account
        if governor_address is None:
            self.governor_address = self.web3.eth.accounts[1]
        else:
            self.governor_address = governor_address
        if commission_beneficiary_address is None:
            self.commission_beneficiary_address = self.web3.eth.accounts[2]
        else:
            self.commission_beneficiary_address = commission_beneficiary_address
        if date_keeper_data is None:
            self.date_keeper_data = DateKeeperData()
        else:
            self.date_keeper_data = date_keeper_data
        self.min_equity_balance=min_equity_balance
        self.commission_percentage=int(commission_percentage/100*RATE_PRECISION_MULTIPLIER)
        self.bank_registry = None

    def tearDown(self):
        self.asyncexec.shutdown()

    def deploy_delegate_contracts(self):
        delegates = []
        self.contract_address_map = {}
        for json_contract in delegate_contracts:
            contract_for_test = from_abi(self.web3, json_contract)
            contract_for_test.deploy_nowait(self.deployment_account)
            delegates.append(contract_for_test)
        for i in range(len(delegate_contracts)):
            self.contract_address_map[delegate_contracts[i]] = delegates[i].get_address()

    def populate_resolver(self, resolver, name):
        truffle_to_add = from_abi(self.web3, name).truffle_contract
        destination = self.contract_address_map[name]
        w3_contract = self.web3.eth.contract(
            abi=truffle_to_add.abi())
        sig_hashes = []
        addresses = []
        tx_hashes = []
        for f in w3_contract.all_functions():
            signature = web3._utils.abi.abi_to_signature(f.abi)
            signature_hash = Web3.keccak(text=signature)
            sig_hashes.append(signature_hash)
            addresses.append(destination)
            if len(sig_hashes) == 10:
                tx_hashes.append(resolver.callable().functions.bulkRegister(sig_hashes, addresses).transact(
                    {'from': self.governor_address}))
                sig_hashes.clear()
                addresses.clear()
        if len(sig_hashes) > 0:
            tx_hashes.append(resolver.callable().functions.bulkRegister(sig_hashes, addresses).transact(
                {'from': self.governor_address}))
        for tx_hash in tx_hashes:
            self.web3.eth.waitForTransactionReceipt(tx_hash)

    def deploy_bank_registry(self):
        token_manager_resolver = from_abi(self.web3, 'Resolver.json')
        token_manager_resolver.deploy_nowait(self.deployment_account, self.governor_address)

        self.populate_resolver(token_manager_resolver, 'TokenManager.json')

        token_manager_router = from_abi(self.web3, 'TokenManagerRouter.json')
        token_manager_router.deploy_nowait(self.deployment_account, self.governor_address,
                                           token_manager_resolver.get_address())

        exchange_mock = from_mock_abi(self.web3, 'ExchangeConnectorMock.json')
        exchange_mock.deploy_nowait(self.deployment_account, self.governor_address, token_manager_router.get_address())

        ddd = self.date_keeper_data
        bank_date_keeper = from_abi(self.web3, 'BankDateKeeper.json')
        bank_date_keeper.deploy_nowait(self.deployment_account, self.governor_address, ddd.weekly_config(),
                                       ddd.bank_dates(), ddd.bank_dates_interval_starts(),
                                       ddd.bank_dates_interval_ends())

        bank_resolver = from_abi(self.web3, 'Resolver.json')
        bank_resolver.deploy_nowait(self.deployment_account, self.governor_address)

        self.populate_resolver(bank_resolver, 'BankBorrow.json')
        self.populate_resolver(bank_resolver, 'BankInvest.json')
        self.populate_resolver(bank_resolver, 'BankRedeem.json')
        self.populate_resolver(bank_resolver, 'BankInitialise.json')
        self.populate_resolver(bank_resolver, 'BankStateGetters.json')

        self.token_validator = from_abi(self.web3, 'TokenValidator.json')
        self.token_validator.deploy_nowait(self.deployment_account, self.governor_address)

        self.bank_registry = from_abi(self.web3, 'BankRegistry.json')
        self.bank_registry.deploy_nowait(self.deployment_account, self.min_equity_balance, self.commission_percentage,
                                    exchange_mock.get_address(), token_manager_router.get_address(),
                                    bank_date_keeper.get_address(), self.governor_address,
                                    bank_resolver.get_address(), self.token_validator.get_address(),
                                    self.commission_beneficiary_address)

        bank_event_emitter = from_abi(self.web3, 'BankEventEmitter.json')
        bank_event_emitter.deploy_nowait(self.deployment_account, self.bank_registry.get_address())

        tx_hash = self.bank_registry.callable().functions.setEventEmitter(bank_event_emitter.get_address()).transact({'from': self.governor_address})
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def bank_registry_instance(self, caller_account=None):
        return BankRegistryAbstract(self.web3, self.asyncexec, self.bank_registry.get_address(), caller_account)

    def create_new_erc20_token(self, owner_address, name: str, symbol: str, decimals: int, amount_to_mint: int)\
            -> FullERC20MockAbstract:
        erc20_contract = from_mock_abi(self.web3, 'FullERC20Mock.json')
        erc20_contract.deploy_nowait(owner_address, name, symbol, decimals, amount_to_mint)
        self.token_validator.callable().functions.addTokensToWhitelist([erc20_contract.get_address()]).transact({'from': self.governor_address})
        return FullERC20MockAbstract(self.web3, self.asyncexec, erc20_contract.get_address(), owner_address)


class ContractForTest:
    def __init__(self, web3, truffle_contract):
        self.truffle_contract = truffle_contract
        self.w3 = web3
        self.tx_receipt = None
        self.tx_hash = None
        self.instance_contract = None

    def deploy_nowait(self, deploy_address, *constructor_args):
        self.w3.eth.defaultAccount = deploy_address
        w3_contract = self.w3.eth.contract(
            abi=self.truffle_contract.abi(),
            bytecode=self.truffle_contract.bytecode())
        self.tx_hash = w3_contract.constructor(*constructor_args).transact({'gas': 3000000})

    def get_address(self):
        if self.tx_receipt is None:
            self.tx_receipt = self.w3.eth.waitForTransactionReceipt(self.tx_hash)
        return self.tx_receipt['contractAddress']

    def callable(self):
        if self.instance_contract is None:
            self.instance_contract = self.w3.eth.contract(abi=self.truffle_contract.abi(), address=self.get_address())
        return self.instance_contract


class DateKeeperData:
    fixed_maturity_week_day = 5
    fixed_q_maturity_week = 3

    def __init__(self, initial_timestamp=None, weeks_in_future_enabled=4,
                 ldd_interval_start=DAY_IN_SECONDS, ldd_interval_end=DAY_IN_SECONDS * 2,
                 min_interval_since_bank_deployment_ts=604800):
        if initial_timestamp is None:
            self.initial_timestamp = nomisma.contractapi.util.str_to_eth_time('Jan 1, 2019 @ 00:00:00 UTC')
        else:
            self.initial_timestamp = initial_timestamp
        self.weeks_in_future_enabled = weeks_in_future_enabled
        self.ldd_interval_start = ldd_interval_start
        self.ldd_interval_end = ldd_interval_end
        self.min_interval_since_bank_deployment_ts = min_interval_since_bank_deployment_ts

    def weekly_config(self):
        return [self.initial_timestamp, self.weeks_in_future_enabled, self.ldd_interval_start,
                self.ldd_interval_end, self.min_interval_since_bank_deployment_ts]

    def third_friday(self, year, month):
        return date(year, month,
                    self.fixed_maturity_week_day + self.fixed_q_maturity_week * 7)  # this isn't a friday!??

    def bank_dates(self):
        # march, june, september, december
        fixed_q_maturity_months = [3, 6, 9, 12]
        # third week of the month

        today = date.today()
        fixed_dates = []
        for month in fixed_q_maturity_months:
            year = today.year
            if today.month + 3 >= month:
                year += 1
            fixed_dates.append(int(time.mktime(self.third_friday(year, month).timetuple()) + 8 * 3600))

        fixed_dates.sort()
        return fixed_dates

    def bank_dates_interval_starts(self):
        return [DAY_IN_SECONDS, DAY_IN_SECONDS, DAY_IN_SECONDS, DAY_IN_SECONDS]

    def bank_dates_interval_ends(self):
        return [DAY_IN_SECONDS * 3, DAY_IN_SECONDS * 3, DAY_IN_SECONDS * 3, DAY_IN_SECONDS * 3]
