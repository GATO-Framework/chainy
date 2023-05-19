import pathlib
import pprint
import string

import yaml


class Prompt:
    _default_path = pathlib.Path("prompts")

    def __init__(self, template, variables):
        self._template = self._load(template)
        self._variables = variables

    def _load(self, filename):
        with open(self._default_path / filename) as file:
            return file.read()

    def substitute(self):
        print(self._template)
        template = string.Template(self._template)
        return template.substitute(self._variables)


class Chain:
    def __init__(self, name, inputs: list[str], prompts: dict[str, Prompt]):
        self._name = name
        self._inputs = inputs
        self._prompts = prompts

    def start(self):
        for name, prompt in self._prompts.items():
            print(name, prompt.substitute())


def parse_config(path: pathlib.Path) -> Chain:
    with open(path, "r") as file:
        chain: dict = yaml.safe_load(file)
    name = path.name.removesuffix(".yml").removesuffix(".yaml")
    inputs = chain.pop("inputs")
    prompts = {name: Prompt(prompt["template"], prompt["substitute"])
               for name, prompt in chain.pop("prompts").items()}
    return Chain(name, inputs, prompts)


def main():
    chain_path = pathlib.Path("chains/example-1.yml")
    chain = parse_config(chain_path)
    pprint.pprint(chain.start())


if __name__ == '__main__':
    main()
