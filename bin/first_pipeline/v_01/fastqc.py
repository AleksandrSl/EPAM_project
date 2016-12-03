import sciluigi as sl
import utils
from subprocess import run, CalledProcessError
from glob import glob
from collections import OrderedDict
from json import load, dump


class FastQC(sl.Task):

    in_data = None
    tool_path = sl.Parameter(default=None)
    outp_path = sl.Parameter()
    # owner_email = 'Alex121994@mail.ru'

    def out_fastq(self):
        print(self.in_data().path)

        print(self.outp_path)
        return sl.TargetInfo(self, self.outp_path + 'fastq_res')

    def run(self):
        print(self.in_data)
        fastqs = utils.deserialize(self.in_data().path, load)
        # #print(self.deps())
        utils.mkdir_if_not_exist(self.outp_path)
        args_dict = OrderedDict()
        args_dict['-o'] = self.outp_path
        cmd = '{tool} {args} {inp1} {inp2}'.format(tool=self.tool_path,
                                                   args=utils.make_args(args_dict),
                                                   inp1=fastqs[0],
                                                   inp2=fastqs[1])
        print(cmd)
        try:
            run(cmd, shell=True, check=True)
        except CalledProcessError as e:
            raise e('i failed')

        utils.serialize(glob(self.outp_path), self.out_fastq().path, dump)



