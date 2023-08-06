import json


REQUIRED_OPTIONS = {'source', 'url', 'credentials'}


def load_config(config):
    """
    Load export config from json file

    :param config: path to config json file
    :return:
    """
    with open(config, 'r') as fd:
        try:
            settings = json.load(fd)
        except json.JSONDecodeError:
            settings = None

        if settings is not None:
            keys = settings.keys()
            for option in REQUIRED_OPTIONS:
                if option not in keys:
                    raise ValueError(f'required option missed {option} ')
        return settings
