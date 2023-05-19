import pathlib

import yaml

from . import model


def parse_chain_config(path: pathlib.Path) -> model.Chain:
    with open(path, "r") as file:
        chain: dict = yaml.safe_load(file)
    name = path.name.removesuffix(".yml").removesuffix(".yaml")
    inputs = chain.pop("inputs")
    prompts = {
        name: model.Prompt(
            model=prompt["model"],
            template_path=prompt["template"],
            variables=prompt["substitute"],
        )
        for name, prompt in chain.pop("prompts").items()
    }
    return model.Chain(name, inputs, prompts)
