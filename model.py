import pathlib
import string


class Prompt:
    _default_path = pathlib.Path("prompts")

    def __init__(self, template_path: str, variables: dict[str, str]):
        self._template = self._load(template_path)
        self._variables = variables

    def _load(self, filename):
        with open(self._default_path / filename) as file:
            return file.read()

    def substitute(self, inputs, outputs):
        template = string.Template(self._template)
        variables = {name: inputs.get(key) or outputs.get(key)
                     for name, key in self._variables.items()}
        return template.substitute(variables)


class Chain:
    def __init__(self, name, inputs: list[str], prompts: dict[str, Prompt]):
        self._name = name
        self._inputs = inputs
        self._prompts = prompts
        self._outputs = {}

    def start(self, *input_values: str):
        inputs = dict(zip(self._inputs, input_values))
        for name, prompt in self._prompts.items():
            print(name, prompt.substitute(inputs, self._outputs))
            print("----")
