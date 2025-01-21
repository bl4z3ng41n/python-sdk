from setuptools import setup, find_packages
from setuptools.command.install import install
import platform
import requests
import zipfile
import tempfile
from pathlib import Path
import stat

# Constants
OWNER = "anyone-protocol"
REPO = "ator-protocol"
VERSION = "v0.4.9.10"
RELEASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{VERSION}"

PLATFORM_MAP = {
    "linux": "linux",
    "darwin": "macos",
    "windows": "windows",
}

ARCH_MAP = {
    "arm64": "arm64",
    "aarch64": "arm64",
    "x86_64": "amd64",
}

class CustomInstallCommand(install):
    """Custom installation command to download and install the Anon binary."""
    def run(self):
        # Run the standard install process
        install.run(self)

        # Determine platform and architecture
        system = platform.system().lower()
        arch = platform.machine().lower()

        if system not in PLATFORM_MAP:
            print(f"Unsupported platform: {system}")
            raise OSError("Unsupported platform")
        
        if arch not in ARCH_MAP:
            print(f"Unsupported architecture: {arch}")
            raise OSError("Unsupported architecture")

        platform_name = PLATFORM_MAP[system]
        arch_name = ARCH_MAP[arch]

        asset_name = f"anon-live-{platform_name}-{arch_name}.zip"
        binary_dir = Path.home() / ".anon_python_sdk" / "bin"
        binary_dir.mkdir(parents=True, exist_ok=True)

        # Fetch release data
        print("Fetching release information...")
        response = requests.get(RELEASE_URL)
        response.raise_for_status()
        assets = response.json().get("assets", [])
        download_url = next(
            (asset["browser_download_url"] for asset in assets if asset["name"] == asset_name),
            None,
        )

        if not download_url:
            print(f"Binary for platform {platform_name} and architecture {arch_name} is not available.")
            return

        # Download and extract the binary
        print(f"Downloading binary from {download_url}...")
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / asset_name
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(binary_dir)

        # Make the binary executable
        for file in binary_dir.iterdir():
            if file.is_file():
                file.chmod(file.stat().st_mode | stat.S_IEXEC)

        print(f"Binary installed to {binary_dir}")


# Standard setup.py configuration
setup(
    name="anon_python_sdk",
    version="0.0.8",
    description="Python SDK for Anon",
    packages=find_packages(),
    package_data={"anon_python_sdk": ["bin/*"]},
    include_package_data=True,
    install_requires=[
        "requests[socks]",
        "stem"
    ],
    cmdclass={
        "install": CustomInstallCommand,  # Use the custom install command
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)