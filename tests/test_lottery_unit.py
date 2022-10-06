from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery


# Check if the entry price calculation is correct
def test_get_entrance_fee():
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
