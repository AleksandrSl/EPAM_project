import glob

path_to_fastq = '/home/aleksandrsl/Desktop/EPAM_project/data/sequences/'
iterator = iter(sorted(glob.glob(path_to_fastq + '*.fastq.gz')))
for fastq in iterator:
    paired_fastq = (fastq, next(iterator))
    print(paired_fastq)