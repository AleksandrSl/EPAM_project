import luigi
import json
import logging
import sciluigi as sl
import os
import glob
import utils
from subprocess import call

###############################################################################################################
# !!!! Class must implement out_.... and in_... methods
# out_method must return TargetInfo
###############################################################################################################

class FastqcTask3(sl.Task):
    """
    Process output of trimmomatic
    """

    # Parameter
    in_data = None
    tool_path = '/home/aleksandrsl/Desktop/EPAM_project/tools/fastqc/fastqc'
    outp_path = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v3/'


    def out_fastq(self):
        return [sl.TargetInfo(self, fastqc_res) for fastqc_res in glob.glob(self.outp_path + '*')]

    # Implementation
    def run(self):
        utils.mkdir_if_not_exist(self.outp_path)

        fastqs = [file for file in in_data()]
        cmd = '{tool_path} -o {out_path} {inp_1} {inp_2} {inp_3} {inp_4}'.format(tool_path=self.tool_path,
                                                                             out_path=self.outp_path,
                                                                             inp_1=fastqs[0],
                                                                             inp_2=fastqs[1],
                                                                             inp_3=fastqs[2],
                                                                             inp_4=fastqs[3])
        call(cmd, shell=True)


class TrimmoTask(sl.ExternalTask):
    """
    Execute trimmomatic on fastq files
    """
    # Parameter
    inp_data = None

    tool_path = '/home/aleksandrsl/Desktop/EPAM_project/tools/trimmomatic-0.36/trimmomatic-0.36.jar'
    adapters_path = '/home/aleksandrsl/Desktop/EPAM_project/tools/trimmomatic-0.36/adapters/'
    outp_path = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/trimmed_seqs/'
    adapter = 'TruSeq3-SE.fa'
    outp_name = 'trimmed_seq'
    adapter_full_path = adapters_path + adapter
    outp_full_path = outp_path + outp_name

    # I/O
    def out_trimmo(self):
        return [sl.TargetInfo(self, trimmo_res) for trimmo_res in glob.glob(self.outp_path + '*')]

    ###################################################################3
    # ILLUMINACLIP:<fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>:<minAdapterLength>:<keepBothReads>
    # SLIDINGWINDOW:<windowSize>:<requiredQuality>
    # LEADING:<quality>
    ####################################################################

    # Implementation
    def run(self):
        utils.mkdir_if_not_exist(self.outp_path)
        cmd = 'java -jar {tool_path} PE -basein {fastq_file} -baseout {outp_full_path} ' \
              'ILLUMINACLIP:{adapter_full_path}:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:32 ' \
              'MINLEN:36'.format(tool_path=self.tool_path,
                                 outp_full_path=self.outp_full_path,
                                 adapter_full_path=self.adapter_full_path,
                                 fastq_file=self.inp_data[0]
                                 )
        # logging.log.info("COMMAND TO EXECUTE: " + cmd)
        call(cmd, shell=True)
