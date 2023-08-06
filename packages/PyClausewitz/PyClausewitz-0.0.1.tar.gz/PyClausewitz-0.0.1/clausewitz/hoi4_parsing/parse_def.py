from typing import Dict

from pyparsing import Regex, dblQuotedString, removeQuotes, Combine, Optional, Word, nums, ZeroOrMore, Suppress, \
    Forward, dictOf, pythonStyleComment, ParseResults


def string_to_int(toks: ParseResults) -> int:
    return int(toks[0])


def string_to_float(toks: ParseResults) -> float:
    return float(toks[0])


def string_to_bool(toks: ParseResults) -> bool:
    result_dict = {
        'yes': True,
        'no': False,
        'Yes': True,
        'No': False,
        'true': True,
        'false': False,
        'True': True,
        'False': False
    }  # type: Dict[str, bool]

    return result_dict[toks[0]]


Identifier = Regex(r"[^=\"\s{}]+")
String = dblQuotedString().addParseAction(removeQuotes)

Integer = Combine(Optional('-') + Word(nums))
Integer.addParseAction(string_to_int)

Boolean = Regex(r'yes|no')
Boolean.addParseAction(string_to_bool)

Float = Regex(r'-?\d+(\.\d*)')
Float.addParseAction(string_to_float)

Date = Combine(Word(nums) + '.' + Word(nums) + '.' + Word(nums))

Primitive = Date | Float | Integer | Boolean | String | Identifier

Header = Identifier

ProvinceKey = Combine('-' + Word(nums))

Dictionary = Forward()
EmptyDict = Forward()
List = ZeroOrMore(Primitive)
CurlyList = Suppress("{") + List + Suppress("}")
CurlyDict = Suppress("{") + Dictionary + Suppress("}")
EmptyCurly = Suppress("{") + Suppress("}")
OptionalEmptyCurlyBraces = Optional(Suppress("{") + Suppress("}"))

Key = Identifier + Suppress('=')
Value = (CurlyDict | CurlyList | Primitive) + OptionalEmptyCurlyBraces

Dictionary << dictOf(Key, Value)
comment = pythonStyleComment
Dictionary.ignore(comment)
