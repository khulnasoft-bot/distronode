# Editable dependencies in API Docker Compose Development Environment

This folder contains the symlink to editable dependencies for API

During the bootstrap of api development environment we will try to crawl through the symlinks and mount (the source of the symlink) to `tools_api_` containers and `init_api` containers then install all the dependencies in editable mode

## How to enable/disable editable dependnecies

### Enable

Set `EDITABLE_DEPENDENCIES=true` either as an Environment Variable before invoking `make docker-compose`

```bash
export EDITABLE_DEPENDENCIES=true
```

or during invocation of `make docker-compose`

```bash

EDITABLE_DEPENDENCIES=true make docker-compose
```

This will cause the `make docker-compose-source` to template out docker-compose file with editable dependencies.

### Disable

To disable editable dependency simply `unset EDITABLE_DEPENDENCIES`

## How to add editable dependencies

Adding symlink to the directory that contains the source of the editable dependencies will cause the dependency to be mounted and installed in the docker-compose development environment.

Both relative path or absolute path will work.

### Examples

I have `api` checked out at `~/projects/src/github.com/TheRealHaoLiu/api`
I have `django-distronode-base` checked out at `~/projects/src/github.com/TheRealHaoLiu/django-distronode-base`

From root of API project `~/projects/src/github.com/TheRealHaoLiu/api`

I can either do

```bash
ln -s ~/projects/src/github.com/TheRealHaoLiu/distronode-runner tools/docker-compose/editable_dependencies/
```

or

```bash
ln -s ../distronode-runner tools/docker-compose/editable_dependencies/
```

## How to remove indivisual editable dependencies

Simply removing the symlink from  `tools/docker-compose/editable_dependencies` **will cause problem**!

and the volume `tools_api_var_lib` needs to be deleted as well with

```bash
make docker-compose-down
docker volume rm tools_api_var_lib
```

