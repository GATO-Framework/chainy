import pathlib
import pprint

import yaml


class Chain:
    def __init__(self, name, inputs, prompts):
        self._name = name
        self._inputs = inputs
        self._prompts = prompts


def parse_config(path: pathlib.Path):
    with open(path, "r") as file:
        chain: dict = yaml.safe_load(file)
    name = path.name.removesuffix(".yml").removesuffix(".yaml")
    inputs = chain.pop("inputs")
    prompts = chain.pop("prompts")
    return Chain(name, inputs, prompts)


if __name__ == '__main__':
    chain_path = pathlib.Path("chains/example-1.yml")
    chain_config = parse_config(chain_path)
    pprint.pprint(chain_config)
