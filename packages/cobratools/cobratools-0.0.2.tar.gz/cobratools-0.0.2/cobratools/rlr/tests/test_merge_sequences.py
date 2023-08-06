# -*- coding: utf-8 -*-
"""
Tests for Merge
"""

# pylint: disable=E0401
from Bio.Alphabet import SingleLetterAlphabet
# pylint: disable=E0401
from Bio.Seq import Seq
# pylint: disable=E0401
from Bio.SeqRecord import SeqRecord
# pylint: disable=E0401
from Bio import AlignIO

# pylint: disable=W0611
from cobratools.rlr.models.merger import Merge


def test_overlap():
    """
    +/+
    :return:
    """
    sr_1 = SeqRecord(Seq("AAAAAAA", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 10,
                                  'size': 7,
                                  'strand': 1,
                                  'srcSize': 1000})
    sr_2 = SeqRecord(Seq("AAAAAAA", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 12,
                                  'size': 7,
                                  'strand': 1,
                                  'srcSize': 1000})

    o_size = Merge.overlap(sr_1, sr_2)
    assert o_size

    sr_2 = SeqRecord(Seq("AAAA", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 10,
                                  'size': 4,
                                  'strand': 1,
                                  'srcSize': 1000})

    o_size = Merge.overlap(sr_1, sr_2)
    assert o_size

    sr_2 = SeqRecord(Seq("AAAA", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 12,
                                  'size': 4,
                                  'strand': 1,
                                  'srcSize': 1000})

    o_size = Merge.overlap(sr_1, sr_2)
    assert o_size

    sr_2 = SeqRecord(Seq("AAAA", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 13,
                                  'size': 4,
                                  'strand': 1,
                                  'srcSize': 1000})

    o_size = Merge.overlap(sr_1, sr_2)
    assert o_size

    sr_2 = SeqRecord(Seq("AAAA", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 25,
                                  'size': 4,
                                  'strand': 1,
                                  'srcSize': 1000})

    o_size = Merge.overlap(sr_1, sr_2)
    assert not o_size


