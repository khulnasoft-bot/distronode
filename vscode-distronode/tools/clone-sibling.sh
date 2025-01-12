#!/bin/bash
set -euo pipefail

if [[ -d ../distronode-language-server ]]; then
    echo "Distronode Language Server already cloned"
else
    echo "Cloning Distronode Language Server"
    git clone https://github.com/distronode/distronode-language-server ../distronode-language-server
fi

# install dependencies of distronode-language-server before linking it to vscode-distronode
echo "Installing deps and compiling Distronode Language Server"
cd ../distronode-language-server
npm ci
cd ../vscode-distronode
