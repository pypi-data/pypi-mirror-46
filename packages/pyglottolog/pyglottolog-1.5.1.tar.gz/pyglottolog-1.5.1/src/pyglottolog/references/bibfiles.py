# bibfiles.py - ordered collection of bibfiles with load/save api

from __future__ import unicode_literals, print_function

import re
import collections
import unicodedata
import datetime

from six import string_types

import attr

from clldutils.misc import UnicodeMixin
from clldutils.path import memorymapped, Path
from clldutils.source import Source
from clldutils.text import split_text
from clldutils.inifile import INI

from . import bibtex
from .bibfiles_db import Database

__all__ = ['BibFiles', 'BibFile', 'Entry']

BIBFILES = 'bibfiles.sqlite3'


class BibFiles(list):
    """Ordered collection of `BibFile` objects accessible by filname or index."""

    @classmethod
    def from_path(cls, path):
        """BibTeX files from `<path>/bibtex/*.bib` if listed in `<path>/BIBFILES.ini`."""
        if not isinstance(path, Path):
            path = Path(path)
        ini = INI.from_file(path / 'BIBFILES.ini', interpolation=None)
        return cls(cls._iterbibfiles(ini, path / 'bibtex'))

    @staticmethod
    def _iterbibfiles(ini, bibtex_path):
        for sec in ini.sections():
            if sec.endswith('.bib'):
                fpath = bibtex_path / sec
                if not fpath.exists():  # pragma: no cover
                    raise ValueError('invalid bibtex file referenced in BIBFILES.ini')
                yield BibFile(fname=fpath, **ini[sec])

    def __init__(self, bibfiles):
        super(BibFiles, self).__init__(bibfiles)
        self._map = {b.fname.name: b for b in self}

    def __getitem__(self, index_or_filename):
        """Retrieve a bibfile by index or filename."""
        if isinstance(index_or_filename, string_types):
            return self._map[index_or_filename]
        return super(BibFiles, self).__getitem__(index_or_filename)

    def to_sqlite(self, filepath=BIBFILES, rebuild=False):
        """Return a database with the bibfiles loaded."""
        return Database.from_bibfiles(self, filepath, rebuild=rebuild)

    def roundtrip_all(self):
        """Load and save all bibfiles with the current settings."""
        return [b.roundtrip() for b in self]


def file_if_exists(i, a, value):
    if value.exists() and not value.is_file():
        raise ValueError('invalid path')  # pragma: no cover


@attr.s
class BibFile(UnicodeMixin):

    fname = attr.ib(validator=file_if_exists)
    name = attr.ib(default=None)
    title = attr.ib(default=None)
    description = attr.ib(default=None)
    abbr = attr.ib(default=None)
    encoding = attr.ib(default='utf-8')
    normalize = attr.ib(default='NFC')
    sortkey = attr.ib(
        default=None,
        converter=lambda s: None if s is None or s.lower() == 'none' else s)
    priority = attr.ib(default=0, converter=int)
    url = attr.ib(default=None)

    @property
    def id(self):
        return self.fname.stem

    def __getitem__(self, item):
        if item.startswith(self.id + ':'):
            item = item.split(':', 1)[1]
        text = None
        with memorymapped(self.fname) as string:
            m = re.search(b'@[A-Za-z]+\{' + re.escape(item.encode(self.encoding)), string)
            if m:
                next = string.find(b'\n@', m.end())
                if next >= 0:
                    text = string[m.start():next]
                else:
                    text = string[m.start():]
        if text:
            for k, (t, f) in bibtex.iterentries_from_text(text, encoding=self.encoding):
                return Entry(k, t, f, self)
        raise KeyError(item)

    def visit(self, visitor=None):
        entries = collections.OrderedDict()
        for entry in self.iterentries():
            if visitor is None or visitor(entry) is not True:
                entries[entry.key] = (entry.type, entry.fields)
        self.save(entries)

    @property
    def size(self):
        return self.fname.stat().st_size

    @property
    def mtime(self):
        return datetime.datetime.fromtimestamp(self.fname.stat().st_mtime)

    def iterentries(self):
        for k, (t, f) in bibtex.iterentries(filename=self.fname, encoding=self.encoding):
            yield Entry(k, t, f, self)

    def keys(self):
        return ['{0}:{1}'.format(self.id, e.key) for e in self.iterentries()]

    @property
    def glottolog_ref_id_map(self):
        return {
            e.key: e.fields['glottolog_ref_id'] for e in self.iterentries()
            if 'glottolog_ref_id' in e.fields}

    def update(self, fname, log=None):
        entries, new = collections.OrderedDict(), 0
        ref_id_map = self.glottolog_ref_id_map
        for key, (type_, fields) in bibtex.iterentries(fname, self.encoding):
            if key in ref_id_map and 'glottolog_ref_id' not in fields:
                fields['glottolog_ref_id'] = ref_id_map[key]
            else:
                new += 1
            entries[key] = (type_, fields)
        self.save(entries)
        if log:
            log.info('{0} new entries'.format(new))

    def load(self, preserve_order=None):
        """Return entries as bibkey -> (entrytype, fields) dict."""
        if preserve_order is None:
            preserve_order = self.sortkey is None
        return bibtex.load(self.fname, preserve_order, encoding=self.encoding)

    def save(self, entries):
        """Write bibkey -> (entrytype, fields) map to file."""
        bibtex.save(
            entries,
            filename=self.fname,
            sortkey=self.sortkey,
            encoding=self.encoding,
            normalize=self.normalize)

    def __unicode__(self):
        return '<%s %s>' % (self.__class__.__name__, self.fname.name)

    def check(self, log):
        entries = self.load()  # bare BibTeX syntax
        invalid = bibtex.check(filename=self.fname)  # names/macros etc.
        verdict = ('(%d invalid)' % invalid) if invalid else 'OK'
        method = log.warn if invalid else log.info
        method('%s %d %s' % (self, len(entries), verdict))
        return len(entries), verdict

    def roundtrip(self):
        print(self)
        self.save(self.load())

    def show_characters(self, include_plain=False):
        """Display character-frequencies (excluding printable ASCII)."""
        with self.fname.open(encoding=self.encoding) as fd:
            text = fd.read()
        hist = collections.Counter(text)
        table = '\n'.join(
            '%d\t%-9r\t%s\t%s' % (n, c, c, unicodedata.name(c, ''))
            for c, n in hist.most_common()
            if include_plain or not 20 <= ord(c) <= 126)
        print(table)


