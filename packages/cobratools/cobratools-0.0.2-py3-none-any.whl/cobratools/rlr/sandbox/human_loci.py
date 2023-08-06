import glob
import os

root_folder = './output/06_rnaz_2/results'

humans = 0
loci = 0
folders = []
for folder in [f.path for f in os.scandir(root_folder) if f.is_dir()]:
    target = os.path.join(folder, '*.maf')
    humans_are_here = False
    for w in glob.glob(target):
        with open(w, 'r') as f:
            line = True
            while line:
                line = f.readline()
                if line.startswith('s hg19'):
                    humans_are_here = True
                    line = False
    if humans_are_here:
        humans += 1
        # folders.append(os.path.basename(os.path.normpath(folder)))
        folders.append(folder)
    loci += 1
print("{} human sequences in {} loci".format(humans, loci))

with open('loci_with_humans_mm10.bed', 'w') as mouse_file, \
        open('loci_with_humans_hg19.bed', 'w') as human_file:
    for folder in folders:
        target = os.path.join(folder, '*.maf')
        for w in glob.glob(target):
            with open(w, 'r') as f:
                line = True
                while line:
                    line = f.readline()
                    if line.startswith('s mm10'):
                        tokens = line.split()
                        chrom = tokens[1].split('.')[1]
                        start = tokens[2]
                        end = str(int(tokens[2]) + int(tokens[3]))
                        name = os.path.basename(os.path.normpath(folder))
                        score = '0'
                        strand = tokens[4]
                        output = '\t'.join(
                            [chrom, start, end, name, score, strand])
                        # s hg19.chr8 133829219 137
                        mouse_file.write(output + '\n')
                    if line.startswith('s hg19'):
                        tokens = line.split()
                        chrom = tokens[1].split('.')[1]
                        start = tokens[2]
                        end = str(int(tokens[2]) + int(tokens[3]))
                        name = os.path.basename(os.path.normpath(folder))
                        score = '0'
                        strand = tokens[4]
                        output = '\t'.join(
                            [chrom, start, end, name, score, strand])
                        # s hg19.chr8 133829219 137
                        human_file.write(output + '\n')
