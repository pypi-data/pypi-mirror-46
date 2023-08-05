
import os
import re
import yaml
import argparse
from argparse import *
from types import SimpleNamespace


__version__ = '1.5.0'


class ArgumentParser(argparse.ArgumentParser): #pylint: disable=function-redefined
    """Extension to python's argparse which simplifies parsing of configuration
    options from command line arguments, yaml configuration files, environment
    variables and hard-coded defaults.
    """

    groups = {}

    def parse_args(self, *args, env=True, nested=True, **kwargs):
        """Parses command line argument strings.

        All the arguments from `argparse.ArgumentParser.parse_args
        <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        are supported. Additionally it accepts:

        Args:
            env (bool): Whether to merge with the parsed environment.
            nested (bool): Whether the namespace should be nested.

        Returns:
            SimpleNamespace: An object with all parsed values as nested attributes.
        """

        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.parse_env(nested=False) if env else None

        cfg = super().parse_args(*args, **kwargs)

        if not nested:
            return cfg

        return self._dict_to_namespace(self._flat_namespace_to_dict(cfg))


    def parse_yaml(self, file_path, env=True, defaults=True, nested=True):
        """Parses a yaml file given its path.

        Args:
            file_path (str): Path to the yaml file to parse.
            env (bool): Whether to merge with the parsed environment.
            defaults (bool): Whether to merge with the parser's defaults.
            nested (bool): Whether the namespace should be nested.

        Returns:
            SimpleNamespace: An object with all parsed values as nested attributes.
        """
        cwd = os.getcwd()
        os.chdir(os.path.abspath(os.path.join(file_path, os.pardir)))
        try:
            with open(os.path.basename(file_path), 'r') as f:
                parsed_yaml = self.parse_yaml_from_string(f.read(), env, defaults, nested)
        finally:
            os.chdir(cwd)
        return parsed_yaml


    def parse_yaml_from_string(self, yaml_str, env=True, defaults=True, nested=True):
        """Parses yaml given as a string.

        Args:
            yaml_str (str): The yaml content.
            env (bool): Whether to merge with the parsed environment.
            defaults (bool): Whether to merge with the parser's defaults.
            nested (bool): Whether the namespace should be nested.

        Returns:
            SimpleNamespace: An object with all parsed values as attributes.
        """
        cfg = yaml.safe_load(yaml_str)
        self.check_config(cfg)

        def map_value_nested(cfg, keys, func):
            if len(keys) > 1:
                map_value_nested(cfg[keys[0]], keys[1:], func)
            else:
                cfg[keys[0]] = func(cfg[keys[0]])

        cfg_flat = self._namespace_to_dict(self._dict_to_flat_namespace(cfg))
        for action in self.__dict__['_actions']:
            if isinstance(action, ActionPath) and action.dest in cfg_flat:
                map_value_nested(cfg, action.dest.split('.'), action.type)

        if not nested:
            cfg = self._namespace_to_dict(self._dict_to_flat_namespace(cfg))

        if env:
            cfg = self.merge_config(cfg, self.parse_env(defaults=defaults, nested=nested))

        elif defaults:
            cfg = self.merge_config(cfg, self.get_defaults(nested=nested))

        return self._dict_to_namespace(cfg)


    def dump_yaml(self, cfg):
        """Generates a yaml string for a configuration object.

        Args:
            cfg (SimpleNamespace | dict): The configuration object to dump.

        Returns:
            str: The configuration in yaml format.
        """
        if not isinstance(cfg, dict):
            cfg = self._namespace_to_dict(cfg)

        self.check_config(cfg, skip_none=True)

        cfg = self._namespace_to_dict(self._dict_to_flat_namespace(cfg))
        for action in self.__dict__['_actions']:
            if isinstance(action, ActionPath):
                if cfg[action.dest] is not None:
                    cfg[action.dest] = cfg[action.dest](absolute=False)
            elif isinstance(action, ActionConfigFile):
                del cfg[action.dest]
        cfg = self._flat_namespace_to_dict(self._dict_to_namespace(cfg))

        return yaml.dump(cfg, default_flow_style=False, allow_unicode=True)


    def parse_env(self, env=None, defaults=True, nested=True):
        """Parses environment variables.

        Args:
            env (object): The environment object to use, if None `os.environ` is used.
            defaults (bool): Whether to merge with the parser's defaults.
            nested (bool): Whether the namespace should be nested.

        Returns:
            SimpleNamespace: An object with all parsed values as attributes.
        """
        if env is None:
            env = os.environ
        cfg = {}
        for action in self.__dict__['_actions']:
            env_var = (self.prog+'_' if self.prog else '') + action.dest
            env_var = env_var.replace('.', '__').upper()
            if env_var in env:
                cfg[action.dest] = self._parse_value(env[env_var], action, env_var)

        if nested:
            cfg = self._flat_namespace_to_dict(SimpleNamespace(**cfg))

        if defaults:
            cfg = self.merge_config(cfg, self.get_defaults(nested=nested))

        return self._dict_to_namespace(cfg)


    def get_defaults(self, nested=True):
        """Returns a namespace with all default values.

        Args:
            nested (bool): Whether the namespace should be nested.

        Returns:
            SimpleNamespace: An object with all default values as attributes.
        """
        cfg = {}
        for action in self.__dict__['_actions']:
            if len(action.option_strings) > 0 and action.default != '==SUPPRESS==':
                cfg[action.dest] = action.default

        if nested:
            cfg = self._flat_namespace_to_dict(SimpleNamespace(**cfg))

        return self._dict_to_namespace(cfg)


    def add_argument_group(self, *args, name=None, **kwargs):
        """Adds a group to the parser.

        All the arguments from `argparse.ArgumentParser.add_argument_group
        <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument_group>`_
        are supported. Additionally it accepts:

        Args:
            name (str): Name of the group. If set the group object will be included in the parser.groups dict.

        Returns:
            The group object.
        """
        group = argparse._ArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        if name is not None:
            self.groups[name] = group
        return group


    def check_config(self, cfg, skip_none=False):
        """Checks that the content of a given configuration object conforms with the parser.

        Args:
            cfg (SimpleNamespace | dict): The configuration object to check.
            skip_none (bool): Whether to skip checking of values that are None.

        Raises:
            Exception: For any part of the configuration object that does not conform.
        """
        if not isinstance(cfg, dict):
            cfg = self._namespace_to_dict(cfg)

        def find_action(dest):
            for action in self.__dict__['_actions']:
                if action.dest == dest:
                    return action
            return None

        def check_values(cfg, base=None):
            for key, val in cfg.items():
                if skip_none and val is None:
                    continue
                kbase = key if base is None else base+'.'+key
                if isinstance(val, dict):
                    check_values(val, kbase)
                else:
                    self._parse_value(val, find_action(kbase), kbase)

        check_values(cfg)


    @staticmethod
    def merge_config(cfg_from, cfg_to):
        """Merges the first configuration into the second configuration.

        Args:
            cfg_from (SimpleNamespace | dict): The configuration from which to merge.
            cfg_to (SimpleNamespace | dict): The configuration into which to merge.

        Returns:
            SimpleNamespace | dict: The merged configuration with same type as cfg_from.
        """
        def merge_values(cfg_from, cfg_to):
            for k, v in cfg_from.items():
                if v is None:
                    continue
                if k not in cfg_to or not isinstance(v, dict):
                    cfg_to[k] = v
                else:
                    cfg_to[k] = merge_values(cfg_from[k], cfg_to[k])
            return cfg_to

        out_dict = isinstance(cfg_from, dict)
        cfg_from = cfg_from if isinstance(cfg_from, dict) else ArgumentParser._namespace_to_dict(cfg_from)
        cfg_to = cfg_to if isinstance(cfg_to, dict) else ArgumentParser._namespace_to_dict(cfg_to)
        cfg = merge_values(cfg_from, cfg_to.copy())
        return cfg if out_dict else ArgumentParser._dict_to_namespace(cfg)


    @staticmethod
    def _parse_value(value, action, key):
        """Parses a value for a given action.

        Args:
            value (object): The value to parse.
            action (Action): The action used for parsing.
            key (str): The configuration key.

        Raises:
            Exception: If parsing of value fails.
        """
        if action is None:
            raise Exception('Unexpected configuration key: '+key)
        if action.type is None:
            if action.choices is not None:
                if value not in set(action.choices):
                    raise Exception('Unexpected configuration value for key: '+key)
            elif not isinstance(value, str):
                raise Exception('Unexpected configuration value for key: '+key)
        else:
            try:
                value = action.type(value)
            except:
                raise Exception('Unexpected configuration value for key: '+key)
        return value


    @staticmethod
    def _flat_namespace_to_dict(cfg_ns):
        """Converts a flat namespace into a nested dictionary.

        Args:
            cfg_ns (SimpleNamespace): The configuration to process.

        Returns:
            dict: The nested configuration dictionary.
        """
        cfg_dict = {}
        for k, v in vars(cfg_ns).items():
            ksplit = k.split('.')
            if len(ksplit) == 1:
                cfg_dict[k] = v
            else:
                kdict = cfg_dict
                for num, kk in enumerate(ksplit[:len(ksplit)-1]):
                    if kk not in kdict:
                        kdict[kk] = {}
                    elif not isinstance(kdict[kk], dict):
                        raise Exception('Conflicting namespace base: '+'.'.join(ksplit[:num]))
                    kdict = kdict[kk]
                if ksplit[-1] in kdict:
                    raise Exception('Conflicting namespace base: '+k)
                kdict[ksplit[-1]] = v
        return cfg_dict


    @staticmethod
    def _dict_to_flat_namespace(cfg_dict):
        """Converts a nested dictionary into a flat namespace.

        Args:
            cfg_dict (dict): The configuration to process.

        Returns:
            SimpleNamespace: The configuration namespace.
        """
        cfg_ns = {}

        def flatten_dict(cfg, base=None):
            for key, val in cfg.items():
                kbase = key if base is None else base+'.'+key
                if isinstance(val, dict):
                    flatten_dict(val, kbase)
                else:
                    cfg_ns[kbase] = val

        flatten_dict(cfg_dict)

        return SimpleNamespace(**cfg_ns)


    @staticmethod
    def _dict_to_namespace(cfg_dict):
        """Converts a nested dictionary into a nested namespace.

        Args:
            cfg_args (dict): The configuration to process.

        Returns:
            SimpleNamespace: The nested configuration namespace.
        """
        def expand_dict(cfg):
            for k, v in cfg.items():
                if isinstance(v, dict):
                    cfg[k] = expand_dict(v)
            return SimpleNamespace(**cfg)
        return expand_dict(cfg_dict)


    @staticmethod
    def _namespace_to_dict(cfg_ns):
        """Converts a nested namespace into a nested dictionary.

        Args:
            cfg_args (SimpleNamespace): The configuration to process.

        Returns:
            dict: The nested configuration dictionary.
        """
        def expand_namespace(cfg):
            cfg = dict(vars(cfg))
            for k, v in cfg.items():
                if isinstance(v, SimpleNamespace):
                    cfg[k] = expand_namespace(v)
            return cfg
        return expand_namespace(cfg_ns)


