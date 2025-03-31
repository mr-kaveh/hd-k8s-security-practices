import os
import subprocess
import shutil

# Define node details
master_ip = "192.168.1.100"  # IP address of the master node
worker_ips = ["192.168.1.101", "192.168.1.102"]  # IP addresses of the worker nodes

# Define base directory for PKI files
base_dir = "/etc/kubernetes/pki"

# Group node details into a dictionary for easier reference
nodes = {"master": master_ip, "workers": worker_ips}


# Function to create a directory if it doesn't exist
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)  # Create the directory
        print(f"Created directory: {path}")


# Function to generate a private key and self-signed certificate for a component
def generate_key_and_cert(component):
    key_file = f"{base_dir}/{component}.key"  # Path for the key file
    csr_file = f"{base_dir}/{component}.csr"  # Path for the Certificate Signing Request file
    crt_file = f"{base_dir}/{component}.crt"  # Path for the certificate file

    print(f"Generating key and cert for {component}...")

    # Generate a private key
    subprocess.run(["openssl", "genrsa", "-out", key_file, "2048"], check=True)
    # Generate a CSR using the private key
    subprocess.run(["openssl", "req", "-new", "-key", key_file, "-out", csr_file, "-subj", f"/CN={component}"], check=True)
    # Create a self-signed certificate using the CSR and private key
    subprocess.run(["openssl", "x509", "-req", "-in", csr_file, "-signkey", key_file, "-out", crt_file], check=True)

    return key_file, crt_file


# Function to copy key and certificate files to a specific node
def copy_files_to_node(ip, component, key_file, crt_file):
    target_dir = f"/etc/kubernetes/pki/{component}"  # Target directory on the node
    print(f"Copying files for {component} to node {ip}...")

    create_dir(target_dir)  # Ensure target directory exists
    shutil.copy(key_file, target_dir)  # Copy the private key
    shutil.copy(crt_file, target_dir)  # Copy the certificate
    print(f"Files copied to {ip}:{target_dir}")


# Function to set up components by generating keys/certs and copying them to nodes
def setup_components():
    components = ["etcd", "scheduler", "apiserver", "kubelet"]  # Components of the cluster

    for component in components:
        # Generate key and certificate for the component
        key_file, crt_file = generate_key_and_cert(component)

        # Copy files to the master node
        copy_files_to_node(master_ip, component, key_file, crt_file)

        # Copy kubelet-specific files to all worker nodes
        if component == "kubelet":
            for worker_ip in worker_ips:
                copy_files_to_node(worker_ip, component, key_file, crt_file)


# Function to create basic configuration files for each component
def create_config_files():
    print("Creating configuration files...")
    components = ["etcd", "scheduler", "apiserver", "kubelet"]  # Components to configure

    for component in components:
        config_file = f"/etc/kubernetes/config/{component}.conf"  # Path for the config file
        create_dir(os.path.dirname(config_file))  # Ensure config directory exists
        with open(config_file, "w") as f:
            # Write basic configuration details
            f.write(f"# Configuration file for {component}\n")
            f.write(f"component: {component}\n")
            f.write(f"server: {nodes['master'] if component != 'kubelet' else nodes['workers']}\n")
        print(f"Configuration created: {config_file}")


# Main function to orchestrate the script
def main():
    print("Setting up Kubernetes cluster PKI and configuration...")
    create_dir(base_dir)  # Ensure base directory for PKI exists
    setup_components()  # Generate certificates and set up components
    create_config_files()  # Generate configuration files


# Entry point of the script
if __name__ == "__main__":
    main()
