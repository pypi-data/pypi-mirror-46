
import argparse


class RemainderStore(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        remainder={}

        for v in values:
            if "=" in v:
                name, value = v.split('=')
                remainder[name] = value
            else:
                remainder[v] = str(True)

        setattr(namespace, "remaining_args", remainder)


class ArgumentBase(object):

    def __init__(self, root_parser, root_subparsers):
        self.root_parser = root_parser
        self.root_subparsers = root_subparsers
        self.args = None

    def set_args(self, args):
        self.args = args

    @property
    def remaining_args(self):
        if hasattr(self.args, "remaining_args"):
            return self.args.remaining_args
        else:
            return {}
