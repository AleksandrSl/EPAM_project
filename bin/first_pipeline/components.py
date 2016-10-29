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
# TODO: right email to creators to ask about information above

###############################################################################################################


        # fastqc [-o output dir] [--(no)extract] [-f fastq|bam|sam]  [-c contaminant file] seqfile1 .. seqfileN
        # logging.log.info("COMMAND TO EXECUTE: " + cmd)
# class FastqcTask_v2(sl.Task):
#     """
#     Process n fastq files
#     """
#
#     # Parameter
#     in_data = None
#     tool_path = '~/Desktop/EPAM_project/tools/fastqc/fastqc'
#     out_path = '~/Desktop/EPAM_project/data/first_try/fastq_res_v3'
#
#     # I/O
#     def out_fastq(self):
#         return [sl.TargetInfo(self, fastq_res) for fastq_res in
#                 glob.glob(self.out_path + '*')]
#
#     # Implementation
#     def run(self):
#         utils.mkdir_if_not_exist(self.path_to_res)
#         #if
#         fastqs = [fastq for fastq in self.in_data()]
#         cmd = '~/Desktop/EPAM_project/tools/fastqc/fastqc -o /home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v2 ' + self.fastq_file_path[0] + ' ' + self.fastq_file_path[1]
#         cmd = '{tool_path} -o {out_path} {in_1} {in_2}'.format(tool_path=self.tool_path,
#                                                                              out_path=self.out_path,
#                                                                              in_1=fastqs[0],
#                                                                              in_2=fastqs[1])
#         call(cmd, shell=True)


class FastqcTask3(sl.Task):
    """
    Process output of trimmomatic
    """

    # Parameter
    in_data = None
    n = None
    tool_path = '/home/aleksandrsl/Desktop/EPAM_project/tools/fastqc/fastqc'
    outp_path = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/fastq_res_v3' + n +'/'


    def out_fastq(self):
        return sl.TargetInfo(self, self.outp_path + 'fastq_res.txt')

    # Implementation
    def run(self):
        utils.mkdir_if_not_exist(self.outp_path)
        with open(self.in_data().path, 'r') as infile:
            inp_data = json.load(infile)
        fastqs = [file for file in inp_data]
        cmd = '{tool_path} -o {out_path} {inp_1} {inp_2} {inp_3} {inp_4}'.format(tool_path=self.tool_path,
                                                                             out_path=self.outp_path,
                                                                             inp_1=fastqs[0],
                                                                             inp_2=fastqs[1],
                                                                             inp_3=fastqs[2],
                                                                             inp_4=fastqs[3])
        call(cmd, shell=True)
        with self.out_fastq().open('w') as outfile:
            res = [fastq_res for fastq_res in
                glob.glob(self.outp_path + '*')]
            json.dump(res, outfile)


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
        return sl.TargetInfo(self, self.outp_path + 'trimmo_res.txt')

    ###################################################################3
    # ILLUMINACLIP:<fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>:<minAdapterLength>:<keepBothReads>
    # MAXINFO:<targetLength>:<strictness>
    # SLIDINGWINDOW:<windowSize>:<requiredQuality>
    # LEADING:<quality>
    # CROP:<length>
    # TRAILING:<quality>
    # HEADCROP: < length >
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
        with self.out_trimmo().open('w') as outfile:
            res = [trimmo_res  for trimmo_res in
                glob.glob(self.outp_path + '*')]
            json.dump(res, outfile)


    #luigi - -local - scheduler - -module luigi - ex.luigi - example Task2 - -samplename testsample Как запустить скрипт

class TrimmoTaskWParameters(sl.ExternalTask):
    """
    Execute trimmomatic on fastq files
    """
    # Parameter
    inp_data = None
    trimmo_parameters = None
    n = None

    # default_trimmo_parameters = {'maxinfo': None,
    # 'slidingwindow': None,
    # 'leading': 30,
    # 'crop': None,
    # 'trailing': 30,
    # 'headcrop': 15,
    # }

    default_trimmo_parameters = {'leading': 30,
                                 'trailing': 30,
                                 'headcrop': 15,
                                 }

    tool_path = '/home/aleksandrsl/Desktop/EPAM_project/tools/trimmomatic-0.36/trimmomatic-0.36.jar'
    adapters_path = '/home/aleksandrsl/Desktop/EPAM_project/tools/trimmomatic-0.36/adapters/'
    outp_path = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/trimmed_seqs' + n + '/'
    adapter = 'TruSeq3-SE.fa'
    outp_name = 'trimmed_seq'
    adapter_full_path = adapters_path + adapter
    outp_full_path = outp_path + outp_name

    # I/O
    def out_trimmo(self):
        return sl.TargetInfo(self, self.outp_path + 'trimmo_res.txt')

    ###################################################################3
    # ILLUMINACLIP:<fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>:<minAdapterLength>:<keepBothReads>
    # MAXINFO:<targetLength>:<strictness>
    # SLIDINGWINDOW:<windowSize>:<requiredQuality>
    # LEADING:<quality>
    # CROP:<length>
    # TRAILING:<quality>
    # HEADCROP: < length >
    ####################################################################

    # Implementation
    def run(self):
        utils.mkdir_if_not_exist(self.outp_path)
        if not self.trimmo_parameters:
            self.trimmo_parameters = self.default_trimmo_parameters
        # cmd = 'java -jar {tool_path} PE -basein {fastq_file} -baseout {outp_full_path} ' \
        #       'ILLUMINACLIP:{adapter_full_path}:2:30:10 MAXINFO:{maxinfo} ' \
        #       'CROP:{crop} LEADING:{leading} ' \
        #       'TRAILING:{trailing} HEADCROP:{headcrop} ' \
        #       'SLIDINGWINDOW:{slidingwindow}'.format(tool_path=self.tool_path,
        #                          outp_full_path=self.outp_full_path,
        #                          adapter_full_path=self.adapter_full_path,
        #                          fastq_file=self.inp_data[0],
        #                          **self.trimmo_parameters
        #                          )
        cmd = 'java -jar {tool_path} PE -basein {fastq_file} -baseout {outp_full_path} ' \
            'ILLUMINACLIP:{adapter_full_path}:2:30:10 ' \
            'LEADING:{leading} ' \
            'TRAILING:{trailing} ' \
            'HEADCROP:{headcrop}'.format(tool_path=self.tool_path,
                                 outp_full_path=self.outp_full_path,
                                 adapter_full_path=self.adapter_full_path,
                                 fastq_file=self.inp_data[0],
                                 **self.trimmo_parameters
                                 )

        call(cmd, shell=True)
        with self.out_trimmo().open('w') as outfile:
            res = [trimmo_res  for trimmo_res in
                glob.glob(self.outp_path + '*')]
            json.dump(res, outfile)
