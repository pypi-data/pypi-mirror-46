import os
import json
import stat
from pathlib import Path


VERSION = (0, 1, 0, 'final', 0)


def get_version():
    "Returns a PEP 386-compliant version number from VERSION."
    assert len(VERSION) == 5
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if VERSION[2] == 0 else 3
    main = '.'.join(str(x) for x in VERSION[:parts])

    sub = ''
    if VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[VERSION[3]] + str(VERSION[4])

    return str(main + sub)


def load_settings(
    current_settings,
    filename='.settings.json',
    directory='.',
    depth=0,
    store=True,
):
    """ Load settings...

        filename - Name of json file with settings
        directory - Path of the directory where `filename` lives
        depth - Number of parent directories to scan for `filename`
        store = Store settings into the globals variable.

        Should be called in your django settings.py like so:

            from json_settings2 import load_settings
            load_settings(globals())

        Will return the dictionary with all loaded variables added to it.
    """
    assert isinstance(current_settings, dict)
    path = Path(os.path.expanduser(directory)).absolute()
    file_path = path / filename
    depth_counter = 0

    while not file_path.exists():
        if depth_counter > depth:
            raise FileNotFoundError(
                f'File {filename} not found using {path} with depth of {depth}'
            )
        file_path = path.parents[depth_counter] / filename
        depth_counter += 1

    with file_path.open() as fd:
        json_data = json.load(fd)

    for k, v in json_data.items():
        if k == k.upper() and store:
            # Django setting, set it
            current_settings[k] = v

    return json_data


def write_settings_from_django(
    *settings_vars,
    filename='.settings.json',
    directory='.',
    indent=4,
    force=False,
):
    """ Helper to write settings from current django settings
        to json settings.

        settings_vars = List of django settings to include in json settings
        filename = Filename of the json settings file
        directory = Directory in which to save `filename`
        indent = Indentation level for the json output. Set to "None" for
                 the most compact file.
        force = If `directory`/`filename` exists, overwrite it

        Example:

            write_settings_from_django(DATABASES, DEBUG, ADMINS, SECRET_KEY)

    """
    from django.conf import settings

    path = Path(os.path.expanduser(directory)).absolute() / filename
    if path.exists() and not force:
        raise FileExistsError(f'File {path} already exists. Not overwriting.')

    _vars = {}
    for setting in settings_vars:
        _vars[setting] = getattr(settings, setting)

    with path.open(mode='w') as fd:
        json.dump(_vars, fd, indent=indent)

    # Equivilent of 0600
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
