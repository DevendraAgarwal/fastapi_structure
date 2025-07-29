"""Service to Retrieve Environment Variables"""

import os
from typing import Any
from dotenv import load_dotenv

from src.meta_classes.singleton import Singleton


class EnvironmentService(metaclass=Singleton):
    """Environment Service To Get ENV Variable

    Args:
        metaclass (_type_, optional): _description_. Defaults to Singleton.
    """
    def __init__(self):
        self._load_environment_variables()

    def _load_environment_variables(self):
        load_dotenv()

    def get(self, key: str, default: Any = None) -> Any:
        """_summary_

        Args:
            key (str): Key Name

        Returns:
            Any: _description_
        """
        value = os.getenv(key)
        if value is None:
            value = default
        return value

    def get_all_env_variables(self):
        """Get All Environment Variable in Dict Format

        Returns:
            _type_: _description_
        """
        return dict(os.environ)


env = EnvironmentService()
