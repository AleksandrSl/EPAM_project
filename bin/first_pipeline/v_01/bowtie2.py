import sciluigi as sl
from itertools import zip_longest
from subprocess import run, CalledProcessError
from collections import OrderedDict
import utils
from glob import glob
from json import dump, load

class Bowtie2(sl.Task):

    tool_path = sl.Parameter()
    index = sl.Parameter()
    outp_path = sl.Parameter()
    in_data = None

    def out_bowtie2(self):
        return sl.TargetInfo(self, self.outp_path + 'bowtie2_res')

    def run(self):
        utils.mkdir_if_not_exist(self.outp_path)
        o = self.outp_path + 'res.sam'
        fastqs = [fastq for fastq in utils.deserialize(self.in_data().path, load) if fastq.endswith('P')]
        cmd = '{tool} -x {index} -1 {inp1} -2 {inp2} -S {o}'.format(tool=self.tool_path,
                                                                        index=self.index,
                                                                        inp1=fastqs[0],
                                                                        inp2=fastqs[1],
                                                                        o=o)
        print('Command', cmd)
        try:
            run(cmd, shell=True, check=True)
        except CalledProcessError:
            print('i failed')
        else:
            utils.serialize(glob(self.outp_path + '*'), self.out_bowtie2().path, dump)

    # bowtie2 -x ./GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.bowtie_index -1 ../trimmed_seq_1P -2 ../trimmed_seq_2P -S res.sam