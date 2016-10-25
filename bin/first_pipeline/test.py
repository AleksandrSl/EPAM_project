import glob, os
import sci
#import /home/Desktop/EPAM_project/tools/sciluidgi-master
# path_to_fastq = '/home/aleksandrsl/Desktop/EPAM_project/data/sequences/'
# iterator = iter(sorted(glob.glob(path_to_fastq + '*.fastq.gz')))
# for fastq in iterator:
#     paired_fastq = (fastq, next(iterator))
#     print(paired_fastq)
#
#
# path_to_fastq = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/sequences/'  # Test
# s = sorted(glob.glob(path_to_fastq + '*.fastq.gz'))
# print(list(zip(s[::2], s[1::2])))

print(os.path.dirname(os.getcwd()))



# cmd = 'java -jar $path_to_trimmo PE -basein {fastq_file} -baseout $full_path_to_res ' \
#               'ILLUMINACLIP:$full_path_to_adapter:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 ' \
#               'MINLEN:36'.format(fastq_file=self.fastq_file_path[0])
#

path_to_trimmo = '/home/aleksandrsl/Desktop/EPAM_project/tools/trimmomatic-0.36/trimmomatic-0.36.jar'
path_to_adapters = '/home/aleksandrsl/Desktop/EPAM_project/tools/trimmomatic-0.36/adapters/'
path_to_res = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/trimmed_seqs/'
#
# adapter = 'TruSeq3-SE.fa'
# res_file_name = 'trimmed_seq'
# full_path_to_adapter = path_to_adapters + adapter
# full_path_to_res = path_to_res + res_file_name
# print(list(map(os.path.basename, glob.glob(path_to_res + '*'))))
# dic =  {os.path.basename(trimmo_res): trimmo_res for trimmo_res in glob.glob(path_to_res + '*')}
# cmd = '~/Desktop/EPAM_project/tools/fastqc/fastqc -o /home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v2 {0} {1} {2} {3}'.format(*dic.values())
# print(cmd)