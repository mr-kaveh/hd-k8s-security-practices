
## Enable TLS for all intra-cluster communication(use cert-manager)
### 1. Verify Current TLS Configuration

First, check your current TLS setup:

	kubectl get --raw / | jq '.paths[] | select(contains("certs"))'

### 2. Enable TLS for API Server

Update your API server configuration (usually in  `/etc/kubernetes/manifests/kube-apiserver.yaml`):

	spec:
	  containers:
	  - command:
	    - kube-apiserver
	    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
	    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
	    - --client-ca-file=/etc/kubernetes/pki/ca.crt
	    - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
	    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key

### 3. Configure kubelet TLS

On each node, edit  `/var/lib/kubelet/config.yaml`:

	serverTLSBootstrap: true
	tlsCertFile: /var/lib/kubelet/pki/kubelet.crt
	tlsPrivateKeyFile: /var/lib/kubelet/pki/kubelet.key
	clientCAFile: /etc/kubernetes/pki/ca.crt

### 4. Enable TLS for etcd

Edit your etcd configuration (typically  `/etc/kubernetes/manifests/etcd.yaml`):

	spec:
	  containers:
	  - command:
	    - etcd
	    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
	    - --key-file=/etc/kubernetes/pki/etcd/server.key
	    - --client-cert-auth=true
	    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
	    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
	    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
	    - --peer-client-cert-auth=true
	    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

### 5. Configure Controller Manager and Scheduler

Update their manifests to use TLS:

	# For controller-manager
	spec:
	  containers:
	  - command:
	    - kube-controller-manager
	    - --use-service-account-credentials=true
	    - --root-ca-file=/etc/kubernetes/pki/ca.crt
	    - --service-account-private-key-file=/etc/kubernetes/pki/sa.key

	# For scheduler
	spec:
	  containers:
	  - command:
	    - kube-scheduler
	    - --tls-cert-file=/etc/kubernetes/pki/scheduler.crt
	    - --tls-private-key-file=/etc/kubernetes/pki/scheduler.key

- Use The **External Secrets Operator (ESO)**
		
		helm repo add external-secrets https://charts.external-secrets.io
		helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace
		
example Secret store:

	apiVersion: external-secrets.io/v1beta1
	kind: SecretStore
	metadata:
	  name: aws-secret-store
	  namespace: default
	spec:
	  provider:
	    aws:
	      service: SecretsManager
	      region: us-east-1
	      auth:
	        secretRef:
	          accessKeyIDSecretRef:
	            name: aws-credentials
	            key: access-key
	          secretAccessKeySecretRef:
	            name: aws-credentials
	            key: secret-access-key



 
