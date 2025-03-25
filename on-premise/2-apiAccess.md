**Enable Role-Based Access Control (RBAC):**

#### How RBAC works

 1. **Define Roles**: We identify Roles within our Organization(Administrator, Developer, etc,..)
 2. **Define Permissions**: What each role can do (read, write, delete)
 3. **Assign Role to Users**: Link users to roles based on their responsibilities in our Organization

##### Keep in mind that users should have **least privilege** access.

#### Examples:

 - Grants full access to a "Cluster Admin" role:

		apiVersion: rbac.authorization.k8s.io/v1
		kind: ClusterRole
		metadata:
		  name: cluster-admin
		rules:
		  - apiGroups: ["*"]
		    resources: ["*"]
		    verbs: ["*"]

Now we bind our role to user using **ClusterRoleBinding**

	apiVersion: rbac.authorization.k8s.io/v1
	kind: ClusterRoleBinding
	metadata:
		name: cluster-admin-binding
	subjects:
		- kind: User
		  name: admin
		  apiGroup: rbac.authorization.k8s.io
	roleRef:
		kind: ClusterRole
		name: cluster-admin
		apiGroup: rbac.authorization.k8s.io


 Example: Allow only **admins** to deploy applications.

	apiVersion: rbac.authorization.k8s.io/v1
	kind: Role
	metadata:
	  namespace: production
	  name: developer-role
	rules:
	- apiGroups: [""]
	  resources: ["pods"]
	  verbs: ["get", "list", "create"]

- Grant access to Developer

		apiVersion: rbac.authorization.k8s.io/v1
		kind: Role
		metadata:
			namespace: dev-ns
			name: developer-role
		rules:
			- apiGroups: [""]
			  resources: ["pods", "services", "deployments"]
			  verbs: ["get", "list", "create", "update", "delete"]

Binding Role to a Developer Group:

	apiVersion: rbac.authorization.k8s.io/v1
	kind: RoleBinding
	metadata:
	  namespace: dev-namespace
	  name: developer-binding
	subjects:
	  - kind: Group
	    name: dev-team
	    apiGroup: rbac.authorization.k8s.io
	roleRef:
	  kind: Role
	  name: developer-role
	  apiGroup: rbac.authorization.k8s.io

##### Note here: the subject kind which is defined as group does refer to the LDAP group called dev-team; that is because the Kubernetes cluster does not manage group definitions. it only enforces permissions based on the group information provided by the authentication system. You need to configure and manage groups externally.

#### Integrate with an Identity Provider (OIDC, LDAP, or Active Directory)
##### 1. Set Up an LDAP Server

	helm install openldap stable/openldap --namespace identity

##### 2.Integrate LDAP with Kubernetes Authentication
Kubernetes does not natively support LDAP, so you'll need an intermediary authentication mechanism, which i am gonna use OpenID Connect(OIDC) 

	User -> LDAP (via Identity Provider) -> OIDC Tokens -> Kubernetes API Server

 ##### Step 1: Set Up Identity Provider (e.g., Keycloak or Dex)
-   Deploy **Dex** in your cluster or externally.
-   Configure Dex to use LDAP:

		connectors:
		- type: ldap
		  id: ldap
		  name: LDAP
		  config:
		    host: ldap.dirserver.com:389
		    insecureNoSSL: true
		    bindDN: uid=admin,dc=dirserver,dc=com
		    bindPW: admin-password
		    userSearch:
		      baseDN: ou=Users,dc=dirserver,dc=com
		      filter: "(objectClass=person)"
		      username: uid
		      idAttr: uid
		      emailAttr: mail
		      nameAttr: cn
		    groupSearch:
		      baseDN: ou=Groups,dc=dirserver,dc=com
		      filter: "(objectClass=groupOfNames)"
		      userMatchers:
		        - userAttr: DN
		          groupAttr: member
		      nameAttr: cn

##### Step 2: Configure Kubernetes API Server for OIDC
	--oidc-issuer-url=https://dex.ouroidc.com/realms/token-universe
	--oidc-client-id=kubernetes
	--oidc-username-claim=email
	--oidc-groups-claim=groups
	--oidc-ca-file=/etc/kubernetes/pki/ca.crt

##### Step 3: Get OIDC Tokens for kubectl

We use **kubectl plugin** or tools like `kubelogin`, `kube-oidc-proxy`, or `dex-k8s-authenticator` for browser-based login.

Example config snippet for `~/.kube/config`:

	users:
	- name: oidc-user
	  user:
	    auth-provider:
	      name: oidc
	      config:
	        idp-issuer-url: https://dex.ouroidc.com/realms/token-universe
	        client-id: kubernetes
	        client-secret: hd-client-secret
	        id-token: hd-id-token
	        refresh-token: hd-refresh-token






