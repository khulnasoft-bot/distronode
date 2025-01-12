# -*- coding: utf-8 -*-
# Copyright: (c) 2020-2021, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Requirement resolver implementations."""

from __future__ import annotations

try:
    from resolvelib import Resolver
except ImportError:
    class Resolver:  # type: ignore[no-redef]
        pass


class CollectionDependencyResolver(Resolver):
    """A dependency resolver for Distronode Collections.

    This is a proxy class allowing us to abstract away importing resolvelib
    outside of the `distronode.galaxy.dependency_resolution` Python package.
    """
