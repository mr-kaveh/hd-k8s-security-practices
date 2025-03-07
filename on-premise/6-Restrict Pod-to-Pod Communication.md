-   Use **NetworkPolicies** to limit which pods can talk to each other.
Example: Only allow web app to communicate with the database:

		apiVersion: networking.k8s.io/v1
		kind: NetworkPolicy
		metadata:
		  name: allow-web-to-db
		  namespace: production
		spec:
		  podSelector:
		    matchLabels:
		      role: database
		  ingress:
		    - from:
		        - podSelector:
		            matchLabels:
		              role: webapp
		      ports:
		        - protocol: TCP
		          port: 5432
