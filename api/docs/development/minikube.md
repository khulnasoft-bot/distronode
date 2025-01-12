# Running Development Environment in Kubernetes

## Start Minikube

If you do not already have Minikube, install it from:
https://minikube.sigs.k8s.io/docs/start/

Note: This environment has only been tested on Linux.

```
$ minikube start \
    --mount \
    --mount-string="/path/to/api:/api_devel" \
    --cpus=4 \
    --memory=8g \
    --addons=ingress
```

### Verify

Ensure that your API source code is properly mounted inside of the minikube node:

```
$ minikube ssh
$ ls -la /api_devel
```

## Deploy the API Operator

Clone the [api-operator](https://github.com/distronode/distronode/tree/devel/api-operator).

For the following playbooks to work, you will need to:

```
$ pip install openshift
```

If you are not changing any code in the operator itself, git checkout the latest version from https://github.com/distronode/distronode/tree/devel/api-operator/releases, and then follow the instructions in the api-operator [README](https://github.com/distronode/distronode/tree/devel/api-operator#basic-install).

If making changes to the operator itself, run the following command in the root
of the api-operator repo. If not, continue to the next section.

### Building and Deploying a Custom API Operator Image

```
# in api-operator repo on the branch you want to use
$ export IMAGE_TAG_BASE=quay.io/<username>/api-operator
$ export VERSION=<custom-tag>
$ make docker-build
$ docker push ${IMAGE_TAG_BASE}:${VERSION}
```

## Deploy API into Minikube using the API Operator

If have have not made any changes to the API Dockerfile, run the following
command. If you need to test out changes to the Dockerfile, see the
"Custom API Development Image for Kubernetes" section below.

In the root of api-operator:

```
$ distronode-playbook distronode/instantiate-api-deployment.yml \
    -e development_mode=yes \
    -e image=ghcr.io/distronode/distronode/tree/devel/api_kube_devel \
    -e image_version=devel \
    -e image_pull_policy=Always \
    -e service_type=nodeport \
    -e namespace=$NAMESPACE
```
Check the operator with the following commands:

```
# Check the operator deployment
$ kubectl get deployments
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
api                               1/1     1            1           16h
api-operator-controller-manager   1/1     1            1           16h

$ kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
api-operator-controller-manager-b775bfc7c-fn995   2/2     Running   0          16h
```

If there are errors in the image pull, check that it is using the right tag. You can update the tag that it will pull by editing the deployment.

### Custom API Development Image for Kubernetes

I have found `minikube cache add` to be unacceptably slow for larger images such
as this. A faster workflow involves building the image and pushing it to a
registry:

In the root of the API repo:

```
$ make api-kube-dev-build
$ docker push ghcr.io/distronode/distronode/tree/devel/api_kube_devel:${COMPOSE_TAG}
```

In the root of api-operator:

```
$ distronode-playbook distronode/instantiate-api-deployment.yml \
    -e development_mode=yes \
    -e image=ghcr.io/distronode/distronode/tree/devel/api_kube_devel \
    -e image_version=${COMPOSE_TAG} \
    -e image_pull_policy=Always \
    -e service_type=nodeport \
    -e namespace=$NAMESPACE
```

To iterate on changes to the Dockerfile, rebuild and push the image, then delete
the API Pod. A new Pod will respawn with the latest revision.

## Accessing API

To access via the web browser, run the following command:
```
$ minikube service api-service --url
```

To retrieve your admin password
```
$ kubectl get secrets api-admin-password -o json | jq '.data.password' | xargs | base64 -d
```

To tail logs from the containers
```
# Find the api pod name
kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
api-56fbfbb6c8-jkhzl                              4/4     Running   0          13h
api-operator-controller-manager-b775bfc7c-fn995   2/2     Running   0          16h
api-postgres-0                                    1/1     Running   0          16h

# now you know the pod name, tail logs from task container in pod
kubectl logs -f api-56fbfbb6c8-jkhzl -n api  -c api-task

# alternatively, or in a different window tail logs from the web container in pod
kubectl logs -f api-56fbfbb6c8-jkhzl -n api  -c api-web
```

To exec in to the container:
```
# Using same pod name we found above from "kubectl get pods"
$ kubectl exec -it api-56fbfbb6c8-k6p82 -c api-task bash
```

The application will live reload when files are edited just like in the development environment. Just like in the development environment, if the application totally crashes because files are invalid syntax or other fatal problem, you will get an error like "no python application" in the web container. Delete the whole control plane pod and wait until a new one spins up automatically.
```
$ kubectl delete pod api-56fbfbb6c8-k6p82
```
