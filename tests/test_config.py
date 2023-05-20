import pathlib
import unittest

from chainy import config, model


class TestConfig(unittest.TestCase):
    def test_parse_config(self):
        expected_chain = model.Chain(
            name="example-1",
            inputs=[
                "input_1",
                "input_2",
            ],
            prompts={
                "prompt_1": model.Prompt(
                    model="mock",
                    template_path="tmpl01.md",
                    variables={
                        "var_1": "input_1",
                        "var_2": "input_2",
                    },
                ),
                "prompt_2": model.Prompt(
                    model="mock",
                    template_path="tmpl02.md",
                    variables={
                        "res_1": "prompt_1",
                    },
                ),
            },
        )

        test_yaml_path = pathlib.Path("chains/example-1.yml")
        result_chain = config.parse_chain_config(test_yaml_path)

        self.assertEqual(result_chain._name, expected_chain._name)
        self.assertListEqual(result_chain._inputs, expected_chain._inputs)
        for name, prompt in result_chain._prompts.items():
            self.assertIn(name, expected_chain._prompts)
            result_prompt = result_chain._prompts[name]
            expected_prompt = expected_chain._prompts[name]
            self.assertEqual(result_prompt.model(), expected_prompt.model())
            self.assertEqual(result_prompt._template_path,
                             expected_prompt._template_path)
            self.assertDictEqual(result_prompt._variables, expected_prompt._variables)


if __name__ == "__main__":
    unittest.main()
