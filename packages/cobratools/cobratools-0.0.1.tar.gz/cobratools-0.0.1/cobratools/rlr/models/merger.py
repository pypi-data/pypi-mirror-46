# -*- coding] = utf-8 -*-
"""
Merge overlapping sequences

We have something like this an a *.dat file

locus20	mm10.chr3	4605486	4605670	4	81.25	0.990061	-2.99
window32	locus20	mm10.chr3	4605486	4605606	+	4	120	80.31	-30.99	...
window33	locus20	mm10.chr3	4605506	4605626	+	4	120	81.25	-29.06	...
window34	locus20	mm10.chr3	4605526	4605646	+	4	120	81.25	-26.47	...
window35	locus20	mm10.chr3	4605546	4605665	+	4	120	79.97	-30.38	...
window36	locus20	mm10.chr3	4605551	4605670	+	4	120	78.84	-30.03	...

If we look at the locus in the clustered results, we have separate *.maf files.

window32

a score=0
s mm10.chr3 4605486 120 + 160039680 GAAUGAACAAAGAAUGUGGGUUGAAUAACCACUGUGCAU...
    GAUAACAAAUACAGUAAUUCAGUAUCUUCCCCCUCCCCAUUUCCAGAUACAACUUAAGAGUUUUGGAAAUG...
    AAAGACAAGA
s oryCun2.chr3 92030817 114 + 155691105 UAAUGAA-GGAGAAUGAGGGUUGAGUUACAGCUUU...
    GUACAAUAACAAAUACAGUAAUUCAACAUCU-----CUUUCUUUUCCUGAAUCCUACUCAAGGGUUUUGGA...
    GAAGAAAGACAAAA
s panTro4.chr8 74227806 113 + 143986469 UAAUGAA-GGAGAAUGAAGGUUGAGUUACAGCUCC...
    GUACAA-AACAAAUAGAGUAAUUCAGUACCU-----CUUUCUUUUCCUGGAUCCAACGCAAAAGUUUGGGA...
    GAAGAAAGACAAGA
s rheMac3.chr8 81005742 113 + 150158102 UAAUGAA-GGAGAAUGAGGGUUGAAUUACAGCUCU...
    GUACAA-AACAAAUAGAGUAAUUCAGCACCU-----CUUUCUUUUCCUGGAUCCAACGCAAGAGUUUGGGA...
    GAAGAAAGACAAGA

window33

a score=0
s mm10.chr3 4605506 120 + 160039680 UUGAAUAACCACUGUGCAUGAUAACAAAUACAGUAAUUC...
    AGUAUCUUCCCCCUCCCCAUUUCCAGAUACAACUUAAGAGUUUUGGAAAUGAAAGACAAGAAAAUUAUCUG...
    UGUAACAUGA
s oryCun2.chr3 92030836 115 + 155691105 UUGAGUUACAGCUUUGUACAAUAACAAAUACAGUA...
    AUUCAACAUCU-----CUUUCUUUUCCUGAAUCCUACUCAAGGGUUUUGGAGAAGAAAGACAAAAAGAUUA...
    UCUAGGUAAUAUGA
s panTro4.chr8 74227825 114 + 143986469 UUGAGUUACAGCUCCGUACAA-AACAAAUAGAGUA...
    AUUCAGUACCU-----CUUUCUUUUCCUGGAUCCAACGCAAAAGUUUGGGAGAAGAAAGACAAGAAGAUUA...
    UCUAGGUAAUAUGA
s rheMac3.chr8 81005761 114 + 150158102 UUGAAUUACAGCUCUGUACAA-AACAAAUAGAGUA...
    AUUCAGCACCU-----CUUUCUUUUCCUGGAUCCAACGCAAGAGUUUGGGAGAAGAAAGACAAGAAGAUUA...
    UCUAGGUAAUAUGA

window34

a score=0
s mm10.chr3 4605526 120 + 160039680 AUAACAAAUACAGUAAUUCAGUAUCUUCCCCCUCCCCAU...
    UUCCAGAUACAACUUAAGAGUUUUGGAAAUGAAAGACAAGAAAAUUAUCUGUGUAACAUGAUCUCGUGAUU...
    ACCAAUGCAC
s oryCun2.chr3 92030856 115 + 155691105 AUAACAAAUACAGUAAUUCAACAUCU-----CUUU...
    CUUUUCCUGAAUCCUACUCAAGGGUUUUGGAGAAGAAAGACAAAAAGAUUAUCUAGGUAAUAUGAUCUUGA...
    AACUAUCAGUGGAU
s panTro4.chr8 74227845 114 + 143986469 A-AACAAAUAGAGUAAUUCAGUACCU-----CUUU...
    CUUUUCCUGGAUCCAACGCAAAAGUUUGGGAGAAGAAAGACAAGAAGAUUAUCUAGGUAAUAUGAUCUUAA...
    GAAUAUCAGUGGAU
s rheMac3.chr8 81005781 114 + 150158102 A-AACAAAUAGAGUAAUUCAGCACCU-----CUUU...
    CUUUUCCUGGAUCCAACGCAAGAGUUUGGGAGAAGAAAGACAAGAAGAUUAUCUAGGUAAUAUGAUCUUAA...
    GAAUAUCAGUGGAU

window35

a score=0
s mm10.chr3 4605546 119 + 160039680 GUAUCUUCCCCCUCCCCAUUUCCAGAUACAACUUAAGAG...
    UUUUGGAAAUGAAAGACAAGAAAAUUAUCUGUGUAACAUGAUCUCGUGAUUACCAAUGCACAAUGGUGUUC...
    UCCAUCAA-U
s oryCun2.chr3 92030876 113 + 155691105 ACAUCU-----CUUUCUUUUCCUGAAUCCUACUCA...
    AGGGUUUUGGAGAAGAAAGACAAAAAGAUUAUCUAGGUAAUAUGAUCUUGAAACUAUCAGUGGAUAAUGGU...
    GUCCACCAUCAA--
s panTro4.chr8 74227864 115 + 143986469 GUACCU-----CUUUCUUUUCCUGGAUCCAACGCA...
    AAAGUUUGGGAGAAGAAAGACAAGAAGAUUAUCUAGGUAAUAUGAUCUUAAGAAUAUCAGUGGAUAAUGGU...
    GUCCUCCGUCAACU
s rheMac3.chr8 81005800 115 + 150158102 GCACCU-----CUUUCUUUUCCUGGAUCCAACGCA...
    AGAGUUUGGGAGAAGAAAGACAAGAAGAUUAUCUAGGUAAUAUGAUCUUAAGAAUAUCAGUGGAUAAUGGU...
    GUCCUCCGUCAACU

window36

a score=0
s mm10.chr3 4605551 119 + 160039680 UUCCCCCUCCCCAUUUCCAGAUACAACUUAAGAGUUUUG...
    GAAAUGAAAGACAAGAAAAUUAUCUGUGUAACAUGAUCUCGUGAUUACCAAUGCACAAUGGUGUUCUCCAU...
    CAA-UUUGGC
s oryCun2.chr3 92030881 108 + 155691105 U-----CUUUCUUUUCCUGAAUCCUACUCAAGGGU...
    UUUGGAGAAGAAAGACAAAAAGAUUAUCUAGGUAAUAUGAUCUUGAAACUAUCAGUGGAUAAUGGUGUCCA...
    CCAUCAA-------
s panTro4.chr8 74227869 115 + 143986469 U-----CUUUCUUUUCCUGGAUCCAACGCAAAAGU...
    UUGGGAGAAGAAAGACAAGAAGAUUAUCUAGGUAAUAUGAUCUUAAGAAUAUCAGUGGAUAAUGGUGUCCU...
    CCGUCAACUUUGUG
s rheMac3.chr8 81005805 115 + 150158102 U-----CUUUCUUUUCCUGGAUCCAACGCAAGAGU...
    UUGGGAGAAGAAAGACAAGAAGAUUAUCUAGGUAAUAUGAUCUUAAGAAUAUCAGUGGAUAAUGGUGUCCU...
    CCGUCAACUUUGUG

Notice that in this example all strands are "+"
"""

