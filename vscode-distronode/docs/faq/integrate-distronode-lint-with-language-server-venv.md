# How to integrate `distronode-lint` in venv with Distronode Language Extension

## Background: No need to install distronode-lint system-wide

To make Distronode Language Extension fully function, users need to install
`distronode-lint`. The easiest way to install `distronode-lint` is to install it
system-wide as below:

```sh
# Fedora
## sudo dnf install python3-distronode-lint

# Ubuntu
## sudo apt install distronode-lint
```

However, installing Python packages system-wide is not always preferable because
the it affects the whole system behavior. You can install `distronode-lint` in venv
with normal permission, and integrate it with Distronode Language Extension
instead.

## How to use `distronode-lint` in venv

The outline is fairly simple.

1. Create a venv.
2. Install `distronode-lint` in the venv.
3. Configure path to `distronode-lint` and `distronode` executables in the extension
   settings.
