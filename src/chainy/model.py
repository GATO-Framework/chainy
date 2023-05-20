import asyncio
import pathlib
import string
from typing import TypeAlias, Generator

from . import llm, config


class Prompt:
    _default_path = pathlib.Path("prompts")

    def __init__(self, model: str, template_path: str, variables: dict[str, str]):
        self._model = model
        self._template_path = template_path
        self._variables = variables

    def _load(self, filename):
        path = self._default_path / filename
        if not path.exists():
            return ""
        with open(path) as file:
            return file.read()

    def model(self) -> str:
        return self._model

    def template(self):
        return string.Template(self._load(self._template_path))

    def dependencies(self):
        return set(self._variables.values())

    def substitute(self, inputs, outputs):
        return self.template().substitute({
            name: inputs.get(key) or outputs.get(key)
            for name, key in self._variables.items()
        })


DependencyGraph: TypeAlias = dict[str, set[str]]


class Chain:
    def __init__(self, name: str, inputs: list[str], prompts: dict[str, Prompt]):
        self._name = name
        self._inputs = inputs
        self._prompts = prompts
        self._outputs = {}
        self._graph: DependencyGraph = {}
        self._models: dict[str, llm.LargeLanguageModel] = {}

    @classmethod
    def from_config(cls, path: pathlib.Path | str) -> "Chain":
        return config.parse_chain_config(pathlib.Path(path))

    def _build_dependency_graph(self):
        self._graph = {prompt: set() for prompt in self._prompts}
        for name, prompt in self._prompts.items():
            for var in prompt.dependencies():
                is_prompt = var in self._prompts
                is_self = var == name
                if is_self or not is_prompt:
                    continue
                self._graph[name].add(var)

    def _batch_tasks(self) -> Generator[set[str], None, None]:
        self._build_dependency_graph()

        # Perform a topological sort
        while self._graph:
            # Find all nodes with no incoming edges
            batch = {node for node, edges in self._graph.items() if not edges}
            if not batch:
                raise ValueError("Cycle detected in graph")

            # Remove these nodes from the graph
            for node in batch:
                self._graph.pop(node)
            for edges in self._graph.values():
                edges.difference_update(batch)

            yield batch

    async def _execute_prompt(self, name, inputs):
        prompt = self._prompts[name]
        prompt_str = prompt.substitute(inputs, self._outputs)
        model = self._models[prompt.model()]
        return await model.generate(prompt_str)

    def add_model(self, name: str, model: llm.LargeLanguageModel):
        self._models[name] = model

    async def start(self, *input_values: str):
        inputs = dict(zip(self._inputs, input_values))
        for batch in self._batch_tasks():
            tasks = [self._execute_prompt(name, inputs) for name in batch]
            results = await asyncio.gather(*tasks)
            for name, output in zip(batch, results):
                print(name, output)
                self._outputs[name] = output
