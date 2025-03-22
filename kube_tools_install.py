import os
import subprocess

def run_command(command):
    """
    Run a shell command and handle any errors.
    :param command: The command to be executed in the shell.
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {command}\n{e}")
        exit(1)

def install_prerequisites():
    """
    Install prerequisites like git and curl, which are needed to clone repositories
    and download files during the installation process.
    """
    print("Installing prerequisites (git and curl)...")
    # Update the package list to ensure we're installing the latest versions
    run_command("sudo apt-get update -y")
    # Install git and curl if they are not already present
    run_command("sudo apt-get install -y git curl")

def install_kubectx_kubens():
    """
    Clone the kubectx repository from GitHub and set up symbolic links
    to make kubectx and kubens commands available system-wide.
    """
    print("Cloning kubectx and kubens repository...")
    # Clone the repository into the user's home directory
    run_command("git clone https://github.com/ahmetb/kubectx.git ~/.kubectx")
    
    # Create symbolic links to the kubectx and kubens scripts so they can be run globally
    print("Setting up kubectx...")
    run_command("sudo ln -sf ~/.kubectx/kubectx /usr/local/bin/kubectx")
    print("Setting up kubens...")
    run_command("sudo ln -sf ~/.kubectx/kubens /usr/local/bin/kubens")
    
    print("kubectx and kubens have been installed successfully!")

def add_autocompletion():
    """
    Add autocompletion for kubectx and kubens in the user's shell configuration file.
    Supports both bash and zsh shells.
    """
    # Detect the user's current shell (bash or zsh)
    shell = os.environ.get("SHELL", "").split("/")[-1]
    if shell == "bash":
        print("Setting up autocompletion for bash...")
        # Add autocompletion for bash by sourcing the necessary scripts
        run_command("echo 'source <(kubectl completion bash)' >> ~/.bashrc")
        run_command("echo 'source ~/.kubectx/completion/kubectx.bash' >> ~/.bashrc")
        run_command("echo 'source ~/.kubectx/completion/kubens.bash' >> ~/.bashrc")
    elif shell == "zsh":
        print("Setting up autocompletion for zsh...")
        # Add autocompletion for zsh by sourcing the necessary scripts
        run_command("echo 'source <(kubectl completion zsh)' >> ~/.zshrc")
        run_command("echo 'source ~/.kubectx/completion/kubectx.zsh' >> ~/.zshrc")
        run_command("echo 'source ~/.kubectx/completion/kubens.zsh' >> ~/.zshrc")
    else:
        # If the user's shell is neither bash nor zsh, skip the autocompletion setup
        print("Unknown shell type. Skipping autocompletion setup.")
    
    print("Autocompletion has been set up successfully!")

def main():
    """
    The main function orchestrates the installation of prerequisites,
    the cloning and setup of kubectx and kubens, and the configuration of autocompletion.
    """
    # Step 1: Install necessary tools like git and curl
    install_prerequisites()
    # Step 2: Install kubectx and kubens by cloning their repository
    install_kubectx_kubens()
    # Step 3: Add shell autocompletion for convenience
    add_autocompletion()

# Start the process by calling the main function
if __name__ == "__main__":
    main()
