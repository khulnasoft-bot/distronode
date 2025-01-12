"""A runpy entry point for distronode-devtools.

This makes it possible to invoke CLI
via :command:`python3 -m distronode_devtools`.
"""

from __future__ import annotations

from .cli import main


if __name__ == "__main__":
    main()
