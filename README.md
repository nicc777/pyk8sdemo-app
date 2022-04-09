
- [Flask Demo App](#flask-demo-app)
  - [Building](#building)
  - [Pushing the build to a registry](#pushing-the-build-to-a-registry)
  - [Manual Deployment in Kubernetes](#manual-deployment-in-kubernetes)
    - [Preparing a dedicated test namespace (optional)](#preparing-a-dedicated-test-namespace-optional)
    - [Pod Only Deployment](#pod-only-deployment)
    - [Service With Ingress Deployment](#service-with-ingress-deployment)
    - [Obtaining a Shell from one of the Pods](#obtaining-a-shell-from-one-of-the-pods)
    - [Cleanup](#cleanup)
  - [Deployment with ArgoCD](#deployment-with-argocd)

# Flask Demo App

This is a simple Flask demo app intended to be deployed in Kubernetes

I used this demo app in the following blog articles:

* [2022-04-03](https://www.nicc777.com/blog/2022/2022-04-03.html)
* [2022-04-10](https://www.nicc777.com/blog/2022/2022-04-10.html)

_**Note**_: If any of the links above does not work, it may because thearticle is not yet published. You can also visit the [blog repository](https://github.com/nicc777/nicc777-com-site) to see work in progress.

## Building

Run:

```shell
python3 -m build
```

This will create the Python package.

Next, build the docker image:

```shell
docker build --no-cache -t demo-flask-app .
```

## Pushing the build to a registry

Create the following environment variables:

* `REGISTRY_URL` - contains the ECR or similar Docker container registry URL
* `VERSION_TAG` - The version number, for example `4.0`
* `APP_TAG` - The application tag, for example `demo-flask-app`
* `LOCAL_IMAGE_ID` - The ID of the local container image to use as reference

For a Docker registry running locally on IP address `192.168.2.6` you could do the following:

```shell
export REGISTRY_URL=192.168.2.6:5000
export APP_TAG="demo-flask-app"
export LOCAL_IMAGE_ID=`docker image ls | grep demo-flask-app | awk '{print $3}'`
export VERSION_TAG="0.0.1"
```

To use docker hub, for example, change the `REGISTRY_URL` and `APP_TAG` accordingly.

To get the latest image tag info:

```shell
docker image list | grep demo-flask-app
```

Update the environment variable `LOCAL_IMAGE_ID`

If not using a local image repository, ensure you are logged in. For ECR, for example, run the following:

```shell
aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY_URL
```

Then tag and push:

```shell
docker tag $LOCAL_IMAGE_ID $REGISTRY_URL/$APP_TAG\:$VERSION_TAG
docker push $REGISTRY_URL/$APP_TAG\:$VERSION_TAG
```

## Manual Deployment in Kubernetes

The manifests are all located in the `kubernetes_manifests/` directory of this project and commands will be run from within this directory.

### Preparing a dedicated test namespace (optional)

It is not required, but in some cases it may be useful to conduct tests in a temporary namespace. 

Follow these steps to create a new namespace and setting it as your default for the `kubectl` command:

To list the current namespaces, run `kubectl get namespaces`. Ensure the namespace you intend to use is not already listed.

Now create a namespace with the command `kubectl create namespace test`

And set it as your default namespace with the command:

```shell
kubectl config set-context --current --namespace=test
```

To verify the current namespace, run the command:

```shell
kubectl config view -o jsonpath='{.contexts[].context.namespace}'
```

The output should be the same namespace name. Any further kubectl commands will be issued against this namespace, unless it is overridden.

The command `kubectl get all` should also return the following output:

```text
No resources found in test namespace.
```

### Pod Only Deployment

This deployment is useful for scenarios where an ingress is not required. Typical use cases include:

* Troubleshooting or experimenting with `ConfigMaps`, `Secrets`, `Environment Variables` and other internal configurations in the context of a namespace
* Outbound networking tests and troubleshooting (basic tools for these have been included in the image)

To deploy the `pod` only manifest, run the following command:

```shell
kubectl apply -f troubleshooting-app-pod-only.yaml
```

For more info, try running `kubectl get all -o wide` or for maximum information, try running `kubectl get all -o yaml`

### Service With Ingress Deployment

The steps are the same as for the `Pod Only Deployment` with the only difference being to use the `troubleshooting-app.yaml` manifest file.

_**Note**_: It may take 15 to 20 minutes for the Load Balancer to be fully available and the DNS name set. Once this is done, the simple web app can also be opened by a Web Browser, using the DNS name specified in the manifest.

### Obtaining a Shell from one of the Pods

To verify the `pod` name, run the following command: `kubectl get pods`

Copy the `NAME` and run the following command (replacing the `pod-name` with the one copied):

```shell
kubectl exec --stdin --tty pod-name -- /bin/bash
```

Once in a shell within the pod, troubleshooting activities can be executed.

### Cleanup

To delete the deployment, simply run `kubectl delete -f troubleshooting-app-pod-only.yaml` (or whatever manifest file was used to create the deployment)

To verify, wait a minute or so and run `kubectl get all`. The output should be something similar to `No resources found in test namespace.`

## Deployment with ArgoCD

The ArgoCD Application Manifest is in `argocd/application-manifests/demo1_application.yaml`
