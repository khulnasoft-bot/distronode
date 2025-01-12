#!/usr/bin/python
from __future__ import annotations

import json


def main():
    print(json.dumps(dict(changed=False, source='overridden distronode.builtin (should not be possible)')))


if __name__ == '__main__':
    main()
