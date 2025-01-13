from setuptools import setup, find_packages
from setuptools.command.install import install
import platform
import requests
import zipfile
import tempfile
import shutil
from pathlib import Path
import stat

# Constants
OWNER = "anyone-protocol"
REPO = "ator-protocol"
VERSION = "v0.4.9.9"
RELEASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{VERSION}"

PLATFORM_MAP = {
    "linux": "linux",
    "darwin": "macos",
    "windows": "windows",
}

ARCH_MAP = {
    "arm64": "arm64",
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
        asset_dir = f"anon-live-{platform_name}-{arch_name}"

        # Fetch release data
        print("Fetching release information...")
        response = requests.get(RELEASE_URL)
        response.raise_for_status()
        release_data = response.json()

        # Find the correct asset
        download_url = ""
        for asset in release_data.get("assets", []):
            if asset["name"] == asset_name:
                download_url = asset["browser_download_url"]
                print(f"Download URL: {download_url}")
                break

        if not download_url:
            print(f"Platform {platform_name} ({arch_name}) is not supported.")
            raise ValueError("Unsupported platform/architecture combination")

        # Prepare temporary paths
        tmp_dir = Path(tempfile.gettempdir())
        download_dest = tmp_dir / asset_name
        extract_dest = tmp_dir / asset_dir

        print(f"Temporary download path: {download_dest}")
        print(f"Temporary extraction path: {extract_dest}")

        # Download the binary
        self.download_file(download_url, download_dest)

        # Extract the binary
        print("Extracting the binary...")
        self.unzip_file(download_dest, extract_dest)

        # Copy files to the final destination
        binary_dir = Path.home() / ".anon-python-sdk" / "bin"
        binary_dir.mkdir(parents=True, exist_ok=True)

        for file in extract_dest.iterdir():
            if file.is_file():
                self.make_executable(file)
                shutil.copy(file, binary_dir / file.name)

        print("Anon binary installation complete!")

    @staticmethod
    def     download_file(url, output_path):
        """Download a file from a URL."""
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    @staticmethod
    def unzip_file(zip_file_path, output_dir):
        """Extract a zip file to the specified directory."""
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)

    @staticmethod
    def make_executable(file_path):
        """Make a file executable."""
        file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)


# Standard setup.py configuration
setup(
    name="anon-python-sdk",
    version="0.0.2",
    description="Python SDK for Anon",
    packages=find_packages(),
    package_data={"anon_python_sdk": ["bin/*"]},
    include_package_data=True,
    install_requires=[
        "requests",
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