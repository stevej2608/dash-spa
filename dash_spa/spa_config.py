from typing import List, Union
from collections import namedtuple
import os
import re
import iniconfig

class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TiniConfig:

    def __init__(self, config):
        self.config = config

    def get(self, section: str = None):
        """Return a section of the application configuration

        Args:
            section (str, optional): The required section. Defaults to None.
            config (dict, optional): The configuration dict. Defaults to CONFIG.

        Raises:
            ConfigurationError: Reports failure

        Returns:
            Object: Object containing the configuration
        """

        class ConfigWrapper:

            def __init__(self, config):
                self.__dict__ = config

            def get(self, attr, default):
                if attr in self.__dict__:
                    return self.__dict__[attr]
                else:
                    return default

            def __getattr__(self, key):
                if key in self.__dict__:
                    return self.__dict__[key]
                #raise ConfigurationError(f"Configuration error: Attribute {section}.{key} has not been defined.")
                return None

        try:
            if section:
                if section in self.config.sections:
                    dt = self.config.sections[section]
                else:
                    raise ConfigurationError(f"Configuration error: Section {section} has not been defined.")
            else:
                dt = self.config.sections

            obj = ConfigWrapper(dt)
            return obj
        except ConfigurationError as ex:
            raise ConfigurationError(ex.message) from ex


def read_config(files: Union[str, List[str]] ='.env', env: str = None) -> TiniConfig:
    """Read configuration from file. If a list is supplied the configuration
    is taken from the fist file found If the .ini file contains sections then
    the section name is used as a primary key in the returned dictionary.

    Args:
        files (Union[str, List[str]], optional): File(s) to try. Defaults to '.env'.
        env (str, optional): Env variable, if specified will over load with file{$env}.ini

    Raises:
        ConfigurationError: Error is no file found

    Returns:
        TiniConfig: Dictionary created from ini file content
    """

    def aux_filename(filename, env=None):

        if not env:
            return None

        postfix = os.environ.get(env, None)

        if not postfix:
            return None

        parts = filename.split('.')
        if len(parts) > 1:
            parts.insert(-1, postfix)
        else:
            parts.append(postfix)
        return '.'.join(parts)

    def get_config(file):

        def apply_env(config: dict):

            result = {}
            for key, value in config.items():
                m = re.match("\${([A-Z]\w+)}", str(value))
                if m:
                    var = m.group(1)
                    value = os.environ.get(var, None)
                    if value is None:
                        raise ConfigurationError(f'ENV variable "{var}" is not assigned in file "{file}"')
                config[key] = value

        conf = iniconfig.IniConfig(file)

        # Apply any ENV variables and convert types

        for section in conf.sections.values():
            apply_env(section)

            # Convert basic types

            for key, value in section.items():

                if value.lower() in ['true', 'false']:
                    section[key] = value.lower() == 'true'
                    continue

                if value.isdigit():
                    section[key] = int(value)
                    continue

                try:
                    section[key] = float(value)
                except ValueError:
                    pass

        return conf

    files = [files] if isinstance(files, str) else files
    for file in files:
        try:
            conf = get_config(file)
            file = aux_filename(file, env)
            if file:
                aux_conf = get_config(file)
                for section in aux_conf.sections.keys():
                    if section not in conf:
                        conf.config[section] = {}

                    conf_section = conf.sections[section]
                    aux_section = aux_conf[section]

                    for key, value in aux_section.items():
                        conf_section[key] = aux_section[key]

            return TiniConfig(conf)
        except FileNotFoundError:
            pass
        except ConfigurationError as ex:
            raise ConfigurationError(ex.message) from ex

    raise ConfigurationError(f'Unable to find configuration files {files}')


config = read_config(['config/spa_config.ini', 'spa_config.ini', '.env'], 'DASH_SPA_ENV')
