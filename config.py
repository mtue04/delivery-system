import sys
import subprocess
from importlib import metadata
import random

# Define screen parameters
SCREEN_SIZE = 600
FPS = 60

# Define font parameters
FONT_SMALL = "Arial"
FONT_MEDIUM = "assets/fonts/Kanit.ttf"
FONT_BIG = "assets/fonts/Barbra.ttf"
FONT_SIZE_SMALL = 30
FONT_SIZE_MEDIUM = 50
FONT_SIZE_BIG = 80

# Define colors
GRID_LINE_COLOR = "#000000"
BACKGROUND_COLOR = "#FFFFFF"
OBSTACLE_COLOR = "#383A40"
START_COLOR = "#7CCC98"
GOAL_COLOR = "#C2767A"
TIME_COLOR = "#A3BDF0"
FUEL_COLOR = "#F0CFA3"
PATH_COLOR = "#FF0000"


def check_and_install_packages():
    """
    This function checks for required packages listed in requirements.txt and installs any that are missing.
    """
    # Read requirements.txt file to get required packages
    required_packages = []
    with open("requirements.txt", "r") as f:
        required_packages = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

    missing_packages = []
    outdated_packages = []
    up_to_date_packages = []

    for package in required_packages:
        package_name, required_version = (
            package.split("==") if "==" in package else (package, None)
        )

        try:
            installed_version = metadata.version(package_name)
            if required_version and installed_version != required_version:
                outdated_packages.append(
                    (package_name, installed_version, required_version)
                )
            else:
                up_to_date_packages.append((package_name, installed_version))
        except metadata.PackageNotFoundError:
            missing_packages.append(package)

    if missing_packages:
        print("Installing missing packages...")
        for package in missing_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    if outdated_packages:
        print("Updating outdated packages...")
        for package, installed_version, required_version in outdated_packages:
            print(
                f"Updating {package} from {installed_version} to {required_version}..."
            )
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    f"{package}=={required_version}",
                ]
            )

    # Show info about installed packages
    print("Status of required packages:")
    for package, version in up_to_date_packages:
        print(f"{package}: {version} (Installed)")
    for package, installed_version, required_version in outdated_packages:
        print(f"{package}: {installed_version} -> {required_version} (Updated)")
    for package in missing_packages:
        print(f"{package}: (Newly installed)")

    print("All required packages are installed and up-to-date.")


def generate_color():
    return (
        random.randint(150, 255),
        random.randint(150, 255),
        random.randint(150, 255),
    )
