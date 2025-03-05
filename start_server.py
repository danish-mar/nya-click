import os
import platform
import subprocess

def run_flask():
    os_name = platform.system()

    # Detect the shell command based on OS
    if os_name == "Windows":
        activate_cmd = "venv\\Scripts\\activate && flask run"
        terminal = ["cmd.exe", "/k", activate_cmd]
    else:
        activate_cmd = "source .venv/bin/activate && flask run"
        terminal = ["bash", "-c", activate_cmd]

    print("\n🚀 Opening a new terminal and starting Flask...\n")

    try:
        subprocess.Popen(terminal)
    except Exception as e:
        print(f"\n❌ Error launching Flask: {e}\n")

if __name__ == "__main__":
    run_flask()
