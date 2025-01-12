"""Build version text."""

from __future__ import annotations

import importlib.metadata


PKGS = [
    "distronode-builder",
    "distronode-core",
    "distronode-creator",
    "distronode-dev-environment",
    "distronode-devtools",
    "distronode-lint",
    "distronode-navigator",
    "distronode-sign",
    "molecule",
    "pytest-distronode",
    "tox-distronode",
]


def version_builder() -> str:
    """Build a string of formatted versions.

    Returns:
        The versions string
    """
    lines = []
    for pkg in sorted(PKGS):
        try:
            version = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            version = "not installed"
        lines.append(f"{pkg: <40} {version}")

    return "\n".join(lines)
