import dataclasses
from typing import List
from typing import Union
from typing import Optional

import copy
import base64
import uuid


@dataclasses.dataclass(frozen=True)
class KeyPair:
    kind: str
    name: Union[str, int]

    def __post_init__(self):
        if not isinstance(self.kind, str):
            raise ValueError(
                f'kind must be an instance of str, but received: {type(self.kind)} (value: {self.kind})'
            )

        if not (isinstance(self.name, str) or isinstance(self.name, int)):
            raise ValueError(
                f'name must be an instance of str or int, but received: {type(self.name)} (value: {self.name})'
            )

        if self.kind.find("'") >= 0 or self.kind.find('"') >= 0:
            raise ValueError(f'Invalid kind of "{self.kind}", do not include quotes in kind')

        if isinstance(self.name, str):
            if self.name.find("'") >= 0 or self.name.find('"') >= 0:
                raise ValueError(f'Invalid name of "{self.name}", do not include quotes in name')

    @classmethod
    def build(cls, kind: str, name: Union[str, int], implicit_id_str: bool = True):
        if implicit_id_str:
            if isinstance(name, str) and name.isdecimal():
                name = int(name)

        return cls(kind=kind, name=name)

    def is_name(self) -> bool:
        return isinstance(self.name, str)

    def is_id(self) -> bool:
        return isinstance(self.name, int)

    def key_pair_literal(self) -> str:
        if self.is_name():
            return f"'{self.kind}', '{self.name}'"
        else:
            return f"'{self.kind}', {self.name}"


class _BaseKey:
    def parent(self):
        raise NotImplementedError()

    def pairs(self) -> List[KeyPair]:
        return []

    def flat_pairs(self) -> List[Union[str, int]]:
        return []

    def kind(self) -> str:
        raise NotImplementedError()

    def name(self) -> Union[str, int]:
        raise NotImplementedError()

    def key_literal(self) -> str:
        raise NotImplementedError()

    def key_path(self) -> str:
        raise NotImplementedError()

    def key_path_urlsafe(self) -> str:
        raise NotImplementedError()


class NoneKey(_BaseKey):
    _root = None

    @classmethod
    def get_instance(cls):
        if cls._root:
            return cls._root
        cls._root = cls()
        return cls._root

    def parent(self):
        return self

    def pairs(self):
        return []

    def flat_pairs(self):
        return []

    def kind(self):
        return None

    def name(self):
        return None

    def __repr__(self):
        return "NoneKey(kind='None', name='none')"

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def key_literal(self):
        return None

    def key_path(self):
        return None

    def key_path_urlsafe(self):
        return None


@dataclasses.dataclass(frozen=True)
class EntityKey(_BaseKey):
    _pairs: List[KeyPair]

    def __post_init__(self):
        if len(self._pairs) == 0:
            raise ValueError('EntityKey#pairs must have at least one element.')

    def parent(self):
        if len(self._pairs) == 1:
            return NoneKey.get_instance()

        return EntityKey(self._pairs[0:-1])

    def pairs(self):
        return self._pairs

    def flat_pairs(self):
        flat_pairs = []
        for pair in self.pairs():
            flat_pairs.append(pair.kind)
            flat_pairs.append(pair.name)

        return flat_pairs

    def kind(self):
        return self._pairs[-1].kind

    def name(self):
        return self._pairs[-1].name

    def key_literal(self) -> str:
        return 'Key({})'.format(', '.join([
            pair.key_pair_literal() for pair in self.pairs()
        ]))

    def key_path(self) -> str:
        """
        Returns a structured key separated by `/`
        The kind and name are separated by `:`
        """
        pairs = []
        for pair in self.pairs():
            pairs.append(f'{pair.kind}:{pair.name}')
        return '/'.join(pairs)

    def key_url(self) -> str:
        """
        Returns a structured key separated by / between kind and name.
        This format is suitable for expressing in a form embedded in a URL.
        """
        return '/'.join([
            f'{pair.kind}/{pair.name}' for pair in self.pairs()
        ])

    def key_path_urlsafe(self) -> str:
        return self.key_path().replace('/', '%2F').replace(':', '%3A')


class EntityKeyFactory:
    def __init__(self):
        pass

    def build_from_pairs(self, pairs: List[Union[tuple, dict]]) -> EntityKey:
        _pairs = []
        for pair in pairs:
            if isinstance(pair, dict):
                key_pair = KeyPair(pair.get('kind'), pair.get('name'))
            elif isinstance(pair, tuple) or isinstance(pair, list):
                key_pair = KeyPair(pair[0], pair[1])
            else:
                raise ValueError(f'Unknown object type: {type(pair)}, got: {pair}')
            _pairs.append(key_pair)

        return EntityKey(_pairs)

    def build(self, kind: str, name: Union[str, int], parent: Optional[EntityKey] = None) -> EntityKey:
        if parent:
            pairs = copy.deepcopy(parent.pairs())
        else:
            pairs = []
        pairs.append(KeyPair(kind=kind, name=name))

        return EntityKey(pairs)

    def build_for_new(self, kind: str, parent: Optional[EntityKey] = None) -> EntityKey:
        name = self._generate_new_uuid()
        return self.build(kind=kind, name=name, parent=parent)

    def _generate_new_uuid(self) -> str:
        s = base64.b32encode(uuid.uuid4().bytes).decode('utf-8')
        return s.replace('======', '').lower()

    def build_from_key_path(self, key_path: str) -> EntityKey:
        pairs = []
        for pair in key_path.replace('%2F', '/').replace('%3A', ':').split('/'):
            kind, name = pair.split(':')
            pairs.append(KeyPair.build(kind=kind, name=name, implicit_id_str=True))

        return EntityKey(pairs)

    @staticmethod
    def _split_list(l, n):
        """
        list divided by n items.
        :param l: list
        :param n: item size of sub-list
        :return:
        """
        for idx in range(0, len(l), n):
            yield l[idx:idx + n]

    def build_from_key_url(self, key_url: str) -> EntityKey:
        pairs = []

        key_elements = key_url.replace('%2F', '/').split('/')
        key_pairs = list(self._split_list(key_elements, 2))

        for pair in key_pairs:
            kind, name = pair
            pairs.append(KeyPair.build(kind=kind, name=name, implicit_id_str=True))

        return EntityKey(pairs)
