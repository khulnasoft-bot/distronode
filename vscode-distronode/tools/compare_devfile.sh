#!/bin/bash

# Pull devfile template from distronode-creator
CREATOR_REPO="https://github.com/distronode/distronode-creator.git"
CREATOR_DEVFILE_TEMPLATE="src/distronode_creator/resources/common/devfile/devfile.yaml.j2"
EXTENSION_DEVFILE_TEMPLATE="resources/contentCreator/createDevfile/devfile-template.txt"

# Clone distronode-creator repo

TEMP_DIR=$(mktemp -d)
git clone --depth 1 --branch main "$CREATOR_REPO" "$TEMP_DIR"

# Compare the files
if diff "$TEMP_DIR/$CREATOR_DEVFILE_TEMPLATE" "$EXTENSION_DEVFILE_TEMPLATE" > /dev/null; then
    echo "Devfile template matches distronode-creator devfile template."
    rm -rf "$TEMP_DIR"
    exit 0
else
    echo "Devfile template under resources/ does not match the template distronode-creator is using."
    rm -rf "$TEMP_DIR"
    exit 1
fi
