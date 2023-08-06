# -*- coding: utf-8 -*-
"""
Extract interesting bits from GENCODE mouse annotations and save to
BED or GTF format for intersection

If BED, we want output to be like Thiel's BED files

chr1	20679004	20679086	loc880261	1000	+	-30.43	1.000000   ...
    ... mm10.dipOrd1.micMur1.susScr3.sorAra1.sarHar1.ornAna1.anoCar2 ...
    ...	0.43672	0.81	lncRNA

Otherwise, just write the GTF line.

Oh, BTW. Bedtools says it supports BED/GFF/VCF and BAM as input. Be aware that
"the GTF (General Transfer Format) is identical to GFF version 2.

"""

import argparse
from typing import Union

from cobratools.general.models.bed import BedLine
from cobratools.general.models.gtf import GtfLine, InvalidDataError

FEATURE_TYPES = ['gene', 'transcript', 'exon', 'CDS', 'UTR', 'start_codon',
                 'stop_codon', 'Selenocysteine']

THIEL_MAPPING = {'3prime_overlapping_ncRNA': 'lncRNA',
                 'ambiguous_orf': None,
                 'antisense': 'lncRNA',
                 'antisense/antisense_RNA': None,
                 'bidirectional_promoter_lncRNA': 'lncRNA',
                 'disrupted_domain': None,
                 'IG_C_gene': 'other',
                 'IG_C_pseudogene': 'other',
                 'IG_D_gene': 'other',
                 'IG_D_pseudogene': 'other',
                 'IG_J_gene': 'other',
                 'IG_J_pseudogene': None,
                 'IG_LV_gene': 'other',
                 'IG_pseudogene': 'other',
                 'IG_V_gene': 'other',
                 'IG_V_pseudogene': 'other',
                 'known_ncrna': None,
                 'lincRNA': 'lncRNA',
                 'macro_lncRNA': 'lncRNA',
                 'miRNA_pseudogene': None,
                 'miRNA': 'sncRNA',
                 'misc_RNA_pseudogene': None,
                 'misc_RNA': 'other',
                 'Mt_rRNA': None,
                 'Mt_tRNA_pseudogene': None,
                 'Mt_tRNA': None,
                 'non_coding': None,
                 'non_stop_decay': 'other',
                 'nonsense_mediated_decay': 'other',
                 'polymorphic_pseudogene': 'other',
                 'processed_pseudogene': 'other',
                 'processed_transcript': 'lncRNA',
                 'protein_coding': 'mRNA',
                 'pseudogene': 'other',
                 'retained_intron': 'other',
                 'retrotransposed': None,
                 'ribozyme': 'other',
                 'rRNA_pseudogene': None,
                 'rRNA': 'sncRNA',
                 'scaRNA': 'sncRNA',
                 'scRNA_pseudogene': None,
                 'scRNA': 'sncRNA',
                 'sense_intronic': 'other',
                 'sense_overlapping': 'other',
                 'snoRNA_pseudogene': None,
                 'snoRNA': 'sncRNA',
                 'snRNA_pseudogene': None,
                 'snRNA': 'sncRNA',
                 'sRNA': 'sncRNA',
                 'TEC': 'other',
                 'TR_C_gene': 'other',
                 'TR_D_gene': 'other',
                 'TR_J_gene': 'other',
                 'TR_J_pseudogene': 'other',
                 'TR_V_gene': 'other',
                 'TR_V_pseudogene': 'other',
                 'transcribed_processed_pseudogene': 'other',
                 'transcribed_unitary_pseudogene': 'other',
                 'transcribed_unprocessed_pseudogene': 'other',
                 'translated_processed_pseudogene': 'other',
                 'translated_unprocessed_pseudogene': None,
                 'tRNA_pseudogene': None,
                 'unitary_pseudogene': 'other',
                 'unprocessed_pseudogene': 'other',
                 'vaultRNA': None}


def write_gene_type(gtf_line: GtfLine,
                    bed_line: Union[BedLine, None] = None):
    """
    Write line to GENE TYPE file
    :param gtf_line:
    :param bed_line:
    :return:
    """

    try:
        gt = gtf_line.additional['gene_type']
        if bed_line is None:
            out_file = "gene_type_" + gt + ".gtf"
            out_line: Union[GtfLine, BedLine] = gtf_line
        else:
            out_file = "gene_type_" + gt + ".bed"
            out_line = bed_line
        with open(out_file, "a") as ofh:
            ofh.write(str(out_line) + "\n")
    except KeyError:
        # Row does not have gene_type annotation
        # I think, however, every row will have this annotation
        pass
    except IndexError:
        pass


