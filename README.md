# Web3 Wallet Analytics

Read-only EVM wallet balance inspector. It does not request signatures or control funds.

```powershell
pip install -r requirements.txt
$env:RPC_URL="https://your-rpc-endpoint"
python wallet.py --address 0xYourAddress --token 0xErc20Address
```
Check token contracts against official sources. Token metadata is untrusted input.
