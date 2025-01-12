# This file overrides the builtin distronode.module_utils.distronode_release file
# to test that it can be overridden. Previously this was facts.py but caused issues
# with dependencies that may need to execute a module that makes use of facts
data = 'overridden distronode_release.py'
