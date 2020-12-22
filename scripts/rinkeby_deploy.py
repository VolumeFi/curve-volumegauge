#!/usr/bin/python3
from brownie import swap_volumegauge, volumegaugetracker, accounts, Contract

def main():
    accounts.load('tester')
    trackercontract = volumegaugetracker.deploy({"from": accounts[0]})
    gaugecontract = swap_volumegauge.deploy(["0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643", "0x39AA39c021dfbaE8faC545936693aC917d5E7563"], ["0x6B175474E89094C44Da98b954EedeAC495271d0F", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"],["0x773616E4d11A78F511299002da57A0a94577F1f4", "0x986b5E1e1755e3C2440e960477f25201B0a8bbD4"], "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e", "0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", trackercontract, {'from': accounts[0]})
    trackercontract.addGauge(gaugecontract, {"from": accounts[0]})
