from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider(''))
privateKey = ''
filename = 'swap_volumegauge.vy'
#filename = 'volumegaugetracker.vy'

def run_vyper(filename, output_format=None, outfile=None):
        if outfile == None:
                outfile = os.path.splitext(filename)[0] + f"_{output_format}.raw"
        if output_format:
                os.system(f"vyper -f {output_format} {filename} > {outfile}")
        else:
                os.system(f"vyper {filename} > {outfile}")       
        return(outfile)

def load_data(filename, output_format=None):
        filename = run_vyper(filename, output_format)
        abi_file = open(filename, "r")
        abi = abi_file.read().rstrip()
        return abi

contract_ = w3.eth.contract(
    abi=load_data(filename, 'abi'),
    bytecode=load_data(filename)
)

acct = w3.eth.account.privateKeyToAccount(privateKey)

construct_txn = contract_.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

signed = acct.signTransaction(construct_txn)
print(w3.eth.sendRawTransaction(signed.rawTransaction))
