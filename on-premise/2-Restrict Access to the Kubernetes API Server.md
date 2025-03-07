
-   **Use Network Policies** to limit which IPs can reach the Kubernetes API server.
-   **Restrict kubelet access** to prevent unauthorized access to nodes.

Example network policy:

	apiVersion: networking.k8s.io/v1
	kind: NetworkPolicy
	metadata:
	  name: deny-external-access
	  namespace: kube-system
	spec:
	  podSelector:
	    matchLabels:
	      component: apiserver
	  ingress:
	    - from:
	        - ipBlock:
	            cidr: 10.0.0.0/16  # Allow only internal network


