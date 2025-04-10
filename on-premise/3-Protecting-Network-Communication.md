
### **Network Policies**
inside the K8s cluster, we should always control the traffic between the pods. these restrictions bring complications to our configurations specially to our network policies, but then we will make sure the flow of traffic between the pods. here is a very simple example that allow our backend pod(***backend*** is the label) to only accept ingress traffic from the db pod(***db*** is the label):

	apiVersion: networking.k8s.io/v1
	kind: NetworkPolicy
	metadata:
	  name: allow-db-access
	  namespace: default
	spec:
	  podSelector:
	    matchLabels:
	      app: backend # This is the source of our policy
	  policyTypes:
	  - Ingress
	  ingress:
	  - from:
	    - podSelector:
	        matchLabels:
	          app: db # Traffic comes from this pod

Here we are primarily working at **Layer 3 (Network Layer)** and **Layer 4 (Transport Layer)** of the OSI model:
-   **Layer 3 (Network)**: Network policies control the flow of traffic between pods, namespaces, or external IPs based on IP addresses and CIDR blocks.    
-   **Layer 4 (Transport)**: They also manage traffic based on ports and protocols (e.g., TCP, UDP), which are part of the transport layer.

With a network policy, we can allow or deny TCP traffic to a specific pod on port 80 or block UDP traffic entirely, effectively applying security controls at these layers.

Let's create another example to allow only HTTP traffic (port 80) to a pod labeled `app: frontend` from pods labeled `app: backend` in the same namespace, while denying all other traffic:

	apiVersion: networking.k8s.io/v1
	kind: NetworkPolicy
	metadata:
	  name: allow-http-from-backend
	  namespace: default
	spec:
	  podSelector:
	    matchLabels:
	      app: frontend # This is the source of our policy
	  policyTypes:
	  - Ingress
	  ingress:
	  - from:
	    - podSelector:
	        matchLabels:
	          app: backend # Traffic comes from this pod
	    ports:
	    - protocol: TCP
	      port: 80 # Ensures only HTTP traffic is permitted

Now let's look at another example, where the **backend** pods are the target for the policy, and they should only allow traffic(ingress) from **frontend** and are only allowed to send traffic(egress) to **database** pods:

	apiVersion: networking.k8s.io/v1
	kind: NetworkPolicy
	metadata:
	  name: backend-network-policy
	  namespace: default
	spec:
	  podSelector:
	    matchLabels:
	      app: backend
	  policyTypes:
	  - Ingress
	  - Egress
	  ingress:
	  - from:
	    - podSelector:
	        matchLabels:
	          app: frontend
	    ports:
	    - protocol: TCP
	      port: 443
	  egress:
	  - to:
	    - podSelector:
	        matchLabels:
	          app: database
	    ports:
	    - protocol: TCP
	      port: 5432

We can also write more complex policies to even restrict IP Blocks and namespaces:

	apiVersion: networking.k8s.io/v1
	kind: NetworkPolicy
	metadata:
	  name: secure-backend-policy-with-ipblock
	  namespace: default
	spec:
	  podSelector:
	    matchLabels:
	      app: backend
	  policyTypes:
	  - Ingress
	  - Egress
	  ingress:
	  - from:
	    - podSelector:
	        matchLabels:
	          app: frontend
	      namespaceSelector:
	        matchLabels:
	          team: frontend-team
	    - ipBlock:
	        cidr: 192.168.0.0/16
	        except:
	        - 192.168.1.0/24
	    ports:
	    - protocol: TCP
	      port: 80
	  egress:
	  - to:
	    - podSelector:
	        matchLabels:
	          app: database
	      namespaceSelector:
	        matchLabels:
	          team: database-team
	    - ipBlock:
	        cidr: 10.0.0.0/8
	        except:
	        - 10.1.0.0/16
	    ports:
	    - protocol: TCP
	      port: 5432
