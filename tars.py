#!/usr/bin/env python3
"""
TARS - Transparent Auditable Resilience System

This script generates cryptographic birth certificates and performs proof-of-life monitoring
for WireGuard VPN servers to ensure server integrity and provenance.

This version includes comments and explanations on how to configure the script
to work with different EVM-based blockchain networks.
"""

import os
import sys
import time
import hashlib
import argparse
import yaml
import json
import requests
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from web3 import Web3
from eth_account import Account
import getpass

# Enable unaudited features to use local private keys
Account.enable_unaudited_hdwallet_features()

# Load configuration
CONFIG_FILE = 'config.yaml'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Configuration file '{CONFIG_FILE}' not found.")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    return config

def generate_key_pair():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def save_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)

def load_key(filename):
    with open(filename, 'rb') as f:
        key_data = f.read()
    return key_data

def get_file_contents(file_path):
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return b''

def compute_hash(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()

def sign_data(private_key, data):
    signature = private_key.sign(data)
    return signature

def verify_signature(public_key, data, signature):
    try:
        public_key.verify(signature, data)
        return True
    except Exception:
        return False

def get_server_state(config):
    files_to_hash = []
    for root, dirs, files in os.walk('/'):
        for name in files:
            file_path = os.path.join(root, name)
            # Exclude specified files
            if any(Path(file_path).match(pattern) for pattern in config['excluded_files']):
                continue
            files_to_hash.append(file_path)
    # Read and concatenate all file contents
    state_data = b''
    for file_path in files_to_hash:
        state_data += get_file_contents(file_path)
    return state_data

def publish_to_blockchain(data, config, wallet_password):
    # Connect to the EVM-based network using the RPC URL from the config
    web3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    if not web3.isConnected():
        print("Failed to connect to the blockchain network.")
        return

    # Load wallet private key
    encrypted_key_path = config['wallet_key_file']
    with open(encrypted_key_path, 'r') as keyfile:
        encrypted_key = keyfile.read()
    try:
        private_key = Account.decrypt(encrypted_key, wallet_password)
    except Exception as e:
        print(f"Failed to decrypt wallet key: {e}")
        return

    account = Account.from_key(private_key)
    nonce = web3.eth.getTransactionCount(account.address)

    # Construct transaction
    tx = {
        'nonce': nonce,
        # 'to' can be None if publishing directly to the blockchain without a recipient
        'to': config.get('contract_address', None),  # If interacting with a smart contract
        'value': 0,
        'gas': config.get('gas_limit', 200000),
        'gasPrice': web3.toWei(config.get('gas_price_gwei', 30), 'gwei'),
        'data': data  # Data to be stored on the blockchain
    }

    # Set the chain ID for the target network
    tx['chainId'] = config.get('chain_id', 137)  # Default is 137 for Polygon Mainnet

    # Sign transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Send transaction
    try:
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaction sent: {web3.toHex(tx_hash)}")
    except Exception as e:
        print(f"Failed to send transaction: {e}")

def generate_birth_certificate(config):
    # Generate key pair
    private_key_obj, public_key_obj = generate_key_pair()
    private_key = private_key_obj.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = public_key_obj.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    # Save keys
    save_key(private_key, 'private_key.pem')
    save_key(public_key, 'public_key.pem')

    # Get initial server state
    state_data = get_server_state(config)

    # Compute hash of the state
    state_hash = compute_hash(state_data)

    # Sign the hash
    signature = sign_data(private_key_obj, state_hash)

    # Create birth certificate
    birth_certificate = {
        'server_id': config['server_id'],
        'timestamp': datetime.utcnow().isoformat(),
        'state_hash': state_hash.hex(),
        'signature': signature.hex(),
        'public_key': public_key.hex(),
        'excluded_files': config['excluded_files']
    }

    # Save birth certificate
    with open('birth_certificate.json', 'w') as f:
        json.dump(birth_certificate, f, indent=4)

    # Serialize data to publish (e.g., hash of the birth certificate)
    data_to_publish = compute_hash(json.dumps(birth_certificate).encode('utf-8'))

    # Get wallet password
    wallet_password = getpass.getpass(prompt='Enter wallet password: ')

    # Publish birth certificate hash to blockchain
    publish_to_blockchain(data_to_publish, config, wallet_password)

    print("Birth certificate generated and published.")

def start_monitoring(config):
    # Load private key
    private_key_data = load_key('private_key.pem')
    private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_data)

    # Get wallet password
    wallet_password = getpass.getpass(prompt='Enter wallet password: ')

    while True:
        # Get current server state
        state_data = get_server_state(config)

        # Compute hash of the state
        state_hash = compute_hash(state_data)

        # Sign the hash
        signature = sign_data(private_key_obj, state_hash)

        # Create proof-of-life certificate
        proof_of_life = {
            'server_id': config['server_id'],
            'timestamp': datetime.utcnow().isoformat(),
            'state_hash': state_hash.hex(),
            'signature': signature.hex()
        }

        # Serialize data to publish (e.g., hash of the proof-of-life)
        data_to_publish = compute_hash(json.dumps(proof_of_life).encode('utf-8'))

        # Publish proof-of-life hash to blockchain
        publish_to_blockchain(data_to_publish, config, wallet_password)

        print(f"Proof-of-life published at {proof_of_life['timestamp']}.")

        # Wait for the next interval
        time.sleep(config['proof_interval'])

def main():
    parser = argparse.ArgumentParser(description='TARS - Transparent Auditable Resilience System')
    parser.add_argument('--generate-birth-certificate', action='store_true', help='Generate cryptographic birth certificate')
    parser.add_argument('--start-monitoring', action='store_true', help='Start proof-of-life monitoring')
    args = parser.parse_args()

    config = load_config()

    if args.generate_birth_certificate:
        generate_birth_certificate(config)
    elif args.start_monitoring:
        start_monitoring(config)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()