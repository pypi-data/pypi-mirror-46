# -*- coding: utf-8 -*-
"""
For tinkering with RNAz output files
"""

import re

from cobratools.general.models.fasta import Fasta

RECORD_DELIMITER = "############################  RNAz 2.1  ##############################"
SEQUENCE_ANNOUNCEMENT = "######################################################################"


class RNAz:
    """
    For parsing RNAz
    """
    STATLINE = re.compile(r'(^\s[A-Z][A-Za-z\s\+/-]*\:[\s]+)(.+)')

    def parse(self, filename):
        """
        Parse RNAz output file
        :param filename:
        """
        record = {}
        records = []
        with open(filename, "r") as fh:
            n = 0
            line = True
            header = False
            while line:
                line = fh.readline()
                if not header:
                    if RECORD_DELIMITER == line.strip():
                        record = {'sequences': []}
                        n += 1
                        header = True
                    else:
                        # We're in the sequence section
                        last = False
                        if line.startswith('>'):
                            if line.startswith('>consensus'):
                                last = True
                            seq = Fasta.parse_info_line(line)
                            # Next two lines are sequence itself and Ivogram
                            seq['sequence'] = fh.readline().strip()
                            seq['ivogram'] = fh.readline().strip()
                            record['sequences'].append(seq)
                            if last:
                                records.append(record)
                elif header:
                    if SEQUENCE_ANNOUNCEMENT == line.strip():
                        header = False
                    else:
                        m = self.STATLINE.search(line)
                        if m is not None:
                            key = m.group(1).split(':')[0].strip()
                            value = m.group(2).strip()
                            record[key] = value
        return records

    @staticmethod
    def extract_fasta():
        """
        TODO
        :return:
        """
