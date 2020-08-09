import os
from congressionalrecord.parsing.sections import SectionParser


class DocParser(object):

    def __init__(self, cr_file, body_parser=None, *args, **kwargs):
        self.doc_id = os.path.basename(cr_file.name.split(".htm")[0])
        self.in_data = cr_file.read()
        if not body_parser:
            body_parser = SectionParser()
        self.body_parser = body_parser

    def parse(self, *args, **kwargs):
        output = {
            "id": self.doc_id,
        }
        parsed_body = self.body_parser.generate_ans(self.in_data, start_tag="pre")
        parsed_content = []
        for parsed_item in parsed_body:
            if parsed_item.get("type") == "top-level":
                parsed_item.pop("type")
                output.update(parsed_item)
            else:
                parsed_content.append(parsed_item)
        output["content"] = parsed_content
        return output


'''
    def get_header(self):
        """
        Only after I wrote this did I realize
        how bad things can go when you call
        next() on an iterator instead of treating
        it as a list.

        This code works, though.
        """
        header_in = next(self.the_text)
        if header_in == u'':
            header_in = next(self.the_text)
        match = re.match(self.re_vol_file, header_in)
        if match:
            vol, num, wkday, month, day, year = match.group(
                'vol', 'num', 'wkday', 'month', 'day', 'year')
        else:
            return False
        header_in = next(self.the_text)
        match = re.match(self.re_chamber, header_in)
        if match:
            if match.group('chamber') == 'Extensions of Remarks':
                chamber = 'House'
                extensions = True
            else:
                chamber = match.group('chamber')
                extensions = False
        else:
            return False
        header_in = next(self.the_text)
        match = re.match(self.re_pages, header_in)
        if match:
            pages = match.group('pages')
        else:
            return False
        header_in = next(self.the_text)
        match = re.match(self.re_trail, header_in)
        if match:
            pass
        else:
            return False
        return vol, num, wkday, month, day, year, chamber, pages, extensions

    def write_header(self):
        self.crdoc['id'] = self.access_path
        header = self.get_header()
        if header:
            self.crdoc['header'] = {'vol': header[0], 'num': header[1],
                                    'wkday': header[2], 'month': header[3], 'day': header[4],
                                    'year': header[5], 'chamber': header[6], 'pages': header[7],
                                    'extension': header[8]}
        self.crdoc['doc_title'] = self.doc_title
'''
