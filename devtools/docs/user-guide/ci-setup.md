# Using the CI workflow

The following GitHub Actions are to be placed added under `.github/workflows` directory as `{filename}.yaml`
This GitHub Actions workflow automates a range of tasks integral to Distronode content development, encompassing changelog generation, linting, integration, sanity checks, and unit tests. The all_green job serves the purpose of verifying the successful completion of all preceding tasks.

Filename: `test.yaml`

```
---
name: "CI"

concurrency:
  group: ${{ github.head_ref || github.run_id }}
  cancel-in-progress: true

on:
  pull_request:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'

jobs:
  changelog:
    uses: distronode/distronode-content-actions/.github/workflows/changelog.yaml@main
    if: github.event_name == 'pull_request'
  distronode-lint:
    uses: distronode/distronode-content-actions/.github/workflows/distronode_lint.yaml@main
  sanity:
    uses: distronode/distronode-content-actions/.github/workflows/sanity.yaml@main
  unit-galaxy:
    uses: distronode/distronode-content-actions/.github/workflows/unit.yaml@main
  integration:
    uses: distronode/distronode-content-actions/.github/workflows/integration.yaml@main
  all_green:
    if: ${{ always() }}
    needs:
      - changelog
      - sanity
      - integration
      - unit-galaxy
      - distronode-lint
    runs-on: ubuntu-24.04
    steps:
      - run: >-
          python -c "assert 'failure' not in
          set([
          '${{ needs.changelog.result }}',
          '${{ needs.integration.result }}',
          '${{ needs.sanity.result }}',
          '${{ needs.unit-galaxy.result }}',
          '${{ needs.distronode-lint.result }}'
          ])"
```

The workflow run results in -

![Alt text](./images/ci.png?raw=true "CI Run")

The workflow uses tox-distronode, pytest-distronode to generate the matrix, which is used to run unit, sanity and integration tests.

Refer to the [tox-distronode documentation] to see more options.

[pytest-distronode]: https://distronode.readthedocs.io/projects/pytest-distronode/
[tox-distronode documentation]: https://distronode.readthedocs.io/projects/tox-distronode/