class ActionConfigFile(Action):
    """Action to indicate that an argument is a configuration file."""

    def __init__(self, **kwargs):
        opt_name = kwargs['option_strings']
        opt_name = opt_name[0] if len(opt_name) == 1 else [x for x in opt_name if x[0:2] == '--'][0]
        if '.' in opt_name:
            raise Exception('Config file must be a top level option.')
        kwargs['type'] = str
        super().__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if not isinstance(getattr(namespace, self.dest), list):
            setattr(namespace, self.dest, [])
        getattr(namespace, self.dest).append(Path(values, mode='r'))
        cfg_file = parser.parse_yaml(values, env=False, defaults=False, nested=False)
        for key, val in vars(cfg_file).items():
            setattr(namespace, key, val)


class ActionYesNo(Action): 
    """Paired action --opt, --no_opt to set True or False respectively."""

    def __init__(self, **kwargs):
        opt_name = kwargs['option_strings'][0]
        if 'dest' not in kwargs:
            kwargs['dest'] = re.sub('^--', '', opt_name).replace('-', '_')
        kwargs['option_strings'] += [re.sub('^--', '--no_', opt_name)]
        kwargs['nargs'] = 0
        kwargs['type'] = lambda x: x if isinstance(x, bool) else raise_(ValueError)
        super().__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string.startswith('--no_'):
            setattr(namespace, self.dest, False)
        else:
            setattr(namespace, self.dest, True)


