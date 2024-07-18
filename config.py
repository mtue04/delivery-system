import pkg_resources
import subprocess
import sys

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
        required_packages = f.readlines()
    required_packages = [package.strip() for package in required_packages]

    # Get installed packages list
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted([i.key for i in installed_packages])

    # Check if all required packages are installed
    missing_packages = []
    for package in required_packages:
        if package not in installed_packages_list:
            missing_packages.append(package)

    if len(missing_packages) == 0:
        print("All required packages are installed.")
    else:
        print("The following packages are missing:", ", ".join(missing_packages))
        print("Installing missing packages...")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
