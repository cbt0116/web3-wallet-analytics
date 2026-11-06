import argparse, os
from web3 import Web3

ERC20_ABI = [
 {"constant": True, "inputs":[{"name":"owner","type":"address"}],
  "name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},
 {"constant": True, "inputs":[],
  "name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
 {"constant": True, "inputs":[],
  "name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}
]

def inspect_wallet(w3, wallet, tokens):
    wallet = Web3.to_checksum_address(wallet)
    native = w3.from_wei(w3.eth.get_balance(wallet), "ether")
    result = {"address": wallet, "native_balance": str(native), "tokens": []}
    for address in tokens:
        contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=ERC20_ABI)
        decimals = contract.functions.decimals().call()
        raw = contract.functions.balanceOf(wallet).call()
        result["tokens"].append({
            "contract": address, "symbol": contract.functions.symbol().call(),
            "balance": str(raw / (10 ** decimals))
        })
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--address", required=True)
    p.add_argument("--token", action="append", default=[])
    a = p.parse_args()
    rpc = os.getenv("RPC_URL")
    if not rpc: raise SystemExit("Set RPC_URL")
    w3 = Web3(Web3.HTTPProvider(rpc))
    if not w3.is_connected(): raise SystemExit("RPC connection failed")
    print(inspect_wallet(w3, a.address, a.token))
