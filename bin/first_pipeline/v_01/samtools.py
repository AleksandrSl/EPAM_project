import sciluigi as sl
from subprocess import run, CalledProcessError
import utils
from glob import glob
from json import dump, load

class Samtools(sl.Task):

    in_data = None
    tool_path = sl.Parameter()
    outp_path = sl.Parameter()
    working_dir = sl.Parameter()
    ref_fasta = sl.Parameter()

    def out_data(self):
        return sl.TargetInfo(self, self.outp_path + 'samtools_res')

    def run(self):
        sam_file = utils.deserialize(self.in_data().path, load)[0]
        utils.mkdir_if_not_exist(self.outp_path)
        with utils.cd(self.working_dir):
            cmds = ['{tool} view -bS {sam_file} > res.bam'.format(tool=self.tool_path, sam_file=sam_file),
                    '{tool} sort res.bam -o sorted.bam -O BAM'.format(tool=self.tool_path),
                    '{tool} index sorted.bam'.format(tool=self.tool_path),
                    # Make index fo reference
                    '{tool} faidx {ref_fasta}'.format(tool=self.tool_path, ref_fasta=self.ref_fasta)]
            for cmd in cmds:
                try:
                    run(cmd, shell=True, check=True)
                except CalledProcessError as e:
                    raise e('failed')
            utils.serialize(glob('*'), self.out_data().path, dump)