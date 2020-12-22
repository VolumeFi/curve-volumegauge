#!/usr/bin/python3
from brownie import swap_volumegauge, volumegaugetracker, accounts, Contract

def main():
    accounts.load('0')
    # volumegaugetracker.deploy({"from": accounts[0]})
    # swap_volumegauge.deploy(["0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643", "0x39AA39c021dfbaE8faC545936693aC917d5E7563"], ["0x6B175474E89094C44Da98b954EedeAC495271d0F", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"],["0x773616E4d11A78F511299002da57A0a94577F1f4", "0x986b5E1e1755e3C2440e960477f25201B0a8bbD4"], "0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x106F1E2b2F8F454988016e2A5F5dB27e1A1F9Cf2", {'from': accounts[0]})
    # volumegaugetracker.addGauge(swap_volumegauge, {"from": accounts[0]})
