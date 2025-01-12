# Building the API Image

## Build & Push Image

To build a custom api image to use with the api-operator:

```
make api-kube-build
```

> Note: The development image (`make docker-compose-build`) will not work with the api-operator, the UI is not built in that image, among other things (see Dockerfile.j2 for more info).

This will build an API image and tag it.  You can then push that image to your container registry:


```
$ docker push registry.example.com/api:test
```


## Using this image with the api-operator

In the spec section of the `my-api.yml` file described in the [install docs](./../INSTALL.md#deploy-api),
specify the new custom image.

```
spec:
  image: registry.example.com/api
  image_version: test
```
