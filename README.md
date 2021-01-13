# DeFi volumegauge

Volume Gauges for DeFi aim to solve the problem: How to incentivize marketing partners to drive more liquidity providers to their pools using the pool rewards without a centralized affiliate marketing budget?

VolumeGauges track affiliate performance and rewards them from the pool rewards.

VolumeGauges for Curve contracts allow the Curve ecosystem to make proposals that distribute rewards to the affiliate that drive exchange volume through the pool. The affiliate may in turn reward LPs with innovative incentive programs that go beyond trading fee rebates.

VolumeGauges use [Volume-weighted Exponential Moving Average](https://www.financialwisdomforum.org/gummy-stuff/EMA.htm)


## Testing and Development on testnet

### Dependencies
* [nodejs](https://nodejs.org/en/download/) - >=v8, tested with version v14.15.4
* [python3](https://www.python.org/downloads/release/python-368/) from version 3.6 to 3.8, python3-dev
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.12.0](https://github.com/eth-brownie/brownie/releases/tag/v1.12.0)

The contracts are compiled using [Vyper](https://github.com/vyperlang/vyper), however, installation of the required Vyper versions is handled by Brownie.

### Setup

To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html). Next, clone the repo and install the developer dependencies:

```bash
git clone https://github.com/Promise-Protocol/volumegauge.git
cd volumegauge
pip install -r requirements.txt
```

### Ganache-cli

Install Node.js(>=v8) and ganache-cli globally.

```bash
npm install -g ganache-cli
```

```bash
ganache-cli --fork https://mainnet.infura.io/v3/1755ac442e6849a98568b6a9f7d191a0 -p 7545
```

And wait until local RPC is ready.(a few seconds)

### Brownie network setting (only once in the beginning)
```bash
brownie networks add Development forkedmain host=http://127.0.0.1 accounts=10 evm_version=istanbul fork=mainnet port=7545 mnemonic=brownie cmd=ganache-cli timeout=300
```


### Running the Tests

```bash
brownie test -s
```
