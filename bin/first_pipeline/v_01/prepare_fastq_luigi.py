from glob import glob
from marshal import dump
import luigi

class prep_fastq(luigi.Task):

    #def __init__(self):
    #    print('Init!!')
    #    super(sl.Task, self).__init__()

    data_path = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/sequences/'
    outp_path = '/home/aleksandrsl/Desktop/EPAM_project/data/first_try/'
    #print(data_path)

    def run(self):
        print('run')
        s = sorted(glob.glob(self.data_path + '*.fastq.gz'))
        paired_fastq = list(zip(s[::2], s[1::2]))[0]

        with self.output().open('w') as outfile:
            print(paired_fastq)
            dump(paired_fastq, outfile)

    def output(self):
        print('out_data')
        return luigi.LocalTarget(self.outp_path)
#$ luigi --module my_module MyTask --x 123 --y 456 --local-scheduler

if __name__ == '__main__':
    luigi.run(['prep_fastq'])