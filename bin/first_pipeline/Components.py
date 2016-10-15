import luigi
import logging
import sciluigi as sl
import glob
from subprocess import call

class FastqcTask(sl.Task):

    # Parameter
    fastq_file_path = None

    # I/O
    def fastqc_res(self):
        pass
        # return sl.TargetInfo(self, 'data/' + self.text)

    # Implementation
    def run(self):
        #call('mkdir /home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v2', shell=True)
        cmd = '~/Desktop/EPAM_project/tools/fastqc/fastqc -o /home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v2 ' + self.fastq_file_path
        print('!!!!' + cmd)
        # fastqc [-o output dir] [--(no)extract] [-f fastq|bam|sam]  [-c contaminant file] seqfile1 .. seqfileN
        # logging.log.info("COMMAND TO EXECUTE: " + cmd)
        call(cmd, shell=True)

class FastqcTask_v2(sl.Task):

    # Parameter
    fastq_file_path = None

    # I/O
    def fastqc_res(self):
        pass
        # return sl.TargetInfo(self, 'data/' + self.text)

    # Implementation
    def run(self):
        #call('mkdir /home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v2', shell=True)
        cmd = '~/Desktop/EPAM_project/tools/fastqc/fastqc -o /home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v2 ' + self.fastq_file_path[0] + ' ' + self.fastq_file_path[1]
        print('!!!!' + cmd)
        # fastqc [-o output dir] [--(no)extract] [-f fastq|bam|sam]  [-c contaminant file] seqfile1 .. seqfileN
        # logging.log.info("COMMAND TO EXECUTE: " + cmd)
        call(cmd, shell=True)


# class RawSequencesTask(sl.ExternalTask):
#
#
#     def out_raw_sequences(self):
#         return sl.TargetInfo(self, 'BK0020_S1_L001_R1_001.fastq.gz')
