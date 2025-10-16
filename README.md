# Anon Python SDK

## Overview

The **Anon Python SDK** is a Python interface for the Anon network, enabling developers to interact with Anon functionalities like running nodes, creating circuits, fetching relay information, and making requests through SOCKS5. The SDK is designed to simplify integration with the Anon protocol for developers building privacy-preserving applications.

---

## Features

- **Run Anon client**: Start and manage an Anon node locally with a simple interface.
- **Circuits management**: Fetch, create, and close circuits using the Anon control port.
- **Relay information**: Retrieve relay details by fingerprint.
- **SOCKS5 requests**: Send HTTP requests through the Anon network.
- **Cross-platform**: Works on macOS, Linux, and Windows (amd64, arm64).

---

## Installation

### Using `pip`

Install the SDK directly from PyPI:

```bash
pip install anyone-protocol-sdk
```

Install the SDk with specific version:

```bash
pip install anyone-protocol-sdk==0.0.1b0
```

Uninstall the SDK:

```bash
pip uninstall anyone-protocol-sdk
```

### From Source

Clone the repository and install the SDK:

```bash
git clone https://github.com/anyone-protocol/python-sdk.git
cd python-sdk
pip install .
```

---

## Usage

### Run Anon Node

```python
from anyone_protocol_sdk import Config, Process


# Create a configuration
config = Config(
    auto_terms_agreement=True
)

anon = None

try:
    anon = Process.launch_anon(anonrc_path=config.to_file())
    print("Anon is running...")
except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    anon.stop()
    print("Anon has stopped.")
```

### More Examples

See the [examples](examples) directory for more usage examples.
