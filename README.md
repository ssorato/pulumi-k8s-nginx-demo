# K8s nginx demo

Sample nginx POD with external access.

# Note about deployment replacement

By specifying the ConfigMap `name` rather than using [auto-naming](https://www.pulumi.com/docs/intro/concepts/resources/names/#autonaming), Pulumi will delete and recreate the deployment.
