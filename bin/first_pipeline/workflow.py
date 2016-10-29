import logging
import luigi
import glob
import sciluigi as sl
from components import TrimmoTask, FastqcTask3, TrimmoTaskWParameters

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class TestWF(sl.WorkflowTask):

    paired_fastq = luigi.TupleParameter()
    trimmo_par = luigi.DictParameter()
    n = luigi.IntParameter()

    def workflow(self):

        trimmo = self.new_task('trimmo', TrimmoTaskWParameters)
        fastqc = self.new_task('fastqc', FastqcTask3)

        trimmo.n = self.n
        trimmo.trimmo_parameters = self.trimmo_par
        trimmo.inp_data = self.paired_fastq
        fastqc.n = self.n
        fastqc.in_data = trimmo.out_trimmo

        return locals()


#for name, instance in locals().iteritems():
# if issubclass(type(instance), sl.Task):
#         log.info('{n}, task id: {taskid}\n{n}, hash: {h}',
#                 n=name,
#                 taskid=instance.task_id,
#                 h=instance.__hash__())
# if __name__ == '__main__':
#     sl.run_local(main_task_cls=TestWF, cmdline_args=['--task=fastqc'])

