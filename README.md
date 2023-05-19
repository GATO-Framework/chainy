# Chainy

## Overview

Chainy is a Python package for declarative prompt chaining.
It allows users to define a chain of prompts to be run by a Large Language Model (LLM).
These chains are defined using a YAML configuration file and can include dependencies, which are handled automatically.

## Installation

To install `chainy`, you can use a package manager like `pip`.

```bash
pip install chainy
```

You can find the package repository [here](https://pypi.org/project/chainy/).

## Usage

Chainy uses YAML configuration files to define chains of prompts.
Here's an example of what these configuration files look like:

```yaml
inputs:
  - input_1
  - input_2
prompts:
  prompt_1:
    template: tmpl01.md
    substitute:
      var_1: input_1
      var_2: input_2
  prompt_2:
    template: tmpl02.md
    substitute:
      res_1: prompt_1
```

In this example, `prompt_1` and `prompt_2` are the prompts to be run.
Each prompt includes a template file and a dictionary of variables to be substituted into the template.
The dependencies between prompts are defined in the substitute section: `prompt_2` depends on `prompt_1`.

To run a chain, call the `Chain.start()` method with the required input values:

```python
import pathlib
import chainy.config

chain_path = pathlib.Path("chains/example-1.yml")
chain = chainy.config.parse_config(chain_path)
chain.start("hey", "bud")
```

### Expected Directory Structure

```
|- yourproject/
|--- prompts/
|----- tmpl01.md
|----- tmpl02.md
|--- chains/
|----- example-1.yml
|--- entrypoint.py
```

## Testing

Tests are located in the `tests/` directory. To run them, use your preferred test runner.

## Contributing

We welcome contributions! Please open an issue or submit a pull request if you have something to add.

## License

[MIT](https://choosealicense.com/licenses/mit/)
