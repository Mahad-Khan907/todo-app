# Troubleshooting Guide

This document outlines common issues and solutions for the Event-Driven Todo System deployed on Kubernetes.

## Common Pod Startup Issues

### ImagePullBackOff
**Symptoms**: Pods stuck in `ImagePullBackOff` status
**Causes**:
- Incorrect image repository/tag in deployment manifests
- Private registry credentials not configured
- Image doesn't exist in the specified registry

**Solutions**:
```bash
# Check the pod events for more details
kubectl describe pod <pod-name>

# Verify the image name in the deployment
kubectl get deployment <deployment-name> -o yaml

# If using private registry, ensure imagePullSecrets are configured:
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry-server> \
  --docker-username=<your-name> \
  --docker-password=<your-password> \
  --docker-email=<your-email>
```

### ContainerCreating/Init:CrashLoopBackOff
**Symptoms**: Pods stuck in `ContainerCreating` or restarting continuously
**Causes**:
- Insufficient resources (CPU/memory)
- Volume mount issues
- Missing dependencies or configuration

**Solutions**:
```bash
# Check pod status and events
kubectl get pods
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name> --previous

# Verify resource requests/limits
kubectl top pods
```

### Dapr Sidecar Injection Failures
**Symptoms**: Applications failing to start with Dapr-related errors
**Causes**:
- Dapr control plane not running
- Incorrect Dapr annotations in deployment
- Network policies blocking Dapr communication

**Solutions**:
```bash
# Verify Dapr control plane is running
kubectl get pods -n dapr-system

# Check Dapr logs
kubectl logs -l app=dapr-placement-server -n dapr-system
kubectl logs -l app=dapr-sidecar-injector -n dapr-system

# Verify your deployment has correct Dapr annotations
kubectl describe deployment <your-app-deployment>
```

### SQLAlchemy vs SQLModel Dependency Conflict
**Symptoms**: Docker build failures with error "Could not find a version that satisfies the requirement SQLAlchemy<2.1.0,>=2.0.14 (from sqlmodel)"
**Causes**:
- Version incompatibility between SQLModel and SQLAlchemy
- Restrictive version constraints in requirements.txt

**Solutions**:
```bash
# Update requirements.txt with compatible versions:
sqlmodel==0.0.14
sqlalchemy==1.4.41

# Or use a more flexible constraint:
sqlmodel
SQLAlchemy>=1.4,<2.0
```

### Docker Build Timeouts
**Symptoms**: Docker builds failing with connection timeouts during pip downloads
**Causes**:
- Large build context size
- Network connectivity issues during build
- Slow dependency downloads

**Solutions**:
```bash
# Create a .dockerignore file to exclude unnecessary files
# Optimize Dockerfile with multi-stage builds
# Use pip wheel caching for faster builds
```

## Kafka/Redpanda Connectivity Issues

### Producer/Consumer Connection Failures
**Symptoms**: Applications unable to connect to Kafka/Redpanda
**Causes**:
- Kafka/Redpanda service not running
- Network policies blocking connections
- Incorrect broker addresses in application configuration

**Solutions**:
```bash
# Check Kafka/Redpanda pods and services
kubectl get pods,services -l app=kafka
kubectl get pods,services -l app=redpanda

# Test connectivity from inside the cluster
kubectl run test-kafka --image=busybox --rm -it --restart=Never -- \
  wget -O- http://kafka:9092

# Verify Dapr component configuration
kubectl get component task-pubsub -o yaml
```

## Database Connection Issues

### Connection Timeout/Refused
**Symptoms**: Applications failing to connect to the database
**Causes**:
- Database service not running
- Incorrect database URL
- Network policies blocking database access

**Solutions**:
```bash
# Check database pods and services
kubectl get pods,services -l app=postgres

# Test database connectivity
kubectl run pg-test --image=postgres:13 --rm -it --restart=Never -- \
  psql -h postgres-service -U postgres -c "\dt"

# Verify database configuration in secrets
kubectl get secrets db-secret -o yaml
```

## Health Check Failures

### Liveness/Readiness Probes Failing
**Symptoms**: Pods restarting or not becoming ready
**Causes**:
- Application taking too long to start
- Health check endpoints returning incorrect status
- Resource constraints causing slow response

**Solutions**:
```bash
# Check pod events for probe failures
kubectl describe pod <pod-name>

# Adjust probe settings in deployment
# Increase initialDelaySeconds, periodSeconds, or failureThreshold
```

## Dapr-Specific Troubleshooting

### Dapr Sidecar Not Starting
```bash
# Check if the sidecar injector is working
kubectl logs -l app=dapr-sidecar-injector -n dapr-system

# Verify the deployment has correct annotations
# Should include: dapr.io/enabled: "true"
# And other required annotations

# Check if the application port is correctly specified
# dapr.io/app-port annotation should match the app's listening port
```

### Service Invocation Issues
```bash
# Verify the app-id is correctly set
kubectl get configuration dapr-config -o yaml

# Check if the service can be reached via Dapr
# Use Dapr's service invocation API with the correct app-id
```

## Monitoring and Debugging Commands

### Essential Commands for Debugging
```bash
# General cluster status
kubectl get nodes,pods,svc,ingress,configmaps,secrets

# Check all pods in all namespaces
kubectl get pods --all-namespaces

# Get detailed information about a resource
kubectl describe <resource-type> <resource-name>

# View logs from a pod
kubectl logs <pod-name> [-c <container-name>]

# Follow logs in real-time
kubectl logs -f <pod-name>

# Execute commands inside a running pod
kubectl exec -it <pod-name> -- /bin/sh

# Check cluster events
kubectl get events --sort-by='.lastTimestamp'
```

### Dapr-Specific Debugging
```bash
# Check Dapr runtime version
dapr --version

# Check Dapr status for a specific pod
kubectl exec -it <pod-with-dapr-sidecar> -c daprd -- dapr status

# View Dapr logs for a specific pod
kubectl logs <pod-with-dapr-sidecar> -c daprd
```

### Networking Issues
```bash
# Test connectivity between services
kubectl run test --image=nicolaka/netshoot --rm -it --restart=Never -- \
  netstat -rn

# Check network policies
kubectl get networkpolicy

# Test DNS resolution
kubectl run test --image=busybox --rm -it --restart=Never -- nslookup <service-name>
```

## Performance Issues

### High Memory/CPU Usage
```bash
# Monitor resource usage
kubectl top pods
kubectl top nodes

# Check resource limits and requests
kubectl describe pod <pod-name>

# Review application logs for memory leaks
kubectl logs <pod-name>
```

## Recovery Procedures

### Rolling Back a Deployment
```bash
# Check deployment revision history
kubectl rollout history deployment/<deployment-name>

# Undo the last deployment
kubectl rollout undo deployment/<deployment-name>

# Rollback to a specific revision
kubectl rollout undo deployment/<deployment-name> --to-revision=<revision-number>
```

### Resetting a Pod
```bash
# Delete a problematic pod to trigger recreation
kubectl delete pod <pod-name>

# Force delete a pod that's stuck terminating
kubectl delete pod <pod-name> --grace-period=0 --force
```