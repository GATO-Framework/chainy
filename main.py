import asyncio
import pathlib

import yaml

from model import Chain, Prompt


def parse_config(path: pathlib.Path) -> Chain:
    with open(path, "r") as file:
        chain: dict = yaml.safe_load(file)
    name = path.name.removesuffix(".yml").removesuffix(".yaml")
    inputs = chain.pop("inputs")
    prompts = {name: Prompt(prompt["template"], prompt["substitute"])
               for name, prompt in chain.pop("prompts").items()}
    return Chain(name, inputs, prompts)


def main():
    chain_path = pathlib.Path("chains/example-2.yml")
    chain = parse_config(chain_path)
    asyncio.run(chain.start("hey", "bud"))


if __name__ == '__main__':
    main()
