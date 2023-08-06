import json
import os
import platform
import sys

from ctypes import cdll, c_char_p
from typing import List, Dict

try:
    system_platform = {
        'linux': 'linux',
        'linux2': 'linux',
        # 'darwin': 'darwin',
        # 'win32': 'windows',
        # 'cygwin': 'windows',
    }[sys.platform]

    system_architecture = {
        ('64bit', 'ELF'): 'amd64',
        ('32bit', 'ELF'): '386',
    }[platform.architecture()]

except KeyError:
    raise OSError("Unknown platform or architecture: {} {}".format(
        sys.platform, platform.architecture()[0]))

lib = cdll.LoadLibrary(os.path.join(
    os.path.dirname(__file__),
    "bridge-{}-{}.so".format(system_platform, system_architecture)
))
lib.Dump.argtypes = [c_char_p]
lib.Dump.restype = c_char_p


class Node:
    def __init__(
            self: "Node",
            value: str,  # actual content
            next: "Node",  # the next item in the current sexp
            children: List["Node"],  # the children of this sexp
            attributes: Dict[str, bool],  # special attributes for this node
            original: str,  # original line used before parsing
            flags: List[str],  # only top Node should have this set
            start_line: int,
            # the line in the original dockerfile where the node begins
            end_line: int  # the line in the original dockerfile where the node ends
    ):
        self.value = value
        self.next = next
        self.children = children
        self.attributes = attributes
        self.original = original
        self.flags = flags
        self.start_line = start_line
        self.end_line = end_line

    @staticmethod
    def from_json(blob):
        if blob is None:
            return None
        return Node(
            value=blob.get("Value"),
            next=Node.from_json(blob.get("Next")),
            children=list(Node.from_json(b) for b in blob.get("Children") or []),
            attributes=blob.get("Attributes"),
            original=blob.get("Original"),
            flags=blob.get("Flags"),
            start_line=blob.get("StartLine"),
            end_line=blob.get("EndLine")
        )


def parse(s):
    if type(s) != bytes:
        s = s.encode('utf-8')
    return Node.from_json(json.loads(lib.Dump(s)))
