# TARS: Transparent Auditable Resilience System for WireGuard Deployment

![TARS Logo](docs/images/6fc40cb1-6646-49ce-b559-971887e8cfd4_577x433.webp)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![GitHub Stars](https://img.shields.io/github/stars/BlorpBleep/TARS.svg?style=social&label=Star&maxAge=3600)](https://github.com/BlorpBleep/TARS/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/BlorpBleep/TARS.svg)](https://github.com/BlorpBleep/TARS/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/BlorpBleep/TARS.svg)](https://github.com/BlorpBleep/TARS/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/BlorpBleep/TARS.svg)](https://github.com/BlorpBleep/TARS/pulls)
[![GitHub Contributors](https://img.shields.io/github/contributors/BlorpBleep/TARS.svg)](https://github.com/BlorpBleep/TARS/graphs/contributors)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/BlorpBleep/TARS.svg)](https://github.com/BlorpBleep/TARS/commits/main)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/BlorpBleep/TARS)
[![GitHub Sponsors](https://img.shields.io/badge/sponsor-GitHub-%23EA4AAA.svg)](https://github.com/sponsors/BlorpBleep)

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Configuring for Different EVM Networks](#configuring-for-different-evm-networks)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)
- [Support](#support)

---

## Introduction

**TARS** (Transparent Auditable Resilience System) is an open-source solution for secure and verifiable deployment of WireGuard VPN servers. It ensures server integrity and provenance through cryptographic birth certificates and proof-of-life mechanisms. Designed to treat servers as disposable appliances, TARS allows for dynamic scaling while preserving user privacy and anonymity.

---

## Features

- **Cryptographic Birth Certificates**: Verifies the server's initial state upon deployment.
- **Proof-of-Life Signals**: Regularly confirms server integrity and detects tampering.
- **User Privacy Assurance**: Excludes dynamic configurations from integrity checks to maintain anonymity.
- **Scalability**: Supports dynamic addition and removal of servers.
- **Open-Source**: Built entirely with open-source tools and libraries.
- **Blockchain Integration**: Publishes proofs to a public blockchain for transparency.
- **EVM Network Support**: Compatible with various Ethereum Virtual Machine (EVM)-based networks.

---

## How It Works

1. **Deployment**: Each server generates a cryptographic birth certificate containing its initial state.
2. **Monitoring**: The server monitors every bit of its system, excluding specified dynamic files.
3. **Proof Publishing**: At regular intervals, the server publishes a proof-of-life hash to a public blockchain.
4. **Verification**: Any party can verify the server's integrity using the public proofs.
5. **Tamper Detection**: Unauthorized changes trigger verification failures and initiate alerts.

---

## Installation

### Prerequisites

- **Operating System**: Linux-based OS
- **Dependencies**:
  - WireGuard
  - OpenSSL
  - Python 3.8+
  - Git
  - Python Packages:
    - `cryptography`
    - `PyYAML`
    - `web3`
    - `requests`

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/BlorpBleep/TARS.git
   cd TARS
   ```

2. **Install System Dependencies**

   ```bash
   sudo apt-get update
   sudo apt-get install wireguard openssl python3 python3-pip
   ```

3. **Install Python Packages**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure TARS**

   - Edit the `config.yaml` file to suit your environment.
   - Specify dynamic files to exclude in the birth certificate.
   - Configure blockchain settings for your chosen EVM network.

---

## Usage

### Generating a Birth Certificate

Run the following command to generate a cryptographic birth certificate:

```bash
python3 tars.py --generate-birth-certificate
```

You will be prompted to create a wallet password for encrypting your blockchain wallet key.

### Starting Proof-of-Life Monitoring

To start the regular proof-of-life checks and publish proofs:

```bash
python3 tars.py --start-monitoring
```

You will be prompted to enter your wallet password.

### Verifying Server Integrity

Use the verification script to check server integrity:

```bash
python3 verify.py --server <server_id>
```

*(Note: Implement `verify.py` to retrieve and verify proofs from the blockchain.)*

---

## Configuration

### `config.yaml` Parameters

- `server_id`: Unique identifier for the server.
- `excluded_files`: List of dynamic files to exclude from integrity checks.
- `proof_interval`: Time interval (in seconds) between proof-of-life publications.
- `rpc_url`: RPC endpoint URL of the blockchain network.
- `chain_id`: Chain ID of the blockchain network.
- `wallet_key_file`: Path to the encrypted wallet key file.
- `contract_address`: Address of a smart contract (if interacting with one).
- `gas_limit`: Maximum amount of gas to use per transaction.
- `gas_price_gwei`: Gas price in Gwei.

### Example `config.yaml`

```yaml
server_id: "server-12345"
excluded_files:
  - "/etc/wireguard/wg0.conf"
  - "/var/log/*"
  - "/proc/*"
  - "/sys/*"
  - "/tmp/*"
proof_interval: 3600

# EVM Network Configuration
rpc_url: "https://polygon-rpc.com"        # Polygon Mainnet RPC URL
chain_id: 137                             # Polygon Mainnet Chain ID
wallet_key_file: "wallet.key"
contract_address: null                    # Set to smart contract address if needed
gas_limit: 200000
gas_price_gwei: 30                        # Adjust according to network conditions
```

---

### Configuring for Different EVM Networks

TARS supports integration with various EVM-based blockchain networks. To configure TARS for a different network, update the `rpc_url`, `chain_id`, and gas settings in your `config.yaml`.

#### Ethereum Mainnet

```yaml
rpc_url: "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
chain_id: 1
gas_price_gwei: 100
```

#### Binance Smart Chain (BSC) Mainnet

```yaml
rpc_url: "https://bsc-dataseed.binance.org/"
chain_id: 56
gas_price_gwei: 5
```

#### Avalanche Mainnet

```yaml
rpc_url: "https://api.avax.network/ext/bc/C/rpc"
chain_id: 43114
gas_price_gwei: 25
```

#### Fantom Mainnet

```yaml
rpc_url: "https://rpcapi.fantom.network"
chain_id: 250
gas_price_gwei: 1
```

#### Ethereum Testnets (Rinkeby, Ropsten)

```yaml
rpc_url: "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"
chain_id: 4
gas_price_gwei: 10
```

**Note**: Ensure your wallet is funded with the appropriate tokens to pay for gas fees on the selected network.

---

## Contributing

We welcome contributions from the community!

### How to Contribute

1. **Fork the Repository**

   Click the "Fork" button at the top right of this page.

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add your feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Submit your pull request for review.

### Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact

- **Project Maintainer**: [Your Name](mailto:developer@cicadavpn.com)
- **GitHub Issues**: [Create an Issue](https://github.com/BlorpBleep/TARS/issues)
- **Discussion Forum**: [GitHub Discussions](https://github.com/BlorpBleep/TARS/discussions)
- **Discord**: [Join our Discord server](https://discord.gg/cicadavpn)

---

## Acknowledgments

- **WireGuard**: [https://www.wireguard.com](https://www.wireguard.com)
- **Ed25519 Libraries**: For cryptographic operations.
- **Web3.py**: For blockchain interactions.
- **Open-Source Community**: For continuous support and contributions.

---

## Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the project maintainer.

---

*By reimagining server deployment with cryptographic assurances, TARS aims to enhance the security and trustworthiness of VPN infrastructures in an increasingly connected world.*

---

# Instructions for Setting Up the Blockchain Wallet

To interact with the blockchain network, you need to set up a wallet:

### Generating a Wallet

1. **Run the Wallet Generation Script**

   ```python
   from eth_account import Account
   import getpass
   import json

   # Generate a new account
   new_account = Account.create()
   private_key = new_account.key

   # Securely store the private key
   password = getpass.getpass(prompt='Create a wallet password: ')
   encrypted_key = Account.encrypt(private_key, password)

   # Save the encrypted key to a file
   with open('wallet.key', 'w') as f:
       json.dump(encrypted_key, f)

   print(f"New account created: {new_account.address}")
   ```

2. **Fund Your Wallet**

   - For **Testnets**: Use a faucet to get test tokens.
   - For **Mainnets**: Purchase a small amount of the network's native token to pay for transaction fees.

### Security Recommendations

- **Protect Your Private Key**: Keep `wallet.key` secure and do not share it.
- **Use Strong Passwords**: When creating your wallet password, use a strong, unique password.
- **Backup**: Keep backups of your `wallet.key` and remember your password.

---

# Additional Information

## Monitoring Gas Prices

Gas prices can fluctuate based on network congestion. Consider implementing dynamic gas price adjustments or using APIs to set `gas_price_gwei` appropriately.

## Interacting with Smart Contracts

If you deploy a smart contract for proof storage:

- **Update `contract_address`** in `config.yaml` with your contract's address.
- Modify `tars.py` to interact with the contract's methods.
- Ensure you have the contract's ABI and understand its functions.

## Implementing `verify.py`

The `verify.py` script should:

- Connect to the blockchain network.
- Retrieve published proofs using the server ID.
- Verify the proofs against the server's public key.

---

# Quick Links

- **White Paper**: [Read the TARS White Paper](docs/white_paper.md)
- **Changelog**: [See What's New](changelog.md)

---

# Stay Connected

- **Twitter**: [Follow us on Twitter](https://twitter.com/cicadavpn)
- **Newsletter**: [Subscribe to our newsletter](https://cicadavpn.substack.com/)
- **Blog**: [Read our latest posts](https://cicadavpn.com/blog)

---

By updating the README with these enhancements, we've included detailed instructions on configuring TARS for different EVM-based networks, added information on setting up the blockchain wallet, and provided additional resources for users and contributors.

If you have any further requests or need additional modifications, feel free to let me know!