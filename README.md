# volumegauge
Volume Gauges for DeFi 

1. Deployment
    - Deploy volumegaugetracker.vy
    - Deploy swap_volumegauge.vy
        deploy with parameters (cDAI, cUSDC, DAI, USDC, DAI/ETH Aggregator, USDC/ETH Aggregator, swap contract, volumegaugetracker)

2. Usage
    approve token to the swap_volumegauge and run exchange (or exchange_underlying) just like swap contract.