
### How the script functions:

1.  **Certificate and Key Generation**:
    
    -   Creates RSA keys using OpenSSL.
        
    -   Generates a self-signed certificate for each component.
        
2.  **Directory Management**:
    
    -   Ensures directories for certificates and configuration files are created.
        
3.  **File Distribution**:
    
    -   Copies certificates and keys to appropriate locations for the master and worker nodes.
        
4.  **Configuration Files**:
    
    -   Generates simple configuration files for each component with details like component name and target server.
        

### Note:

-   You need OpenSSL installed on the system to run this script.
    
-   Adjust the IPs, paths, and file structure as per your actual cluster configuration.
    
-   For a production environment, consider using proper Certificate Authorities (CAs) and secure methods for distributing files.
