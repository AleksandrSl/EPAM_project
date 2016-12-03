import sciluigi as sl
from glob import glob
from json import dump
import luigi

class PrepareFastq(sl.Task):

    #def __init__(self):
    #    print('Init!!')
    #    super(sl.Task, self).__init__()

    data_path = sl.Parameter()
    outp_path = sl.Parameter()
    # Write parameters in config whithout ', or it will interpret this as directory name
    # Path must be FILE!!!!!

    def out_data(self):
        return sl.TargetInfo(self, self.outp_path)

    def run(self):
        print('run')
        s = sorted(glob(self.data_path + '*.fastq.gz'))
        paired_fastq = list(zip(s[::2], s[1::2]))[0]

        with self.out_data().open('w') as outfile:
            dump(paired_fastq, outfile)