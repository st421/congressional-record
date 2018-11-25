    # Flow control for metadata generation
    def gen_file_metadata(self):
        # Sometimes the searchtitle has semicolons in it so .split(';') is a nogo
        temp_ref = self.cr_dir.mods.find('accessid', text=self.access_path)
        if temp_ref is None:
            raise RuntimeError(
                "{} doesn't have accessid tag".format(self.access_path))
        self.doc_ref = temp_ref.parent
        matchobj = re.match(self.re_vol, self.doc_ref.searchtitle.string)
        if matchobj:
            self.doc_title, self.cr_vol, self.cr_num = matchobj.group(
                'title', 'vol', 'num')
        else:
            logging.warning('{0} yields no title, vol, num'.format(
                self.access_path))
            self.doc_title, self.cr_vol, self.cr_num = \
                'None', 'Unknown', 'Unknown'
        self.find_people()
        self.find_related_bills()
        self.find_related_laws()
        self.find_related_usc()
        self.find_related_statute()
        self.date_from_entry()
        self.chamber = self.doc_ref.granuleclass.string
        self.re_newspeaker = self.make_re_newspeaker()
        self.item_types['speech']['patterns'] = [self.re_newspeaker]