import logging
import luigi
import glob
import sciluigi as sl
from components import TrimmoTask, FastqcTask3

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class SimpleWF(sl.WorkflowTask):

    path_to_fastq = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/sequences/'  #
    s = sorted(glob.glob(path_to_fastq + '*.fastq.gz'))
    paired_fastq = list(zip(s[::2], s[1::2]))[0]

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
if __name__ == '__main__':
    sl.run_local(main_task_cls=SimpleWF, cmdline_args=['--task=fastqc'])

