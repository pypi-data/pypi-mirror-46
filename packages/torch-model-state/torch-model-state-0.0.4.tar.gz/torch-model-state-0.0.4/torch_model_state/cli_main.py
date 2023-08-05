import json
from pathlib import Path

import argparse_schema

from .configs import ArgumentConfig
from .state_utils import load_state_file, from_state


def cli_main():  # pragma: no cover
    with open(str(Path(__file__).parent / 'schema' / 'argument_config.json')) as f:
        schema = json.load(f)
    argument = ArgumentConfig(argparse_schema.parse(schema))

    state = load_state_file(argument.state_file, device=argument.device)

    if argument.extra_import:
        __import__(argument.extra_import)
    model = from_state(state, device=argument.device) if argument.load_model else None

    del state.model
    del state.optimizers

    print(json.dumps(vars(state), indent=2))
    if model is not None:
        print(model)
