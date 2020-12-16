# volumegauge
Volume Gauges for DeFi 

1. Deployment
    - Deploy volumegaugetracker.vy
    - Deploy swap_volumegauge.vy
        deploy with parameters (cDAI, cUSDC, DAI, USDC, DAI/ETH Aggregator, USDC/ETH Aggregator, swap contract, volumegaugetracker)
    
    Coins
    0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643 cDAI
    0x39AA39c021dfbaE8faC545936693aC917d5E7563 cUSDC
    
    Underlying coins
    0x6B175474E89094C44Da98b954EedeAC495271d0F DAI
    0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 USDC
    
    Aggregators
    0x773616E4d11A78F511299002da57A0a94577F1f4 DAI / ETH
    0x986b5E1e1755e3C2440e960477f25201B0a8bbD4 USDC / ETH

    Base
    0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56  Cruve.fi: Compound Swap

2. Usage
    Approve token to the swap_volumegauge and run exchange (or exchange_underlying) instead of swap contract.
    Other operations are processed at swap contract.