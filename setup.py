import os
import platform
import subprocess
import sys

# Function to create a virtual environment
def create_virtualenv():
    print("\n🐍 Creating a virtual environment...\n")

    venv_dir = "venv"

    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print(f"✅ Virtual environment created successfully in {venv_dir}/\n")
    except subprocess.CalledProcessError:
        print("\n❌ Error creating virtual environment.\n")
        exit(1)

# Function to install dependencies
def install_dependencies():
    print("\n📦 Installing dependencies from requirements.txt...\n")

    pip_executable = os.path.join("venv", "Scripts" if platform.system() == "Windows" else "bin", "pip")

    try:
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
        print("\n✅ Dependencies installed successfully!\n")
    except subprocess.CalledProcessError:
        print("\n❌ Error installing dependencies. Make sure your `requirements.txt` exists and is valid.\n")
        exit(1)

# Function to create .env file
def create_env_file():
    print("\n🛠️  Setting up .env file...")

    admin_username = input("Enter Admin Username: ").strip()
    admin_password = input("Enter Admin Password: ").strip()

    env_content = f"ADMIN_USERNAME={admin_username}\nADMIN_PASSWORD={admin_password}\n"

    try:
        with open(".env", "w") as env_file:
            env_file.write(env_content)
        print("\n✅ .env file created successfully!\n")
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}\n")
        exit(1)

# Function to check OS and provide necessary messages
def setup_environment():
    os_name = platform.system()
    if os_name == "Windows":
        print("\n🔹 Detected Windows OS")
        print("⚠️ If you're using PowerShell, use: `python setup.py`")
    else:
        print("\n🔹 Detected UNIX-based OS (Linux/macOS)")

# Run setup
if __name__ == "__main__":
    setup_environment()
    create_virtualenv()
    install_dependencies()
    create_env_file()

    print("\n🚀 Setup complete! Your project is ready to go.\n")
    print("\n🔹 To activate the virtual environment:")
    if platform.system() == "Windows":
        print("   - Run: `venv\\Scripts\\activate` (cmd) or `venv\\Scripts\\Activate.ps1` (PowerShell)")
    else:
        print("   - Run: `source venv/bin/activate`")
    print("\n🔹 To start Flask:")
    print("   - Run: `flask run`\n")
