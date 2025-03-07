-   Use **FluentBit, ELK, Loki, or CloudWatch** to collect logs.
-   Enable **audit logs** to detect unauthorized access.

Enable Kubernetes auditing:

	apiVersion: audit.k8s.io/v1
	kind: Policy
	rules:
	- level: Request
	  verbs: ["create", "delete"]
	  resources:
	  - group: ""
	    resources: ["pods"]
