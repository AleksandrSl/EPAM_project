import sciluigi as sl
from itertools import zip_longest
from subprocess import run, CalledProcessError
from collections import OrderedDict
import utils
from glob import glob
from json import dump, load

class MarkDuplicates(sl.Task):

    tool_path = sl.Parameter()
    outp_path = sl.Parameter()
    working_dir = sl.Parameter()
    in_data = None

    def out_data(self):
        return sl.TargetInfo(self, self.outp_path + 'mark_dupl_res')

    def run(self):
        with utils.cd(self.working_dir):
            utils.mkdir_if_not_exist(self.outp_path)
            res = utils.deserialize(self.in_data().path, load)
            cmds = ['java -jar {tool} MarkDuplicates INPUT=sorted.bam OUTPUT=dedup_reads.bam ' \
                  'METRICS_FILE=metrics.txt'.format(tool=self.tool_path),
            # Add readgroups info
            'java -jar {tool} AddOrReplaceReadGroups I=dedup_reads.bam ' \
                   'O=dedup_reads_w_readgroups.bam RGID=4 RGLB=lib1 ' \
                   'RGPL=illumina RGPU=unit1 RGSM=20'.format(tool=self.tool_path)]
            for cmd in cmds:
                print('Command', cmd)
                try:
                    run(cmd, shell=True, check=True)
                except CalledProcessError:
                    print('i failed')
                else:
                    utils.serialize(glob('*'), self.out_data().path, dump)
