import os
import subprocess
import shutil

# Define node details
master_ip = "192.168.1.100"
worker_ips = ["192.168.1.101", "192.168.1.102"]

# Define directories
base_dir = "/etc/kubernetes/pki"
nodes = {"master": master_ip, "workers": worker_ips}


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def generate_key_and_cert(component):
    key_file = f"{base_dir}/{component}.key"
    csr_file = f"{base_dir}/{component}.csr"
    crt_file = f"{base_dir}/{component}.crt"
    print(f"Generating key and cert for {component}...")

    subprocess.run(["openssl", "genrsa", "-out", key_file, "2048"], check=True)
    subprocess.run(["openssl", "req", "-new", "-key", key_file, "-out", csr_file, "-subj", f"/CN={component}"], check=True)
    subprocess.run(["openssl", "x509", "-req", "-in", csr_file, "-signkey", key_file, "-out", crt_file], check=True)

    return key_file, crt_file


def copy_files_to_node(ip, component, key_file, crt_file):
    target_dir = f"/etc/kubernetes/pki/{component}"
    print(f"Copying files for {component} to node {ip}...")

    create_dir(target_dir)
    shutil.copy(key_file, target_dir)
    shutil.copy(crt_file, target_dir)
    print(f"Files copied to {ip}:{target_dir}")


def setup_components():
    components = ["etcd", "scheduler", "apiserver", "kubelet"]

    for component in components:
        key_file, crt_file = generate_key_and_cert(component)

        # Copy files to master
        copy_files_to_node(master_ip, component, key_file, crt_file)

        # Copy files to worker nodes if component is kubelet
        if component == "kubelet":
            for worker_ip in worker_ips:
                copy_files_to_node(worker_ip, component, key_file, crt_file)


def create_config_files():
    print("Creating configuration files...")
    components = ["etcd", "scheduler", "apiserver", "kubelet"]

    for component in components:
        config_file = f"/etc/kubernetes/config/{component}.conf"
        create_dir(os.path.dirname(config_file))
        with open(config_file, "w") as f:
            f.write(f"# Configuration file for {component}\n")
            f.write(f"component: {component}\n")
            f.write(f"server: {nodes['master'] if component != 'kubelet' else nodes['workers']}\n")
        print(f"Configuration created: {config_file}")


def main():
    print("Setting up Kubernetes cluster PKI and configuration...")
    create_dir(base_dir)
    setup_components()
    create_config_files()


if __name__ == "__main__":
    main()
