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
    run_command("sudo apt-get update -y")
    run_command("sudo apt-get install -y git curl")

def install_kubectx_kubens():
    """
    Clone the kubectx repository from GitHub and set up symbolic links
    to make kubectx and kubens commands available system-wide.
    """
    print("Cloning kubectx and kubens repository...")
    run_command("git clone https://github.com/ahmetb/kubectx.git ~/.kubectx")
    
    print("Setting up kubectx...")
    run_command("sudo ln -sf ~/.kubectx/kubectx /usr/local/bin/kubectx")
    print("Setting up kubens...")
    run_command("sudo ln -sf ~/.kubectx/kubens /usr/local/bin/kubens")
    
    print("kubectx and kubens have been installed successfully!")

def install_k9s():
    """
    Install the k9s tool for Kubernetes cluster management.
    """
    print("Installing k9s...")
    # Download the latest k9s release from GitHub and extract it
    run_command("curl -s https://api.github.com/repos/derailed/k9s/releases/latest | grep 'browser_download_url.*Linux_x86_64.tar.gz' | cut -d '\"' -f 4 | wget -qi -")
    run_command("tar -xvf k9s_Linux_x86_64.tar.gz")
    # Move the k9s binary to a directory in the system's PATH
    run_command("sudo mv k9s /usr/local/bin/")
    print("k9s has been installed successfully!")

def add_autocompletion():
    """
    Add autocompletion for kubectx and kubens in the user's shell configuration file.
    Supports both bash and zsh shells.
    """
    shell = os.environ.get("SHELL", "").split("/")[-1]
    if shell == "bash":
        print("Setting up autocompletion for bash...")
        run_command("echo 'source <(kubectl completion bash)' >> ~/.bashrc")
        run_command("echo 'source ~/.kubectx/completion/kubectx.bash' >> ~/.bashrc")
        run_command("echo 'source ~/.kubectx/completion/kubens.bash' >> ~/.bashrc")
    elif shell == "zsh":
        print("Setting up autocompletion for zsh...")
        run_command("echo 'source <(kubectl completion zsh)' >> ~/.zshrc")
        run_command("echo 'source ~/.kubectx/completion/kubectx.zsh' >> ~/.zshrc")
        run_command("echo 'source ~/.kubectx/completion/kubens.zsh' >> ~/.zshrc")
    else:
        print("Unknown shell type. Skipping autocompletion setup.")
    
    print("Autocompletion has been set up successfully!")

def main():
    """
    The main function orchestrates the installation process.
    """
    install_prerequisites()
    install_kubectx_kubens()
    install_k9s()
    add_autocompletion()

if __name__ == "__main__":
    main()
