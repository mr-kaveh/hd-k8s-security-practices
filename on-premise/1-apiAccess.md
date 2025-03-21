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


