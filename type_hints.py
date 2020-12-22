"""
Примеры использования type hinting
Хинты доступны с python 3.5, но некоторые виды синтаксиса появлялись позже
"""
import random
from typing import List, Dict, Union, Any, Set, Tuple, TypeVar, Type, \
    NamedTuple, Generic


# Аргументы
def fn1(arg1: bool, arg2: str, arg3: int, arg4: float):
    pass


# Возвращаемое значение
def fn2() -> bool:
    return True


# Переменные (с python 3.6)
a: int = 2
b: bool = True


# Аттрибуты класса (с python 3.6)
class C1:
    a: int           # Это - type hint для будущего аттрибута инстанса
    b: bool = True   # А это - type hint для уже существующего аттрибута класса


# Сумма типов - union (значение может быть одним из перечисленных)
def fn3(arg1: bool) -> Union[str, int]:
    if arg1:
        return 'aaa'
    else:
        return 123


# Разные дженерики (параметризируемые типы) из модуля typing
d1: Dict[str, int] = {'a': 1, 'b': 2}
l1: List[str] = ['a', 'b']
s1: Set[str] = {'a', 'b'}
t1: Tuple[str, int, float] = ('a', 1, 3.0)


# Any - любой тип, по отдельности работает как отсутствие type hint,
# но можно использовать его как аргумент дженериков
def fn4(d: Dict[str, Any]) -> Any:
    return random.choice(list(d.values()))


# Сложные типы можно описывать и как простые
d2: dict = {1: 2}    # синоним Dict[Any, Any]
d3: list = [3, 'a']  # синоним List[Any]


# Длинные описания типов можно класть в переменные, причём UpperCamelCase
# им в самый раз
TSubconfig1 = Tuple[str, int, int, float]
TSubconfig2 = Dict[str, int]
TSubconfig3 = Dict[str, TSubconfig1]
TMyConfig = Dict[str, Union[TSubconfig2, TSubconfig3]]
complex1: TMyConfig = {
    'sub_conf2_1': {'str1': 123},
    'sub_conf2_2': {'str2': 456},
    'sub_conf3_1': {
        'sub_conf1_1': ('a', 1, 2, 1.0),
        'sub_conf1_2': ('z', 4, 5, 3.0),
    },
}
# NB: это хорошо подходит, если ключей каждого подтипа в словаре может быть
# 0 или более. Если набор ключей всегда одинаковый, лучше использовать
# namedtuple(), тем более в typing есть его брат: NamedTuple


# NamedTuple, аналог collections.NamedTuple, но типизированный
class MyTuple(NamedTuple):
    d: Dict[str, int]
    l: List[str]
    a: int
    s: str


t = MyTuple(d={'a': 1}, l=['a', 'b'], a=1, s='abcde')


# TypeVar - нужен для создания дженериков. Аналог дженерик-аргумента во многих
# статически типизированных языках
T = TypeVar('T')
U = TypeVar('U')


# Простой дженерик-метод
#
# Проверка типов ругнётся, если сделать, например, так:
# l1: List[str] = ['a']
# a1: int = fn_t(l)
#
# Хорошее IDE подскажет методы str, если написать
# fn_t(['a']).
def fn_t(arg1: List[T]) -> T:
    return random.choice(arg1)


# Дженерик фабричный метод, использует typing.Type
# Передаём аргументом класс, на выходе получаем инстанс
def fn_t_generic(arg1: Type[T]) -> T:
    return arg1()


# Дженерик класс.
# Те переменные, которые являются его generic-аргументами, можно использовать
# примерно везде в теле объекта (но только как type hints)
# На те, которые дженерик-аргументом в данном контексте не являются,
# ругнётся линтер
class GenericClass1(Generic[T, U]):
    """ Дженерик-класс с двумя аргументами типа """
    a1: T
    a2: U

    def __init__(self, a1: T, a2: U):
        self.a1 = a1
        self.a2 = a2

    def get_a1(self) -> T:
        return self.a1

    def get_a2(self) -> U:
        return self.a2

    def set_a1_from_dict(self, arg1: Dict[str, T], key: str):
        self.a1 = arg1[key]

    def get_a1_or_a2(self, a1: bool) -> Union[T, U]:
        val: Union[T, U]
        if a1:
            val = self.a1
        else:
            val = self.a2
        return val


class GenericClass1StrInt(GenericClass1[str, int]):
    """ Сабкласс от дженерика, определивший аргументы типа как str и int"""
    def get_typed_a1(self) -> str:
        return self.get_a1()

    def get_typed_a2(self) -> int:
        return self.get_a2()


generic_subclass_instance = GenericClass1StrInt('abcd', 1234)
generic_inline_instance = GenericClass1[float, str](1.0, 'abcd')


class PartialGenericClass1SubclassBool(GenericClass1[bool, U]):
    """
    Частичный сабкласс от дженерика, определивший первый аргумент как bool.
    Сам является дженериком со одним аргументом (U исходного класса)
    """
    def get_typed_a1(self) -> bool:
        return self.get_a1()


class CompleteGenericClass1SubclassBoolStr(PartialGenericClass1SubclassBool[str]):
    """ Доопределение второго дженерик-аргумента """
    def get_typed_a2(self) -> str:
        return self.get_a2()
