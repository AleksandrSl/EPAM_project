import logging
import luigi
import sciluigi as sl
from Components import RawSequencesTask, FastqcTask, FastqcTask_v2

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class TestWF(sl.WorkflowTask):

    # task = luigi.Parameter()
    paired_fastq = luigi.TupleParameter()
    #fastq_1, fastq_2 = paired_fastq

    def workflow(self):
        # First variant

        # fastqc_1 = self.new_task('fastqc_1', FastqcTask)
        # fastqc_2 = self.new_task('fastqc_2', FastqcTask)
        #
        # self.fastq_1, self.fastq_2 = self.paired_fastq
        #
        # Workflow definition

        # fastqc_1.fastq_file_path = self.fastq_1
        # fastqc_2.fastq_file_path = self.fastq_2

        # Second variant
        fastqc = self.new_task('fastqc', FastqcTask_v2)
        fastqc.fastq_file_path = self.paired_fastq
        #

        # for name, instance in locals().iteritems():
        #     if issubclass(type(instance), sl.Task):
        #         log.info('{n}, task id: {taskid}\n{n}, hash: {h}',
        #                 n=name,
        #                 taskid=instance.task_id,
        #                 h=instance.__hash__())

        return locals()

