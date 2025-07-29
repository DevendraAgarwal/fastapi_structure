"""
Global App Service Used to store key Value Pair
to Set and Retrieve the data
"""

from ..meta_classes.singleton import Singleton


class AppGlobalService(metaclass=Singleton):
    """Global App Service:
    Used to Set and Get the Key Value Pair
    Import It as Global Variable with Alias `ags`

    Args:
        metaclass (_type_, optional): _description_. Defaults to Singleton.
    """

    app: dict = {}
