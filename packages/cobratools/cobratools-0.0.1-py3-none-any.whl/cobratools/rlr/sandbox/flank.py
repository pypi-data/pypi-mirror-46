# -*- coding: utf-8 -*-
"""
Add flanking regions to MSA in FASTA format

>mm10.chr3 3984870 100 - 160039680
                    ACAAGCUGUAUAUAUUUGGAGCCUUCUAUUCAUUGGAGGC
                    UCCAGUCUGUGAACAAUCUGAGAUGGAGAUUGUCUUAAAG
                    ACUUUAUACUGAAAAGAAAU <-- distilled FASTA
                    ACAAGCUGUAUAUAUUUGGAGCCUUCUAUUCAUUGGAGGC
                    UCCAGUCUGUGAACAAUCUGAGAUGGAGAUUGUCUUAAAG
                    ACUUUAUACUGAAAAGAAAU <-- degapped RNAz output
                    AAAUUUAUAUUUGUACAAAC <-- upstream flank
                    ACAAGCUGUAUAUAUUUGGAGCCUUCUAUUCAUUGGAGGC
                    UCCAGUCUGUGAACAAUCUGAGAUGGAGAUUGUCUUAAAG
                    ACUUUAUACUGAAAAGAAAU
                    AUAUCUUUUCCAUCUAGAUU <-- downstream flank
"""
import glob
import os
import sys
from pathlib import Path

# pylint: disable=E0401
from Bio import SeqIO
# pylint: disable=E0401
from Bio.Alphabet.IUPAC import IUPACAmbiguousRNA
# pylint: disable=E0401
from Bio.Seq import Seq
# pylint: disable=E0401
from Bio.SeqRecord import SeqRecord
from general.models.btools import Bedtools

OUT_DIR = './output/temp/'
NUM_FLANK_NTS = 20


def flank(sr):
    """
    end = str(start + length + NUM_FLANK_NTS)
    start = str(start - NUM_FLANK_NTS)

    :param sr:
    :return:
    """
    species = sr.id.split('.')[0]
    chrom = sr.id.split('.')[1]
    d_tokens = sr.description.split()
    start = int(d_tokens[1]) - NUM_FLANK_NTS
    size = int(d_tokens[2]) + 2 * NUM_FLANK_NTS
    end = start + size
    strand = d_tokens[3]
    src_size = int(d_tokens[4])
    assert start + size <= src_size
    s = Bedtools.get_fasta(species, chrom, start, end, strand)
    match = s[NUM_FLANK_NTS:int(d_tokens[2]) + NUM_FLANK_NTS]
    try:
        assert match.upper() == str(sr.seq).upper()
    except AssertionError:
        print(match.upper())
        print(str(sr.seq).upper())
        return None
    new_description = "{} {} {} {} flanked, b={}".format(start,
                                                         size,
                                                         strand,
                                                         src_size,
                                                         NUM_FLANK_NTS)
    new_sr = SeqRecord(
        Seq(s, IUPACAmbiguousRNA),
        id=sr.id,
        name=sr.id,
        description=new_description)
    return new_sr


if __name__ == '__main__':

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    f = sys.argv[1]
    if os.path.isfile(f):
        FILE_LIST = [f]
    else:
        FILE_LIST = glob.glob(os.path.join(f, '*.fa'))

    for file_name in FILE_LIST:

        parts = Path(file_name).name.split('.')
        if len(parts) > 1:
            ext = parts[-1]
            del parts[-1]
            root_name = '.'.join(parts)
        else:
            root_name = parts[0]
        output_file_name = '.'.join([root_name, 'flanked', 'fa'])

        srs = []
        for sr_ in SeqIO.parse(file_name, "fasta"):
            if not flank(sr_):
                break
            srs.append(flank(sr_))
        outfile = os.path.join(OUT_DIR, output_file_name)
        with open(outfile, "w") as fh:
            SeqIO.write(srs, fh, "fasta-2line")
