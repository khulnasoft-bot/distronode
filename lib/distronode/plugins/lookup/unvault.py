# (c) 2020 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

DOCUMENTATION = """
    name: unvault
    author: Distronode Core Team
    version_added: "2.10"
    short_description: read vaulted file(s) contents
    description:
        - This lookup returns the contents from vaulted (or not) file(s) on the Distronode controller's file system.
    options:
      _terms:
        description: path(s) of files to read
        required: True
    notes:
      - This lookup does not understand 'globbing' nor shell environment variables.
    seealso:
      - ref: playbook_task_paths
        description: Search paths used for relative files.
"""

EXAMPLES = """
- distronode.builtin.debug: msg="the value of foo.txt is {{ lookup('distronode.builtin.unvault', '/etc/foo.txt') | string | trim }}"
"""

RETURN = """
  _raw:
    description:
      - content of file(s) as bytes
    type: list
    elements: raw
"""

from distronode.errors import DistronodeParserError
from distronode.plugins.lookup import LookupBase
from distronode.module_utils.common.text.converters import to_text
from distronode.utils.display import Display

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []

        self.set_options(var_options=variables, direct=kwargs)

        for term in terms:
            display.debug("Unvault lookup term: %s" % term)

            # Find the file in the expected search path
            lookupfile = self.find_file_in_search_path(variables, 'files', term)
            display.vvvv(u"Unvault lookup found %s" % lookupfile)
            if lookupfile:
                actual_file = self._loader.get_real_file(lookupfile, decrypt=True)
                with open(actual_file, 'rb') as f:
                    b_contents = f.read()
                ret.append(to_text(b_contents))
            else:
                raise DistronodeParserError('Unable to find file matching "%s" ' % term)

        return ret