@attr.s
class Entry(UnicodeMixin):

    key = attr.ib()
    type = attr.ib()
    fields = attr.ib()
    bib = attr.ib()

    # FIXME: add method to apply triggers!

    lgcode_regex = '[a-z0-9]{4}[0-9]{4}|[a-z]{3}|NOCODE_[A-Z][^\s\]]+'
    lgcode_in_brackets_pattern = re.compile("\[(" + lgcode_regex + ")\]")
    recomma = re.compile("[,/]\s?")
    lgcode_pattern = re.compile(lgcode_regex + "$")

    def __unicode__(self):
        """
        :return: BibTeX representation of the entry.
        """
        res = "@%s{%s" % (self.type, self.key)
        for k, v in bibtex.fieldorder.itersorted(self.fields):
            res += ',\n    %s = {%s}' % (k, v.strip() if hasattr(v, 'strip') else v)
        res += '\n}\n' if self.fields else ',\n}\n'
        return res

    def text(self):
        """
        :return: Text linearization of the entry.
        """
        return Source(self.type, self.key, _check_id=False, **self.fields).text()

    @property
    def id(self):
        return '{0}:{1}'.format(self.bib.id, self.key)

    @classmethod
    def lgcodes(cls, string):
        if string is None:
            return []
        codes = cls.lgcode_in_brackets_pattern.findall(string)
        if not codes:
            # ... or as comma separated list of identifiers.
            parts = [p.strip() for p in cls.recomma.split(string)]
            codes = [p for p in parts if cls.lgcode_pattern.match(p)]
            if len(codes) != len(parts):
                codes = []
        return codes

    @staticmethod
    def parse_ca(s):
        if s:
            match = re.search('computerized assignment from "(?P<trigger>[^\"]+)"', s)
            if match:
                return match.group('trigger')

    def languoids(self, langs_by_codes):
        res = []
        if 'lgcode' in self.fields:
            for code in self.lgcodes(self.fields['lgcode']):
                if code in langs_by_codes:
                    res.append(langs_by_codes[code])
        return res, self.parse_ca(self.fields.get('lgcode'))

    def doctypes(self, hhtypes):
        res = []
        if 'hhtype' in self.fields:
            for ss in split_text(self.fields['hhtype'], separators=',;'):
                ss = ss.split('(')[0].strip()
                if ss in hhtypes:
                    res.append(hhtypes[ss])
        return res, self.parse_ca(self.fields.get('hhtype'))