# pylint: disable=E0401
from Bio.Alphabet import SingleLetterAlphabet
# pylint: disable=E0401
from Bio.Seq import Seq
# pylint: disable=E0401
from Bio.SeqRecord import SeqRecord

from cobratools.general.models.common import StrandAware


class Merge(StrandAware):
    """
    Input is two or more multiple sequence alignments in Biopython
    """

    @staticmethod
    def validate(sr):
        """
        Simple sanity check
        :param sr:
        :return:
        """
        assert int(sr.annotations['size']) == len(sr)
        assert sr.annotations['start'] + sr.annotations['size'] - 1 \
               <= sr.annotations['srcSize']

    @staticmethod
    def sort(sr_1, sr_2):
        """
        :param sr_1:
        :param sr_2:
        :return:
        """
        if sr_1 is None or sr_2 is None:
            return None, None
        if int(sr_1.annotations['start']) < int(sr_2.annotations['start']):
            return sr_1, sr_2
        elif int(sr_1.annotations['start']) > int(sr_2.annotations['start']):
            return sr_2, sr_1
        else:
            # Same start, return LONGER sequence first
            if int(sr_1.annotations['size']) < int(sr_2.annotations['size']):
                return sr_2, sr_1
            elif int(sr_1.annotations['size']) > int(sr_2.annotations['size']):
                return sr_1, sr_2
            else:
                # Sequences are identical
                return sr_1, sr_2

    @staticmethod
    def overlap(sr_1, sr_2):
        """
        Calculate overlap
        :param sr_1:
        :param sr_2:
        :return: bool
        """
        sr_1, sr_2 = Merge.sort(sr_1, sr_2)
        if sr_1 is None or sr_2 is None:
            return False
        sr_1_end = Merge.seq_end(sr_1)
        return int(sr_2.annotations['start']) <= sr_1_end

    @staticmethod
    def seq_end(sr):
        """
        NOTE: Size annotation ONLY COUNTS NUCLEOTIDES NOT GAPS
        :param sr:
        :return:
        """
        return int(sr.annotations['start']) \
               + int(sr.annotations['size']) - 1

    @staticmethod
    def merge_seq(sr_1, sr_2):
        """

        :param sr_1:
        :param sr_2:
        :return:
        """
        merged = None
        if Merge.overlap(sr_1, sr_2):
            sr_1_end = Merge.seq_end(sr_1)
            sr_2_end = Merge.seq_end(sr_2)
            if sr_1_end >= sr_2_end:
                s = str(sr_1.seq)
            else:
                str_1 = str(sr_1.seq)
                x = int(sr_2.annotations['start']) - \
                    int(sr_1.annotations['start'])
                x = x + str_1[0:x].count('-')  # compensate for gaps
                s = str(sr_1.seq[0:x]) + str(sr_2.seq)
            annotations = {'start': sr_1.annotations['start'],
                           'size': sr_1.annotations['size'],
                           'nts_merged': len(str(s)) - s.count('-'),
                           'strand': sr_1.annotations['strand'],
                           'srcSize': sr_1.annotations['srcSize']
                           }
            description = "{} {} {} {} merged" \
                .format(str(annotations['start']),
                        str(annotations['nts_merged']),
                        Merge.get_strand(annotations['strand']),
                        str(annotations['srcSize']))
            merged = SeqRecord(Seq(s, SingleLetterAlphabet),
                               id=sr_1.id,
                               name=sr_1.name,
                               description=description,
                               annotations=annotations)
        return merged
