# -*- coding: utf-8 -*-
"""Query the worldcat.org 'classify.oclc.org' service for metadata."""

import logging
import re

from isbnlib.dev import stdmeta
from isbnlib.dev._bouth23 import u
from isbnlib.dev.webquery import query as wquery

UA = 'isbnlib (gzip)'
SERVICE_URL = 'http://classify.oclc.org/classify2/Classify?isbn={isbn}'\
              '&maxRecs=1'
SERVICE_URL2 = 'http://www.worldcat.org/oclc/{oclc}'
LOGGER = logging.getLogger(__name__)

RE_FLDS = re.compile(r'\s([a-z]+)="', re.I | re.M | re.S)
RE_VALS = re.compile(r'="(.*?)"', re.I | re.M | re.S)
RE_WORK = re.compile(r'<work .*/>', re.I | re.M | re.S)
RE_EDIT = re.compile(r'<edition .*/>', re.I | re.M | re.S)
RE_PUB = re.compile(r'<textarea name="" id="util-em-note" .*/textarea>',
                    re.I | re.M | re.S)
RE_FP = re.compile(r'(Publisher):\s*', re.I | re.M | re.S)
RE_VP = re.compile(r'Publisher:\s*(.*?)\n', re.I | re.M | re.S)
RE_YEAR = re.compile(r'([0-2][0-9]{3})', re.I | re.M | re.S)


def _clean(txt):
    """Util function to clean Author strings."""
    # delete annotations
    txt = re.sub(r'\[.*\]', '', txt)
    txt = re.sub(r'\(.*\)', '', txt)
    txt = re.sub(r'[0-9]{4}\s*\-*[0-9]{0,4}', '', txt)
    # delete abbreviations
    txt.strip('. ')
    # std name
    txt.strip(', ')
    if ',' in txt:
        txt = ' '.join(x.strip() for x in txt.split(',')[::-1])
    return txt.strip()


def _mapper(isbn, records):
    """Mapp: canonical <- records."""
    # canonical: ISBN-13, Title, Authors, Publisher, Year, Language
    canonical = {}
    try:
        canonical['ISBN-13'] = u(isbn)
        canonical['Title'] = records.get('title', u('')).replace(' :', ':')
        buf = records.get('author', u(''))
        canonical['Authors'] = [_clean(x) for x in buf.split('|')]
        canonical['Publisher'] = records.get('publisher', u(''))
        canonical['Year'] = records.get('year', u(''))
        canonical['Language'] = records.get('lang', u(''))
    except IndexError:  # pragma: no cover
        LOGGER.debug("RecordMappingError for %s with data %s", isbn, records)
        return canonical
    # call stdmeta for extra cleanning and validation
    return stdmeta(canonical)


def _records(isbn, data):
    """Classify (canonically) the parsed data."""
    # check data
    if not data:  # pragma: no cover
        LOGGER.debug('NoDataForSelectorError for %s', isbn)
        return {}
    # map canonical <- records
    return _mapper(isbn, data)


def noparser(xmlthing):
    """Keep the raw response from the service."""
    return xmlthing


def parser_work(xmlthing):
    """RE parser for classify.oclc service (work branch)."""
    match = RE_WORK.search(u(xmlthing))
    if match:
        try:
            buf = match.group()
            flds = RE_FLDS.findall(buf)
            vals = RE_VALS.findall(buf)
            return dict(zip(flds, vals))
        except Exception:  # pragma: no cover
            pass
    return None


def parser_edit(xmlthing):
    """RE parser for classify.oclc service (edition branch)."""
    match = RE_EDIT.search(u(xmlthing))
    if match:
        try:
            buf = match.group()
            flds = RE_FLDS.findall(buf)
            vals = RE_VALS.findall(buf)
            return dict(zip(flds, vals))
        except Exception:  # pragma: no cover
            pass
    return None


def parser_pub(htmlthing):
    """RE parser for classify.oclc service (publisher and year)."""
    match = RE_PUB.search(u(htmlthing))
    if match:
        try:
            buf = match.group()
            flds = RE_FP.findall(buf)
            vals = RE_VP.findall(buf)
            return dict(zip(flds, vals))
        except Exception:  # pragma: no cover
            pass
    return None


def query(isbn):
    """Query the classify.oclc service for metadata."""
    xml = wquery(
        SERVICE_URL.format(isbn=isbn),
        user_agent=UA,
        data_checker=None,
        parser=noparser)
    if not xml or 'response code="102"' in xml:
        LOGGER.debug("The service 'oclc' is temporarily down!")
        return {}

    data = parser_edit(xml)
    if not data:
        LOGGER.debug("The parser 'edit' was unsucessful for %s!", isbn)
        data = parser_work(xml)
        if not data:  # pragma: no cover
            LOGGER.debug("The parser 'work' was unsucessful for %s!", isbn)
            return {}

        data['year'] = data.get('hyr', u('')) or data.get('lyr', u(''))
        return _records(isbn, data)

    # try to add more data...
    oclc = data.get('oclc', u(''))
    if oclc:
        data2 = wquery(
            SERVICE_URL2.format(oclc=oclc),
            user_agent=UA,
            data_checker=None,
            parser=parser_pub)
        if not data2:  # pragma: no cover
            LOGGER.debug("The parser 'pub' was unsucessful for %s!", isbn)
        else:
            buf = data2.get('Publisher', u('')).split(':')[1]
            publisher, year = buf.split(',')
            data['publisher'] = publisher.strip()
            data['year'] = RE_YEAR.search(year.strip('. ')).group(0)

    return _records(isbn, data)
