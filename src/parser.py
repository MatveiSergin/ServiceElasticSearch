from typing import Protocol

import lxml.etree as ET

class XmlParserProtocol(Protocol):
    def parse_xml(self, tag: str = None) -> dict:
        pass


class XmlParser:
    def __init__(self, path: str):
        self.path = path

    def parse_xml(self, tag: str = None) -> dict:
        data = ET.iterparse(self.path, events=('end',), tag=tag)
        for event, elem in data:
            child_data = {}

            for e in elem:
                child_data[e.tag] = e.text


            result = child_data | dict(elem.attrib) | {tag: elem.text}
            yield result
            elem.clear()