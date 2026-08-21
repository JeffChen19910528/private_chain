"""Interactively decrypt a geth keystore file and save the raw private key."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chain_tools.chain import get_web3
from chain_tools.wallet import decrypt_keystore, list_keystore_files

OUTPUT_FILE = "private_key.txt"


def main():
    web3 = get_web3()

    files = list_keystore_files()
    print("Keystore files:")
    for idx, path in enumerate(files):
        print(f"{idx + 1}. {path.name}")

    file_index = int(input("Enter the number of the keystore file you want to decrypt: ")) - 1
    password = input("Enter your keystore password: ")

    try:
        private_key = decrypt_keystore(web3, files[file_index], password)
        print("Decryption successful.")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(private_key.hex())
        print(f"Private key saved to {OUTPUT_FILE}")
    except ValueError as exc:
        print("Error:", exc)


if __name__ == "__main__":
    main()
