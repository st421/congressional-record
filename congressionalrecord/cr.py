from __future__ import absolute_import

import json
import os
from datetime import datetime, timedelta
from zipfile import ZipFile

from congressionalrecord.parsing.file_parser import ParseCRFile
from congressionalrecord.retriever import CRRetriever


class CRManager(object):
    DATE_FORMAT = "%Y-%m-%d"
    CR_PREFIX ="CREC-"

    def __init__(self, day, parser_class=None, retriever=None, **kwargs):
        if not retriever:
            retriever = CRRetriever()
        if not parser_class:
            parser_class = ParseCRFile
        if isinstance(day, str):
            day = datetime.strptime(day, self.DATE_FORMAT)
        
        self.retriever = retriever
        self.parser_class = parser_class
        self.day = day

    @property
    def filename(self):
        return self.build_filename(self.day)

    @classmethod
    def build_filename(cls, day, **kwargs):
        day_str = datetime.strftime(day,'%Y-%m-%d')
        return f"{cls.CR_PREFIX}.{day_str}"

    def __call__(self):
        raise NotImplementedError()


class LocalCRManager(CRManager):
    DEFAULT_SKIP_PARSING = ['-Pgnull', 'FrontMatter']

    def __init__(self, day, *args, output_dir="output", skip_parsing_for=None, output_format=None, **kwargs):
        super().__init__(day, *args, **kwargs)
        self.output_path = os.path.join(output_dir, self.filename)
        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)
        if not skip_parsing_for:
            skip_parsing_for = self.DEFAULT_SKIP_PARSING
        self.skip_parsing_for = skip_parsing_for
        self.output_format = output_format

    def __call__(self):
        cr_data = self.retriever.get_cr(self.filename)
        self.save(self.output_path, cr_data)
        self.extract(self.output_path)
        self.parse()

    @property
    def unextracted(self):
        return os.path.join(self.output_path, ".zip")

    def save(self, cr_data, **kwargs):
        with open(self.unextracted, 'wb') as outfile:
            outfile.write(cr_data)
            return outfile

    def get_mods(self, **kwargs):
        ''' Load up all metadata for this directory
         from the mods file.'''
        mods_path = os.path.join(self.output_path, 'mods.xml')
        with open(mods_path, 'r') as mods_file:
            return BeautifulSoup(mods_file, "lxml")

    def parse(self, **kwargs):
        for html_file in os.listdir(os.path.join(self.output_path, 'html')):
            parse_path = os.path.join(self.output_path, 'html', html_file)
            for skip_str in self.skip_parsing_for:
                if skip_str in parse_path:
                    continue
                else:
                    crfile = ParseCRFile(parse_path, crdir)
                    yield crfile

    def extract(self, delete_unextracted=True, **kwargs):
        with ZipFile(self.unextracted, 'r') as the_zip:
            the_zip.extractall()
        if self.output_format:
            subfolder = os.path.join(self.output_path, self.output_format)
            if not os.path.isdir(subfolder):
                os.makedirs(subfolder)
        if delete_unextracted:
            os.remove(self.unextracted)


class LocalJsonCRManager(LocalCRManager):

    def __init__(self, day, *args, **kwargs):
        super().__init__(day, *args, output_format="json", **kwargs)

    def parse(self, **kwargs):
        for crfile in super().parse():
            with open(os.path.join(self.output_path, self.output_format, crfile.filepath), 'w') as out_json:
                json.dump(crfile.crdoc, out_json)


def get_and_parse_cr(self, start_day, end_day=None, **kwargs):
    start = datetime.strptime(start_day, self.DATE_FORMAT)
    if end_day:
        end = datetime.strptime(end_day, self.DATE_FORMAT)
    else:
        end = start
    current = start
    while current <= end:
        cr_manager = CRManager(current)
        cr_manager()
        current += timedelta(days=1)
