import os
import subprocess
import chromedriver_autoinstaller

def get_chrome_version():
    """Get the installed Chrome browser version."""
    result = subprocess.run(
        ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    version = result.stdout.decode().strip().split(' ')[-1]
    return version


def get_driver_path(full_chrome_version: str):
    """Get the installed Chrome browser version without the patch number."""
    chrome_version = full_chrome_version.split('.')[0]
    return f'./{chrome_version}/chromedriver'  # Path to the downloaded chromedriver


def download_chromedriver():
    chrome_version = get_chrome_version()
    print(f"Installed Chrome version: {chrome_version}")
    driver_path = get_driver_path(chrome_version)
    print("Checking if Chromedriver is already downloaded...")
    if os.path.exists(driver_path):
        print("Chromedriver is already downloaded.")
        return driver_path

    print("Downloading Chromedriver...")

    chromedriver_autoinstaller.install(True)  # Automatically install matching ChromeDriver
    print("ChromeDriver installed successfully.")
    return driver_path

if __name__ == '__main__':
    download_chromedriver()
