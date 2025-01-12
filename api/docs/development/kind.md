# Running Development Environment in Kubernetes using Kind Cluster

## Start Kind Cluster
Note: This environment has been tested on MacOS and Fedora with Docker.

If you do not already have Kind, install it from:
https://kind.sigs.k8s.io/docs/user/quick-start/

Create Kind cluster config file
```yml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraMounts:
  - hostPath: /path/to/api
    containerPath: /api_devel
  extraPortMappings:
  - containerPort: 30080
    hostPort: 30080
```

Start Kind cluster
```bash
 kind create cluster --config kind-cluster.yaml
```

Verify API source tree is mounted in the kind-control-plane container
```bash
 docker exec -it kind-control-plane ls /api_devel
```

## Deploy the API Operator

Clone the [api-operator](https://github.com/distronode/distronode/tree/devel/api-operator).

For the following playbooks to work, you will need to:

```bash
 pip install openshift
```

If you are not changing any code in the operator itself, git checkout the latest version from https://github.com/distronode/distronode/tree/devel/api-operator/releases, and then follow the instructions in the api-operator [README](https://github.com/distronode/distronode/tree/devel/api-operator#basic-install).

If making changes to the operator itself, run the following command in the root
of the api-operator repo. If not, continue to the next section.

### Building and Deploying a Custom API Operator Image

```bash
# in api-operator repo on the branch you want to use
 export IMAGE_TAG_BASE=quay.io/<username>/api-operator
 make docker-build docker-push deploy
```

Check the operator deployment
```bash
 kubectl get deployments
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
api-operator-controller-manager   1/1     1            1           16h
```

## Deploy API into Kind Cluster using the API Operator

If you have not made any changes to the API Dockerfile, run the following
command. If you need to test out changes to the Dockerfile, see the
"Custom API Development Image for Kubernetes" section below.

In the root of api-operator:

```bash
 distronode-playbook distronode/instantiate-api-deployment.yml \
    -e development_mode=yes \
    -e image=ghcr.io/distronode/distronode/tree/devel/api_kube_devel \
    -e image_version=devel \
    -e image_pull_policy=Always \
    -e service_type=nodeport \
    -e namespace=api \
    -e nodeport_port=30080
```
Check the operator with the following commands:

```bash
# Check the operator deployment
 kubectl get deployments
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
api                               1/1     1            1           16h
api-operator-controller-manager   1/1     1            1           16h

 kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
api-operator-controller-manager-b775bfc7c-fn995   2/2     Running   0          16h
```

If there are errors in the image pull, check that it is using the right tag. You can update the tag that it will pull by editing the deployment.

### Custom API Development Image for Kubernetes

Set these environmental variables before starting:
```bash
export DEV_DOCKER_TAG_BASE=quay.io/<USERNAME>
export COMPOSE_TAG=<IMAGE_TAG>
```
In the root of the API repo:

```bash
make api-kube-dev-build
docker push $DEV_DOCKER_TAG_BASE/api_kube_devel:$COMPOSE_TAG
```

In the root of api-operator:

```bash
 distronode-playbook distronode/instantiate-api-deployment.yml \
    -e development_mode=yes \
    -e image=$DEV_DOCKER_TAG_BASE/api_kube_devel \
    -e image_version=$COMPOSE_TAG \
    -e image_pull_policy=Always \
    -e service_type=nodeport \
    -e namespace=$NAMESPACE
```

To iterate on changes to the Dockerfile, rebuild and push the image, then delete
the API Pod. A new Pod will respawn with the latest revision.

## Accessing API

To access via the web browser, use the following URL:
```
http://localhost:30080
```

To retrieve your admin password
```bash
 kubectl get secrets api-admin-password -o json | jq '.data.password' | xargs | base64 -d
```

To tail logs from the task containers
```bash
 kubectl logs -f deployment/api-task -n api -c api-task
```

To tail logs from the web containers
```bash
 kubectl logs -f deployment/api-web -n api -c api-web
```

NOTE: If there's multiple replica of the api deployment you can use `stern` to tail logs from all replicas. For more information about `stern` check out https://github.com/wercker/stern.

To exec in to the a instance of the api-task container:
```bash
 kubectl exec -it deployment/api -n api -c api-task bash
```

The application will live reload when files are edited just like in the development environment. Just like in the development environment, if the application totally crashes because files are invalid syntax or other fatal problem, you will get an error like "no python application" in the web container. Delete the whole control plane pod and wait until a new one spins up automatically.
```bash
oc delete pod -l app.kubernetes.io/component=api
```
