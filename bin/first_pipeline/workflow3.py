import logging
import luigi
import glob
import sciluigi as sl
from components import TrimmoTask, FastqcTask3

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class TestWF(sl.WorkflowTask):

    task = luigi.Parameter()
    paired_fastq = list(zip(s[::2], s[1::2]))[0]

    #fastq_1, fastq_2 = paired_fastq

    def workflow(self):

        trimmo = self.new_task('trimmo', TrimmoTask)
        fastqc = self.new_task('fastqc', FastqcTask3)

        trimmo.inp_data = self.paired_fastq
        fastqc.in_upstream = trimmo.out_trimmo

        return locals()


#for name, instance in locals().iteritems():
# if issubclass(type(instance), sl.Task):
#         log.info('{n}, task id: {taskid}\n{n}, hash: {h}',
#                 n=name,
#                 taskid=instance.task_id,
#                 h=instance.__hash__())
# if __name__ == '__main__':
#     sl.run_local(main_task_cls=TestWF, cmdline_args=['--task=fastqc'])

