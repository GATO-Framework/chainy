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

### Configuration

Chainy uses YAML configuration files to define chains of prompts.
Here's an example of what these configuration files look like:

```yaml
inputs:
  - input_1
  - input_2
prompts:
  prompt_1:
    model: my_model
    template: tmpl01.md
    substitute:
      var_1: input_1
      var_2: input_2
  prompt_2:
    model: my_model
    template: tmpl02.md
    substitute:
      res_1: prompt_1
```

In this example, `prompt_1` and `prompt_2` are the prompts to be run.
Each prompt includes a template file and a dictionary of variables to be substituted into the template.
The dependencies between prompts are defined in the substitute section: `prompt_2` depends on `prompt_1`.

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

### Bring Your Own Model (BYOM)

Each prompt must specify the alias of the model that will be used to generate the response.
Models must be added to a chain with `Chain.add_model(name, model)` before the chain is started.

Models are user defined classes that adhere to the `LanguageModelProtocol` or `ChatModelProtocol`,
which can be found in the [`llm`](src/chainy/llm.py) module.
Essentially, the model needs to expose the appropriate `generate()` method, then `chainy` will take it from there.

### Running a Chain

To run a chain, call the `Chain.start()` method with the required input values:

```python
from chainy.model import Chain

# STEP 1: Load your chain from configuration
chain = Chain.from_config("chains/example-1.yml")

# STEP 2: Add your model(s)
model = ...  # instantiate your model here!
chain.add_model("my_model", model)

# STEP 3: Start the chain
chain.start("hey", "bud")
```

## Testing

Tests are located in the `tests/` directory. To run them, use your preferred test runner.

## Contributing

We welcome contributions! Please open an issue or submit a pull request if you have something to add.

## License

[MIT](https://choosealicense.com/licenses/mit/)
