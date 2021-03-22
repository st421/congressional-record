import re
from html2ans.parsers.base import BaseElementParser, ParseResult


class TableRowParser(BaseElementParser):
    applicable_elements = ['tr']
    cr_volume_regex = r'^\[Congressional Record Volume (?P<vol>[0-9]+), Number (?P<num>[0-9]+)'\
        + r' \((?P<wkday>[A-Za-z]+), (?P<month>[A-Za-z]+) (?P<day>[0-9]+), (?P<year>[0-9]{4})\)\]'

    def construct_output(self, element, *args, **kwargs):
        result = {}
        for link in element.find_all('a'):
            print(link)
            if link.text == "PDF":
                link_parts = link.attrs.get('href').split("/")
                _id = link_parts[-1]
                result["id"] = _id.replace(".pdf", "")
            else:
                link_text_parts = link.text.split(";")
                #regex_output = re.match(self.cr_volume_regex, )
                result["label"] = link_text_parts[0]
                result["link"] = link.attrs.get('href')
            if "id" in result and "label" in result:
                return result
        return result

    def parse(self, element, *args, **kwargs):
        return ParseResult(self.construct_output(element), True)
