import collections

import yaml
from swiss_python.logger.log_utils import get_logger


def flatten_dict(d, parent_key='', sep='_', to_upper=False):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if to_upper:
            new_key = new_key.upper()
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep, to_upper=to_upper).items())
        else:
            items.append((new_key, v))
    return dict(items)


def yaml_to_flat_dict(src_file):
    logger = get_logger()
    try:
        f_yaml = open(src_file, 'r')
        d = yaml.load(f_yaml, Loader=yaml.FullLoader)
        return flatten_dict(d=d)

    except Exception as e:
        logger.error('Exception caught. type: {}, message: {}'.format(type(e), str(e)))
        return {}
