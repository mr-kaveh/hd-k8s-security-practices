### **1. Use Trusted Base Images**

-   We should Always start with a base image from a trusted source, such as official repositories or verified registries like Docker Hub or Red Hat Container Catalog.
    
-   We prefer minimal base images like Alpine or Distroless to reduce the attack surface.

		# Use a minimal and trusted base image like Alpine 		
		FROM alpine:3.18

		# Add only necessary files and packages 		
		RUN apk add --no-cache python3 		
		COPY app.py /app/

		CMD ["python3", "/app/app.py"]

##### Note: We may use `FROM scratch` for extremely minimal images if your application doesn’t require a full OS. scratch base images are suitable for *Security-first*  deployments, since there are no unnecessary files, libraries, or tools that could introduce vulnerabilities.

	# Start from scratch 	FROM scratch

	# Set up working directory 	WORKDIR /app

	# Copy Go binary into the image 	COPY ./data-wrangler /app/data-wrangler

	# Specify the application to run 	ENTRYPOINT ["/app/data-wrangler"]

    

### **2. Regularly Scan Images for Vulnerabilities**

-   We use Trivy to identify vulnerabilities in your images. these scan could be integrated in both in CI and/or CD Pipelines
    
-   Integrate vulnerability scanning into your CI/CD pipeline to catch issues early.
    


		stages:
		  - build
		  - scan
		  - notify

		build-job:
		  stage: build
		  script:
		    - docker build -t hd-data-wrangler:latest .

		trivy-scan:
		  stage: scan
		  image: aquasec/trivy:latest
		  variables:
		    DOCKER_HOST: tcp://docker:2376
		    DOCKER_TLS_CERTDIR: "/certs"
		  services:
		    - docker:19.03.12
		  script:
		    # Scan the Docker image and save the output
		    - trivy image --severity HIGH,CRITICAL --format json --output trivy-report.json hd-data-wrangler:latest || export TRIVY_EXIT_CODE=$?
		    # Print results for debugging
		    - cat trivy-report.json
		  allow_failure: true # Allow this job to fail, so the pipeline can proceed
		  artifacts:
		    when: always
		    paths:
		      - trivy-report.json

		high-critical-action:
		  stage: notify
		  script:
		    # Perform actions if HIGH or CRITICAL vulnerabilities are found
		    - echo "High/Critical vulnerabilities found! Taking appropriate actions."
		    - # e.g., Notify team via email or Slack
		    - ./scripts/notify-team.sh
		  only:
		    - if: $TRIVY_EXIT_CODE == "1"

		no-issues-action:
		  stage: notify
		  script:
		    # Perform actions if no high/critical vulnerabilities are found
		    - echo "No high/critical vulnerabilities detected. Proceeding with deployment."
		  only:
		    - if: $TRIVY_EXIT_CODE == "0"


### **3. Choosing the Right Image**

-   We use **official or LTS images** for production environments to ensure regular updates and better security.
    
-   For experimental or cutting-edge projects, you can explore **rolling or community-contributed images**.
    
-   Enterprises may opt for **enterprise-grade images** to meet compliance and support requirements.
    

### **4. Sign and Verify Images**

a.   Use image signing tools like Docker Content Trust (DCT) or Notary to ensure the integrity of your images:

		export DOCKER_CONTENT_TRUST=1
		docker push hd-image-registry/hd-image:v1.1.22
		
	
*This command signs the image when pushing to your registry.*	

 b. Enable Admission Controller for Image Validation with Kyverno:
  - Installation of Kyverno:
  
  		kubectl create -f https://github.com/kyverno/kyverno/releases/download/v1.11.1/install.yaml
 - We then need to create the ClusterPolicy to enforce:
 
    	apiVersion: kyverno.io/v1
		kind: ClusterPolicy
		metadata:
		  name: require-signed-images
		spec:
		  validationFailureAction: enforce
		  rules:
		    - name: validate-signatures
		      match:
		        resources:
		          kinds:
		            - Pod
		      validate:
		        message: "Images must be signed."
		        pattern:
		          spec:
		            containers:
		              - image: "*@sha256:*"

see the full example on how to test and verify it here:
https://github.com/mr-kaveh/hd-k8s-security-practices/tree/master/kyverno-hd-example

### **5. Avoid Running Containers as Root**

This is to avoid **Privilege escalation attacks**.

**Details:**

-   Explicitly create a non-root user in the Dockerfile.    
-   Limit the container’s capabilities.
    
**Example: Dockerfile**

	FROM python:3.9.21

	# Create a non-root user and switch to it
	RUN useradd -m aiuser
	USER aiuser

	COPY . /home/aiuser/app
	WORKDIR /home/aiuser/app
	CMD ["python", "ml-modeler.py"]
It is also a good practice to define **Pod Security Context**:
	
	apiVersion: v1
	kind: Pod
	metadata:
	  name: secure-pod
	spec:
	  containers:
	    - name: secure-container
	      image: my-app:latest
	      securityContext:
	        runAsNonRoot: true
	        runAsUser: 1000


### **6. Use Multi-Stage Builds**

Multi-stage builds reduce image size by separating build and runtime dependencies:

	FROM ubuntu:18.04 AS compile-image
	RUN apt-get update
	RUN apt-get install -y --no-install-recommends gcc build-essential

	# Create a non-root user and switch to it
	RUN useradd -m appuser
	USER appuser


	WORKDIR /home/appuser
	COPY hello.c .
	RUN gcc -o helloworld hello.c


	# This is the second and final image; it copies the compiled binary
	# over but starts from the base ubuntu:18.04 image.
	FROM ubuntu:18.04 AS runtime-image


	COPY --from=compile-image /home/appuser/helloworld .
	CMD ["./helloworld"]

I have a full article on Multistage build here:
https://www.linkedin.com/pulse/docker-multi-stage-builds-smaller-images-faster-hossein-davoodi/?trackingId=9NEG%2BaP5TMWDiRSKrteW0Q%3D%3D