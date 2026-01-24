### Phase 4 Objective: Diagnose Cluster Health with `kagent`

This skill details how to use `kagent` to monitor, analyze, and debug the Kubernetes cluster running in Minikube.

#### 1. Perform a Full Cluster Health Check
- **Command**: `kagent --analyze-cluster`
- **Purpose**: Get a comprehensive report of the cluster's health, including node status, resource pressure (CPU/memory), and the state of critical system pods (e.g., kube-dns, etcd).
- **Action**: Review the report for any warnings or errors.

#### 2. Analyze Resource Allocation for a Specific Deployment
- **Command**: `kagent --analyze-deployment frontend-deployment`
- **Purpose**: Check the resource utilization (CPU/memory requests vs. limits vs. actual usage) for all pods managed by the `frontend-deployment`.
- **Action**: Identify if pods are over-provisioned or under-provisioned. Use this data to adjust `resources` in the Helm chart for better efficiency.

#### 3. Diagnose Pod Issues
- **Command**: `kagent --diagnose-pod <pod-name>`
- **Purpose**: When a pod is stuck in a `Pending`, `CrashLoopBackOff`, or `Error` state, this command provides a detailed diagnosis. It checks for common issues like:
  - Failed volume mounts.
  - Insufficient cluster resources.
  - Image pull errors.
  - Liveness/readiness probe failures.
- **Action**: Follow the recommendations provided by `kagent` to resolve the pod issue.

#### 4. Monitor Network Policies
- **Command**: `kagent --audit-network`
- **Purpose**: To ensure that traffic is flowing correctly between the frontend, backend, and any other services. It checks for misconfigured NetworkPolicies or service routing issues.
- **Action**: Address any connectivity problems reported by the audit.
