#!/usr/bin/env python3
# ^ This is a shebang that essentially tells Linux devices what to run this script with
# The line is ignored unless directly executed in the shell (`./PS3RPD.py`)
import subprocess  # used for running uv installer and PS3RPD script
import sys  # used for exiting the program with proper exit codees # to check path for "uv"
import shutil  # to check path for "uv" and "curl"


def ask_install_uv():
    print("uv package manager is not installed.")
    print("uv can be installed via curl with the following command:")
    print("curl -LsSf https://astral.sh/uv/install.sh | sh")
    choice = input("Would you like to run it now? [y/N]: ").strip().lower()
    if choice == "y":
        if shutil.which("curl") is None:
            print("`curl` not found, cannot run command")
            print(
                "Please install curl with `sudo apt-get install curl -y` before running again"
            )
            sys.exit(1)
        try:
            subprocess.check_call(
                ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
            )
            print("uv installed successfully. Please restart the script.")
            sys.exit(0)
        except Exception as e:
            print(f"Installation failed: {e}")
            sys.exit(1)
    else:
        print("uv is required to run the script with dependencies. Exiting.")
        sys.exit(1)


def run_with_uv():
    # Run current script via uv to manage dependencies
    args = ["uv", "run", "--script", "./PS3RPD.py"]
    try:
        subprocess.check_call(args)
    except Exception as e:
        print(f"Failed to run script with uv: {e}")
        sys.exit(1)


def main():
    if shutil.which("uv") is None:
        ask_install_uv()
    else:
        run_with_uv()


if __name__ == "__main__":
    main()
