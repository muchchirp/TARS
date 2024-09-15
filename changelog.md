# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - YYYY-MM-DD

### Added

- **Core Functionality**
  - Initial release of TARS with core features.
  - Generation of **Cryptographic Birth Certificates** to verify server's initial state.
  - Implementation of **Proof-of-Life Monitoring** to regularly confirm server integrity.
  - Exclusion of specified dynamic files from integrity checks to maintain user privacy.
  - Support for **EVM-based Blockchain Integration** to publish proofs to a public blockchain.
  - Command-line interface (`tars.py`) with options:
    - `--generate-birth-certificate`
    - `--start-monitoring`

- **Blockchain Wallet Setup**
  - Scripts and instructions for generating and managing a blockchain wallet.
  - Secure storage and encryption of the wallet's private key.

- **EVM Network Support**
  - Compatibility with multiple EVM-based networks, including:
    - Ethereum Mainnet and Testnets
    - Polygon (Matic) Mainnet
    - Binance Smart Chain (BSC) Mainnet
    - Avalanche Mainnet
    - Fantom Mainnet
  - Configuration options in `config.yaml` for network parameters:
    - `rpc_url`
    - `chain_id`
    - `gas_price_gwei`
    - `gas_limit`

- **Documentation**
  - Comprehensive **README** with:
    - Introduction and features overview.
    - Detailed installation and usage instructions.
    - Configuration guidelines for different EVM networks.
    - Contribution guidelines and code of conduct.
    - Contact information and support resources.
  - **White Paper** outlining the theoretical foundation and technical details.
  - **API Documentation** for developers.
  - **Instructions** for setting up the blockchain wallet and managing keys.

- **Sample Configuration Files**
  - Example `config.yaml` demonstrating how to configure TARS.
  - Sample `requirements.txt` listing necessary Python packages.

- **License**
  - Project licensed under the **MIT License**.

- **Community and Support**
  - GitHub Issues and Discussions for community engagement.
  - Discord server for real-time support and collaboration.
  - Acknowledgments section recognizing key technologies and contributors.

### Changed

- N/A (Initial release)

### Fixed

- N/A (Initial release)

---

## [Unreleased]

### Planned Features

- **Verification Script (`verify.py`)**
  - Tool for retrieving and verifying proofs from the blockchain.
  - Ability to independently confirm server integrity.

- **Automated Revocation**
  - Mechanisms to automatically decommission compromised servers.
  - Alerting system for immediate response to integrity breaches.

- **Extended Proofs**
  - Incorporation of additional system metrics into proof-of-life hashes.
  - Enhanced monitoring capabilities.

- **User Verification Tools**
  - Client-side applications for users to verify server integrity.
  - Browser extensions or mobile apps for ease of use.

- **Dynamic Gas Price Adjustment**
  - Integration with gas price APIs to adjust `gas_price_gwei` based on network conditions.

- **Smart Contract Integration**
  - Deployment of smart contracts for structured proof storage.
  - Enhanced data retrieval and querying capabilities.

---

**Note:** Dates and version numbers are placeholders and should be updated to reflect the actual release date when publishing.