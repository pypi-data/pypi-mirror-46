import os


__author__ = 'Artur Tamborski <tamborskiartur@gmail.com>'
__license__ = 'MIT'
__version__ = '0.0.8'
__all__ = ['load_config']


def _get_attr(klass, attr_name, default_value=None):
    value = getattr(klass, attr_name, default_value)

    if type(value) is type(default_value):
        return value

    raise TypeError("Type of '%s.%s' attribute differs from the expected "
                    "type '%s'." % (klass.__name__, attr_name,
                                    type(default_value).__name__))


def _set_attr(klass, attr_name, value, safe, from_env):
    attr = getattr(klass, attr_name)

    if from_env:
        try:
            value = int(value)
        except ValueError:
            pass

        if value == 'TRUE':
            value = True

        if value == 'FALSE':
            value = False

    if not safe or attr is None or type(attr) is type(value):
        return setattr(klass, attr_name, value)

    raise TypeError("'%s.%s' expected value with type '%s', got value '%s' "
                    "with type '%s' instead." % (klass.__name__, attr_name,
                     type(attr).__name__, value, type(value).__name__))


def _deep_merge(source, destination):
    for key, value in source.items():
        if type(value) is dict:
            node = destination.setdefault(key, {})
            _deep_merge(value, node)
        else:
            if destination is None:
                destination = {}
            destination[key] = value
    return destination


def _uppercase_keys_in_dict(data):
    ret = {}

    for key, value in data.items():
        new_key = key.replace('-', '_').upper()

        if type(data[key]) is dict:
            value = _uppercase_keys_in_dict(data[key])

        ret[new_key] = value
    return ret


def _load_first_file_from_dirs(name, dirs, loaders):

    for d in dirs:
        path = os.path.expanduser(d) + '/' + name
        if not os.path.isfile(path):
            continue

        with open(path) as file:
            try:
                ext = name.rsplit('.')[1]
                mod = loaders[ext][0]
                fun = loaders[ext][1]
                data = getattr(__import__(mod), fun)(file)
                if data:
                    return _uppercase_keys_in_dict(data)

            except ImportError:
                raise ImportError("Failed to load '%s'. Could not "
                                  "find module that supports '%s' "
                                  "file format." % (name, ext))
    return {}


def _overwrite_attrs(klass, config, safe, env_prefix=''):
    klass_name = klass.__name__.upper()

    if klass_name not in config:
        return

    if env_prefix and not env_prefix.endswith('__'):
        env_prefix += '__'

    for attr_name in vars(klass):
        if attr_name.islower():
            continue

        attr_key = attr_name.upper()
        attr_value = getattr(klass, attr_name)
        sub_config = config[klass_name]

        if type(attr_value) is not type:
            env_name = env_prefix + klass_name + '__' + attr_key

            value = sub_config.get(attr_key, attr_value)
            value = os.environ.get(env_name, value)

            _set_attr(klass, attr_key, value, safe, env_name in os.environ)
        else:
            if not attr_name.istitle() or attr_key not in sub_config:
                continue

            if sub_config[attr_key] is None:
                raise TypeError("Class '%s.%s' expected value with"
                                " type 'dict', got 'None' instead."
                                % (klass.__name__, attr_name))

            _overwrite_attrs(attr_value, sub_config, safe,
                    env_prefix=env_prefix + klass_name)


def load_config(klass):
    """ Update config class with values found in configuration file,
        secrets file and environment variables.
    """
    if not isinstance(klass, type):
        raise TypeError("Function 'load_config()' expected value with "
                        "'class' type as an argument, got value with "
                        "type '%s' instead." % type(klass).__name__)

    t_safe = _get_attr(klass, '_type_safe', True)
    prefix = _get_attr(klass, '_environ_prefix', '')
    c_name = _get_attr(klass, '_config_filename', 'config.yaml')
    s_name = _get_attr(klass, '_secret_filename', 'secret.yaml')
    c_path = _get_attr(klass, '_config_filepath', ['.'])
    s_path = _get_attr(klass, '_secret_filepath', ['.'])
    f_load = _get_attr(klass, '_format_loaders', {
        'ini':  ['ini',  'load'], 'json': ['json',      'load'],
        'toml': ['toml', 'load'], 'yaml': ['yaml', 'safe_load']})
    config = _load_first_file_from_dirs(c_name, c_path, f_load)
    secret = _load_first_file_from_dirs(s_name, s_path, f_load)
    config = _deep_merge(secret, config)

    _overwrite_attrs(klass, config, t_safe, env_prefix=prefix)
