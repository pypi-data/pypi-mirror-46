import logging
import logging.config
from collections import Iterable, Mapping
from copy import deepcopy
from typing import List, Union, Type, TypeVar

from pyhocon import ConfigTree

from aiconf.aiconf import format_config
from aiconf.exceptions import MalformattedConfigException

U = TypeVar("U")


def load_class(class_string: str,
               restrict_to: Union[Type[U], List[Type[U]]] = None,
               relative_import: str = ""):
    try:
        module_name, cls_name = class_string.rsplit(".", 1)
    except ValueError:
        cls_name = class_string
        module_name = ""

    if relative_import:
        x = ".".join((relative_import, module_name)).rstrip(".")
        try:
            mod = __import__(x, fromlist=cls_name)
        except ModuleNotFoundError:
            mod = __import__(module_name, fromlist=cls_name)
    else:
        mod = __import__(module_name, fromlist=cls_name)
    cls = getattr(mod, cls_name)

    if restrict_to:
        check_subclass(cls, restrict_to)
    return cls


def get_all_subclasses(cls):
    """
    Returns all (currently imported) subclasses of a given class.

    :param cls: Class to get subclasses of.

    :return: all currently imported subclasses.
    """
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in get_all_subclasses(c))


def check_subclass(cls, restrict_to):
    """
    Performs a check whether a given class is a subclass of given class(es).

    :raises: :class:`ValueError` if class is not subclass of given class(es).

    :param cls: Class to check.

    :param restrict_to: Class(es) to check whether the given class is subclass of.
    """
    if not restrict_to:
        return
    if not isinstance(restrict_to, Iterable) and not isinstance(restrict_to,
                                                                str):
        restrict_to = [restrict_to]
    if not any(cls == target_cls or cls in get_all_subclasses(target_cls) for
               target_cls in restrict_to):
        raise ValueError(
            "{} is not subclass of any of {}".format(cls, restrict_to))


def get_constructor_and_args(config):
    # class only
    if not isinstance(config, ConfigTree) and not isinstance(config, dict):
        return config, dict()

    # who knows whether we're going to reuse the config one day...
    config = deepcopy(config)

    # new style factory method
    if "()" in config:
        cls = config.pop('()')
        return cls, config
    # old style
    elif "class" in config and 'args' in config:
        return config["class"], config["args"]
    # new style class
    elif "class" in config and 'args' not in config:
        cls = config.pop('class')
        return cls, config
    # wrong style
    else:
        raise MalformattedConfigException(
            "The config must be either provided in the format {{class: cls; args: {{}} }}"
            "or {{class/(): cls; arg1:val1; arg2:val2;}} but was {}.".format(
                format_config(config))
        )


def safe_construct(config_or_instance: Union[ConfigTree, U],
                   restrict_to: Union[Type[U], List[Type[U]]] = None,
                   relative_import: str = "",
                   perform_subclass_check=True, **kwargs) -> U:
    """
    Helper function to combine load_class and construct.

    Useful when an argument could be either already an instance or a
    config describing how to set up the instance.

    :param perform_subclass_check: Whether to perform the subclass check
        even if the given argument is an instance already.
    :param relative_import: String to prepend to the absolute import.
    :param restrict_to: Class to be constructed must be of this type(s).
    :param config_or_instance: Config to construct from or the actual
        instance.
    :param kwargs: Keyword args to be passed to constructor
    :return: Parsed class if possible.
    """
    if isinstance(config_or_instance, ConfigTree):
        return construct_from_config(config_or_instance, restrict_to,
                                     relative_import, **kwargs)
    if perform_subclass_check:
        check_subclass(config_or_instance.__class__, restrict_to)
    return config_or_instance


def construct_from_config(config: ConfigTree,
                          restrict_to: Union[Type[U], List[Type[U]]] = None,
                          relative_import: str = "", **kwargs) -> U:
    """
    Helper function to combine load_class and construct.

    Config layout supposed to be like this:

    ``{class_string: args_as_cfg}``

    where args_as_cfg are either dict, list or a single argument

    :param relative_import: String to prepend to the absolute import.

    :param restrict_to: Class to be constructed must be of this type(s).

    :param config: Config to construct from.

    :return: Parsed class if possible.
    """
    logger = logging.getLogger(__name__)
    cls_name, construct_args = get_constructor_and_args(config)
    logger.debug("Loading '{}' from config...".format(cls_name))
    cls = load_class(cls_name, restrict_to=restrict_to,
                     relative_import=relative_import)
    return construct(cls, construct_args, **kwargs)


def construct(cls: Type[U], args_as_cfg: ConfigTree, cascading=True,
              **kwargs) -> U:
    """
    Default factory method for a given class and given arguments.

    Construct the class with given arguments. Arguments parameter can be
    a single argument, a List.

    :param cls: Given arguments
    :param args_as_cfg:
    :param cascading: Whether to progressively construct nesting classes.
    :return:
    """
    logger = logging.getLogger(__name__)
    if isinstance(args_as_cfg, Mapping):
        args = deepcopy(args_as_cfg)
        for name, value in args.items():
            if isinstance(value, ConfigTree) and cascading:
                args[name] = construct_from_config(value)
        for k, v in kwargs.items():
            args.put(k, v)
        logger.debug(
            "Constructing {} with keyword arguments {}".format(cls.__name__,
                                                               args))
        return cls(**args)
    if isinstance(args_as_cfg, Iterable) and not isinstance(args_as_cfg, str):
        logger.debug("Constructing {} with arguments...".format(cls.__name__))
        return cls(*args_as_cfg)
    else:
        # one arg only
        logger.debug(
            "Constructing {} with one single argument".format(cls.__name__))
        return cls(args_as_cfg)
