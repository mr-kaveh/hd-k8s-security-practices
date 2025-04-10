##### Run these

	docker build -t go-image:v1 .
	export DOCKER_CONTENT_TRUST=1
	export DOCKER_CONTENT_TRUST_SERVER=notary.docker.io
	docker login
	docker tag go-image:v1 mrdavoodi/go-image:v1
	docker push mrdavoodi/go-image:v1
	
In case there is a problem with signing the image while pushing like the following error:
###### couldn't add target to targets: could not find necessary signing keys

then use cosign to resign the image again and then push to Docker Hub

	cosign sign docker.io/mrdavoodi/go-image:v1
	
now we create a policy with Kyverno and test it with a deployment:

	kubectl create -f https://github.com/kyverno/kyverno/releases/download/v1.11.1/install.yaml
##### Kyverno Policy
	apiVersion: kyverno.io/v1
	kind: ClusterPolicy
	metadata:
	  name: require-signed-images
	spec:
	  validationFailureAction: enforce
	  background: false
	  rules:
	    - name: validate-image-signatures
	      match:
	        resources:
	          kinds:
	            - Pod
	      validate:
	        message: "Images must be signed and use a content digest (e.g., @sha256:<digest>)."
	        pattern:
	          spec:
	            containers:
	              - image: "*@sha256:*"
and then run:
	
	kubectl apply -f kyverno-policy.yaml

##### Deployment

	apiVersion: apps/v1
	kind: Deployment
	metadata:
	  name: unsigned-deployment
	spec:
	  replicas: 1
	  selector:
	    matchLabels:
	      app: unsigned-app
	  template:
	    metadata:
	      labels:
	        app: unsigned-app
	    spec:
	      containers:
	        - name: unsigned-container
	          image: nginx:latest

this image is not signed , by try to apply this deployment, you will get error, then edit the deployment as follows:

	apiVersion: apps/v1
	kind: Deployment
	metadata:
	  name: signed-deployment
	spec:
	  replicas: 1
	  selector:
	    matchLabels:
	      app: signed-app
	  template:
	    metadata:
	      labels:
	        app: signed-app
	    spec:
	      containers:
	        - name: signed-container
	          image: <your-registry>/<username>/your-image@sha256:<digest>


### **Kyverno + Cosign Example**
	apiVersion: kyverno.io/v1
	kind: ClusterPolicy
	metadata:
	  name: verify-signed-images
	spec:
	  validationFailureAction: Enforce
	  rules:
	  - name: verify-image-signature
	    match:
	      resources:
	        kinds:
	        - Pod
	    verifyImages:
	    - imageReferences:
	      - "ghcr.io/example/image:*"
	      type: Cosign
	      key: "https://fulcio.sigstore.dev"