class ActionPath(Action):
    """Action to check and store a file path.

    Args:
        mode (str): The required type and access permissions among [drwx] as a keyword argument, e.g. ActionPath(mode='drw').
    """
    def __init__(self, **kwargs):
        if 'mode' in kwargs:
            self._mode = kwargs['mode']
        elif not '_mode' in kwargs:
            raise Exception('Expected mode keyword argument.')
        else:
            self._mode = kwargs.pop('_mode')
            kwargs['type'] = lambda x: x if isinstance(x, Path) else Path(x, mode=self._mode) if isinstance(x, str) else raise_(ValueError)
            super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            kwargs['_mode'] = self._mode
            return ActionPath(**kwargs)
        setattr(args[1], self.dest, Path(args[2], mode=self._mode))


class Path(object):
    """Stores a (possibly relative) path and the corresponding absolute path.

    When an object is created it is checked that: the path exists, whether it is
    a file or directory and has the required access permissions. The absolute
    path of can be obtained without having to remember the working directory
    from when the object was created.

    Args:
        path (str): The path to check and store.
        mode (str): The required type and access permissions among [drwx].
        cwd (str): Working directory for relative paths. If None, then os.getcwd() is used.

    Args called:
        absolute (bool): If false returns the original path given, otherwise the corresponding absolute path.
    """
    def __init__(self, path, mode='r', cwd=None):
        if not isinstance(mode, str):
            raise Exception('Expected mode to be a string.')
        if len(set(mode)-set('drwx')) > 0:
            raise Exception('Expected mode to only include [drwx] flags.')

        if cwd is None:
            cwd = os.getcwd()

        if isinstance(path, Path):
            abs_path = path(absolute=True)
            path = path()
        elif not isinstance(path, str):
            raise Exception('Expected path to be a string or a Path.')
        else:
            abs_path = path if os.path.isabs(path) else os.path.join(cwd, path)

        ptype = 'Directory' if 'd' in mode else 'File'
        if not os.access(abs_path, os.F_OK):
            raise ArgumentTypeError(ptype+' does not exist: '+abs_path)
        if 'd' in mode and not os.path.isdir(abs_path):
            raise ArgumentTypeError('Path is not a directory: '+abs_path)
        if 'd' not in mode and not os.path.isfile(abs_path):
            raise ArgumentTypeError('Path is not a file: '+abs_path)
        if 'r' in mode and not os.access(abs_path, os.R_OK):
            raise ArgumentTypeError(ptype+' is not readable: '+abs_path)
        if 'w' in mode and not os.access(abs_path, os.W_OK):
            raise ArgumentTypeError(ptype+' is not writeable: '+abs_path)
        if 'x' in mode and not os.access(abs_path, os.X_OK):
            raise ArgumentTypeError(ptype+' is not executable: '+abs_path)

        self.path = path
        self.abs_path = abs_path

    def __str__(self):
        return self.abs_path

    def __call__(self, absolute=True):
        return self.abs_path if absolute else self.path


def raise_(ex):
    """Raise that works within lambda functions.

    Args:
        ex (Exception): The exception object to raise.
    """
    raise ex
