from brownie import accounts, network, config, MockV3Aggregator, VRFCoordinatorMock, Contract

FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]

DECIMALS = 8
INITIAL_VALUE = 200000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in [*FORKED_LOCAL_ENV, *LOCAL_BLOCKCHAIN_ENV]:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
}


def get_contract(contract_name):
    # Grab the contract addresses from the brownie config if defined,
    # otherwise, deploy a mock version of that contract, and return that mock contract
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]

    else:
        contract_addrass = config["network"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_addrass, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("Deployed!")
