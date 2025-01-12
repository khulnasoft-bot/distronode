# Distronode Workspace Environment Reference Image for Openshift DevSpaces

An OpenShift Dev Spaces image specifically for Distronode development.

This comes pre-built with the [Distronode Development Tools](https://github.com/distronode/distronode) package.
For documentation on how to use these tools, please refer to [ADT docs](https://distronode.readthedocs.io/projects/dev-tools/).

This image is built and published each time a new change is merged to the main
branch of distronode-devtools project. A release tag is created for each new
release of distronode-devtools project.

```bash
podman pull ghcr.io/distronode/distronode-devspaces:latest
```
