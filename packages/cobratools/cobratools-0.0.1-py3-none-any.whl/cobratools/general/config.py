"""
Configuration
"""

from typing import List

# pylint: disable = E0401
# noinspection PyPackageRequirements
from mypy_extensions import TypedDict

# pylint: disable=C0103
Conf = TypedDict('Conf', {'MAF_DATA_PATH': str,
                          'GENOME_DATA_PATH': str,
                          'TARGET_SPECIES': List[str],
                          'MIN_MSA_LEN': int,  # residues
                          'SAMPLE_PROB': float  # within interval (0.0, 1.0]
                          })

CONF = {
    'MAF_DATA_PATH':
        '/Users/clayton/Workspace/Bioinformatics/RLR_pipeline/data/multiz/maf',
    'GENOME_DATA_PATH': '/Volumes/Public/Genome',
    'TARGET_SPECIES': ['mm10', 'hg19', 'oryCun2', 'rheMac3', 'susScr3',
                       'equCab2', 'canFam3'],
    'MIN_MSA_LEN': 50,
    'SAMPLE_PROB': 1.0,
}  # type: Conf
