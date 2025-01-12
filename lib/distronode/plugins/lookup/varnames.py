# (c) 2017 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

DOCUMENTATION = """
    name: varnames
    author: Distronode Core Team
    version_added: "2.8"
    short_description: Lookup matching variable names
    description:
      - Retrieves a list of matching Distronode variable names.
    options:
      _terms:
        description: List of Python regex patterns to search for in variable names.
        required: True
    seealso:
        - plugin_type: lookup
          plugin: distronode.builtin.vars
"""

EXAMPLES = """
- name: List variables that start with qz_
  distronode.builtin.debug: msg="{{ lookup('distronode.builtin.varnames', '^qz_.+') }}"
  vars:
    qz_1: hello
    qz_2: world
    qa_1: "I won't show"
    qz_: "I won't show either"

- name: Show all variables
  distronode.builtin.debug: msg="{{ lookup('distronode.builtin.varnames', '.+') }}"

- name: Show variables with 'hosts' in their names
  distronode.builtin.debug: msg="{{ q('varnames', 'hosts') }}"

- name: Find several related variables that end specific way
  distronode.builtin.debug: msg="{{ query('distronode.builtin.varnames', '.+_zone$', '.+_location$') }}"

- name: display values from variables found via varnames (note "*" is used to dereference the list to a 'list of arguments')
  debug: msg="{{ lookup('vars', *lookup('varnames', 'distronode_play_.+')) }}"

"""

RETURN = """
_value:
  description:
    - List of the variable names requested.
  type: list
"""

import re

from distronode.errors import DistronodeError
from distronode.module_utils.common.text.converters import to_native
from distronode.module_utils.six import string_types
from distronode.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        if variables is None:
            raise DistronodeError('No variables available to search')

        self.set_options(var_options=variables, direct=kwargs)

        ret = []
        variable_names = list(variables.keys())
        for term in terms:

            if not isinstance(term, string_types):
                raise DistronodeError('Invalid setting identifier, "%s" is not a string, it is a %s' % (term, type(term)))

            try:
                name = re.compile(term)
            except Exception as e:
                raise DistronodeError('Unable to use "%s" as a search parameter: %s' % (term, to_native(e)))

            for varname in variable_names:
                if name.search(varname):
                    ret.append(varname)

        return ret
