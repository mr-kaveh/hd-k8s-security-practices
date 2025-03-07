
-   Use **Falco** to detect suspicious activity.
-   Set up **Prometheus alerts** for unusual CPU/memory spikes.

Example Falco rule (Detect exec into a container):

	- rule: Terminal Shell in Container
	  desc: Detect exec into a container
	  condition: evt.type=execve and container.id!=host and proc.name=sh
	  output: "Terminal shell exec detected (user=%user.name command=%proc.cmdline)"
