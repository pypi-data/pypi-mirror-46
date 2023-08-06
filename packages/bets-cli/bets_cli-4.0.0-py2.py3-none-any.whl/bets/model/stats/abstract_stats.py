from typing import Dict, List, Union

from tabulate import tabulate


class AbstractStats:
    KEYS: List[str]

    def __getitem__(self, key: str):
        try:
            return self.__dict__[key]
        except KeyError:
            if hasattr(self, key):
                return getattr(self, key)
            raise

    def __repr__(self):
        return repr(self.as_dict())

    def __str__(self):
        return tabulate([self.as_dict()], headers="keys", floatfmt=".02f", stralign="right")

    def as_tuple(self) -> tuple:
        return tuple(self[key] for key in self.KEYS)

    def as_dict(self) -> Dict[str, Union[int, float, str]]:
        return {key: self[key] for key in self.KEYS}
