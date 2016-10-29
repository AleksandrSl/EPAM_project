import sciluigi as sl
import luigi
import glob
from workflow import TestWF
import components


class MetaWF(sl.WorkflowTask):
    '''
    Meta workflow
    '''

    path_to_fastq = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/sequences/'  # Test

    def workflow(self):
        # tasks = []
        # iterator = iter(sorted(glob.glob(self.path_to_fastq + '*.fastq.gz')))
        # for fastq in iterator:
        #     paired_fastq = (fastq, next(iterator))
        #     print(paired_fastq)
        #     wf = self.new_task('TestWf', TestWF, paired_fastq=paired_fastq)
        #     tasks.append(wf)
        # return tasks

        tasks = []
        s = sorted(glob.glob(self.path_to_fastq + '*.fastq.gz'))
        for paired_fastq in list(zip(s[::2], s[1::2])):
            wf = self.new_task('TestWf', TestWF, paired_fastq=paired_fastq)
            tasks.append(wf)
        return tasks


if __name__ == '__main__':
    # luigi.run(local_scheduler=True, main_task_cls=MetaWF)
    sl.run_local(main_task_cls=MetaWF)