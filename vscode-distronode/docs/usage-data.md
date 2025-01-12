# Data collection

`vscode-distronode` has opt-in telemetry collection, provided by
[vscode-redhat-telemetry](https://github.com/redhat-developer/vscode-redhat-telemetry).

## What's included in the vscode-distronode telemetry data

- distronode-language-server start
- errors during `distronode-language-server` start
- any errors from LSP requests
- Distronode core version
- distronode-lint version if installed and enabled
- `distronode-playbook` command runs successfully or fails.
- `distronode-navigator` run command runs successfully or fails.
- Distronode vault (distronode-vault) command run in case it fails.
- Resync Distronode inventory (distronode-inventory) command run in case it fails.
- Execution environment enabled or disabled
- Distronode Lightspeed enabled or disabled
- Distronode Lightspeed code assist enabled or disabled

## What's included in the general telemetry data

Please see the
[vscode-redhat-telemetry data collection information](https://github.com/redhat-developer/vscode-redhat-telemetry/blob/HEAD/USAGE_DATA.md)
for information on what data it collects.

## How to opt-in or out

Use the `redhat.telemetry.enabled` setting to enable or disable telemetry
collection.

Note that this extension abides by Visual Studio Code's telemetry level: if
`telemetry.telemetryLevel` is set to off, then no telemetry events will be sent
to Red Hat, even if `redhat.telemetry.enabled` is set to true. If
`telemetry.telemetryLevel` is set to `error` or `crash`, only events containing
an error or errors property will be sent to Red Hat.
