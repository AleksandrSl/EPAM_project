import logging
import luigi
import glob
import sciluigi as sl
from components import TrimmoTask, FastqcTask3

# ========================================================================

log = logging.getLogger('sciluigi-interface')

# ========================================================================

class TestWF(sl.WorkflowTask):

    paired_fastq = luigi.TupleParameter()
    trimmo_par = luigi.DictParameter()

    def workflow(self):

        trimmo = self.new_task('trimmo', TrimmoTask)
        fastqc = self.new_task('fastqc', FastqcTask3)

        trimmo.inp_data = self.paired_fastq
        trimmo.parameters = self.trimmo_par
        fastqc.in_upstream = trimmo.out_trimmo

        return locals()