import luigi
import sciluigi as sl

class FastqcTask(sl.Task):

    # Parameter
    text = luigi.Parameter()

    # I/O

    def fastqc_res(self):
        return sl.TargetInfo(self, 'data/' + self.text)

    # Implementation
    def run(self):
        return sl.TargetInfo(self )

    cmd = 'cat ' + self.in_data().path + ' | sed "s/A/T/g" > ' + self.out_replatot().path
    log.info("COMMAND TO EXECUTE: " + cmd)
    call(cmd, shell=True)