def test_sort_neq():
    """

    :return:
    """
    sr_1 = SeqRecord(Seq("AGUCUGUCCGAAUAAAAUACGAU", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 30002,
                                  'size': 23,
                                  'strand': 1,
                                  'srcSize': 160039680})
    sr_2 = SeqRecord(Seq("AAAUACGAUAAAGCAGCACAGCAGGAUUU", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="Sequence +",
                     annotations={'start': 30016,
                                  'size': 30,
                                  'strand': 1,
                                  'srcSize': 160039680})

    sr_1, sr_2 = Merge.sort(sr_1, sr_2)
    assert int(sr_1.annotations['start']) < int(sr_2.annotations['start'])

    temp = sr_1
    sr_1 = sr_2
    sr_2 = temp
    sr_1, sr_2 = Merge.sort(sr_1, sr_2)
    assert int(sr_1.annotations['start']) < int(sr_2.annotations['start'])


def test_sort_eq():
    """
    LONGER sequence first, if start coords same. If start coords same and
    sequence length same, return in original order
    :return:
    """
    sr_1 = SeqRecord(Seq("AGUCUGUCCGAAUAAAAUACGAU", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="I am sequence #1",
                     annotations={'start': 30002,
                                  'size': 23,
                                  'strand': 1,
                                  'srcSize': 160039680})
    sr_2 = SeqRecord(Seq("AGUCUGUCCGAAU", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="I am sequence #2",
                     annotations={'start': 30002,
                                  'size': 13,
                                  'strand': 1,
                                  'srcSize': 160039680})
    sr_3 = SeqRecord(Seq("AGUCUGUCCGAAU", SingleLetterAlphabet),
                     id="zz99.chr3",
                     name="Just a test",
                     description="I am sequence #3",
                     annotations={'start': 30002,
                                  'size': 13,
                                  'strand': 1,
                                  'srcSize': 160039680})

    tsr_1, tsr_2 = Merge.sort(sr_1, sr_2)
    assert int(tsr_1.annotations['start']) == int(tsr_2.annotations['start'])
    assert int(tsr_1.annotations['size']) > int(tsr_2.annotations['size'])

    tsr_1, tsr_2 = Merge.sort(sr_2, sr_1)
    assert int(tsr_1.annotations['size']) > int(tsr_2.annotations['size'])

    tsr_1, tsr_2 = Merge.sort(sr_2, sr_3)
    assert int(tsr_1.annotations['size']) == int(tsr_2.annotations['size'])
    assert tsr_1.description == 'I am sequence #2'

    tsr_1, tsr_2 = Merge.sort(sr_3, sr_2)
    assert int(tsr_1.annotations['size']) == int(tsr_2.annotations['size'])
    assert tsr_1.description == 'I am sequence #3'



def test_merge():
    """
    :return:
    """

    sr_1 = SeqRecord(Seq(
        "GAAUGAACAAAGAAUGUGGGUUGAAUAACCACUGUGCAUGAUAACAAAUACAGUAAUUCA"
        "GUAUCUUCCCCCUCCCCAUUUCCAGAUACAACUUAAGAGUUUUGGAAAUGAAAGACAAGA",
        SingleLetterAlphabet),
                     id="mm10.chr3",
                     name="mm10.chr3",
                     description="",
                     annotations={'start': 4605486,
                                  'size': 120,
                                  'strand': 1,
                                  'srcSize': 160039680})
    assert str(sr_1.seq) == "GAAUGAACAAAGAAUGUGGGUUGAAUAACCACUGUGCAUG" \
                            "AUAACAAAUACAGUAAUUCAGUAUCUUCCCCCUCCCCAUU" \
                            "UCCAGAUACAACUUAAGAGUUUUGGAAAUGAAAGACAAGA"

    sr_2 = SeqRecord(Seq(
        "UUGAAUAACCACUGUGCAUGAUAACAAAUACAGUAAUUCAGUAUCUUCCCCCUCCCCAUU"
        "UCCAGAUACAACUUAAGAGUUUUGGAAAUGAAAGACAAGAAAAUUAUCUGUGUAACAUGA",
        SingleLetterAlphabet),
                     id="mm10.chr3",
                     name="mm10.chr3",
                     description="",
                     annotations={'start': 4605506,
                                  'size': 120,
                                  'strand': 1,
                                  'srcSize': 160039680})
    assert str(sr_2.seq) == "UUGAAUAACCACUGUGCAUGAUAACAAAUACAGUAAUUCA" \
                            "GUAUCUUCCCCCUCCCCAUUUCCAGAUACAACUUAAGAGU" \
                            "UUUGGAAAUGAAAGACAAGAAAAUUAUCUGUGUAACAUGA"

    merged = Merge.merge_seq(sr_1, sr_2)

    assert str(merged.seq) == "GAAUGAACAAAGAAUGUGGGUUGAAUAACCACUGUGCA" \
                              "UGAUAACAAAUACAGUAAUUCAGUAUCUUCCCCCUCCC" \
                              "CAUUUCCAGAUACAACUUAAGAGUUUUGGAAAUGAAAG" \
                              "ACAAGAAAAUUAUCUGUGUAACAUGA"


def test_merge_multiple_1():
    """
    Read alignment blocks from MAF files and produce merged MAF data
    """
    files = ["./tests/data/window32.maf", "./tests/data/window33.maf",
             "./tests/data/window34.maf", "./tests/data/window35.maf",
             "./tests/data/window36.maf"]
    sequences = {}
    alignment_blocks = []
    for file in files:
        alignment_blocks.append(AlignIO.parse(file, "maf"))
    for msas in alignment_blocks:
        for msa in msas:
            # If reading a window file, there should be only one MSA. But
            # there will be two or more sequences per MSA
            for sr in msa:
                if sr.id in sequences.keys():
                    sequences[sr.id].append(sr)
                else:
                    sequences[sr.id] = [sr]
    for id_, seq_list in sequences.items():
        merged = seq_list[0]
        for another in seq_list[1:]:
            merged = Merge.merge_seq(merged, another)
        sequences[id_] = [merged]

    for id_, seq_list in sequences.items():
        print(sequences[id_][0].seq)
        if id_ == 'mm10.chr3':
            assert str(sequences[id_][0].seq) == 'GAAUGAACAAAGAAUGUGG' \
                                                 'GUUGAAUAACCACUGUGCA' \
                                                 'UGAUAACAAAUACAGUAAU' \
                                                 'UCAGUAUCUUCCCCCUCCC' \
                                                 'CAUUUCCAGAUACAACUUA' \
                                                 'AGAGUUUUGGAAAUGAAAG' \
                                                 'ACAAGAAAAUUAUCUGUGU' \
                                                 'AACAUGAUCUCGUGAUUAC' \
                                                 'CAAUGCACAAUGGUGUUCU' \
                                                 'CCAUCAA-UUUGGC'
        elif id_ == 'oryCun2.chr3':
            assert str(sequences[id_][0].seq) == 'UAAUGAA-GGAGAAUGAGG' \
                                                 'GUUGAGUUACAGCUUUGUA' \
                                                 'CAAUAACAAAUACAGUAAU' \
                                                 'UCAACAUCU-----CUUUC' \
                                                 'UUUUCCUGAAUCCUACUCA' \
                                                 'AGGGUUUUGGAGAAGAAAG' \
                                                 'ACAAAAAGAUUAUCUAGGU' \
                                                 'AAUAUGAUCUUGAAACUAU' \
                                                 'CAGUGGAUAAUGGUGUCCA' \
                                                 'CCAUCAA-------'
        elif id_ == 'panTro4.chr8':
            assert str(sequences[id_][0].seq) == 'UAAUGAA-GGAGAAUGAAG' \
                                                 'GUUGAGUUACAGCUCCGUA' \
                                                 'CAA-AACAAAUAGAGUAAU' \
                                                 'UCAGUACCU-----CUUUC' \
                                                 'UUUUCCUGGAUCCAACGCA' \
                                                 'AAAGUUUGGGAGAAGAAAG' \
                                                 'ACAAGAAGAUUAUCUAGGU' \
                                                 'AAUAUGAUCUUAAGAAUAU' \
                                                 'CAGUGGAUAAUGGUGUCCU' \
                                                 'CCGUCAACUUUGUG'
        elif id_ == 'rheMac3.chr8':
            assert str(sequences[id_][0].seq) == 'UAAUGAA-GGAGAAUGAGG' \
                                                 'GUUGAAUUACAGCUCUGUA' \
                                                 'CAA-AACAAAUAGAGUAAU' \
                                                 'UCAGCACCU-----CUUUC' \
                                                 'UUUUCCUGGAUCCAACGCA' \
                                                 'AGAGUUUGGGAGAAGAAAG' \
                                                 'ACAAGAAGAUUAUCUAGGU' \
                                                 'AAUAUGAUCUUAAGAAUAU' \
                                                 'CAGUGGAUAAUGGUGUCCU' \
                                                 'CCGUCAACUUUGUG'
        else:
            print("Well, this is unexpected!")
