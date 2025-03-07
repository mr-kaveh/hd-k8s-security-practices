
-   **Enable TLS for all intra-cluster communication** (use cert-manager).
   -   **Use etcd encryption:** Ensure sensitive data in `etcd` is encrypted:

	kubectl get secrets -n kube-system

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



 

