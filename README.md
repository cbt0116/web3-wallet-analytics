# Web3 Wallet Analytics

A lightweight, read-only EVM wallet inspection script built with Python and web3.py. It retrieves a wallet's native currency balance and the balances of explicitly supplied ERC-20 token contracts through a configured JSON-RPC endpoint.

The script does not request signatures, manage private keys, construct transactions, or move funds.

## Features

- Connect to an EVM-compatible network through an HTTP JSON-RPC endpoint.
- Validate and checksum-normalize the wallet and token contract addresses using web3.py.
- Read the wallet's native balance.
- Query ERC-20 `balanceOf`, `decimals`, and `symbol` methods for each supplied token contract.
- Display the collected result in the terminal.

## Requirements

- Python 3.10 or newer is recommended.
- An HTTP RPC endpoint for the EVM network you want to inspect.
- A compatible ERC-20 token contract address for each token query.

Dependency:
- `web3>=6.15,<8`

## Installation

Clone the repository:

```bash
git clone https://github.com/cbt0116/web3-wallet-analytics.git
cd web3-wallet-analytics
```

Create and activate a virtual environment.

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Set `RPC_URL` to an HTTP RPC endpoint for the network you intend to query.

**Windows PowerShell**
```powershell
$env:RPC_URL="https://your-rpc-endpoint"
```

**macOS / Linux**
```bash
export RPC_URL="https://your-rpc-endpoint"
```

Use a trusted RPC provider and keep any provider API key or credential out of source control.

## Usage

Inspect a wallet's native balance:

```bash
python wallet.py --address 0xYourWalletAddress
```

Inspect the native balance and one ERC-20 token:

```bash
python wallet.py --address 0xYourWalletAddress --token 0xTokenContractAddress
```

Pass `--token` multiple times to inspect multiple token contracts:

```bash
python wallet.py \
  --address 0xYourWalletAddress \
  --token 0xFirstTokenContract \
  --token 0xSecondTokenContract
```

The script prints a Python dictionary containing:
- `address`: checksum-formatted wallet address
- `native_balance`: native balance converted from wei
- `tokens`: a list of token contract address, symbol, and formatted balance

The script does not currently return JSON-formatted output or include fiat valuations, transaction history, NFT holdings, or portfolio performance.

## How it works

The main function is `inspect_wallet(w3, wallet, tokens)` in `wallet.py`.

1. Converts the wallet address to checksum format.
2. Reads the native balance with `w3.eth.get_balance` and converts it from wei.
3. For each supplied token address, creates a contract instance using a minimal ERC-20 ABI.
4. Calls `decimals()`, `balanceOf(wallet)`, and `symbol()`.
5. Returns the collected values as a Python dictionary.

## Current limitations

- **Read-only and limited scope:** this is a balance inspector, not a complete wallet analytics or portfolio platform.
- **Explicit token list:** it queries only token contracts passed with `--token`; it does not discover all tokens held by an address.
- **Network-dependent:** it queries whichever network the configured RPC endpoint serves. It does not independently verify the chain ID or network identity.
- **No transaction history:** transfers, approvals, NFT holdings, and historical balances are not indexed.
- **No fiat pricing:** there are no market prices, valuations, or profit/loss calculations.
- **Token metadata is untrusted:** a contract may return misleading symbols or decimals, or may not implement the expected ERC-20 methods.
- **Numeric precision:** token balances are currently formatted using Python floating-point division, which can lose precision for some token amounts.
- **Error handling:** RPC failures, invalid addresses, and non-standard token contracts are not yet handled with tailored user-facing errors.
- **No committed tests:** this repository currently contains no automated test suite.

Verify token contract addresses using official project sources and the relevant chain's trusted explorer. Never treat a displayed token symbol as proof of authenticity.

## Roadmap

1. Use integer/base-unit or `Decimal` arithmetic to preserve token precision.
2. Add chain ID verification and clearer RPC/network diagnostics.
3. Add structured error handling for invalid addresses and non-standard token contracts.
4. Add unit tests with mocked Web3 calls and integration tests against a test network.
5. Add optional token discovery through a trusted indexing provider.
6. Add historical activity and pricing only with clearly identified data sources.
7. Add machine-readable JSON output and a more complete command-line interface.

## Security

This tool is designed for public, read-only blockchain queries. It should never need a wallet seed phrase or private key. Do not enter or share private keys, seed phrases, or signing credentials to use this project.

## License

No license file is currently included. Unless a license is added, the repository should not be assumed to grant permission to reuse, modify, or distribute the code.
