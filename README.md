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
pip install anon-python-sdk
```

Install the SDk with specific version:

```bash
pip install anon-python-sdk==0.0.10
```

Uninstall the SDK:

```bash
pip uninstall anon-python-sdk
```

### From Source

Clone the repository and install the SDK:

```bash
git clone https://github.com/anyone-protocol/anon-python-sdk.git
cd anon-python-sdk
pip install .
```

---

## Usage

### Run Anon Node

```python
from anyone_protocol_sdk import AnonRunner, AnonConfig
import time

# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True
)

# Initialize the runner
runner = AnonRunner(config)

try:
    # Start Anon
    runner.start()
    # Perform tasks
finally:
    runner.stop()
```

### More Examples

See the [examples](examples) directory for more usage examples.
