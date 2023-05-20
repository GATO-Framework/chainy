import asyncio
import pathlib
import time
import unittest

from chainy import config, model
from tests import mock_llm


class TestPrompt(unittest.TestCase):

    def setUp(self) -> None:
        self._prompt = model.Prompt(
            model="mock",
            template_path="tmpl01.md",
            variables={"var_1": "input_1", "var_2": "input_2"}
        )

    def test_prompt_model(self):
        self.assertEqual(self._prompt.model(), "mock")

    def test_prompt_dependencies(self):
        self.assertSetEqual(self._prompt.dependencies(), {"input_1", "input_2"})

    def test_prompt_substitute(self):
        expected_content = "\n".join([
            "This is a test.", "",
            "Variable 1: hey",
            "Variable 2: bud",
        ])
        content = self._prompt.substitute({"input_1": "hey", "input_2": "bud"}, {})
        self.assertEqual(content, expected_content)


class TestChain(unittest.TestCase):
    def test_chain_start(self):
        chain_path = pathlib.Path("chains/example-2.yml")
        chain = config.parse_chain_config(chain_path)
        t = time.perf_counter()
        chain.add_model("mock", mock_llm.MockLanguageModel())
        asyncio.run(chain.start("hey", "bud"))
        total_time = time.perf_counter() - t
        self.assertLess(total_time, 4.1)


if __name__ == "__main__":
    unittest.main()
