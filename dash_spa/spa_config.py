from typing import List, Union
import os
import re
from iniconfig import IniConfig

class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TSectionConfig:

    def __init__(self, config: dict):
        self.__dict__ = config

    def get(self, attr, default_value):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            return default_value

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return None

UNDEFINED_SECTION = TSectionConfig({})
"""Returned when section is not present in configuration"""

class TConfig:

    def __init__(self, config):
        self.config = config

    def get(self, section: str = None, default_value: dict = None) -> TSectionConfig:
        """Return a section of the application configuration or the entire config.

        If the requested section does not exist the constant object
        UNDEFINED_SECTION is returned

        Args:
            section (str, optional): The required section. Defaults to None.
            default_value (dict, optional): Value returned if section not present

        Raises:
            ConfigurationError: Reports failure

        Returns:
            TSectionConfig: Object the section configuration or the entire config if section is None
        """

        try:
            if section:
                if section in self.config.sections:
                    dt = self.config.sections[section]
                    return TSectionConfig(dt)

                if default_value == None:
                    return UNDEFINED_SECTION

                return TSectionConfig(default_value)

            return TSectionConfig(self.config.sections)

        except ConfigurationError as ex:
            raise ConfigurationError(ex.message) from ex


def read_config(files: Union[str, List[str]] ='.env', env: str = None) -> TConfig:
    """Read configuration from file. If a list is supplied the configuration
    is taken from the fist file found. If the .ini file contains sections then
    the section name is used as a primary key in the returned dictionary.

    Args:
        files (Union[str, List[str]], optional): File(s) to try. Defaults to '.env'.
        env (str, optional): Env variable, if specified will over load with file{$env}.ini

    Raises:
        ConfigurationError: Error is no file found

    Returns:
        TConfig: Dictionary created from ini file content
    """

    def _aux_filename(filename:str, env_postfix:str=None) -> str:
        """Return file name with postix extension defined in env applied or None.

        Args:
            filename (str): Bse filename
            env_postfix (str, optional): ENV variable that holds postfix. Defaults to None.

        Returns:
            str: File name with postfix (if any) or None
        """

        if not env_postfix:
            return None

        postfix = os.environ.get(env_postfix, None)

        if not postfix:
            return None

        parts = filename.split('.')
        if len(parts) > 1:
            parts.insert(-1, postfix)
        else:
            parts.append(postfix)
        return '.'.join(parts)


    def _read_ini_file(path:str) -> dict:
        """Read content of given file

        Args:
            path (str): File to be read

        Returns:
            dict: configuration
        """


        def apply_env(config: dict):
            """Resolve dict entries of the form:

            config['password'] = '${SPA_ADMIN_PASSWORD}'

            SPA_ADMIN_PASSWORD is expected to be and ENV variable
            """
            result = {}
            for key, value in config.items():
                m = re.match("\${([A-Z]\w+)}", str(value))
                if m:
                    var = m.group(1)
                    value = os.environ.get(var, None)
                    if value is None:
                        raise ConfigurationError(f'ENV variable "{var}" is not assigned in file "{path}"')
                config[key] = value

        conf = IniConfig(path)

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
            main_conf = _read_ini_file(file)
            file = _aux_filename(file, env)
            if file:
                aux_conf = _read_ini_file(file)
                for section in aux_conf.sections.keys():
                    if section not in main_conf:
                        main_conf.config[section] = {}

                    conf_section = main_conf.sections[section]
                    aux_section = aux_conf[section]

                    for key, value in aux_section.items():
                        conf_section[key] = aux_section[key]

            return TConfig(main_conf)
        except FileNotFoundError:
            pass
        except ConfigurationError as ex:
            raise ConfigurationError(ex.message) from ex

    raise ConfigurationError(f'Unable to find configuration files {files}')


config = read_config(['config/spa_config.ini', 'spa_config.ini', '.env'], 'DASH_SPA_ENV')
