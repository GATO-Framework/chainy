import asyncio
import pathlib
import time
import unittest

from chainy import config, model
from tests import mock_llm


class TestPrompt(unittest.TestCase):

    def setUp(self) -> None:
        self._prompt_1 = model.Prompt(
            model="mock",
            template_path="tmpl01.md",
            variables={"var_1": "input_1", "var_2": "input_2"}
        )
        self._prompt_1_output = "\n".join([
            "This is a test.", "",
            "Variable 1: hey",
            "Variable 2: bud",
        ])
        self._prompt_2 = model.Prompt(
            model="mock",
            template_path="tmpl02.md",
            variables={"res_1": "prompt_1"}
        )

    def test_prompt_model(self):
        self.assertEqual(self._prompt_1.model(), "mock")
        self.assertEqual(self._prompt_2.model(), "mock")

    def test_prompt_dependencies(self):
        self.assertSetEqual(self._prompt_1.dependencies(), {"input_1", "input_2"})
        self.assertSetEqual(self._prompt_2.dependencies(), {"prompt_1"})

    def test_prompt_substitute(self):
        prompt_1_expected_output = "\n".join([
            "This is a test.", "",
            "Variable 1: hey",
            "Variable 2: bud",
        ])
        prompt_2_expected_output = "\n".join([
            "This is the second prompt.", "",
            f"Result of prompt 1: {prompt_1_expected_output}",
        ])

        inputs = {"input_1": "hey", "input_2": "bud"}
        outputs = {}
        content = self._prompt_1.substitute(inputs, outputs)
        self.assertEqual(content, prompt_1_expected_output)

        inputs = {}
        outputs = {"prompt_1": prompt_1_expected_output}
        content = self._prompt_2.substitute(inputs, outputs)
        self.assertEqual(content, prompt_2_expected_output)


class TestChain(unittest.TestCase):
    def setUp(self) -> None:
        chain_path = pathlib.Path("chains/example-2.yml")
        self._chain = config.parse_chain_config(chain_path)

    def test_chain_start(self):
        t = time.perf_counter()
        self._chain.add_model("mock", mock_llm.MockLanguageModel())
        asyncio.run(self._chain.start("hey", "bud"))
        total_time = time.perf_counter() - t
        self.assertLess(total_time, 4.1)


if __name__ == "__main__":
    unittest.main()