def write_transcript_type(gtf_line: GtfLine,
                          bed_line: Union[BedLine, None] = None):
    """
    Write line to TRANSCRIPT TYPE file
    :param gtf_line:
    :param bed_line:
    :return:
    """
    try:
        gt = gtf_line.additional['transcript_type']
        if bed_line is None:
            out_file = "transcript_type_" + gt + ".gtf"
            out_line: Union[GtfLine, BedLine] = gtf_line
        else:
            out_file = "transcript_type_" + gt + ".bed"
            out_line = bed_line
        with open(out_file, "a") as ofh:
            ofh.write(str(out_line) + "\n")
    except KeyError:
        # Row does not have transcript_type annotation
        pass
    except IndexError:
        pass


def write_aggregated_type(gtf_line: GtfLine,
                          bed_line: Union[BedLine, None] = None):
    """
    Write line to AGGREGATED TRANSCRIPT TYPE FILE
    :param gtf_line:
    :param bed_line:
    :return:
    """
    try:
        key = gtf_line.additional['transcript_type']
    except KeyError:
        return
    try:
        agg_type = THIEL_MAPPING[key]
        if agg_type is None:
            print("Warning! Unmapped key: {}".format(key))
        else:
            if bed_line is None:
                out_file = "agg_trans_type_" + agg_type + ".gtf"
                out_line: Union[GtfLine, BedLine] = gtf_line
            else:
                out_file = "agg_trans_type_" + agg_type + ".bed"
                out_line = bed_line
            with open(out_file, "a") as ofh:
                ofh.write(str(out_line) + "\n")
    except KeyError:
        print("Warning! Key not found in mapping: {}".format(key))
    except IndexError:
        pass


def write_feature_type(gtf_line: GtfLine,
                       bed_line: Union[BedLine, None] = None):
    """
    Write line to FEATURE TYPE file
    :param gtf_line:
    :param bed_line:
    :return:
    """
    try:
        ft = gtf_line.feature_type
        if bed_line is None:
            out_file = "feature_" + ft + ".gtf"
            out_line: Union[GtfLine, BedLine] = gtf_line
        else:
            out_file = "feature_" + ft + ".bed"
            out_line = bed_line
        with open(out_file, "a") as ofh:
            ofh.write(str(out_line) + "\n")
    except IndexError:
        pass


def run(fn: str, out_format: str):
    """
    Do the do
    :param fn: str
    :param out_format: str
    :return:
    """
    with open(fn, "r") as fh:
        line = 'true'
        while line:
            line = fh.readline()
            if not line.startswith('#'):
                try:
                    gtfline = GtfLine(line)
                except InvalidDataError:
                    if line != '':
                        print("Invalid data: {}".format(line))
                    continue
                if gtfline.feature_type in FEATURE_TYPES:
                    if out_format == 'bed':
                        d = {'chrom': gtfline.chrom,
                             'chromStart': gtfline.start,
                             'chromEnd': gtfline.end,
                             'name': 'mm10.' + gtfline.chrom + '_'
                                     + gtfline.feature_type,
                             'score': 0,
                             'strand': gtfline.score,
                             'thickStart': None,
                             'thickEnd': None,
                             'itemRgb': None,
                             'blockCount': None,
                             'blockSizes': None,
                             'blockStarts': None}
                        bedline: Union[BedLine, None] = BedLine(d)
                    else:
                        bedline = None
                    write_gene_type(gtfline, bedline)
                    write_transcript_type(gtfline, bedline)
                    write_aggregated_type(gtfline, bedline)
                    write_feature_type(gtfline, bedline)
                else:
                    print("Unknown feature type: {}"
                          .format(gtfline.feature_type))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input Gencode file")
    parser.add_argument("-o", '--output-format',
                        type=str, default='gtf',
                        choices=['gtf', 'bed'],
                        help="Output format (gtf or bed)")
    ARGS = parser.parse_args()
    IN_FILEPATH = ARGS.file
    OUTPUT_FORMAT = ARGS.output_format
    try:
        run(IN_FILEPATH, OUTPUT_FORMAT)
    except FileNotFoundError:
        print("File {} not found".format(IN_FILEPATH))
        exit(1)
    exit(0)
