# volumegauge
Volume Gauges for DeFi 

1. Deployment (Mainnet)
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


    - Run register swap_volumegauge address to volumegaugetracker using addGauge()

2. Usage (Mainnet)
    Approve token to the swap_volumegauge and run exchange (or exchange_underlying) instead of swap contract.
    
    Other operations are processed at swap contract.

3. Deploy for Test (Rinkeby)
    - Deploy volumegaugetracker.vy
    - Deploy swap_volumegauge.vy (update code for constant of eth/usd aggregator address)
    
        Base
        
        0xA319E978505b19b5E145436Cc040c12E70e1840b
        

        Coins
        
        0x6D7F0754FFeb405d23C51CE938289d4835bE3b14 cDAI
        
        0x5B281A6DdA0B271e91ae35DE655Ad301C976edb1 cUSDC
        
        
        Underlying coins
        
        0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa DAI
        
        0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b USDC
        

        Aggregators
        
        0x74825DbC8BF76CC4e9494d0ecB210f676Efa001D DAI / ETH
        
        0xdCA36F27cbC4E38aE16C4E9f99D39b42337F6dcf USDC / ETH
        

    - Deploy test.sol on Rinkeby Testnet.
        constructor parameter: deployed gauge address

4. Test (Rinkeby)
    - Test exchange
        Send cToken(cDAI or cUSDC) on Rinkeby to the deployed smart contract.
        
        Run "test_compound_token" transaction with parameters same as exchange of swap contract.
    
    - Test exchange_underlying
        Send token(DAI or USDC) on Rinkeby to the deployed smart contract.
        
        Run "test_underlying_token" transaction with parameters same as exchange of swap contract.
    
    - Deposit
        Test might fail as insufficient deposit amount.
        
        At that time, you can send cTokens(cDAI and cUSDC) to the deployed smart contract and run "deposit" for adding liquidity.
    
    - Faucet Tokens
        https://app.compound.finance/

* Contract Source Code of the Tokens(DAI, USDC) were not verified. So you won't be able to approve tokens to contracts easily. That's why I built this test contract.

* deployed address on Rinkeby (deposited only 1K cTokens ~ 20 underlying tokens)

    volumegaugetracker 0x042f2ef486192c633245a0324F60b1911a1Ac245
    
    swap_volumegauge 0x8fB761472A1c466f2E09976ED04F0954D5E61B13
    
    test 0x4BE8b1310537D477E9461e3671A553195c858190
