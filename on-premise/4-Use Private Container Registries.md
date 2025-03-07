
-   **Avoid public registries (e.g., Docker Hub)**; use **Harbor, AWS ECR, or Azure ACR**.
-   **Sign images with Cosign/Sigstore** to prevent tampering.

Example: Enforce only signed images in Kubernetes:

	apiVersion: policy/v1beta1
	kind: PodSecurityPolicy
	metadata:
	  name: signed-images-only
	spec:
	  requiredDropCapabilities:
	    - ALL
	  allowedHostPaths: []
	  runAsUser:
	    rule: MustRunAsNonRoot
	  seLinux:
	    rule: RunAsAny
