from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import ipaddress
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import ansible.errors as errors

class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        return [ipaddress.ip_network(terms[0].split("/")[0] + "/" + terms[0].split("/")[1], strict=False).netmask]


#if __name__ == "__main__":
#     print(LookupModule.run("asd", "192.168.0.1", "0.0.0.15"))