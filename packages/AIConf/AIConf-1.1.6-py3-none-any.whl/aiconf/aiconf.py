import json
import logging
import os
import re
from typing import Union, Tuple

import argparse

from overrides import overrides
from pyhocon import ConfigFactory, ConfigTree


class ConfigReader:
    """


    Reads and parses the config under the given config.
    Given a default config merges it with the given config (useful when
    you have a default application config).
    """

    def __init__(self, path='', default=''):
        """
        Initializes the reader.

        Accepts a config config and a default config config (or resource).

        :param path: Path to the config.
        :param default: fallback config (path, resource or string)
        """

        try:
            # is resource
            default = default.decode("utf-8")
        except AttributeError:
            try:
                # is path
                default = ConfigFactory.parse_file(default)
            except (FileNotFoundError, TypeError, OSError):
                # let's assume it's just a string (for now)
                pass

        if not path and not default:
            raise ValueError("Either config or fallback must be specified!")
        if path:
            try:
                self.config = ConfigFactory.parse_file(path)
            except FileNotFoundError:
                logging.getLogger(__name__).warning(
                    "{} doesn't exist! will load default only! {}".format(
                        path, os.getcwd())
                )
                self.config = ""
        else:
            self.config = ""

        if isinstance(default, str):
            default: ConfigTree = ConfigFactory.parse_string(default)
        if isinstance(self.config, str):
            self.config: ConfigTree = ConfigFactory.parse_string(self.config)
        self.default: ConfigTree = default

    def read_config(self):
        """
        Reads the config and returns a parsed mapping between config
        keys and (parsed) values.

        If no config is found under config, loads the default config only.

        :return: Mapping from config entries to their parsed values.
        """
        if not self.config:
            return self.default
        # cfg_str = '{}\n{}'.format(self.default, self.config)
        if not self.default:
            return self.config
        if self.config and self.default:
            return ConfigTree.merge_configs(self.default, self.config)


class ConfArgumentParser(argparse.ArgumentParser):
    int_only = re.compile(r'[-+]?([\d]+)$')
    int_or_float = numeric_const_pattern = re.compile(
        r"[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?")

    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=None,
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True,
                 default_config=None):
        super().__init__(prog, usage, description, epilog, parents or [],
                         formatter_class, prefix_chars,
                         fromfile_prefix_chars, argument_default,
                         conflict_handler, add_help, allow_abbrev)
        self.default_config = default_config
        self._args = None
        self._conf = None

    @property
    def args(self):
        return self._args

    @property
    def conf(self):
        return self._conf

    def parse_string(self,
                     k: str,
                     v: str) -> Tuple[str, Union[bool, str, int, float]]:
        if v in ["yes", "true"]:
            return k, True
        if v in ['no', 'false']:
            return k, False
        if re.match(ConfArgumentParser.int_only, v):
            return k, int(v)
        if re.match(ConfArgumentParser.int_or_float, v):
            return k, float(v)
        return k, v

    @overrides
    def parse_args(self, args=None, namespace=None):
        args = super().parse_args(args, namespace)
        self._conf = ConfigReader(args.config,
                                  default=self.default_config).read_config()
        self._args = args
        if args.c:
            for cs in args.c:
                for c in cs:
                    self._conf = ConfigTree.merge_configs(
                        self._conf,
                        ConfigFactory.parse_string(c)
                    )
            return args


def get_arg_parser(description, default_config) -> ConfArgumentParser:
    parser = ConfArgumentParser(description=description,
                                default_config=default_config)
    parser.add_argument("config", metavar="config", type=str)
    parser.add_argument('-c', action='append', nargs='+')
    return parser


def format_config(config) -> str:
    """
    Formats the config in a more-or-less readable way.

    :class:`ConfigReader`
    :meth:`ConfigReader.read_config`

    :param config: Config to be formatted.
    :return: Formatted config.
    """
    return json.dumps(config.as_plain_ordered_dict(), indent=4)


def fqcn(cls):
    return '.'.join((cls.__class__.__module__, cls.__class__.__name__))
