# -*- coding] = utf-8 -*-
"""
Alphabets. See: https://en.wikipedia.org/wiki/FASTA_format and IUPAC-IUB

We user ordered dict so that we can ensure a specific order when iterating
(plain dict can't guarantee this). This is important for testing!
"""

from collections import OrderedDict

d: OrderedDict = OrderedDict()
d['A'] = 'Adenine'
d['C'] = 'Cytosine'
d['G'] = 'Guanine'
d['T'] = 'Thymine'
d['U'] = 'Uracil'
d['R'] = 'A or G (puRine)'
d['Y'] = 'C, T or U	(pYrimidines)'
d['K'] = 'G, T or U	(Ketones)'
d['M'] = 'A or C (bases with aMino groups)'
d['S'] = 'C or G (Strong interaction)'
d['W'] = 'A, T or U	(Weak interaction)'
d['B'] = 'not A'
d['D'] = 'not C'
d['H'] = 'not G'
d['V'] = 'neither T nor U'
d['N'] = 'any (Nucleic acid)'
d['-'] = 'gap of indeterminate length'
d['.'] = 'gap of indeterminate length'

NUCLEOTIDE_ALPHABET = d

TRANS_T2U = str.maketrans("NACGTRYKMSWBDHVnacgtrykmswbdhv-",
                          "NACGURYKMSWBDHVnacgurykmswbdhv-")

# pylint: disable=W0105
"""
A	Alanine
B	Aspartic acid (D) or Asparagine (N)
C	Cysteine
D	Aspartic acid
E	Glutamic acid
F	Phenylalanine
G	Glycine
H	Histidine
I	Isoleucine
J	Leucine (L) or Isoleucine (I)
K	Lysine
L	Leucine
M	Methionine/Start codon
N	Asparagine
O	Pyrrolysine
P	Proline
Q	Glutamine
R	Arginine
S	Serine
T	Threonine
U	Selenocysteine
V	Valine
W	Tryptophan
Y	Tyrosine
Z	Glutamic acid (E) or Glutamine (Q)
X	any
*	translation stop
-	gap of indeterminate length
"""
