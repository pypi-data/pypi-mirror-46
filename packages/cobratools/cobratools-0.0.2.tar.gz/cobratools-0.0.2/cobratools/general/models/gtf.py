# -*- coding] = utf-8 -*-
"""
Parser and stuff for GENCODE annotation data. Not a general-purpose class for
any and all GTFs

##description: evidence-based annotation of the mouse genome (GRCm38),
    version M17 (Ensembl 92)
##provider: GENCODE
##contact: gencode-help@ebi.ac.uk
##format: gtf
##date: 2018-03-22
chr1	HAVANA	gene	3073253	3074322	.	+	.
    gene_id "ENSMUSG00000102693.1"; gene_type "TEC"; gene_name "RP23-271O17.1";
    level 2; havana_gene "OTTMUSG00000049935.1";
chr1	HAVANA	transcript	3073253	3074322	.	+	.
    gene_id "ENSMUSG00000102693.1"; transcript_id "ENSMUST00000193812.1";
    gene_type "TEC"; gene_name "RP23-271O17.1"; transcript_type "TEC";
    transcript_name "RP23-271O17.1-001"; level 2;
    transcript_support_level "NA";
    tag "basic"; havana_gene "OTTMUSG00000049935.1";
    havana_transcript "OTTMUST00000127109.1";
chr1	HAVANA	exon	3073253	3074322	.	+	.
    gene_id "ENSMUSG00000102693.1"; transcript_id "ENSMUST00000193812.1";
    gene_type "TEC"; gene_name "RP23-271O17.1"; transcript_type "TEC";
    transcript_name "RP23-271O17.1-001"; exon_number 1;
    exon_id "ENSMUSE00001343744.1"; level 2; transcript_support_level "NA";
    tag "basic"; havana_gene "OTTMUSG00000049935.1";
    havana_transcript "OTTMUST00000127109.1";

column-number	content	values/format
1	chromosome name	chr{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
        20,21,22,X,Y,M} or GRC accession a
2	annotation source	{ENSEMBL,HAVANA}
3	feature type	{gene, transcript, exon, CDS, UTR, start_codon,
        stop_codon, Selenocysteine}
4	genomic start location	integer-value (1-based)
5	genomic end location	integer-value
6	score(not used)	.
7	genomic strand	{+,-}
8	genomic phase (for CDS features)	{0,1,2,.}
9	additional information as key-value pairs	see below

gene_id	all	ENSGXXXXXXXXXXX.X b,c _Xg	all
transcript_id d	all except gene	ENSTXXXXXXXXXXX.X b,c _Xg	all
gene_type	all	list of biotypes	all
gene_status e	all	{KNOWN, NOVEL, PUTATIVE}	until 25 and M11
gene_name	all	string	all
transcript_type d	all except gene	list of biotypes	all
transcript_statusd,e	all except gene	{KNOWN, NOVEL, PUTATIVE}
    until 25 and M11
transcript_name d	all except gene	string	all
exon_number f	all except gene/transcript/Selenocysteine
    integer (exon position in the transcript from its 5' end)	all
exon_id f	all except gene/transcript/Selenocysteine
    ENSEXXXXXXXXXXX.X b _Xg	all
level	all	1 (verified loci),
2 (manually annotated loci),
3 (automatically annotated loci)

For list of biotypes, see: https://www.gencodegenes.org/pages/biotypes.html
"""

import re
from typing import Dict


class Error(Exception):
    """
    Base class for exceptions in this module.
    """


class InvalidDataError(Error):
    """
    Invalid data error
    """


# pylint: disable=R0902
class GtfLine:
    """
    GTF line will look something like this:

    chr1	ENSEMBL	gene	3102016	3102125	.	+	.	...
        ...gene_id "ENSMUSG00000064842.1"; gene_type "snRNA"; ...
        ... gene_name "Gm26206"; level 3;

    Here we make an object of it.
    """

    def __init__(self, s: str):
        """
        Init
        :param s: str
        """
        tokens = s.split('\t')
        if len(tokens) != 9:
            raise InvalidDataError("Invalid data")
        self.chrom = tokens[0]
        self.source = tokens[1]
        self.feature_type = tokens[2]
        self.start = int(tokens[3])
        self.end = int(tokens[4])
        self.score = tokens[5]  # Not used. Expect "."
        self.strand = tokens[6]
        self.phase = tokens[7]
        self.additional = self._addl2dict(tokens[8])

    @staticmethod
    def _addl2dict(s: str) -> Dict:
        """
        Parse additional attributes string to dict, with a nod to Mark Meyers
        :param s: str
        :return: dict
        """
        pairs = re.findall(r'(\S+?) (.+?);', s)
        d = {}
        for k, v in pairs:
            if v.isdigit():
                v = int(v)
            else:
                v = v.strip('"')
            d[k] = v
        return d

    @staticmethod
    def is_number(s: str) -> bool:
        """
        Is this a string representation of an int or float?
        :param s: str
        :return: bool
        """
        try:
            int(s)
            return True
        except ValueError:
            try:
                float(s)
                return True
            except ValueError:
                return False

    def __str__(self) -> str:
        """
        Convert object to string
        :return: str
        """
        lst = [self.chrom, self.source, self.feature_type,
               str(self.start), str(self.end), str(self.score),
               self.strand, self.phase]
        addl = []
        for key, value in self.additional.items():
            if isinstance(value, (int, float)):
                addl.append(key + " " + str(value))
            elif self.is_number(value):
                addl.append(key + " " + value)
            else:
                addl.append(key + ' "' + value + '"')
        if addl:
            lst.append("; ".join(addl) + ";")
        return '\t'.join(lst)


if __name__ == '__main__':
    GTF_LINE = GtfLine('chr1	ENSEMBL	gene	3102016	3102125	.	+	.	'
                       'gene_id "ENSMUSG00000064842.1"; gene_type "snRNA"; '
                       'gene_name "Gm26206"; level 3;')
    print(GTF_LINE.chrom)
    print(GTF_LINE.feature_type)
    print(int(GTF_LINE.start))
    print(int(GTF_LINE.end))
    print(GTF_LINE.strand)
    print(GTF_LINE.additional)
