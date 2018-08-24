from enum import Enum, EnumMeta


class CustomEnumMeta(EnumMeta):
    def __getitem__(self, arg):
        for a, b in self._member_map_.items():
            if b.value[0] == arg:
                return b.value[1]
        return super(CustomEnumMeta, self).__getitem__(arg)


class Enum(Enum):
    __metaclass__ = CustomEnumMeta

    def __init__(self, code, display_name=''):
        self.code = code
        self.display_name = display_name

    def __eq__(self, other):
        if not other:
            return False
        return self.code == other.code if type(other) == self.__class__ else self.code == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __int__(self):
        if type(self.code) is not int:
            raise ValueError('Code attribute is not a int.')

        return self.code

    def __unicode__(self):
        return self.display_name if self.display_name else self.code

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def choices(cls, key='code', value='display_name'):
        return tuple([(getattr(b, key), getattr(b, value)) for a, b in cls.__members__.items()])

    @classmethod
    def list(cls, attr='code'):
        """
        Make a list with attr attribute values
        """
        return cls.to_list(cls.__members__.items(), attr)

    @classmethod
    def list_from_set(cls, set_, attr='code'):
        """
        Make a list with attr attribute values
        """
        return [getattr(b, attr) for a, b in set_]

    @classmethod
    def get(cls, **kwargs):
        for chave, enum in cls._member_map_.items():
            for arg, val in kwargs.iteritems():
                if hasattr(enum, arg) and getattr(enum, arg) == val:
                    return enum
