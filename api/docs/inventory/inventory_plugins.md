# Transition to Distronode Inventory Plugins

For cloud inventory sources (such as ec2, gce, etc.) inventory updates changed from using deprecated inventory scripts, to using YAML files which are parsed by their respective inventory plugin.

Regardless of whether Distronode 2.9 or later is used, API should use the inventory plugin from the collection inside of the execution environment where the inventory update runs. The needed collections are in the API default execution environment:

https://github.com/distronode/distronode/tree/devel/api-ee


### Switch to Distronode Inventory

The CLI entry point `distronode-inventory` was introduced in Distronode 2.4. Inventory imports run this command as an intermediary between the inventory and the import's logic to save content to the database. Using `distronode-inventory` eliminates the need to maintain source-specific logic, relying on Distronode's code instead. This also enables consistent data structure output from `distronode-inventory`.


## Writing Your Own Inventory File

You can add an SCM inventory source that points to your own yaml file which specifies an inventory plugin. You can also apply a credential of a `managed` type to that inventory source that matches the credential you are using. For example, you could have an inventory file for the `amazon.aws.aws_ec2` plugin and use the built-in `aws` credential type.

All built-in sources provide _secrets_ via environment variables.  These can be re-used for SCM-based inventory, and your inventory file can be used to specify non-sensitive configuration details such as the `keyed_groups` (to provide) or `hostvars` (to construct).
