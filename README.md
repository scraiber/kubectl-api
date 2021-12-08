# kubectl-api

Kubectl-api is an API based on kubectl and FastAPI. It is supposed to be deployed in a Kubernetes cluster, such that different services and perhaps users can make use of it for creating/configuring/deleting resources from **within** the cluster by accessing this API, where we can execute any kubectl command. Please find the registry [here](https://hub.docker.com/r/scraiber/kubectl-api).


## Installing kubectl-api in a cluster

In order to install kubectl-api we can use the Helm chart in this repo, so, provided Helm 3 and kubectl is installed and properly configured on your local machine, you can run it as follows:

```
kubectl create ns kubectl-api
helm install my-release ./chart/kubectl-api --namespace kubectl-api 
```



## Accessing the API

In the following, we assume that a port-forward of the service has been made and that the service can be accessed at `localhost:8000`. **Important:** You should never expose this service to the public as it would mean a huge security risk - it is solely meant to be used by other services and perhaps by authorized users.

Currently, there are two possibilities for accessing the API. In the first one, you access the `general` API, where you just enter a string like `http://localhost:8000/general/get ns` resp. `http://localhost:8000/general/get%20ns` to get the namespaces running and you will get a response like

```
{
    "Output":"NAME              STATUS   AGE\ncert-manager      Active   7d9h\ndefault           Active   96d\nkube-node-lease   Active   96d\nkube-public       Active   96d\nkube-system       Active   96d\nkubectl-api       Active   24h\nmonitoring        Active   7d15h\n", 
    "Error":""
}
```


Of, course, you can enter any kubectl request you like.

However, if you want to create/configure/delete a resource by utilizing a YAML file, then you can make use of the `general_json` API. Here you enter a `kube_str`, which is essentially the command you want to run, and a list of strings called `yaml_file`, which is essentially the lines of the YAML file you want to use - alternatively you can just enter a list of length one, where the YAML file resides in it with `\n` seperating the lnie. So, for instance, if you want to create a `ServiceAccount` named `test-sa` n the namespace `monitoring`you could run the following curl request

```
curl -X GET \
    -H "Content-type: application/json" \
    -H "Accept: application/json" -d '{"kube_str":"apply -f sa.yaml", "yaml_file": ["apiVersion: v1","kind: ServiceAccount","metadata:","  name: test-sa","  namespace: monitoring"]}' \ 
    "http://localhost:8000/general_json"
```

and you get

```
{
    "Output":"serviceaccount/test-sa created\n",
    "Error":""
}
```
