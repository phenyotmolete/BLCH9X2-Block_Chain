# SimpleBlockchain — Assignment 4: Wallet & Digital Signature Lab

## Install

```bash
pip install -r requirements.txt
```

## Run the demo

```bash
python demo_wallets.py
```

This creates two wallets (Alice, Bob), signs a canonical transaction payload,
verifies it, then demonstrates that:
- a mutated payload fails verification, and
- verifying under the wrong public key fails verification.

## Files

- `wallet.py` — `Wallet` class (create / address / sign / verify) and
  `canonical_tx_payload()` helper.
- `demo_wallets.py` — end-to-end demo script matching the assignment checkpoints.
- `requirements.txt` — `ecdsa>=0.18.0`.

## Security note

This module generates fresh, throwaway ECDSA key pairs for coursework
purposes only. Do **not** use it with real (mainnet) private keys, seed
phrases, or funded addresses.
