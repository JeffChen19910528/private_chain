# private_chain

A local private Ethereum chain (geth) + Truffle project for demonstrating
double-spend attacks against a deliberately vulnerable `ERC20Token` contract.

## Setup

```bash
./initproject.sh
./init.sh
./start.sh
```

```bash
pip install -r requirements.txt        # runtime deps
pip install -r requirements-dev.txt     # + pytest, for running tests
```

Copy `.env.example` to `.env` and fill in real values (RPC URL, file paths,
and `DOUBLE_SPEND_PRIVATE_KEY` for the demo script). `.env`,
`password.txt`, `private_key.txt`, and `address.txt` are gitignored - they
hold local-chain secrets/derived data and should never be committed.

## Compiling and deploying the contract

```bash
cd truffleProject
./compile.sh
```

## Python tooling

Shared connection/contract/wallet logic lives in `chain_tools/`; the
runnable demos are thin scripts in `scripts/`:

- `scripts/run_demo.py` - creates two funded contract accounts and races a
  same-nonce double-spend transfer.
- `scripts/exploit_vulnerable_erc20.py` - exercises the vulnerable
  `ERC20Token.transfer()`, which calls `_transfer` twice.
- `scripts/decrypt_keystore.py` - interactively decrypts a geth keystore
  file and writes the raw private key to `private_key.txt`.

Run any of them with `python scripts/<name>.py` from the project root
(requires a running chain from `./start.sh`).

## Tests

```bash
pytest tests/ -v
```

These are unit tests for the config/wallet/contract-loading logic
(`chain_tools/`) and run without a live chain. They do not exercise the
account/network-management shell scripts or the on-chain demo scripts,
which need a running geth node.

## Account management scripts

- `createAccount.sh` - creates a new keystore account and appends its
  password to `password.txt`.
- `deleteAccount.sh` - removes a keystore account.
- `backup_geth.sh` / `restore_geth.sh` - back up/restore the `data/`
  directory.
