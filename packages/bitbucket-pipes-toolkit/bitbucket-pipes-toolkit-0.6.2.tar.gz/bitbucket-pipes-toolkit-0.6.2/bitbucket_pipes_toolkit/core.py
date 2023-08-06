import os

import yaml
from cerberus import Validator

from .helpers import fail, success, configure_logger, enable_debug, get_logger


logger = configure_logger()


class Pipe:

    def fail(self, message):
        fail(message=message)

    def success(self, message, do_exit=False):
        success(message, do_exit=do_exit)

    def enable_debug_log_level(self):
        if self.get_variable('DEBUG'):
            logger.setLevel('DEBUG')

    def __init__(self, pipe_metadata=None, schema=None):
        if pipe_metadata is None:
            pipe_metadata = os.path.join(os.path.dirname(__file__), 'pipe.yml')
        with open(pipe_metadata, 'r') as f:
            self.metadata = yaml.safe_load(f.read())

        self.variables = None
        self.schema = schema

    @classmethod
    def from_pipe_yml(cls, ):
        pass

    def validate(self):
        if self.schema is None:
            schema = self.metadata['variables']
        else:
            schema = self.schema

        validator = Validator(
            schema=schema, purge_unknown=True)
        env = {key:yaml.safe_load(value) for key, value in os.environ.items() if key in schema}

        if not validator.validate(env):
            self.fail(
                message=f'Validation errors: \n{yaml.dump(validator.errors, default_flow_style = False)}')
        validated = validator.validated(env)
        return validated

    def get_variable(self, name):
        return self.variables[name]

    def run(self):
        self.variables = self.validate()
        self.enable_debug_log_level()

