from collections import defaultdict
from functools import partial
from xml.parsers.expat import ParserCreate

from .base import Codec, use_if_format_is


@use_if_format_is("svg")
@use_if_format_is("xml")
class XML(Codec):
    """ Codec to parse a raw XML string into a nested dict of elements by each attribute.
        EXAMPLE: to find the ID of the second element with a class of "small", use d["class"]["small"][1]["id"]. """

    def decode(self, contents:bytes, **kwargs) -> dict:
        """ Return a list of attribute dicts for each category of element along with the raw XML byte string. """
        d = defaultdict(partial(defaultdict, list), self.default(contents))
        def start_element(name:str, attrs:dict, d=d, list_append=list.append) -> None:
            attrs["name"] = name
            for k in attrs:
                list_append(d[k][attrs[k]], attrs)
        p = ParserCreate(**kwargs)
        p.StartElementHandler = start_element
        p.Parse(contents.decode('utf-8'))
        return d

    def default(self, contents:bytes=b"") -> dict:
        """ By default, the bytes are not decoded at all, just wrapped in a dict. """
        return {"raw": contents}
