import sys
import re
sys.path.insert(0, "/home/kz/projects/idioms")
from ...idioms.utils.matlab import gen_header, gen_signature, extract_atomic_variables, boilerplate_end, \
    boilerplate_start
from ...idioms.utils.pathutils import realpath
from ...idioms.utils.stringutils import tabs_to_spaces
import os


class MatlabSimulation:
    def __init__(self, filepath, boilerplate_start, boilerplate_end):
        self.filepath = realpath(filepath)
        self.name, ext = os.path.splitext(os.path.basename(self.filepath))
        with open(self.filepath, 'r') as f:
            self.input = tabs_to_spaces(f.read())
            extracted = extract_atomic_variables(self.input)
            self.body = extracted.body
            self.vars = extracted.vars
        self.formatted = self._adjust_indentation()
        self.preamble = gen_header(self.vars)
        self.signature = gen_signature(self.filepath)
        self.boilerplate = (boilerplate_start, boilerplate_end)
        self.output = f"""{self.preamble}\n{self.signature}{self.boilerplate[0]}{self.formatted}{self.boilerplate[1]}"""

    def _adjust_indentation(self):
        last_line = self.boilerplate[0][-1]
        leftpad = re.findall(r"^(\s*)", last_line)[0]
        indented = []
        for line in self.body.split("\n"):
            line = f"{leftpad}{line.strip()}"
            indented.append(line)
        return '\n'.join(indented)

