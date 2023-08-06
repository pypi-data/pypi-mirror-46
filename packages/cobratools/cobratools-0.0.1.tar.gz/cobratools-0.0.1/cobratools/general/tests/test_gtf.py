# -*- coding: utf-8 -*-
"""
Tests for GFF/GFT format parsing
"""

from cobratools.general.models.gtf import GtfLine


def test_parse_additional():
    """
    Test parsing of additional annotations
    :return:
    """
    s = 'gene_id "ENSMUSG00000102693.1"; ' \
        'transcript_id "ENSMUST00000193812.1"; gene_type "TEC"; ' \
        'gene_name "RP23-271O17.1"; transcript_type "TEC"; ' \
        'transcript_name "RP23-271O17.1-001"; exon_number 1; ' \
        'exon_id "ENSMUSE00001343744.1"; level 2; ' \
        'transcript_support_level "NA"; tag "basic"; ' \
        'havana_gene "OTTMUSG00000049935.1"; ' \
        'havana_transcript "OTTMUST00000127109.1";'
    # pylint: disable=W0212
    d = GtfLine._addl2dict(s)
    assert d['gene_id'] == "ENSMUSG00000102693.1"
    assert d['transcript_id'] == "ENSMUST00000193812.1"
    assert d['gene_type'] == "TEC"
    assert d['gene_name'] == "RP23-271O17.1"
    assert d['transcript_type'] == "TEC"
    assert d['transcript_name'] == "RP23-271O17.1-001"
    assert d['exon_number'] == 1
    assert d['exon_id'] == "ENSMUSE00001343744.1"
    assert d['level'] == 2
    assert d['transcript_support_level'] == "NA"
    assert d['tag'] == "basic"
    assert d['havana_gene'] == "OTTMUSG00000049935.1"
    assert d['havana_transcript'] == "OTTMUST00000127109.1"
