import logging
import luigi
import sciluigi as sl
from components import TrimmoTask, FastqcTask3

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class TestWF_v2(sl.WorkflowTask):

    # task = luigi.Parameter()
    paired_fastq = luigi.TupleParameter()
    #fastq_1, fastq_2 = paired_fastq

    def workflow(self):

        trimmo = self.new_task('trimmo', TrimmoTask)
        fastqc = self.new_task('fastqc', FastqcTask3)

        trimmo.inp_data = self.paired_fastq
        fastqc.in_data = trimmo.out_trimmo

        return locals()