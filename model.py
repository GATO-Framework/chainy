import pathlib
import string

import llm


class Prompt:
    _default_path = pathlib.Path("prompts")

    def __init__(self, template_path: str, variables: dict[str, str]):
        self._template = self._load(template_path)
        self._variables = variables

    def _load(self, filename):
        path = self._default_path / filename
        if not path.exists():
            return ""
        with open(path) as file:
            return file.read()

    def dependencies(self):
        return self._variables.values()

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

    def _build_dependency_graph(self) -> dict[str, set[str]]:
        graph = {prompt: set() for prompt in self._prompts}

        for name, prompt in self._prompts.items():
            for var in prompt.dependencies():
                is_prompt = var in self._prompts
                is_self = var == name
                if is_self or not is_prompt:
                    continue
                graph[name].add(var)

        return graph

    def _topological_sort(self, graph: dict[str, set[str]]) -> list[set[str]]:
        # Create a list that will hold the batches of nodes
        result = []

        # While there are nodes in the graph
        while graph:
            # Find all nodes with no incoming edges
            batch = {node for node, edges in graph.items() if not edges}
            if not batch:
                raise ValueError("Cycle detected in graph")

            # Remove these nodes from the graph
            for node in batch:
                graph.pop(node)
            for edges in graph.values():
                edges.difference_update(batch)

            # Add this batch to the result
            result.append(batch)

        return result

    def start(self, *input_values: str):
        graph = self._build_dependency_graph()
        print(graph)
        print(self._topological_sort(graph))
        inputs = dict(zip(self._inputs, input_values))
        for name, template in self._prompts.items():
            prompt = template.substitute(inputs, self._outputs)
            model = llm.MockLanguageModel()
            output = model.generate(prompt)
            self._outputs[name] = output
            print(name, prompt)
            print("----")
