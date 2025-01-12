#!/usr/bin/env fish
# Script: env-setup.fish
# Description: Modifies the environment for running Distronode from a checkout
# Usage: . ./hacking/env-setup [-q]

# Set PYTHON_BIN
if not set -q PYTHON_BIN
    for exe in python3 python
        if command -v $exe > /dev/null
            set -gx PYTHON_BIN (command -v $exe)
            break
        end
    end
    if not set -q PYTHON_BIN
        echo "No valid Python found"
        exit 1
    end
end

# Retrieve the path of the current directory where the script resides
set HACKING_DIR (dirname (status -f))
set FULL_PATH ($PYTHON_BIN -c "import os; print(os.path.realpath('$HACKING_DIR'))")
set DISTRONODE_HOME (dirname $FULL_PATH)

# Set quiet flag
set QUIET ""
if contains -- (string split -m 1 " " $argv) -q --quiet
    set QUIET "true"
end

# Set environment variables
set -gx PREFIX_PYTHONPATH $DISTRONODE_HOME/lib
set -gx DISTRONODE_TEST_PREFIX_PYTHONPATH $DISTRONODE_HOME/test/lib
set -gx PREFIX_PATH $DISTRONODE_HOME/bin
set -gx PREFIX_MANPATH $DISTRONODE_HOME/docs/man

# Set PYTHONPATH
if not set -q PYTHONPATH
    set -gx PYTHONPATH $PREFIX_PYTHONPATH
else if not string match -qr $PREFIX_PYTHONPATH'($|:)' $PYTHONPATH
    if not test -n "$QUIET"
        echo "Appending PYTHONPATH"
    end
    set -gx PYTHONPATH "$PREFIX_PYTHONPATH:$PYTHONPATH"
end

# Set distronode_test PYTHONPATH
if not string match -qr $DISTRONODE_TEST_PREFIX_PYTHONPATH'($|:)' $PYTHONPATH
    if not test -n "$QUIET"
        echo "Appending PYTHONPATH"
    end
    set -gx PYTHONPATH "$DISTRONODE_TEST_PREFIX_PYTHONPATH:$PYTHONPATH"
end

# Set PATH
if not contains -- $PREFIX_PATH $PATH
    set -gx PATH $PREFIX_PATH $PATH
end

# Set MANPATH
if not set -q MANPATH
    set -gx MANPATH $PREFIX_MANPATH
else if not string match -qr $PREFIX_MANPATH'($|:)' $MANPATH
    set -gx MANPATH "$PREFIX_MANPATH:$MANPATH"
end

pushd $DISTRONODE_HOME
if test -n "$QUIET"
    # Remove any .pyc files found
    find . -type f -name "*.pyc" -exec rm -f '{}' ';' &> /dev/null
else
    # Remove any .pyc files found
    find . -type f -name "*.pyc" -exec rm -f '{}' ';'
    # Display setup details
    echo ""
    echo "Setting up Distronode to run out of checkout..."
    echo ""
    echo "PATH=$PATH"
    echo "PYTHONPATH=$PYTHONPATH"
    echo "PYTHON_BIN=$PYTHON_BIN"
    echo "DISTRONODE_LIBRARY=$DISTRONODE_LIBRARY"
    echo "MANPATH=$MANPATH"
    echo ""
    echo "Remember, you may wish to specify your host file with -i"
    echo ""
    echo "Done!"
    echo ""
end
popd

# Unset QUIET variable
set -e QUIET
