import logging

import sciluigi as sl
from v_01.prepare_fastq_task import PrepareFastq
from fastqc import FastQC
from v_01.trimmomatic import TrimmoTaskWParameters
from v_01.bowtie2 import Bowtie2
from v_01.samtools import Samtools
from v_01.mark_duplicates import MarkDuplicates
from v_01.BQSR import BQSR

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class FastQCWF(sl.WorkflowTask):

    def workflow(self):

        prepare = self.new_task('prepare', PrepareFastq,
                                data_path='/home/aleksandrsl/Desktop/EPAM_project/data/first_try/sequences/')
        #fastqc = self.new_task('fastqc', FastQC)
        trimmo = self.new_task('trimmo', TrimmoTaskWParameters)
        bowtie2 = self.new_task('bowtie2', Bowtie2)
        samtools = self.new_task('samtools', Samtools)
        mark_duplicates = self.new_task('mark_duplicates', MarkDuplicates)
        bqsr = self.new_task('BQSR', BQSR)
        #fastqc.in_data = prepare.out_data
        trimmo.in_data = prepare.out_data
        bowtie2.in_data = trimmo.out_trimmo
        samtools.in_data = bowtie2.out_bowtie2
        mark_duplicates.in_data = samtools.out_data
        BQSR.in_data = mark_duplicates.out_data

        # fastqc.in_data = self.paired_fastq
        return locals()


#for name, instance in locals().iteritems():
# if issubclass(type(instance), sl.Task):
#         log.info('{n}, task id: {taskid}\n{n}, hash: {h}',
#                 n=name,
#                 taskid=instance.task_id,
#                 h=instance.__hash__())

if __name__ == '__main__':
    sl.run_local(main_task_cls=FastQCWF)

