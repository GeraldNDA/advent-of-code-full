from typing import Callable, TypeVar, Tuple, List, Generic, Optional

Text = List[str]  # list of characters
T = TypeVar("T")
U = TypeVar("U")

class Parser(Generic[T]):
    func: Callable[[Text], T]

    def __init__(self, func: Callable[[Text], T]) -> None:
        self.func = func

    def parse(self, text: Text) -> T:
        "Actually run the parser."
        return self.func(text)

    def bind(self, f: Callable[[T], "Parser[U]"]) -> "Parser[U]":
        return Parser(lambda s: f(self.parse(s)).parse(s))

    @classmethod
    def pure(cls, v: U) -> "Parser[U]":
        return cls(lambda s: v)


class ListWrapper(Generic[T]):
    l: List[T]

    def __init__(self, l: List[T]) -> None:
        self.l = l

    def bind(self, f: Callable[[T], "ListWrapper[U]"]) -> "ListWrapper[U]":
        return ListWrapper([u for t in self.l for u in f(t).l])

    @classmethod
    def pure(cls, v: U) -> "ListWrapper[U]":
        return cls([v])

    def __repr__(self) -> str:
        return "ListWrapper({})".format(self.l)


class Maybe(Generic[T]):
    # value is either T, or None
    value: Optional[T]

    def __init__(self, value: Optional[T]) -> None:
        self.value = value

    def bind(self, f: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        if self.value is None:
            return Maybe(None)
        return f(self.value)

    @classmethod
    def pure(cls, v: U) -> "Maybe[U]":
        return cls(v)

    def __repr__(self) -> str:
        return "Maybe({})".format(self.value)



def replicateM(times, thing):
    if times == 0:
        return type(thing).pure(())
    else:
        return thing.bind(lambda val:
            replicateM(times - 1, thing).bind(lambda rest_of_list:
                type(thing).pure((val,) + rest_of_list)
            )
        )
do_twice = lambda m: replicateM(2, m)
do_thrice = lambda m: replicateM(3, m)
do_four_times= lambda m: replicateM(4, m)

parse_char = Parser(lambda x: x.pop(0))
l = ["a", "b", "c", "d", "e"]
parse_result = do_twice(parse_char).parse(l)
print(parse_result, l)  # ['a', 'b', 'c'] ['d', 'e']

my_numbers = ListWrapper([1, 2, 3])
cartesian_product_with_self = do_thrice(my_numbers)
print(cartesian_product_with_self)  # ListWrapper([(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)])


possibly_none_value = Maybe("yay!")
pair_of_above = do_four_times(possibly_none_value)
print(pair_of_above)  # Maybe(("yay!", "yay!"))

possibly_none_value = Maybe(None)
pair_of_above = do_four_times(possibly_none_value)
print(pair_of_above) # Maybe(None) - not Maybe((None, None))!